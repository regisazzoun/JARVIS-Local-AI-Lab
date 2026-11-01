"""Extend the installed context guard with native Ollama and canonical admission.

One existing ComputeQueue, no new scheduler/database. WebUI uses native calls;
Qwen Code retains its working OpenAI-to-native translation and tool protocol.
"""
import importlib.util,json,os,sys,threading,time,urllib.request,urllib.error,copy,hashlib,sqlite3
from http.server import ThreadingHTTPServer
from contextlib import closing
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
BUDGET=27648
READOUT_HINT='\nJARVIS gateway — phase de restitution uniquement. Le budget de ce tour impose de présenter maintenant les résultats déjà obtenus. Aucun outil n’est proposé pour cette réponse. Réponds à la demande propriétaire initiale à partir des reçus présents, avec leurs limites et inconnues. Distingue faits, hypothèses, refus et travail non achevé ; n’annonce jamais une opération ou un succès non démontré. Ne lance et ne demande aucun nouvel outil. Cette phase ne valide aucune mission ; elle restitue les observations existantes.'

def canonical_client_receipt(content):
    """Recognize a real archived client receipt, never a model declaration."""
    try:
        value=json.loads(content);receipt=value.get('client_receipt') or {};ident=receipt.get('audit_id')
        if type(ident) is not int or not receipt.get('request_id'):return None
        with closing(sqlite3.connect('file:'+str(old.EMPTY_MEMORY)+'?mode=ro',uri=True,timeout=5)) as db:
            row=db.execute("SELECT target FROM audit WHERE id=? AND operation='client_tool_result'",(ident,)).fetchone()
        if not row:return None
        stored=json.loads(row[0])
        if stored.get('request_id')!=receipt['request_id'] or not stored.get('origin','').startswith('OpenWebUI'):return None
        if not isinstance(stored.get('result'),dict) or 'ok' not in stored['result']:return None
        if value.get('tool') not in (None,stored.get('tool')):return None
        return ident
    except (ValueError,TypeError,AttributeError,sqlite3.Error):return None

def result_readout(data,budget=BUDGET,receipt_checker=None):
    """Preserve every original message; close only tools for a final readout.

    No tool result, owner constraint or message is shortened. If metadata
    removal cannot fit, keep the original rejection. Structured contracts
    and requests without actual canonical client results are not rewritten.
    """
    messages=data.get('messages',[])
    if not data.get('tools') or data.get('format') or not isinstance(messages,list):return None
    if any(not isinstance(m,dict) or not isinstance(m.get('content',''),(str,type(None))) for m in messages):return None
    checker=receipt_checker or canonical_client_receipt
    refs=set()
    for message in messages:
        if message.get('role')=='tool' and isinstance(message.get('content'),str):
            ref=checker(message['content'])
            if type(ref) is int and ref>0:refs.add(ref)
    if not refs:return None
    result=copy.deepcopy(data);result.pop('tools',None);result.pop('tool_choice',None)
    if result['messages'] and result['messages'][0].get('role')=='system' and isinstance(result['messages'][0].get('content'),str):
        result['messages'][0]['content']+=READOUT_HINT
    else:result['messages'].insert(0,{'role':'system','content':READOUT_HINT})
    result['messages'].append({'role':'user','content':'Message automatique de passerelle JARVIS, pas une nouvelle autorisation propriétaire : montre maintenant les résultats déjà obtenus sur la demande initiale. Utilise uniquement les résultats existants, sans lancer ni demander aucun autre outil. Présente les inconnues et le travail non achevé honnêtement.'})
    raw=json.dumps(result,ensure_ascii=False,separators=(',',':')).encode()
    if len(raw)>budget:return None
    return result,{'phase':'result_readout','observed_client_receipts':sorted(refs),'forwarded_input_bytes':len(raw),'message_values_preserved':True,'new_tools_allowed':False}

def valid_readout_response(body):
    try:items=[json.loads(line) for line in body.splitlines() if line.strip()]
    except (ValueError,TypeError):return False
    return bool(items and items[-1].get('done') is True and any(item.get('message',{}).get('content') for item in items) and not any(item.get('error') or item.get('message',{}).get('tool_calls') for item in items))

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
        if not 0<n<=(1000000 if self.path=='/api/chat' else BUDGET):self.reject(413,'Split request before transmission; approved byte budget27648',n);return
        raw=None;model='qwen3-coder-next:q4_K_M';role='mission';self.readout_mode=False;readout_meta={}
        if self.path=='/api/chat':
            try:
                incoming=self.rfile.read(n);data=json.loads(incoming);model=data.get('model');opts=dict(data.get('options') or {})
                if model not in MODELS:raise ValueError('Unapproved model')
                ctx=opts.get('num_ctx',32768)
                if not isinstance(ctx,int) or ctx>32768 or ctx<=0:raise ValueError('Context outside approved32768 window')
                opts['num_ctx']=32768;predict=opts.get('num_predict',4096)
                opts['num_predict']=min(predict,4096) if isinstance(predict,int) and predict>0 else 4096
                data['options']=opts;data.setdefault('keep_alive','10m');raw=json.dumps(data,ensure_ascii=False,separators=(',',':')).encode();role='critical'
                if len(raw)>BUDGET:
                    readout=result_readout(data)
                    if not readout:self.reject(413,'Split request before transmission; approved byte budget27648',len(raw));return
                    data,readout_meta=readout;raw=json.dumps(data,ensure_ascii=False,separators=(',',':')).encode();self.readout_mode=True
                    archive=old.ROOT/('readout-source-'+str(time.time_ns())+'.json');archive.write_bytes(incoming);archive.chmod(0o600)
                    readout_meta.update(original_input_bytes=n,original_request_sha256=hashlib.sha256(incoming).hexdigest(),original_private_archive=archive.name,forwarded_sha256=hashlib.sha256(raw).hexdigest())
            except (ValueError,TypeError) as e:self.reject(400,str(e),n);return
        ident=None;stop=threading.Event();entry={'time':time.time(),'path':self.path,'role':role,'model':model,'input_bytes':n,'node':'Dell1',**readout_meta}
        if raw is not None:entry['forwarded_input_bytes']=len(raw)
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
            if ident:QUEUE.finish(ident,metrics={'gateway':True,'path':self.path,'role':role,'http_status':entry['http_status'],'forwarded_input_bytes':entry.get('forwarded_input_bytes'),'phase':entry.get('phase')},error=None if entry['http_status']==200 else 'Gateway transport not successful')
            with LOG.open('a') as f:f.write(json.dumps(entry)+'\n')
    def forward(self,path,raw):
        try:
            with urllib.request.urlopen(urllib.request.Request(UPSTREAM+path,data=raw,headers={'Content-Type':'application/json'}),timeout=600) as r:
                if getattr(self,'readout_mode',False):
                    body=r.read()
                    if not valid_readout_response(body):
                        rejected=old.ROOT/('readout-response-rejected-'+str(time.time_ns())+'.jsonl');rejected.write_bytes(body);rejected.chmod(0o600)
                        self.reject(409,'Readout did not produce a final text without tools; no new operation dispatched',len(raw or b''));return
                    self.send_response(r.status);self.send_header('Content-Type',r.headers.get('Content-Type','application/json'));self.send_header('Connection','close');self.end_headers();self.wfile.write(body);self.wfile.flush();return
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
