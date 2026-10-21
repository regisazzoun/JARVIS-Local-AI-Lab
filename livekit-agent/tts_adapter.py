"""PiperLocalAdapter: adaptateur TTS local utilisant Piper via le venv /opt/jarvis/voice.

Conforme à LiveKit agents.TTS avec ChunkedStream synchrone (pas de coroutine).
"""

import asyncio
import io
import time
import wave
from pathlib import Path
from typing import Optional

# Importation du SDK LiveKit Agents pour TTS et ChunkedStream
from livekit.agents import tts as lk_tts
from livekit.rtc import AudioFrame


class _PiperChunkedStream(lk_tts.ChunkedStream):
    """Implémente ChunkedStream avec rendu asynchrone via _run()."""
    
    def __init__(self, adapter: "PiperLocalAdapter", text: str) -> None:
        from livekit.agents.types import APIConnectOptions
        super().__init__(tts=adapter, input_text=text, conn_options=APIConnectOptions())
        self._text = text
        self._model_path = adapter._model_path
        self._sample_rate = adapter.sample_rate
    
    async def _run(self, output_emitter: lk_tts.AudioEmitter) -> None:
        """Méthode abstraite requise par ChunkedStream : asynchrone, rend via emitter."""
        try:
            # Le modèle est chargé en amont/hors boucle pour que le premier
            # tour ne bloque pas le VAD pendant le démarrage de Piper.
            piper_instance = await self._tts._ensure_piper_loaded()
            
            # Synthèse bloc: crée un WAV en mémoire puis extrait PCM
            pcm_bytes = await asyncio.to_thread(
                lambda: self._synthesize_to_pcm(self._text, piper_instance)
            )
            
            # Initialisation du flux audio (requise par ChunkedStream)
            output_emitter.initialize(
                request_id=str(int(time.time_ns())),
                sample_rate=self._sample_rate,
                num_channels=1,
                mime_type="audio/pcm",
                stream=False,
            )
            
            # Émission des frames PCM (16 bits, mono)
            # Trames de 20ms à 16kHz = 320 bytes
            for i in range(0, len(pcm_bytes), 320):
                chunk = pcm_bytes[i:i+320]
                if len(chunk) > 0:
                    output_emitter.push(chunk)
            
            output_emitter.flush()
            
        except Exception as e:
            # Propage l'erreur via le mécanisme SDK
            self._tts.emit(
                "error",
                lk_tts.TTSError(
                    timestamp=asyncio.get_running_loop().time(),
                    label=self._tts.model,
                    error=e,
                    recoverable=False,
                )
            )
            raise
    
    @staticmethod
    def _load_piper_sync(model_path: str) -> object:
        """Charge PiperVoice depuis /opt/jarvis/voice/venv (fonction bloquante)."""
        import sys
        venv_site = Path("/opt/jarvis/voice/venv/lib/python3.13/site-packages")
        if str(venv_site) not in sys.path:
            sys.path.insert(0, str(venv_site))
        
        # Import direct depuis le venv (piper-tts package)
        from piper import PiperVoice
        
        # Charge le modèle
        return PiperVoice.load(model_path=model_path)
    
    @staticmethod
    def _synthesize_to_pcm(text: str, piper_instance) -> bytes:
        """Synthétise le texte en PCM brut 16-bit mono.
        
        Utilise l'API PiperVoice.synthesize_wav(text, wav_file) qui écrit dans un objet Wave_write.
        """
        # Crée un buffer mémoire pour le WAV
        wav_buffer = io.BytesIO()
        
        # Écrit le WAV avec les paramètres corrects
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16 bits
            wav_file.setframerate(16000)  # 16kHz
            
            # Piper écrit le contenu audio dans le WAV
            piper_instance.synthesize_wav(text, wav_file)
        
        # Extraire les données PCM (sauter l'en-tête WAV de 44 bytes)
        with wave.open(io.BytesIO(wav_buffer.getvalue()), 'rb') as stream:
            if stream.getframerate() != 44100:
                raise RuntimeError('Unexpected Piper rate; explicit resampling required')
            pcm_data = stream.readframes(stream.getnframes())
        
        return pcm_data


class PiperLocalAdapter(lk_tts.TTS):
    """Adaptateur TTS pour LiveKit utilisant un modèle Piper local.
    
    Conformité SDK : synthesize() retourne SYNCHRONEMENT un ChunkedStream.
    Le rendu audio est asynchrone dans _run().
    """
    
    def __init__(self, model_path: str = "/opt/jarvis/voice/models/tts/fr_FR-tom-medium.onnx",
                 sample_rate: int = 44100):
        self._model_path = model_path
        self._piper_instance = None
        self._piper_lock = asyncio.Lock()
        super().__init__(
            capabilities=lk_tts.TTSCapabilities(
                streaming=False,   # Piper n'est pas réellement streaming
            ),
            sample_rate=sample_rate,
            num_channels=1,        # Mono
        )
    
    @property
    def model(self) -> str:
        return self._model_path
    
    @property
    def provider(self) -> str:
        return "piper"
    
    def synthesize(self, text: str, *, conn_options=None) -> lk_tts.ChunkedStream:
        """RETOUT SYNCHRONE d'un objet ChunkedStream (exige par le SDK).
        
        Le rendu audio réel est différé dans _run().
        """
        if not text or not text.strip():
            raise ValueError("Texte vide non supporté")
        
        # Création IMMÉDIATE du flux, pas de await ici
        return _PiperChunkedStream(self, text)

    async def _ensure_piper_loaded(self) -> object:
        """Charge Piper une seule fois dans un thread, jamais sur la boucle audio."""
        if self._piper_instance is not None:
            return self._piper_instance
        async with self._piper_lock:
            if self._piper_instance is None:
                self._piper_instance = await asyncio.to_thread(
                    _PiperChunkedStream._load_piper_sync, self._model_path
                )
        return self._piper_instance

    async def warmup(self) -> None:
        """Précharge Piper avant de démarrer la session temps réel."""
        await self._ensure_piper_loaded()
