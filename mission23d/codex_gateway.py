#!/usr/bin/env python3
"""Codex operator tool: temporary loopback file/room/test gateway for LiveKit.
No model or voice implementation. Credentials stay in the existing private env.
"""
import argparse,asyncio,datetime,json,mimetypes,os,signal,socket,subprocess,sys,threading,time,uuid
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from livekit import api

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--env',type=Path,required=True);p.add_argument('--port',type=int,default=8783);a=p.parse_args();root=a.root.resolve();env={};rooms=set();jobs={};suite_job=None;lock=threading.Lock()
 for line in a.env.read_text().splitlines():
  if '=' in line and not line.lstrip().startswith('#'):
   k,v=line.split('=',1);env[k.strip()]=v.strip().strip('"\'')
 for k in ('LIVEKIT_API_KEY','LIVEKIT_API_SECRET','LIVEKIT_URL'):assert env.get(k),'Missing private configuration: '+k
 async def room_operation(room,create):
  client=api.LiveKitAPI(url=env['LIVEKIT_URL'].replace('ws://','http://').replace('wss://','https://'),api_key=env['LIVEKIT_API_KEY'],api_secret=env['LIVEKIT_API_SECRET'])
  try:
   if create:
    await client.room.create_room(api.CreateRoomRequest(name=room,empty_timeout=60,departure_timeout=10))
    await client.agent_dispatch.create_dispatch(api.CreateAgentDispatchRequest(agent_name='jarvis-agent',room=room))
   else:await client.room.delete_room(api.DeleteRoomRequest(room=room))
  finally:await client.aclose()
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def reply(self,value,status=200):
   raw=json.dumps(value,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
  def do_GET(self):
   path=urlparse(self.path).path
   try:
    if path in ('/status','/health'):
     with socket.create_connection(('127.0.0.1',7880),timeout=2):pass
     return self.reply({'mission':'23D','ok':True,'gateway':'Codex-operator-tool','active_rooms':len(rooms),'physical_microphone_tested':False})
    if path=='/token':
     room='m23d-web-'+uuid.uuid4().hex[:12];identity='web-'+uuid.uuid4().hex[:8]
     asyncio.run(room_operation(room,True))
     with lock:rooms.add(room)
     token=api.AccessToken(env['LIVEKIT_API_KEY'],env['LIVEKIT_API_SECRET']).with_identity(identity).with_grants(api.VideoGrants(room_join=True,room=room)).with_ttl(datetime.timedelta(minutes=10)).to_jwt()
     return self.reply({'token':token,'room':room,'identity':identity,'url':'ws://localhost:7880','expires_in_s':600})
    if path=='/suite':
     file=root/'reports/suite-summary.json'
     return self.reply({'running':suite_job is not None and suite_job.poll() is None,'returncode':suite_job.poll() if suite_job else None,'summary':json.loads(file.read_text()) if file.exists() else None})
    if path.startswith('/test/'):
     ident=path.split('/')[-1]
     if ident not in jobs:return self.reply({'error':'Unknown test'},404)
     job=jobs[ident];file=job['output']/'result.json';done=job['process'].poll() is not None
     return self.reply({'id':ident,'done':done,'returncode':job['process'].poll(),'result':json.loads(file.read_text()) if file.exists() else None,'audio':f'/reports/{job["output"].name}/received.wav' if done else None})
    relative='index.html' if path=='/' else path.lstrip('/')
    target=(root/relative).resolve()
    allowed=relative=='index.html' or relative.startswith(('fixtures/','vendor/')) or relative.startswith('reports/') and target.name!='routes-private.json' and target.suffix in ('.json','.jsonl','.wav')
    if not allowed or not target.is_relative_to(root) or not target.is_file():return self.reply({'error':'Not found'},404)
    raw=target.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(target.name)[0] or 'application/octet-stream');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
   except Exception as e:self.reply({'error':type(e).__name__+': '+str(e)},503)
  def do_POST(self):
   nonlocal suite_job
   try:
    origin=self.headers.get('Origin','')
    if origin and origin not in (f'http://localhost:{a.port}',f'http://127.0.0.1:{a.port}'):return self.reply({'error':'Origin not allowed'},403)
    length=int(self.headers.get('Content-Length','0'))
    if length>2048:return self.reply({'error':'Request too large'},413)
    data=json.loads(self.rfile.read(length) or '{}')
    if self.path=='/stop':
     room=data.get('room')
     with lock:owned=room in rooms
     if owned:
      asyncio.run(room_operation(room,False))
      with lock:rooms.discard(room)
     return self.reply({'stopped':owned,'room':room})
    if self.path=='/suite':
     with lock:
      if suite_job is not None and suite_job.poll() is None:return self.reply({'running':True,'already_started':True,'pid':suite_job.pid})
      with (root/'logs/suite.log').open('wb') as log:suite_job=subprocess.Popen([sys.executable,str(root/'codex_suite.py')],stdout=log,stderr=log,stdin=subprocess.DEVNULL,start_new_session=True)
     return self.reply({'running':True,'pid':suite_job.pid,'started_by':'authenticated local operator request; see broker caller receipt'},202)
    if self.path=='/test/stop':
     ident=data.get('id');job=jobs.get(ident)
     if not job:return self.reply({'error':'Unknown test'},404)
     if job['process'].poll() is None:os.killpg(job['process'].pid,signal.SIGINT)
     return self.reply({'stop_requested':True,'id':ident})
    if self.path=='/test':
     scenario=data.get('scenario','barge-early')
     if scenario not in ('barge-early','barge-late','nominal','silence','noise'):return self.reply({'error':'Unknown scenario'},400)
     with lock:
      if any(j['process'].poll() is None for j in jobs.values()):return self.reply({'error':'A test is already running'},409)
      ident=uuid.uuid4().hex[:12];output=root/'reports'/('web-'+ident);output.mkdir(parents=True)
      wav='initial' if scenario not in ('noise','silence') else scenario
      command=[sys.executable,str(root/'codex_capture.py'),'--project',str(a.env.parent),'--wav',str(root/'fixtures'/(wav+'.wav')),'--output',str(output),'--timeout','100']
      if scenario.startswith('barge'):command+=['--interrupt-wav',str(root/'fixtures/interrupt.wav'),'--delay','0.6' if scenario=='barge-early' else '2.5']
      if scenario in ('noise','silence'):command+=['--negative']
      with (output/'runner.log').open('wb') as log:process=subprocess.Popen(command,stdout=log,stderr=log,start_new_session=True,stdin=subprocess.DEVNULL)
      jobs[ident]={'process':process,'output':output}
     return self.reply({'id':ident,'scenario':scenario,'state':'running','status_url':'/test/'+ident},202)
    return self.reply({'error':'Not found'},404)
   except Exception as e:self.reply({'error':type(e).__name__+': '+str(e)},503)
 server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler)
 print(json.dumps({'listening':'127.0.0.1','port':a.port,'root':str(root),'credentials_printed':False}),flush=True)
 try:server.serve_forever()
 finally:
  server.server_close()
  for room in list(rooms):
   try:asyncio.run(room_operation(room,False))
   except Exception:pass

if __name__=='__main__':main()
