#!/usr/bin/env python3
"""LiveKit voice agent for JARVIS mission 23."""
import logging
import textwrap

from livekit.agents import Agent, AgentServer, AgentSession, JobContext, cli
from livekit.agents.types import APIConnectOptions
from livekit.agents.voice.agent_session import SessionConnectOptions
from livekit.plugins import silero

from factories import create_llm, create_stt, create_tts

logger = logging.getLogger("livekit.agents.jarvis")
server = AgentServer()


class JarvisAgent(Agent):
    def __init__(self, llm_provider):
        instructions = textwrap.dedent("""            Tu es JARVIS, un assistant vocal hébergé localement.
            Réponds en français de façon concise et naturelle.
            Utilise du texte simple, sans Markdown, avec une à trois phrases courtes.
        """)
        super().__init__(
            instructions=instructions,
            llm=llm_provider,
            turn_handling={"interruption": {"enabled": True, "mode": "vad"}},
        )


@server.rtc_session(agent_name="jarvis-agent")
async def jarvis_voice_agent(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name, "agent": "jarvis-local"}
    logger.info("Initialisation de la session vocale pour room=%s", ctx.room.name)

    # Factories STT/TTS are async; the LLM factory is synchronous and targets Dell1 Ollama.
    stt_provider = await create_stt()
    tts_provider = await create_tts()
    llm_provider = create_llm()
    vad = silero.VAD.load()

    # AgentSession's default APIConnectOptions timeout is 10s. Qwen cold
    # first-token latency was measured at 57.1s while Ollama remained reachable;
    # allow that measured inference to complete without retrying/aborting it.
    session = AgentSession(
        stt=stt_provider,
        tts=tts_provider,
        vad=vad,
        conn_options=SessionConnectOptions(
            llm_conn_options=APIConnectOptions(timeout=90.0, max_retry=2)
        ),
    )
    await ctx.connect()
    await session.start(agent=JarvisAgent(llm_provider), room=ctx.room)


if __name__ == "__main__":
    cli.run_app(server)
