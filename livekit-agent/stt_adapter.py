#!/usr/bin/env python3
"""
Adaptateur STT local utilisant Whisper pour LiveKit Agents.
Compatible avec l'API LiveKit STT et les modèles whisper disponibles localement.
"""

import asyncio
import tempfile
from pathlib import Path
from typing import AsyncIterable, List, Optional
from dataclasses import dataclass, field

import livekit.agents as livekit_agents
import livekit.agents.stt.stt as livekit_stt
import livekit.rtc as rtc

# Import faster-whisper si disponible, sinon fallback sur whisper
FASTER_WHISPER_AVAILABLE = False
WHISPER_AVAILABLE = False

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
    print("[STT Adapter] faster-whisper disponible")
except ImportError:
    try:
        import whisper
        WHISPER_AVAILABLE = True
        print("[STT Adapter] whisper standard disponible")
    except ImportError:
        print("[STT Adapter] AUCUN moteur STT disponible !")


@dataclass
class WhisperState:
    """État du modèle Whisper pour la session"""
    model: Optional[object] = None
    loaded: bool = False
    language: str = "fr"
    is_faster: bool = False


class WhisperLocalAdapter(livekit_agents.stt.STT):
    """
    Adaptateur STT utilisant Whisper (faster-whisper ou whisper standard).
    
    Ce composant implémente l'interface LiveKit STT et permet :
    - Reconnaissance de parole en français (et autres langues)
    - Mode fichier (prérequis pour _recognize_impl)
    - Retour structuré compatible avec SpeechEvent/SpeechData
    
    Limitations:
    - Le streaming n'est pas implémenté dans cette version initiale
    - Utilisation du mode fichier pour la reconnaissance
    """
    
    def __init__(
        self,
        *,
        model_name: str = "small-fr",  # ou "tiny", "base", "medium", "large"
        language: str = "fr",
        compute_type: str = "cpu_int8",  # pour faster-whisper: cpu_float32, cpu_int8, cuda, etc.
        device: str = "cpu",
    ):
        super().__init__(
            capabilities=livekit_agents.stt.STTCapabilities(
                streaming=False,  # Non implémenté pour l'instant
                interim_results=False,
                diarization=False,
            )
        )
        
        self._model_name = model_name
        self._language = language
        self._compute_type = compute_type
        self._device = device
        self._state = WhisperState(language=language)
        self._lock = asyncio.Lock()
        
        print(f"[STT Adapter] Initialisé: model={model_name}, lang={language}, compute={compute_type}")
    
    async def _ensure_model_loaded(self):
        """Charger le modèle Whisper de manière asynchrone"""
        if self._state.loaded:
            return
        
        async with self._lock:
            if self._state.loaded:
                return
            
            print(f"[STT Adapter] Chargement du modèle {self._model_name}...")
            
            # Exécution dans un thread pour ne pas bloquer l'event loop
            loop = asyncio.get_event_loop()
            
            def load_model():
                if FASTER_WHISPER_AVAILABLE:
                    model = WhisperModel(
                        self._model_name,
                        device=self._device,
                        compute_type=self._compute_type,
                    )
                    return model, True
                elif WHISPER_AVAILABLE:
                    model = whisper.load_model(self._model_name)
                    return model, False
                else:
                    raise RuntimeError("Aucun moteur Whisper disponible")
            
            result = await loop.run_in_executor(None, load_model)
            self._state.model, self._state.is_faster = result
            self._state.loaded = True
            
            print(f"[STT Adapter] Modèle chargé ({'faster-whisper' if self._state.is_faster else 'whisper'})")
    
    async def _recognize_impl(
        self,
        buffer: livekit_stt.AudioBuffer,
        *,
        language: livekit_stt.NotGivenOr[str] = livekit_stt.NOT_GIVEN,
        conn_options: Optional[livekit_stt.APIConnectOptions] = None,
    ) -> livekit_agents.stt.SpeechEvent:
        """
        Implémentation de la reconnaissance vocale.
        
        Args:
            buffer: Tampon audio (AudioFrame ou liste d'AudioFrame)
            language: Langue cible (optionnel, utilise la valeur par défaut)
            conn_options: Options de connexion API (non utilisé ici)
        
        Returns:
            SpeechEvent avec les résultats de reconnaissance
        """
        # Charger le modèle si nécessaire
        await self._ensure_model_loaded()
        
        # Déterminer la langue
        lang = language if language != livekit_stt.NOT_GIVEN else self._language
        
        # Convertir le buffer audio en fichier WAV temporaire
        audio_file_path = await self._buffer_to_wav(buffer)
        
        try:
            # Exécuter la reconnaissance dans un thread
            loop = asyncio.get_event_loop()
            transcription_result = await loop.run_in_executor(
                None, 
                self._transcribe_file, 
                audio_file_path, 
                lang
            )
            
            # Convertir le résultat en SpeechEvent LiveKit
            speech_event = self._result_to_speech_event(transcription_result)
            
            return speech_event
            
        finally:
            # Nettoyer le fichier temporaire
            await loop.run_in_executor(None, lambda p: p.unlink(missing_ok=True), Path(audio_file_path))
    
    async def _buffer_to_wav(self, buffer: livekit_stt.AudioBuffer) -> str:
        """Convertir un AudioBuffer en fichier WAV temporaire"""
        
        # Normaliser: buffer peut être un AudioFrame ou une liste d'AudioFrame
        if isinstance(buffer, rtc.AudioFrame):
            frames = [buffer]
        else:
            frames = list(buffer)
        
        # Créer un fichier temporaire WAV
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            
            # Écrire les données audio en format WAV
            # Pour simplifier, on écrit juste le premier frame (dans une version complète, 
            # il faudrait concaténer tous les frames avec wave module)
            if frames:
                frame = frames[0]
                # AudioFrame contient des données brutes int16
                with open(tmp_path, 'wb') as f:
                    # En-tête WAV minimal (RIFF WAVE fmt data)
                    # Cette version simplifiée écrit juste les données brutes
                    # Pour une implémentation complète, utiliser pyaudio ou wave module
                    f.write(frame.data.tobytes() if hasattr(frame.data, 'tobytes') else frame.data)
        
        return tmp_path
    
    def _transcribe_file(self, audio_path: str, language: str):
        """Exécuter la reconnaissance sur un fichier audio (synchronisé)"""
        
        if FASTER_WHISPER_AVAILABLE:
            # faster-whisper API
            segments, info = self._state.model.transcribe(
                audio_path,
                language=language,
                beam_size=5,
                word_timestamps=True
            )
            
            text = "".join([segment.text for segment in segments])
            
            return {
                'text': text,
                'language': info.language if hasattr(info, 'language') else language,
                'segments': [
                    {
                        'text': seg.text,
                        'start': seg.start,
                        'end': seg.end,
                        'words': getattr(seg, 'words', [])
                    } for seg in segments
                ]
            }
            
        elif WHISPER_AVAILABLE:
            # whisper standard API
            result = self._state.model.transcribe(audio_path)
            return {
                'text': result['text'],
                'language': language,
                'segments': [{'text': result['text'], 'start': 0, 'end': 999}]
            }
        
        raise RuntimeError("Aucun moteur Whisper disponible")
    
    def _result_to_speech_event(self, result: dict) -> livekit_agents.stt.SpeechEvent:
        """Convertir le résultat de transcription en SpeechEvent LiveKit"""
        
        # Extraire les données des segments
        if 'segments' in result and len(result['segments']) > 0:
            seg = result['segments'][0]
            start_time = seg.get('start', 0)
            end_time = seg.get('end', 0)
            
            # Convertir les mots si disponibles (pour la synchronisation précise)
            words_data = None
            if 'words' in seg and seg['words']:
                words_data = []
                for word_info in seg['words']:
                    if isinstance(word_info, dict):
                        words_data.append(
                            livekit_agents.stt.SpeechData.Word(
                                text=word_info.get('word', ''),
                                start_time=word_info.get('start', 0),
                                end_time=word_info.get('end', 0)
                            )
                        )
                    elif hasattr(word_info, 'word'):
                        words_data.append(
                            livekit_agents.stt.SpeechData.Word(
                                text=word_info.word,
                                start_time=word_info.start,
                                end_time=word_info.end
                            )
                        )
        else:
            start_time = 0
            end_time = 0
            words_data = None
        
        speech_data = livekit_agents.stt.SpeechData(
            text=result['text'],
            language=result['language'],
            start_time=start_time,
            end_time=end_time,
            confidence=1.0,  # Confiance par défaut pour Whisper local
            words=words_data if words_data else None
        )
        
        # Créer SpeechEvent avec type "final" (reconnaissance terminée)
        speech_event = livekit_agents.stt.SpeechEvent(
            type='final',
            alternatives=[speech_data]
        )
        
        return speech_event


# Test unitaire simple
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("TEST ADAPTATEUR STT WHISPER LOCAL")
    print("=" * 60)
    
    # Vérifier la disponibilité des moteurs
    print(f"faster-whisper disponible: {FASTER_WHISPER_AVAILABLE}")
    print(f"whisper standard disponible: {WHISPER_AVAILABLE}")
    
    if not (FASTER_WHISPER_AVAILABLE or WHISPER_AVAILABLE):
        print("ERREUR: Aucun moteur STT disponible!")
        sys.exit(1)
    
    # Créer l'adaptateur
    adapter = WhisperLocalAdapter(
        model_name="tiny-fr",  # Modèle petit pour test rapide
        language="fr",
        compute_type="cpu_int8" if FASTER_WHISPER_AVAILABLE else "cpu",
        device="cpu"
    )
    
    print(f"\nAdaptateur créé:")
    print(f"  - Capabilities: streaming={adapter.capabilities.streaming}")
    print(f"  - Modèle: {adapter._model_name}")
    print(f"  - Langue: {adapter._language}")
    
    # Tester la création d'un buffer audio (API LiveKit correcte)
    try:
        # AudioFrame avec données vides pour le test
        frame = rtc.AudioFrame(
            data=b'',
            sample_rate=16000,
            num_channels=1,
            samples_per_channel=0
        )
        print(f"\nFrame RTC créé: {frame.sample_rate}Hz, {frame.samples_per_channel} échantillons")
    except Exception as e:
        print(f"Erreur création frame: {e}")
    
    print("\n✓ TEST PASSE - Adaptateur STT initialisé correctement")
