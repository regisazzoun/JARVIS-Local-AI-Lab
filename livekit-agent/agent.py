"""
JARVIS LiveKit Agent - Point d'entrée principal
Mission 23: Interface vocale temps réel avec LiveKit

Architecture:
- LiveKit Agents Framework (job-based)
- STT: Whisper local via adaptateur custom
- TTS: Piper local via adaptateur custom  
- LLM: OpenAI-compatible client pointant vers Ollama Dell
- VAD: Silero pour la détection de parole
"""

import asyncio
import logging

from livekit.agents import Agent, AgentServer, JobContext, cli
from livekit.plugins import silero

# Imports des factories locales (synchrones pour LLM)
from factories import create_llm, create_session

logger = logging.getLogger("jarvis-livekit-agent")

server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext) -> None:
    """
    Point d'entrée appelé par LiveKit pour chaque job.
    
    Cette fonction est asynchrone et reçoit un JobContext.
    Elle doit créer une session et la lancer.
    """
    logger.info(f"=== Job reçu: {ctx.job.id} ===")
    
    # Créer les composants via create_session
    session_data = await create_session(session_id=ctx.job.id)
    
    # Créer l'Agent avec les providers de la session
    agent_instance = Agent(
        stt=session_data.stt,
        tts=session_data.tts,
        llm=session_data.llm,
        vad=silero.VAD.load(),
        allow_interruptions=True,
        min_endpointing_delay=0.5,
        max_endpointing_delay=1.5,
    )
    
    logger.info("Agent JARVIS prêt pour la session")
    
    # Démarrer la session dans le room
    await agent_instance.connect(ctx.room)


if __name__ == "__main__":
    cli.run_app(server)
