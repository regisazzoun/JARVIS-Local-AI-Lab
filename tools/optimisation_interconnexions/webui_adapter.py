"""Thin Open WebUI tools/audio adapter. Canonical JARVIS API owns missions.

No scheduler, model weights, or second canonical memory are created here.
Qwen Code runs one bounded specialist call at a time in dedicated projects.
"""
import sqlite3, datetime, email, email.policy, hashlib, http.cookiejar, json, os, re, secrets, subprocess, threading, time, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
PRIVATE=Path('/home/adminjarvis/JARVIS/qwen-code-openwebui-private')
PROJECTS=Path('/home/adminjarvis/JARVIS/qwen-code-projects')
KEY=(PRIVATE/'adapter-key').read_text().strip()
LOCK=threading.Lock()
class Jarvis:
    def __init__(self):
        self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def request(self,path,data=None,binary=False):
        headers={'X-Jarvis-Request':'1','Content-Type':'application/octet-stream' if binary else 'application/json'}
        raw=data if binary else json.dumps(data).encode() if data is not None else None
        def call():return self.opener.open(urllib.request.Request('http://127.0.0.1:8765'+path,data=raw,headers=headers),timeout=180)
        try:return call().read()
        except urllib.error.HTTPError as e:
            if e.code!=401:raise
            token=secrets.token_urlsafe(32)
            with sqlite3.connect('/opt/jarvis/conversation/runtime/memory.sqlite',timeout=10) as db:
                db.execute('DELETE FROM auth_sessions WHERE expires<=?',(time.time(),))
                db.execute('INSERT INTO auth_sessions(digest,expires) VALUES(?,?)',(hashlib.sha256(token.encode()).hexdigest(),time.time()+28800))
            self.opener.addheaders=[('Cookie','jarvis_session='+token)]
            return call().read()
J=Jarvis()
class Handler(BaseHTTPRequestHandler):
    def setup(self):
        super().setup();self.connection.settimeout(700)
    def log_message(self,*args):pass
    def send(self,value,status=200,mime='application/json'):
        raw=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/health':self.send({'status':'ok','canonical':'JARVIS existing API'});return
        self.send({'error':'not found'},404)
    def do_POST(self):
        if not secrets.compare_digest(self.headers.get('Authorization',''),'Bearer '+KEY):self.send({'error':'unauthorized'},401);return
        n=int(self.headers.get('Content-Length','0'))
        if self.headers.get('Transfer-Encoding','').lower()=='chunked':
            blocks=[];total=0
            while True:
                line=self.rfile.readline(128)
                size=int(line.split(b';',1)[0].strip(),16)
                if size==0:
                    while self.rfile.readline(4096).strip():pass
                    break
                total+=size
                if total>16000000:self.send({'error':'size'},413);return
                blocks.append(self.rfile.read(size))
                if self.rfile.read(2)!=b'\r\n':self.send({'error':'chunk format'},400);return
            raw=b''.join(blocks)
        else:
            if n<=0 or n>16000000:self.send({'error':'size'},413);return
            raw=self.rfile.read(n)
        try:
            if self.path=='/v1/audio/transcriptions':
                msg=email.message_from_bytes(('Content-Type: '+self.headers['Content-Type']+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+raw,policy=email.policy.default)
                parts=[p for p in msg.iter_parts() if p.get_param('name',header='content-disposition')=='file']
                if len(parts)!=1:raise ValueError('one audio file required')
                result=json.loads(J.request('/api/stt',parts[0].get_payload(decode=True),True));self.send({'text':result.get('text',result.get('transcription',''))});return
            d=json.loads(raw)
            if self.path=='/v1/audio/speech':self.send(J.request('/api/tts',{'text':d['input']}),mime='audio/wav');return
            if self.path=='/tools/missions':
                result=json.loads(J.request('/api/missions'))
                rows=result if isinstance(result,list) else result.get('missions',result.get('items',[]))
                self.send({'operation':'mission_list','created':False,'canonical':'existing JARVIS mission engine','count':len(rows),'recent':[{'id':r.get('id'),'state':r.get('state'),'title':str(r.get('title',r.get('goal','')))[:180]} for r in rows[:12]],'details':'Consult JL03 for full persistent events'});return
            if self.path=='/tools/jarvis_task':
                goal=d['goal']
                if not isinstance(goal,str) or not 1<=len(goal)<=2000:raise ValueError('goal length 1..2000')
                result=json.loads(J.request('/api/missions',{'goal':goal,'model':'qwen3-coder-next:q4_K_M','project':'Qwen-WebUI','request_kind':'mission'}))
                if not re.fullmatch('[0-9a-f]{32}',str(result.get('id',''))):
                    self.send({'error':'Invalid canonical mission receipt; inspect the registry before any resubmission','state':'UNKNOWN','created':None},502);return
                self.send({'operation':'mission_create','created':True,**{k:result.get(k) for k in ['id','mission_id','conversation','state']}});return
            if self.path!='/tools/qwen_code':self.send({'error':'not found'},404);return
            project=d.get('project','acceptance');task=d['task']
            if not re.fullmatch('[a-zA-Z0-9_-]{1,48}',project) or not isinstance(task,str) or not 1<=len(task)<=3000:raise ValueError('project identifier or task invalid')
            wd=PROJECTS/project
            if wd.is_symlink() or not wd.is_dir() or wd.resolve().parent!=PROJECTS.resolve():raise ValueError('existing dedicated project required')
            if not LOCK.acquire(False):self.send({'error':'Qwen Code busy; no duplicate dispatched'},409);return
            try:
                ident=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%f')
                out=PRIVATE/(ident+'.jsonl');err=PRIVATE/(ident+'.stderr')
                before=subprocess.check_output(['git','rev-parse','HEAD'],cwd=wd,text=True).strip()
                started=time.monotonic()
                with out.open('w') as o,err.open('w') as e:
                    run=subprocess.run(['/home/adminjarvis/.local/bin/qwen-local-task',task],cwd=wd,stdout=o,stderr=e,timeout=660)
                diff=subprocess.check_output(['git','diff','--'],cwd=wd)
                receipt={'id':ident,'actor':'Qwen Code','trigger':'Open WebUI tool','model':'qwen3-coder-next:q4_K_M','inference_machine':'Dell1','execution_machine':'Mac mini experimental workspace','project':project,'base_commit':before,'returncode':run.returncode,'seconds':round(time.monotonic()-started,2),'diff_sha256':hashlib.sha256(diff).hexdigest(),'trace':str(out),'trace_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'validation':'NOT_INDEPENDENTLY_VALIDATED'}
                lines=[json.loads(l) for l in out.read_text().splitlines() if l.startswith('{')]
                receipt['result']=next((x for x in reversed(lines) if x.get('type')=='result'),{})
                (PRIVATE/(ident+'-receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n');self.send(receipt)
            finally:LOCK.release()
        except (ValueError,KeyError) as e:self.send({'error':str(e),'status':'NOT_EXECUTED'},400)
        except Exception as e:self.send({'error':str(e),'status':'NOT_VALIDATED'},502)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8092),Handler).serve_forever()
