"""Extend the installed context guard with native Ollama and canonical admission.

One existing ComputeQueue, no new scheduler/database. WebUI uses native calls;
Qwen Code retains its working OpenAI-to-native translation and tool protocol.
"""
import importlib.util,json,os,sys,threading,time,urllib.request,urllib.error
from http.server import ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.compute import ComputeQueue,ResourceUnavailable
spec=importlib.util.spec_from_file_location('installed_qwen_guard',Path(__file__).resolve().parents[1]/'qwen_webui/ollama_guard.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
QUEUE=ComputeQueue(os.environ.get('JARVIS_MISSIONS_DB','/opt/jarvis/conversation/runtime/missions.sqlite'))
UPSTREAM=os.environ.get('JARVIS_DELL_OLLAMA_URL','http://192.168.1.75:11435')
WEBUI_WAIT=float(os.environ.get('JARVIS_WEBUI_QUEUE_TIMEOUT','30'))
MODELS={'qwen3-coder-next:q4_K_M','qwen3:32b-q4_K_M','llama3.3:70b-instruct-q4_K_M'}
LOG=Path(os.environ.get('JARVIS_ADMISSION_LOG','/home/adminjarvis/JARVIS/optimisation-interconnexions-ia-private/admission.jsonl'))
class Handler(old.Handler):
    def send_error(self,code,message=None,explain=None):
        message=message or 'Request refused'
        error=message if self.path.startswith('/api/') else {'message':message,'type':'gateway_error','code':str(code)}
        raw=json.dumps({'error':error,'status':code}).encode()
        self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)))
        if code==429:self.send_header('Retry-After','1')
        self.end_headers();self.wfile.write(raw)
    def send_response(self,code,message=None):
        self.observed_http_status=code;super().send_response(code,message)
    def reject(self,status,reason,size=0):
        with LOG.open('a') as f:f.write(json.dumps({'time':time.time(),'path':self.path,'http_status':status,'input_bytes':size,'rejected_before_dispatch':True,'reason':reason})+'\n')
        self.send_error(status,reason)
    def relay(self):
        if self.path in ['/api/version','/api/tags','/api/ps','/v1/models'] and self.command=='GET':
            return self.forward(self.path,None)
        if self.path=='/api/show' and self.command=='POST':
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<4096:self.send_error(413);return
            return self.forward(self.path,self.rfile.read(n))
        if self.path not in ['/api/chat','/v1/chat/completions'] or self.command!='POST':self.reject(403,'Endpoint outside inference scope');return
        n=int(self.headers.get('Content-Length','0'))
        if not 0<n<=27648:self.reject(413,'Split request before transmission; approved byte budget27648',n);return
        raw=None;model='qwen3-coder-next:q4_K_M';role='mission'
        if self.path=='/api/chat':
            try:
                data=json.loads(self.rfile.read(n));model=data.get('model');opts=dict(data.get('options') or {})
                if model not in MODELS:raise ValueError('Unapproved model')
                ctx=opts.get('num_ctx',32768)
                if not isinstance(ctx,int) or ctx>32768 or ctx<=0:raise ValueError('Context outside approved32768 window')
                opts['num_ctx']=32768;predict=opts.get('num_predict',4096)
                opts['num_predict']=min(predict,4096) if isinstance(predict,int) and predict>0 else 4096
                data['options']=opts;data.setdefault('keep_alive','10m');raw=json.dumps(data,ensure_ascii=False,separators=(',',':')).encode();role='critical'
            except (ValueError,TypeError) as e:self.reject(400,str(e),n);return
        ident=None;stop=threading.Event();entry={'time':time.time(),'path':self.path,'role':role,'model':model,'input_bytes':n,'node':'Dell1'}
        try:
            ident=QUEUE.enter('Dell1',model,role,timeout=WEBUI_WAIT if role=='critical' else 120);entry['queue_id']=ident
            def beat():
                while not stop.wait(5):QUEUE.heartbeat(ident)
            threading.Thread(target=beat,daemon=True).start()
            if raw is None:super().relay()
            else:self.forward('/api/chat',raw)
        except ResourceUnavailable as e:
            entry['error']=str(e);self.send_error(429,'Inference busy; canonical priority queue retained')
        finally:
            stop.set();entry['http_status']=getattr(self,'observed_http_status',None);entry['finished']=time.time()
            if ident:QUEUE.finish(ident,metrics={'gateway':True,'path':self.path,'role':role,'http_status':entry['http_status']},error=None if entry['http_status']==200 else 'Gateway transport not successful')
            with LOG.open('a') as f:f.write(json.dumps(entry)+'\n')
    def forward(self,path,raw):
        try:
            with urllib.request.urlopen(urllib.request.Request(UPSTREAM+path,data=raw,headers={'Content-Type':'application/json'}),timeout=600) as r:
                self.send_response(r.status);self.send_header('Content-Type',r.headers.get('Content-Type','application/json'));self.send_header('Connection','close');self.end_headers()
                while True:
                    block=r.read1(8192)
                    if not block:break
                    self.wfile.write(block);self.wfile.flush()
        except urllib.error.HTTPError as e:self.send_error(e.code,'Upstream returned an error')
        except Exception as e:
            try:self.send_error(502,'Inference transport failed')
            except Exception:pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8091),Handler).serve_forever()
