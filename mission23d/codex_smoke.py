#!/usr/bin/env python3
"""Independent acceptance tool for the temporary server; prints no bearer token."""
import asyncio,json,time,urllib.request,uuid
from pathlib import Path
from livekit import api,rtc
import jwt

async def main():
    root=Path(__file__).resolve().parent;report={'actor':'Codex-test-run-by-JARVIS','utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'checks':{}}
    env={}
    for line in (root.parent/'livekit-agent/.env').read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            k,v=line.split('=',1);env[k.strip()]=v.strip().strip('"\'')
    room=rtc.Room();server=None;room_name=None
    try:
        with urllib.request.urlopen('http://127.0.0.1:8783/',timeout=10) as r:page=r.read()
        assert b'JARVIS' in page and b'<html' in page.lower();report['checks']['page_http']=True
        with urllib.request.urlopen('http://127.0.0.1:8783/fixtures/initial.wav',timeout=10) as r:wav=r.read()
        assert wav[:4]==b'RIFF' and len(wav)>10000;report['checks']['real_fixture_http']=True
        with urllib.request.urlopen('http://127.0.0.1:8783/token',timeout=30) as r:credentials=json.load(r)
        claims=jwt.decode(credentials['token'],env['LIVEKIT_API_SECRET'],algorithms=['HS256'],options={'verify_aud':False})
        room_name=claims['video']['room'];assert claims['video']['roomJoin'];assert 0<claims['exp']-time.time()<=900
        assert credentials.get('room')==room_name;report['checks']['signed_short_lived_room_token']=True
        report['room']=room_name
        url=env['LIVEKIT_URL'];server=api.LiveKitAPI(url=url.replace('ws://','http://').replace('wss://','https://'),api_key=env['LIVEKIT_API_KEY'],api_secret=env['LIVEKIT_API_SECRET'])
        dispatch=await server.agent_dispatch.list_dispatch(room_name)
        assert any(x.agent_name=='jarvis-agent' for x in dispatch);report['checks']['real_named_dispatch']=True
        await asyncio.wait_for(room.connect(url,credentials['token']),30)
        for _ in range(300):
            if any(p.track_publications for p in room.remote_participants.values()):break
            await asyncio.sleep(.2)
        assert any(p.track_publications for p in room.remote_participants.values()),'No actual agent audio track'
        report['checks']['rtc_connected_real_agent_audio_track']=True
        report['ok']=True
    except Exception as e:report.update(ok=False,error=f'{type(e).__name__}: {e}')
    finally:
        await room.disconnect()
        if server:
            try:
                if room_name:await server.room.delete_room(api.DeleteRoomRequest(room=room_name));report['checks']['own_room_cleanup']=True
            finally:await server.aclose()
        out=root/'reports/server-smoke.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(report,ensure_ascii=False))
    return 0 if report.get('ok') else 1

if __name__=='__main__':raise SystemExit(asyncio.run(main()))
