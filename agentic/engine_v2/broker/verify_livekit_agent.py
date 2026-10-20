#!/usr/bin/env python3
"""Independent mission23 acceptance test. Not application implementation.
Run through the existing confined host_exec with the project's Python environment.
"""
import argparse,asyncio,importlib,inspect,json,re,sys,time
from pathlib import Path

def factory(project,entry):
    module_name,attribute=entry['factory'].split(':',1)
    if not re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*',module_name):raise ValueError('Invalid factory module')
    module=importlib.import_module(module_name)
    if not Path(module.__file__).resolve().is_relative_to(project):raise ValueError('Factory must belong to the application')
    target=module
    for part in attribute.split('.'):
        if part.startswith('_'):raise ValueError('Public factory required')
        target=getattr(target,part)
    return target(**entry.get('kwargs',{}))

async def verify(project,part):
    from livekit.agents import AgentSession,llm,stt,tts
    project=project.resolve();assert project==Path('/var/lib/jarvis/projects/mission23/livekit-agent')
    sys.path.insert(0,str(project))
    manifest=json.loads((project/'verification.json').read_text())
    if part=='llm':
        provider=factory(project,manifest['llm'])
        if inspect.isawaitable(provider):provider=await provider
        assert isinstance(provider,llm.LLM),'Application factory must return LiveKit LLM'
        context=llm.ChatContext();context.add_message(role='user',content='Réponds simplement bonjour en français.')
        text=''
        try:
            first_start=time.monotonic()
            stream=provider.chat(chat_ctx=context)
            assert isinstance(stream,llm.LLMStream),'chat must return an actual LLMStream, not a coroutine or generator'
            async with stream:
                async for chunk in stream:
                    if chunk.delta and chunk.delta.content:
                        text+=chunk.delta.content
                        if text.strip():
                            first_nonempty_chunk_s=time.monotonic()-first_start
                            break
            assert text.strip(),'No real nonempty response received'
        finally:await provider.aclose()
        print(json.dumps({'check':'real_app_livekit_llm_stream','received_text_chars':len(text),'sdk_type_verified':True,'first_nonempty_chunk_s':first_nonempty_chunk_s}))
        print('LLM_STREAM_VERIFIED')
    else:
        importlib.import_module('agent') # the actual application entry point must import successfully
        session=factory(project,manifest['agent'])
        if inspect.isawaitable(session):session=await session
        assert isinstance(session,AgentSession),'Application factory must build actual AgentSession'
        assert isinstance(session.stt,stt.STT),'Session STT provider missing or incompatible'
        assert isinstance(session.tts,tts.TTS),'Session TTS provider missing or incompatible'
        assert isinstance(session.llm,llm.LLM),'Session LLM provider missing or incompatible'
        print(json.dumps({'check':'real_app_session_construction','stt':type(session.stt).__name__,'tts':type(session.tts).__name__,'llm':type(session.llm).__name__}))
        await session.aclose()
        print('AGENT_ADAPTERS_VERIFIED')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);p.add_argument('--part',choices=['llm','adapters'],required=True);args=p.parse_args()
    asyncio.run(verify(args.project,args.part))
