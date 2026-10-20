"""Factories for LiveKit agent components - mission23 t05"""
import asyncio
from pathlib import Path

# Import des modules locaux du projet
from stt_adapter import WhisperLocalAdapter
from tts_adapter import PiperLocalAdapter

# Dell Ollama configuration
DELL_OLLAMA_URL = "http://192.168.1.75:11434/v1"
DELL_OLLAMA_MODEL = "qwen3.5:27b-q4_K_M"
FAKE_API_KEY = "sk-fake"  # Ollama compat OpenAI ne nécessite pas de vraie clé


def create_llm():
    """Create LLM adapter pointing to Dell Ollama via LiveKit OpenAI plugin."""
    from livekit.plugins.openai import llm as openai_llm_plugin
    
    return openai_llm_plugin.LLM(
        model=DELL_OLLAMA_MODEL,
        base_url=DELL_OLLAMA_URL,
        api_key=FAKE_API_KEY,
        timeout=120.0  # L'inférence Qwen observée peut prendre 58s au premier token
    )


async def create_stt():
    """Create STT adapter using faster-whisper local with canonical model."""
    return WhisperLocalAdapter(
        model_name="/opt/jarvis/voice/models/stt/whisper-small",
        language="fr",
        compute_type="int8",
        device="cpu"
    )


async def create_tts():
    """Create TTS adapter using Piper local with canonical voice."""
    adapter = PiperLocalAdapter(
        model_path="/opt/jarvis/voice/models/tts/fr_FR-tom-medium.onnx"
    )
    # Charger Piper avant que la session commence à recevoir le microphone.
    # PiperVoice.load initialise ONNX Runtime de façon synchrone; le warmup
    # le déporte dans un thread via l'adaptateur.
    await adapter.warmup()
    return adapter


async def create_session(session_id: str = "default"):
    """Create a full AgentSession with all adapters."""
    # Import ici pour éviter d'importer au top-level si non nécessaire
    from livekit.agents import AgentSession
    
    # Create providers (note: LLM is synchronous, STT/TTS are async)
    llm_provider = create_llm()
    stt_provider = await create_stt()
    tts_provider = await create_tts()
    
    # Create session - NOTE: AgentSession n'a pas de paramètre session_id
    # La session_id est gérée par le framework LiveKit via le job context
    session = AgentSession(
        llm=llm_provider,
        stt=stt_provider,
        tts=tts_provider,
    )
    
    return session


if __name__ == "__main__":
    """Self-test for factories."""
    print("=" * 60)
    print("FACTORY SELF-TEST")
    print("=" * 60)
    
    # Test create_llm()
    print("\n1. Test create_llm()...")
    try:
        llm = create_llm()
        print(f"   ✓ LLM créé: model={llm.model}")
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
    
    # Test create_stt()
    print("\n2. Test create_stt()...")
    try:
        stt = asyncio.run(create_stt())
        print(f"   ✓ STT créé")
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
    
    # Test create_tts()
    print("\n3. Test create_tts()...")
    try:
        tts = asyncio.run(create_tts())
        print(f"   ✓ TTS créé")
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
    
    # Test create_session()
    print("\n4. Test create_session()...")
    try:
        session = asyncio.run(create_session(session_id="test-session-001"))
        print(f"   ✓ Session créée:")
        print(f"     - LLM: {'OK' if session.llm else 'MANQUANT'}")
        print(f"     - STT: {'OK' if session.stt else 'MANQUANT'}")
        print(f"     - TTS: {'OK' if session.tts else 'MANQUANT'}")
    except Exception as e:
        print(f"   ✗ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLÉTÉ")
    print("=" * 60)
