#!/usr/bin/env python3
"""Independent actual STT/TTS adapter execution, not just object construction."""
import argparse,asyncio,inspect,json,math,time,wave
from pathlib import Path
from verify_livekit_agent import factory

async def verify(args):
    from livekit import rtc
    from livekit.agents import tts,stt
    import numpy as np
    project=args.project.resolve()
    assert project==Path('/var/lib/jarvis/projects/mission23/livekit-agent')
    import sys
    sys.path.insert(0,str(project))
    manifest=json.loads((project/'verification.json').read_text())
    session=factory(project,manifest['agent'])
    if inspect.isawaitable(session):session=await session
    with wave.open(str(args.wav),'rb') as wav:
        assert wav.getnchannels()==1 and wav.getsampwidth()==2
        sample_rate=wav.getframerate();data=wav.readframes(wav.getnframes())
    frames=[];size=sample_rate//50
    for offset in range(0,len(data),size*2):
        part=data[offset:offset+size*2]
        frames.append(rtc.AudioFrame(data=part,sample_rate=sample_rate,num_channels=1,samples_per_channel=len(part)//2))
    try:
        start=time.monotonic();event=await session.stt.recognize(frames);stt_s=time.monotonic()-start
        assert isinstance(event,stt.SpeechEvent) and event.alternatives,'No actual SpeechEvent transcript'
        transcript=event.alternatives[0].text
        assert 'bonjour' in transcript.lower(),'French fixture not transcribed correctly: '+transcript
        start=time.monotonic();stream=session.tts.synthesize('Bonjour, je suis JARVIS. Le test vocal fonctionne.')
        if inspect.iscoroutine(stream):
            stream.close();raise AssertionError('TTS.synthesize must synchronously return SDK ChunkedStream, not coroutine')
        assert isinstance(stream,tts.ChunkedStream),'TTS returned no actual SDK ChunkedStream'
        count=0;energy=0.;samples=0;first_audio_s=None;rate=None
        async with stream:
            async for chunk in stream:
                assert isinstance(chunk,tts.SynthesizedAudio),'No actual SDK SynthesizedAudio'
                frame=chunk.frame;raw=np.frombuffer(frame.data,dtype=np.int16)
                count+=1;samples+=len(raw);energy+=float(np.sum(raw.astype(float)**2));rate=frame.sample_rate
                if first_audio_s is None and np.any(np.abs(raw)>20):first_audio_s=time.monotonic()-start
        tts_s=time.monotonic()-start
        assert samples>1600 and energy>0 and first_audio_s is not None,'No real non-silent synthesized PCM'
        result={'check':'real_stt_tts_application_adapters','verified':True,'physical_microphone':False,'transcript':transcript,'stt_wall_s':stt_s,'tts_wall_s':tts_s,'tts_first_pcm_s':first_audio_s,'tts_frames':count,'tts_samples':samples,'tts_sample_rate':rate,'tts_rms':math.sqrt(energy/samples),'scope':'Actual French WAV recognition and non-silent SDK TTS stream; no WebRTC or physical listening claimed'}
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False));print('LIVEKIT_COMPONENTS_VERIFIED')
    finally:await session.aclose()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--project',type=Path,default=Path('/var/lib/jarvis/projects/mission23/livekit-agent'));p.add_argument('--wav',type=Path,required=True);p.add_argument('--output',type=Path,required=True);asyncio.run(verify(p.parse_args()))
