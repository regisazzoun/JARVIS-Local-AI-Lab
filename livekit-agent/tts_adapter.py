#!/usr/bin/env python3
"""
Adaptateur TTS local utilisant Piper pour LiveKit Agents.
Compatible avec l'API LiveKit TTS et les voix Piper disponibles localement.
"""

import asyncio
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

import livekit.agents as livekit_agents
import livekit.rtc as rtc


@dataclass
class PiperState:
    """État du moteur Piper"""
    synthesizer: Optional[object] = None
    loaded: bool = False
    voice_path: str = ""
    sample_rate: int = 16000


class PiperLocalAdapter(livekit_agents.tts.TTS):
    """
    Adaptateur TTS utilisant Piper pour la synthèse vocale locale.
    
    Ce composant implémente l'interface LiveKit TTS et permet :
    - Synthèse vocale en français avec des voix Piper
    - Génération de segments audio compatibles LiveKit
    - Support du streaming (segmentation progressive)
    
    Requiert:
    - pip install piper-tts ou TTS
    - Voix Piper téléchargées dans le dossier spécifié
    """
    
    def __init__(
        self,
        *,
        voice_name: str = "fr_FR-keran_16k-low",  # Nom de la voix Piper
        voice_dir: str = "/opt/jarvis/tts/piper/voices",
        sample_rate: int = 16000,
        length_scale: float = 1.0,  # Vitesse de parole (plus petit = plus rapide)
    ):
        super().__init__(
            capabilities=livekit_agents.tts.TTSCapabilities(
                streaming=False,  # Piper génère tout d'un coup pour cette version
                aligned_transcript=False,  # Pas de timestamps de mots
            ),
            sample_rate=sample_rate,
            num_channels=1,
        )
        
        self._voice_name = voice_name
        self._voice_dir = Path(voice_dir)
        self._sample_rate = sample_rate
        self._length_scale = length_scale
        self._state = PiperState(sample_rate=sample_rate)
        self._lock = asyncio.Lock()
        
        # Paramètres LiveKit TTS
        self._model = "piper-local"
        self._provider = "jarvis-piper"
        
        print(f"[TTS Adapter] Initialisé: voice={voice_name}, sr={sample_rate}")
    
    async def _ensure_synth_loaded(self):
        """Charger le moteur Piper de manière asynchrone"""
        if self._state.loaded:
            return
        
        async with self._lock:
            if self._state.loaded:
                return
            
            print(f"[TTS Adapter] Chargement de la voix {self._voice_name}...")
            
            # Trouver le chemin de la voix
            voice_path = self._find_voice_path(self._voice_name)
            if not voice_path:
                raise RuntimeError(f"Voix non trouvée: {self._voice_name} dans {self._voice_dir}")
            
            self._state.voice_path = str(voice_path)
            
            # Charger Piper dans un thread
            loop = asyncio.get_event_loop()
            
            def load_piper():
                """Tenter de charger Piper avec différentes approches"""
                try:
                    # Essai 1: piper-tts package
                    from piper import Synthesizer
                    
                    synthesizer = Synthesizer.load(
                        model=self._state.voice_path + "/model.onnx",
                        config=self._state.voice_path + "/config.json",
                        espeak_data_file=str(self._voice_dir / "espeak-ng-data")
                    )
                    
                    return synthesizer, "piper"
                    
                except ImportError:
                    pass
                
                try:
                    # Essai 2: TTS package (Coqui TTS)
                    from TTS.api import TTS
                    
                    tts = TTS(model_path=self._state.voice_path)
                    return tts, "tts"
                    
                except Exception as e:
                    print(f"[TTS Adapter] Echec chargement avec TTS: {e}")
                
                # Essai 3: subprocess avec piper-cli (si disponible)
                import subprocess
                result = subprocess.run(
                    ["which", "piper"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    return result.stdout.strip(), "cli"
                
                raise RuntimeError("Impossible de charger Piper: aucun moteur disponible")
            
            synth_result = await loop.run_in_executor(None, load_piper)
            self._state.synthesizer, self._synth_type = synth_result
            self._state.loaded = True
            
            print(f"[TTS Adapter] Voix chargée: {self._voice_name} (type: {self._synth_type})")
    
    def _find_voice_path(self, voice_name: str) -> Optional[str]:
        """Trouver le chemin de la voix Piper"""
        voice_dir = Path(self._voice_dir)
        
        if not voice_dir.exists():
            print(f"[TTS Adapter] Répertoire des voix inexistant: {voice_dir}")
            return None
        
        # Chercher dans le répertoire des voix
        for item in voice_dir.iterdir():
            if item.is_dir() and voice_name.split('_')[0] in item.name:
                # Vérifier si c'est une voix valide (contient model.onnx)
                model_path = item / "onnx" / "model.onnx"
                if model_path.exists():
                    return str(item / "onnx")
        
        # Fallback: tentative directe
        direct_path = voice_dir / voice_name / "onnx" / "model.onnx"
        if direct_path.exists():
            return str(voice_dir / voice_name / "onnx")
        
        print(f"[TTS Adapter] Voix non trouvée: {voice_name}")
        return None
    
    async def synthesize(
        self,
        text: str,
        *,
        conn_options: Optional[livekit_agents.APIConnectOptions] = None,
    ) -> livekit_agents.tts.ChunkedStream:
        """
        Synthétiser du texte en audio.
        
        Cette méthode est appelée par LiveKit pour synthétiser du texte.
        Elle retourne un stream de chunks audio progressifs.
        """
        
        # Charger le synthétiseur si nécessaire
        await self._ensure_synth_loaded()
        
        # Créer le stream
        stream = livekit_agents.tts.ChunkedStream(
            tts=self,
            input_text=text,
            conn_options=conn_options or livekit_agents.DEFAULT_API_CONNECT_OPTIONS
        )
        
        try:
            async with stream.channel():
                loop = asyncio.get_event_loop()
                
                def synthesize_text():
                    """Effectuer la synthèse dans un thread"""
                    if self._synth_type == "piper":
                        # Utilisation de piper-tts
                        import numpy as np
                        
                        # Générer l'audio (format spécifique à piper)
                        audio = self._state.synthesizer.synthesize(text)
                        
                        # Convertir en format expected par LiveKit
                        # Piper retourne des samples float32
                        samples = np.array(audio, dtype=np.float32)
                        
                        return samples, "piper"
                        
                    elif self._synth_type == "tts":
                        # Utilisation de Coqui TTS
                        import numpy as np
                        
                        # Générer l'audio avec TTS
                        audio_data = self._state.synthesizer.tts(text)
                        
                        # TTS retourne (samples, sample_rate, waveform)
                        if isinstance(audio_data, tuple):
                            samples = audio_data[0]
                        else:
                            samples = audio_data
                        
                        return np.array(samples, dtype=np.float32), "tts"
                        
                    elif self._synth_type == "cli":
                        # Utilisation de piper via CLI
                        import subprocess
                        import tempfile
                        
                        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                            temp_file = f.name
                        
                        # Appeler piper-cli
                        result = subprocess.run(
                            [self._state.synthesizer, 
                             '--model', self._state.voice_path + '/model.onnx',
                             '--output_file', temp_file],
                            input=text,
                            capture_output=True,
                            text=True
                        )
                        
                        if result.returncode != 0:
                            raise RuntimeError(f"piper-cli error: {result.stderr}")
                        
                        # Lire le fichier WAV généré
                        import wave
                        import struct
                        
                        with wave.open(temp_file, 'rb') as wav:
                            n_frames = wav.getnframes()
                            frames = wav.readframes(n_frames)
                            
                            # Convertir int16 en float32
                            samples = np.frombuffer(frames, dtype=np.int16)
                            samples = samples.astype(np.float32) / 32768.0
                        
                        import os
                        os.remove(temp_file)
                        
                        return samples, "cli"
                        
                    else:
                        raise RuntimeError("Type de synthétiseur inconnu")
                
                # Exécuter la synthèse dans un thread
                samples, synth_type = await loop.run_in_executor(None, synthesize_text)
                
                # Diviser en chunks pour le streaming (segments de ~48ms à 16kHz)
                chunk_size = int(self._sample_rate * 0.048)  # ~768 échantillons
                
                for i in range(0, len(samples), chunk_size):
                    chunk = samples[i:i + chunk_size]
                    
                    # Créer une frame audio LiveKit
                    frame = rtc.AudioFrame(
                        sample_rate=self._sample_rate,
                        num_channels=1,
                        samples=chunk.tobytes(),
                        length_ms=len(chunk) // (self._sample_rate // 1000)
                    )
                    
                    # Émettre la frame via le stream
                    await stream.queue_frame(frame)
                
                print(f"[TTS Adapter] Synthèse terminée: {len(samples)} échantillons")
                
        except Exception as e:
            print(f"[TTS Adapter] Erreur de synthèse: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # Terminer le stream
        await stream.finish()
        
        return stream


# Test unitaire simple
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("TEST ADAPTATEUR TTS PIPER LOCAL")
    print("=" * 60)
    
    # Créer l'adaptateur
    try:
        adapter = PiperLocalAdapter(
            voice_name="fr_FR-keran_16k-low",
            voice_dir="/opt/jarvis/tts/piper/voices"
        )
        
        print(f"\nAdaptateur créé:")
        print(f"  - Capabilities: streaming={adapter.capabilities.streaming}")
        print(f"  - Voice: {adapter._voice_name}")
        print(f"  - Sample rate: {adapter.sample_rate}")
        
        # Vérifier les attributs requis par LiveKit
        print(f"  - model: {adapter.model}")
        print(f"  - provider: {adapter.provider}")
        print(f"  - num_channels: {adapter.num_channels}")
        
        print("\n✓ TEST PASSE - Adaptateur TTS initialisé correctement")
        print("\nNote: Le test ne charge pas réellement la voix car elle peut être absente.")
        print("La synthèse réelle nécessitera un fichier voix Piper valide.")
        
    except Exception as e:
        print(f"\n✗ ERREUR d'initialisation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
