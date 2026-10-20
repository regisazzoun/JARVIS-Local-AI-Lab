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
    room_name='independent23-'+uuid.uuid4().hex[:10]
    if args.token_url:
        import urllib.request,urllib.parse
        url=args.token_url+('&' if '?' in args.token_url else '?')+urllib.parse.urlencode({'room':room_name,'identity':'independent-verifier'})
        with urllib.request.urlopen(url,timeout=10) as response:credentials=json.load(response)
        token=credentials['token'];env['LIVEKIT_URL']=credentials.get('url',args.url)
    else:
        for line in (args.project/'.env').read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                key,value=line.split('=',1);env[key.strip()]=value.strip().strip('"'+chr(39))
        token=api.AccessToken(env['LIVEKIT_API_KEY'],env['LIVEKIT_API_SECRET']).with_identity('independent-verifier').with_grants(api.VideoGrants(room_join=True,room=room_name)).to_jwt()
    # Explicitly create and dispatch the named agent; joining a room alone does not dispatch it.
    api_url=env.get('LIVEKIT_URL',args.url or '').replace('wss://','https://').replace('ws://','http://')
    lkapi=api.LiveKitAPI(url=api_url,api_key=env.get('LIVEKIT_API_KEY'),api_secret=env.get('LIVEKIT_API_SECRET'))
    await lkapi.room.create_room(api.CreateRoomRequest(name=room_name))
    await lkapi.agent_dispatch.create_dispatch(api.CreateAgentDispatchRequest(agent_name='jarvis-agent',room=room_name))
    room=rtc.Room();source=None;receivers=[];audio=[];transcripts=[];first=asyncio.Event();second_transcript=asyncio.Event();resumed_audio=asyncio.Event();state={'second_transcript_at':None};t0=time.monotonic()
    @room.on('track_subscribed')
    def subscribed(track,publication,participant):
        if track.kind!=rtc.TrackKind.KIND_AUDIO:return
        async def receive():
            stream=rtc.AudioStream(track,sample_rate=24000,num_channels=1)
            try:
                async for event in stream:
                    samples=np.frombuffer(event.frame.data,dtype=np.int16)
                    rms=float(np.sqrt(np.mean(samples.astype(float)**2)))
                    audio.append({'t':time.monotonic()-t0,'rms':rms,'samples':len(samples),'participant':participant.identity})
                    if rms>20:
                        first.set()
                        second_at=state['second_transcript_at']
                        if second_at is not None and time.monotonic()-t0>second_at+1.0:resumed_audio.set()
            finally:await stream.aclose()
        receivers.append(asyncio.create_task(receive()))
    @room.on('transcription_received')
    def transcription(segments,participant,publication):
        for segment in segments:
            if segment.final:
                item={'text':segment.text,'participant':participant.identity if participant else None,'t':time.monotonic()-t0}
                transcripts.append(item)
                if len([x for x in transcripts if x['participant']=='independent-verifier'])>=2:
                    state['second_transcript_at']=item['t'];second_transcript.set()
    try:
        await asyncio.wait_for(room.connect(args.url or env['LIVEKIT_URL'],token),30)
        for _ in range(300):
            if room.remote_participants:break
            await asyncio.sleep(.2)
        assert room.remote_participants,'No real agent participant joined'
        for _ in range(150):
            if any(pub.kind==rtc.TrackKind.KIND_AUDIO for peer in room.remote_participants.values() for pub in peer.track_publications.values()):break
            await asyncio.sleep(.2)
        assert any(pub.kind==rtc.TrackKind.KIND_AUDIO for peer in room.remote_participants.values() for pub in peer.track_publications.values()),'Agent joined but published no audio track'
        source=rtc.AudioSource(24000,1);track=rtc.LocalAudioTrack.create_audio_track('verification-wav',source)
        await room.local_participant.publish_track(track,rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE))
        async def publish_wav(path):
            with wave.open(str(path),'rb') as w:
                assert w.getsampwidth()==2 and w.getnchannels()==1
                raw=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16);sr=w.getframerate()
            converted=np.interp(np.arange(0,len(raw),sr/24000),np.arange(len(raw)),raw).astype(np.int16)
            for start in range(0,len(converted),480):
                samples=converted[start:start+480]
                if len(samples)<480:samples=np.pad(samples,(0,480-len(samples)))
                await source.capture_frame(rtc.AudioFrame(data=samples.tobytes(),sample_rate=24000,num_channels=1,samples_per_channel=480))
            await source.wait_for_playout()
            return len(converted)/24000
        begin=time.monotonic()-t0
        input_duration=await publish_wav(args.wav);speech_end=time.monotonic()-t0
        for _ in range(100):
            await source.capture_frame(rtc.AudioFrame(data=bytes(960),sample_rate=24000,num_channels=1,samples_per_channel=480))
        try:
            await asyncio.wait_for(first.wait(),args.timeout)
        except asyncio.TimeoutError:
            args.output.write_text(json.dumps({'check':'webrtc_first_audio_diagnostic','verified':False,'room':room_name,'remote_participants':list(room.remote_participants),'input_duration_s':input_duration,'input_end_s':speech_end,'transcriptions':transcripts,'audio_frames':audio,'reason':'no non-silent remote audio before timeout'},ensure_ascii=False,indent=2)+'\n')
            raise
        interruption=None
        if args.interrupt_wav:
            await asyncio.sleep(args.interrupt_delay)
            interrupt_started=time.monotonic()-t0
            interrupt_duration=await publish_wav(args.interrupt_wav)
            interrupt_end=time.monotonic()-t0
            for _ in range(100):
                await source.capture_frame(rtc.AudioFrame(data=bytes(960),sample_rate=24000,num_channels=1,samples_per_channel=480))
            try:
                await asyncio.wait_for(second_transcript.wait(),args.timeout)
            except asyncio.TimeoutError:
                args.output.write_text(json.dumps({'check':'interruption_diagnostic','verified':False,'room':room_name,'remote_participants':list(room.remote_participants),'interrupt_started_s':interrupt_started,'interrupt_end_s':interrupt_end,'transcriptions':transcripts,'audio_frames':audio,'reason':'second final user transcription did not arrive before timeout'},ensure_ascii=False,indent=2)+'\n')
                raise
            transcript_at=state['second_transcript_at']
            # Give the renewed LLM/TTS turn time to publish non-silent audio.
            try:
                await asyncio.wait_for(resumed_audio.wait(),args.timeout)
            except asyncio.TimeoutError:
                args.output.write_text(json.dumps({'check':'interruption_diagnostic','verified':False,'room':room_name,'remote_participants':list(room.remote_participants),'interrupt_started_s':interrupt_started,'interrupt_end_s':interrupt_end,'second_transcription_s':state['second_transcript_at'],'transcriptions':transcripts,'audio_frames':audio,'reason':'no resumed non-silent audio after second transcription'},ensure_ascii=False,indent=2)+'\n')
                raise
            active_during_interrupt=any(f['rms']>20 and interrupt_started-0.5<=f['t']<=interrupt_started+0.8 for f in audio)
            continued_before_new_transcript=[f for f in audio if f['rms']>20 and interrupt_started+1.0<f['t']<transcript_at]
            interruption={'verified':active_during_interrupt and not continued_before_new_transcript,'interrupt_started_s':interrupt_started,'interrupt_end_s':interrupt_end,'interrupt_input_duration_s':interrupt_duration,'second_transcription_s':transcript_at,'resumed_audio_s':next(f['t'] for f in audio if f['rms']>20 and f['t']>transcript_at+1.0),'audio_continued_during_listening_frames':len(continued_before_new_transcript)}
            assert interruption['verified'],'Could not verify cancellation of active response and resumed audio after the second turn'
        else:
            await asyncio.sleep(3)
        non_silent=[f for f in audio if f['rms']>20 and f['t']>=speech_end]
        assert non_silent and sum(f['samples'] for f in non_silent)>2400,'Remote audio must contain real non-silent PCM'
        assert any('bonjour' in t['text'].lower() and t['participant']=='independent-verifier' for t in transcripts),'No real French input transcription received over LiveKit'
        result={'check':'independent_real_webrtc_wav_to_remote_audio','verified':True,'physical_microphone':False,'url':args.url or env['LIVEKIT_URL'],'room':room_name,'remote_participants':list(room.remote_participants),'input_duration_s':input_duration,'input_started_s':begin,'input_end_s':speech_end,'first_remote_non_silent_s':non_silent[0]['t'],'end_to_first_audio_s':non_silent[0]['t']-speech_end,'received_audio_samples':sum(f['samples'] for f in audio),'peak_frame_rms':max(f['rms'] for f in audio),'transcriptions':transcripts,'interruption':interruption,'interrupt_confirmed':bool(interruption and interruption.get('verified')),'limits':['No physical microphone/listening','Interruption and reconnection require separate evidence']}
        from google.protobuf.json_format import MessageToDict
        stats=await room.get_rtc_stats()
        result['rtc_route_stats']={name:[MessageToDict(item,preserving_proto_field_name=True) for item in values if item.WhichOneof('stats') in ('transport','candidate_pair','local_candidate','remote_candidate')] for name,values in [('publisher',stats.publisher_stats),('subscriber',stats.subscriber_stats)]}
        result['limits'].append('A Tailscale signaling URL alone does not establish the selected media route; inspect RTC candidate-pair stats.')
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
    finally:
        await room.disconnect()
        for task in receivers:task.cancel()
        await asyncio.gather(*receivers,return_exceptions=True)
        if source is not None:await source.aclose()
        try:await lkapi.room.delete_room(api.DeleteRoomRequest(room=room_name))
        finally:await lkapi.aclose()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--project',type=Path,default=Path('/var/lib/jarvis/projects/mission23/livekit-agent'));p.add_argument('--wav',type=Path,required=True);p.add_argument('--url');p.add_argument('--token-url');p.add_argument('--timeout',type=float,default=180);p.add_argument('--interrupt-wav',type=Path);p.add_argument('--interrupt-delay',type=float,default=0.6);p.add_argument('--output',type=Path,required=True);asyncio.run(verify(p.parse_args()))
