#!/usr/bin/env python3
"""Independent WebRTC reception: real published WAV and non-silent remote PCM.
No microphone claim. Test credentials are read privately, never printed.
Run with the application's venv; does not implement application components.
"""
import argparse,asyncio,array,json,math,os,time,uuid,wave
from pathlib import Path

async def verify(args):
    from livekit import api,rtc
    import numpy as np
    env={}
    for line in (args.project/'.env').read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key,value=line.split('=',1);env[key.strip()]=value.strip().strip('\"\'')
    room_name='independent23-'+uuid.uuid4().hex[:10]
    token=api.AccessToken(env['LIVEKIT_API_KEY'],env['LIVEKIT_API_SECRET']).with_identity('independent-verifier').with_grants(api.VideoGrants(room_join=True,room=room_name)).to_jwt()
    room=rtc.Room();receivers=[];audio=[];transcripts=[];first=asyncio.Event();t0=time.monotonic()
    @room.on('track_subscribed')
    def subscribed(track,publication,participant):
        if track.kind!=rtc.TrackKind.KIND_AUDIO:return
        async def receive():
            async for event in rtc.AudioStream(track,sample_rate=24000,num_channels=1):
                samples=np.frombuffer(event.frame.data,dtype=np.int16)
                rms=float(np.sqrt(np.mean(samples.astype(float)**2)))
                audio.append({'t':time.monotonic()-t0,'rms':rms,'samples':len(samples),'participant':participant.identity})
                if rms>20:first.set()
        receivers.append(asyncio.create_task(receive()))
    @room.on('transcription_received')
    def transcription(segments,participant,publication):
        for segment in segments:
            if segment.final:transcripts.append({'text':segment.text,'participant':participant.identity if participant else None,'t':time.monotonic()-t0})
    try:
        await asyncio.wait_for(room.connect(args.url or env['LIVEKIT_URL'],token),30)
        for _ in range(100):
            if room.remote_participants:break
            await asyncio.sleep(.2)
        assert room.remote_participants,'No real agent participant joined'
        source=rtc.AudioSource(24000,1);track=rtc.LocalAudioTrack.create_audio_track('verification-wav',source)
        await room.local_participant.publish_track(track,rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE))
        with wave.open(str(args.wav),'rb') as w:
            assert w.getsampwidth()==2 and w.getnchannels()==1
            raw=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16);sr=w.getframerate()
        converted=np.interp(np.arange(0,len(raw),sr/24000),np.arange(len(raw)),raw).astype(np.int16)
        begin=time.monotonic()-t0
        for start in range(0,len(converted),480):
            samples=converted[start:start+480]
            if len(samples)<480:samples=np.pad(samples,(0,480-len(samples)))
            frame=rtc.AudioFrame(data=samples.tobytes(),sample_rate=24000,num_channels=1,samples_per_channel=480)
            await source.capture_frame(frame)
        await source.wait_for_playout();speech_end=time.monotonic()-t0
        for _ in range(100):
            await source.capture_frame(rtc.AudioFrame(data=bytes(960),sample_rate=24000,num_channels=1,samples_per_channel=480))
        await asyncio.wait_for(first.wait(),args.timeout)
        await asyncio.sleep(3)
        non_silent=[f for f in audio if f['rms']>20]
        assert non_silent and sum(f['samples'] for f in non_silent)>2400,'Remote audio must contain real non-silent PCM'
        result={'check':'independent_real_webrtc_wav_to_remote_audio','verified':True,'physical_microphone':False,'url':args.url or env['LIVEKIT_URL'],'room':room_name,'remote_participants':list(room.remote_participants),'input_duration_s':len(converted)/24000,'input_started_s':begin,'input_end_s':speech_end,'first_remote_non_silent_s':non_silent[0]['t'],'end_to_first_audio_s':non_silent[0]['t']-speech_end,'received_audio_samples':sum(f['samples'] for f in audio),'peak_frame_rms':max(f['rms'] for f in audio),'transcriptions':transcripts,'limits':['No physical microphone/listening','Interruption and reconnection require separate evidence']}
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
    finally:
        await room.disconnect()
        for task in receivers:task.cancel()
        await asyncio.gather(*receivers,return_exceptions=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--project',type=Path,default=Path('/var/lib/jarvis/projects/mission23/livekit-agent'));p.add_argument('--wav',type=Path,required=True);p.add_argument('--url');p.add_argument('--timeout',type=float,default=90);p.add_argument('--output',type=Path,required=True);asyncio.run(verify(p.parse_args()))
