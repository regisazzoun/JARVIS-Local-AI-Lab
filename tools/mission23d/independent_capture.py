#!/usr/bin/env python3
"""Codex independent measurement tool; real RTC PCM, no application replacement."""
import argparse,asyncio,datetime,hashlib,json,time,uuid,wave
from pathlib import Path
import numpy as np
from livekit import api,rtc

async def run(a):
    a.output.mkdir(parents=True,exist_ok=True)
    t0=time.monotonic();events=[];frames=[];transcripts=[];tasks=[];pcm=[]
    def now():return time.monotonic()-t0
    def log(kind,**values):
        row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'t':now(),'event':kind,**values};events.append(row)
        with (a.output/'events-live.jsonl').open('a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
        return row
    env={}
    for line in (a.project/'.env').read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            k,v=line.split('=',1);env[k.strip()]=v.strip().strip('"\'')
    url=env['LIVEKIT_URL'];room_name='m23d-codex-'+uuid.uuid4().hex[:10]
    server=api.LiveKitAPI(url=url.replace('ws://','http://').replace('wss://','https://'),api_key=env['LIVEKIT_API_KEY'],api_secret=env['LIVEKIT_API_SECRET'])
    room=rtc.Room();source=None;queue=asyncio.Queue();first=asyncio.Event();second=asyncio.Event();joined=asyncio.Event();reason=None;interrupt=None;input_end=None
    identity='codex-measurement'
    @room.on('participant_connected')
    def participant(peer):log('participant_connected',identity=peer.identity);joined.set()
    @room.on('transcription_received')
    def transcription(segments,participant,publication):
        for s in segments:
            if s.final:
                row=log('transcription_final',text=s.text,identity=participant.identity if participant else None);transcripts.append(row)
                if sum(x['identity']==identity for x in transcripts)>=2:second.set()
    @room.on('data_received')
    def data(packet):
        try:body=json.loads(packet.data)
        except Exception:return
        log('data_received',topic=packet.topic,body=body)
    @room.on('participant_attributes_changed')
    def attributes(changed,peer):log('participant_attributes',identity=peer.identity,attributes=dict(changed))
    @room.on('track_subscribed')
    def track_subscribed(track,pub,peer):
        if track.kind!=rtc.TrackKind.KIND_AUDIO:return
        log('audio_track_subscribed',identity=peer.identity);joined.set()
        async def receive():
            stream=rtc.AudioStream(track,sample_rate=24000,num_channels=1)
            try:
                async for e in stream:
                    raw=bytes(e.frame.data);s=np.frombuffer(raw,dtype=np.int16);rms=float(np.sqrt(np.mean(s.astype(float)**2)))
                    row={'t':now(),'rms':rms,'samples':len(s)};frames.append(row);pcm.append((row['t'],raw))
                    if rms>20:first.set()
            finally:await stream.aclose()
        tasks.append(asyncio.create_task(receive()))
    async def pump():
        # Continuous microphone-clock equivalent, including silence between WAVs.
        deadline=time.monotonic()
        while True:
            try:raw=queue.get_nowait()
            except asyncio.QueueEmpty:raw=bytes(960)
            await source.capture_frame(rtc.AudioFrame(data=raw,sample_rate=24000,num_channels=1,samples_per_channel=480))
            deadline+=.02;await asyncio.sleep(max(0,deadline-time.monotonic()))
    async def send(path,label):
        with wave.open(str(path),'rb') as w:
            assert w.getnchannels()==1 and w.getsampwidth()==2
            sr=w.getframerate();raw=np.frombuffer(w.readframes(w.getnframes()),np.int16)
        s=np.interp(np.arange(0,len(raw),sr/24000),np.arange(len(raw)),raw).astype(np.int16)
        start=log('wav_started',label=label,file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),duration_s=len(s)/24000)['t']
        for i in range(0,len(s),480):queue.put_nowait(np.pad(s[i:i+480],(0,max(0,480-len(s[i:i+480])))).tobytes())
        while not queue.empty():await asyncio.sleep(.01)
        await asyncio.sleep(.12);log('wav_ended',label=label)
        return start,now()
    try:
        await server.room.create_room(api.CreateRoomRequest(name=room_name))
        await server.agent_dispatch.create_dispatch(api.CreateAgentDispatchRequest(agent_name='jarvis-agent',room=room_name))
        token=api.AccessToken(env['LIVEKIT_API_KEY'],env['LIVEKIT_API_SECRET']).with_identity(identity).with_grants(api.VideoGrants(room_join=True,room=room_name)).to_jwt()
        await asyncio.wait_for(room.connect(url,token),30);log('connected',room=room_name)
        for _ in range(300):
            if any(p.track_publications for p in room.remote_participants.values()):break
            await asyncio.sleep(.2)
        assert room.remote_participants,'No agent participant'
        source=rtc.AudioSource(24000,1,queue_size_ms=100)
        track=rtc.LocalAudioTrack.create_audio_track('continuous-synthetic-mic',source)
        await room.local_participant.publish_track(track,rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE))
        tasks.append(asyncio.create_task(pump()));await asyncio.sleep(1)
        _,input_end=await send(a.wav,'initial')
        await asyncio.wait_for(first.wait(),300)
        if a.interrupt_wav:
            await asyncio.sleep(a.delay)
            # Wait for actively audible PCM, not the historical first-audio latch.
            for _ in range(500):
                if any(f['rms']>20 and now()-.2<=f['t']<=now() for f in frames):break
                await asyncio.sleep(.02)
            else:raise RuntimeError('INVALID: no active audio at interruption')
            interrupt,_=await send(a.interrupt_wav,'interruption')
            try:await asyncio.wait_for(second.wait(),a.timeout)
            except asyncio.TimeoutError:reason='No second user final transcription before timeout'
            if reason is None:
                second_at=next(x['t'] for x in transcripts if x['identity']==identity and x['t']>interrupt)
                for _ in range(int(a.timeout*10)):
                    if any(f['rms']>20 and f['t']>second_at+1 for f in frames):break
                    await asyncio.sleep(.1)
                await asyncio.sleep(6)
        else:await asyncio.sleep(12)
        from google.protobuf.json_format import MessageToDict
        stats=await room.get_rtc_stats()
        routes={k:[MessageToDict(v,preserving_proto_field_name=True) for v in values if v.WhichOneof('stats') in ('transport','candidate_pair')] for k,values in [('publisher',stats.publisher_stats),('subscriber',stats.subscriber_stats)]}
        # Private route evidence may contain addresses. Publish only its hash.
        (a.output/'routes-private.json').write_text(json.dumps(routes,indent=2))
    except Exception as e:reason=f'{type(e).__name__}: {e}';log('error',reason=reason)
    finally:
        log('disconnect_requested');await room.disconnect();log('disconnected')
        for t in tasks:t.cancel()
        await asyncio.gather(*tasks,return_exceptions=True)
        if source:await source.aclose()
        try:await server.room.delete_room(api.DeleteRoomRequest(room=room_name));log('room_deleted')
        except Exception as e:log('cleanup_error',type=type(e).__name__)
        await server.aclose()
        # Arrival-aligned waveform retains gaps and all received samples.
        length=int((max((t for t,_ in pcm),default=0)+.1)*24000)
        output=np.zeros(length,dtype=np.int16)
        for t,raw in pcm:
            s=np.frombuffer(raw,np.int16);start=max(0,int(t*24000)-len(s));end=min(len(output),start+len(s));output[start:end]=s[:end-start]
        audio_path=a.output/'received.wav'
        with wave.open(str(audio_path),'wb') as w:w.setparams((1,2,24000,0,'NONE','not compressed'));w.writeframes(output.tobytes())
        (a.output/'events.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in events))
        (a.output/'frames.json').write_text(json.dumps(frames))
        stop_latency=None;active=None;second_row=None;resumed=None
        if interrupt is not None:
            active=any(f['rms']>20 and interrupt-.2<=f['t']<=interrupt for f in frames)
            # Require actual silent frames for500ms, not absent transport data.
            for i,f in enumerate(frames):
                if f['t']<interrupt:continue
                span=[x for x in frames[i:] if x['t']<=f['t']+.5]
                if len(span)>=45 and span[-1]['t']-f['t']>=.48 and all(x['rms']<=20 for x in span):
                    stop_latency=f['t']-interrupt;break
            second_row=next((x for x in transcripts if x['identity']==identity and x['t']>interrupt),None)
            if second_row:resumed=next((f['t']-second_row['t'] for f in frames if f['rms']>20 and f['t']>second_row['t']+1),None)
        result={'actor':'Codex-independent-tool','physical_microphone':False,'room':room_name,'reason':reason,'input_end_s':input_end,'interrupt_s':interrupt,'audio_active_before_interrupt':active,'stable_silence_latency_s':stop_latency,'second_user_final':second_row,'resumed_audio_after_transcript_s':resumed,'transcripts':transcripts,'first_non_silent_s':next((f['t'] for f in frames if f['rms']>20),None),'criteria':{'active_required':True,'stop_max_s':1,'silence_window_s':.5,'rms_threshold':20},'interruption_audio_pass':bool(active and stop_latency is not None and stop_latency<=1),'limits':['Synthetic WAV; no physical microphone','Arrival-aligned PCM; timings are client observations','Continuity and UI Stop require separate checks'],'artifacts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in a.output.iterdir() if p.is_file()}}
        (a.output/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('artifacts','transcripts')},ensure_ascii=False))
    return 0 if not reason and (not a.interrupt_wav or result['interruption_audio_pass']) else 1

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--project',type=Path,default=Path('/var/lib/jarvis/projects/mission23/livekit-agent'));p.add_argument('--wav',type=Path,required=True);p.add_argument('--interrupt-wav',type=Path);p.add_argument('--delay',type=float,default=.6);p.add_argument('--timeout',type=float,default=150);p.add_argument('--output',type=Path,required=True)
    raise SystemExit(asyncio.run(run(p.parse_args())))
