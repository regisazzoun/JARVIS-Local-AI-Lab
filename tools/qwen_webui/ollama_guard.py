"""Loopback-only OpenAI-compatible relay; reject oversized requests, never truncate."""
from contextlib import closing
import datetime, hashlib, json, os, time, urllib.request, urllib.error, sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
ROOT=Path(os.environ.get('QWEN_RECEIPTS','/home/adminjarvis/JARVIS/qwen-code-openwebui-private/requests'))
ROOT.mkdir(parents=True,exist_ok=True)
BUDGET=27648
EMPTY_MEMORY=Path('/opt/jarvis/conversation/runtime/memory.sqlite')

def empty_response_count(fingerprint,observe=False):
    """Transport incidents in canonical audit; separate from functional P2 cycles."""
    with closing(sqlite3.connect(EMPTY_MEMORY,timeout=10)) as db, db:
        if observe:
            db.execute('INSERT INTO audit(operation,target,created) VALUES(?,?,?)',('client_inference_empty',json.dumps({'fingerprint':fingerprint,'model':'qwen3-coder-next:q4_K_M'}),datetime.datetime.now(datetime.timezone.utc).isoformat()))
        return db.execute("SELECT count(*) FROM audit WHERE operation='client_inference_empty' AND json_extract(CASE WHEN json_valid(target) THEN target ELSE '{}' END,'$.fingerprint')=?",(fingerprint,)).fetchone()[0]

def native_payload(data):
    """Preserve call/result provenance across the two API contracts.

    No model decision or result is invented. Unsupported content is refused
    rather than silently omitted. The input dictionary remains unchanged.
    """
    import copy
    messages=copy.deepcopy(data['messages']);names={}
    for message in messages:
        content=message.get('content')
        if isinstance(content,list):
            if any(not isinstance(part,dict) or part.get('type')!='text' or not isinstance(part.get('text'),str) for part in content):
                raise ValueError('Only text content parts are supported by this local relay')
            message['content']='\n'.join(part['text'] for part in content)
        elif content is None:message['content']=''
        for call in message.get('tool_calls',[]):
            function=call['function'];arguments=function.get('arguments',{})
            if isinstance(arguments,str):arguments=json.loads(arguments)
            if not isinstance(arguments,dict):raise ValueError('Tool arguments must be an object')
            function['arguments']=arguments
            if call.get('id'):names[call['id']]=function['name']
        if message.get('role')=='tool':
            call_id=message.get('tool_call_id')
            if call_id not in names:raise ValueError('Tool result has no preceding matching call')
            name=names[call_id]
            if message.get('tool_name',name)!=name:raise ValueError('Tool result name contradicts its call')
            message['tool_name']=name
    limit=data.get('max_completion_tokens',data.get('max_tokens',4096))
    if type(limit) is not int or limit<=0:raise ValueError('Positive output token limit required')
    payload={'model':data['model'],'messages':messages,'tools':data.get('tools',[]),'stream':True,
            'options':{'num_ctx':32768,'num_predict':min(limit,4096),'temperature':data.get('temperature',0.1)},'keep_alive':'10m'}
    response_format=data.get('response_format')
    if response_format:
        if response_format.get('type')=='json_object':payload['format']='json'
        elif response_format.get('type')=='json_schema':
            schema=response_format.get('json_schema',{}).get('schema')
            if not isinstance(schema,dict):raise ValueError('response_format requires an object JSON schema')
            payload['format']=copy.deepcopy(schema)
        else:raise ValueError('Unsupported response_format; refusing silent contract loss')
    return payload

def finish_reason(item,had_tools):
    if item.get('done_reason')=='length':return 'length'
    return 'tool_calls' if had_tools else 'stop'

def completion_response(data,ident,items):
    """Return the non-streaming OpenAI contract used by compaction/verifiers."""
    message={'role':'assistant','content':''};calls=[];last={}
    for item in items:
        last=item;part=item.get('message',{})
        message['content']+=part.get('content','')
        if part.get('thinking'):message['reasoning_content']=message.get('reasoning_content','')+part['thinking']
        for call in part.get('tool_calls',[]):
            function=call['function']
            calls.append({'id':call.get('id','call_'+str(len(calls))+'_'+ident),'type':'function','function':{'name':function['name'],'arguments':json.dumps(function.get('arguments',{}),ensure_ascii=False)}})
    if calls:message['tool_calls']=calls
    usage={'prompt_tokens':last.get('prompt_eval_count',0),'completion_tokens':last.get('eval_count',0)}
    usage['total_tokens']=sum(usage.values())
    return {'id':'chatcmpl-'+ident,'object':'chat.completion','created':int(time.time()),'model':data['model'],'choices':[{'index':0,'message':message,'finish_reason':finish_reason(last,bool(calls))}],'usage':usage}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self): self.relay()
    def do_POST(self): self.relay()
    def relay(self):
        if self.path not in ['/v1/chat/completions','/v1/models']:
            self.send_error(404); return
        n=int(self.headers.get('Content-Length','0'))
        if n>1000000:self.send_error(413);return
        raw=self.rfile.read(n) if n else None
        ident=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%f')
        record={'time':ident,'actor':'Qwen Code','inference_machine':'Dell1','model':'qwen3-coder-next:q4_K_M','path':self.path,'bytes':n,'budget_bytes':BUDGET,'sha256':hashlib.sha256(raw or b'').hexdigest()}
        if raw:
            data=json.loads(raw)
            if data.get('model')!='qwen3-coder-next:q4_K_M' or n>BUDGET:
                record['status']='REFUSED_BEFORE_INFERENCE';(ROOT/(ident+'.json')).write_text(json.dumps(record));self.send_error(413,'Model or context budget refused');return
            # The established model is retained; cap output and request the approved runtime window.
            try:payload=native_payload(data)
            except (ValueError,KeyError,TypeError) as exc:
                record.update(status='REFUSED_BEFORE_INFERENCE',error=str(exc));(ROOT/(ident+'.json')).write_text(json.dumps(record));self.send_error(400,str(exc));return
            record.update(client_stream=data.get('stream',False),response_format_type=(data.get('response_format') or {}).get('type'),native_structured_format=bool(payload.get('format')))
            fingerprint=hashlib.sha256(json.dumps({k:data.get(k) for k in ('model','messages','tools','response_format')},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            if empty_response_count(fingerprint)>=3:
                record.update(status='BLOCKED_EMPTY_RESPONSE_RETRIES',request_fingerprint=fingerprint)
                (ROOT/(ident+'.json')).write_text(json.dumps(record))
                self.send_error(400,'Three empty model responses for this unchanged request; inspect context and provider traces before a technically changed retry. No fourth inference dispatched.');return
        try:
            if self.path=='/v1/models':
                req=urllib.request.Request('http://192.168.1.75:11435/v1/models')
                with urllib.request.urlopen(req,timeout=20) as r:
                    self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(r.read())
            else:
                # Ollama's OpenAI endpoint does not accept num_ctx. Translate to native chat.
                req=urllib.request.Request('http://192.168.1.75:11435/api/chat',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req,timeout=600) as r:
                    if not data.get('stream',False):
                        items=[json.loads(line) for line in r if line.strip()]
                        complete=completion_response(data,ident,items);raw_complete=json.dumps(complete,ensure_ascii=False).encode()
                        message=complete['choices'][0]['message']
                        if not message.get('content') and not message.get('reasoning_content') and not message.get('tool_calls'):record['empty_response_count']=empty_response_count(fingerprint,True)
                        self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw_complete)));self.end_headers();self.wfile.write(raw_complete)
                        record.update(status='FORWARDED',runtime_num_ctx=32768,max_output_tokens=payload['options']['num_predict'],prompt_eval_count=complete['usage']['prompt_tokens'],eval_count=complete['usage']['completion_tokens'])
                        return
                    self.send_response(200);self.send_header('Content-Type','text/event-stream');self.send_header('Connection','close');self.end_headers()
                    tool_index=0;had_tools=False;had_content=False
                    for line in r:
                        if not line.strip():continue
                        item=json.loads(line);msg=item.get('message',{});delta={}
                        had_content=had_content or bool(msg.get('content') or msg.get('thinking'))
                        if msg.get('content'):delta['content']=msg['content']
                        if msg.get('thinking'):delta['reasoning_content']=msg['thinking']
                        if msg.get('tool_calls'):
                            had_tools=True;delta['tool_calls']=[]
                            for tc in msg['tool_calls']:
                                f=tc['function'];delta['tool_calls'].append({'index':tool_index,'id':tc.get('id','call_'+str(tool_index)+'_'+ident),'type':'function','function':{'name':f['name'],'arguments':json.dumps(f.get('arguments',{}),ensure_ascii=False)}});tool_index+=1
                        done=item.get('done',False)
                        chunk={'id':'chatcmpl-'+ident,'object':'chat.completion.chunk','created':int(time.time()),'model':data['model'],'choices':[{'index':0,'delta':delta,'finish_reason':finish_reason(item,had_tools) if done else None}]}
                        if done:
                            record['runtime_num_ctx']=32768;record['max_output_tokens']=payload['options']['num_predict'];record['done_reason']=item.get('done_reason');record['prompt_eval_count']=item.get('prompt_eval_count');record['eval_count']=item.get('eval_count')
                            chunk['usage']={'prompt_tokens':item.get('prompt_eval_count',0),'completion_tokens':item.get('eval_count',0),'total_tokens':item.get('prompt_eval_count',0)+item.get('eval_count',0)}
                        self.wfile.write(('data: '+json.dumps(chunk)+'\n\n').encode());self.wfile.flush()
                    self.wfile.write(b'data: [DONE]\n\n');self.wfile.flush()
                    if not had_content and not had_tools:record['empty_response_count']=empty_response_count(fingerprint,True)
            record['status']='FORWARDED'
        except Exception as e:
            record['status']='ERROR';record['error']=str(e)
            try:self.send_error(502)
            except Exception:pass
        finally:(ROOT/(ident+'.json')).write_text(json.dumps(record,indent=2)+'\n')
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8091),Handler).serve_forever()
