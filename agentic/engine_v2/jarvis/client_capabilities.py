"""Small client facade over the canonical Registry, memory audit and mission API.

No scheduler or second mission/memory database. Standalone tool calls are
observations/actions, not autonomous missions or independently verified results.
"""
import hashlib,http.cookiejar,json,secrets,time,urllib.request,urllib.error,uuid,re
from pathlib import Path
from .memory import Memory,now
from .tools import Registry
from .mission_store import MissionStore
from .authority_identity import invocation_scope

EXPOSED={'system_status','disk_usage','jarvis_services','software_versions','hardware_inventory','service_logs','read_configuration','web_search','web_fetch','active_memories','propose_memory','host_policy','host_exec','host_read_file','host_write_file','host_edit_file','host_delete_file','host_package','host_service','host_logs','host_diagnostics','host_resources','host_github','host_remote','host_ansible','host_project_service','capability_status','skill_list','skill_run','mcp_tools','compute_status','google_workspace','qwen_code_run','qwen_code_status'}

# Select existing received interfaces for NEW integrated-client missions. No
# owner goal, operational tasks, permissions or historical mission are rewritten.
CLIENT_MISSION_PROFILE={'planning_context_compact':True,'planning_report_steps':True,
    'structured_action_calls':True,'structured_action_two_stage':True,
    'bounded_narrative_review':True,'narrative_review_max_segments':4,
    'atomic_report_review':True,'bounded_interface_errors':True,'factual_finalization':True}
CLIENT_SERVICE_REPORT_PROFILE={'read_only_service_snapshot':True,
    'report_rewrite_from_facts':True,'proof_bound_report_write':True,
    'proof_bound_explanation_mode':'facts_only'}

def fingerprint(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

class CanonicalAPI:
    def __init__(self,root):
        self.root=Path(root);self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def request(self,path,data=None):
        raw=json.dumps(data).encode() if data is not None else None
        def call():return self.opener.open(urllib.request.Request('http://127.0.0.1:8765'+path,data=raw,headers={'Content-Type':'application/json','X-Jarvis-Request':'1'}),timeout=180)
        try:return json.loads(call().read())
        except urllib.error.HTTPError as exc:
            if exc.code!=401:raise
            token=secrets.token_urlsafe(32)
            with Memory(self.root/'runtime/memory.sqlite').connect() as c:
                c.execute('DELETE FROM auth_sessions WHERE expires<=?',(time.time(),))
                c.execute('INSERT INTO auth_sessions(digest,expires) VALUES(?,?)',(hashlib.sha256(token.encode()).hexdigest(),time.time()+28800))
            self.opener.addheaders=[('Cookie','jarvis_session='+token)]
            return json.loads(call().read())

class Capabilities:
    def __init__(self,root='/opt/jarvis/conversation',origin='OpenWebUI',mission=None,task=None,config=None):
        self.root=Path(root);self.origin=origin;self.mission=mission or None;self.task=task or None
        self.config=config or json.loads((self.root/'config/13e.json').read_text());self.memory=Memory(self.root/'runtime/memory.sqlite');self.store=MissionStore(self.root)
    def registry(self):
        reg=Registry(self.memory,self.root,self.config)
        reg.context={'host_target':True,'client_origin':self.origin,'mission_id':self.mission,'task_id':self.task}
        if self.mission:
            self.store.get(self.mission);reg.mission_store=self.store
        return reg
    def catalog(self,query='',offset=0):
        reg=self.registry();rows=[]
        for schema in reg.schemas(True):
            f=schema['function']
            if f['name']=='qwen_code_run' and self.origin.startswith('QwenCode'):continue
            if f['name'] in EXPOSED and str(query).casefold() in (f['name']+' '+f['description']).casefold():rows.append({'name':f['name'],'description':f['description'][:78]})
        offset=max(0,int(offset));page=rows[offset:offset+12]
        return {'source':'canonical active JARVIS Registry','origin':self.origin,'tools':page,'matching_count':len(rows),'next_offset':offset+12 if offset+12<len(rows) else None,'schema_lookup':'jarvis_schema(name), then jarvis_call(name, arguments JSON). Search catalog query or page offset.','mission_tools':'jarvis_missions: list/read/create; creates canonical missions only on explicit owner request','limitations':'Configured does not mean executed. Direct tool receipt is not autonomous mission reception. Google availability must be checked.'}
    def schema(self,name):
        if name not in EXPOSED:raise ValueError('Tool is outside the exposed client catalog')
        reg=self.registry()
        if name not in reg.specs:raise ValueError('Tool not installed in active Registry')
        return {'name':name,'schema':reg.active_schema(name),'description':reg.specs[name][0]}
    def _audit(self,operation,value):
        with self.memory.connect() as c:return c.execute('INSERT INTO audit(operation,target,created) VALUES(?,?,?)',(operation,json.dumps(value,ensure_ascii=False),now())).lastrowid
    def receipt(self,ident,offset=0,limit=600):
        with self.memory.connect() as c:row=c.execute("SELECT id,target,created FROM audit WHERE id=? AND operation='client_tool_result'",(int(ident),)).fetchone()
        if not row:raise ValueError('No such client tool receipt')
        data=json.loads(row['target']);raw=row['target'].encode();offset=max(0,int(offset));limit=max(100,min(3000,int(limit)))
        if len(raw)<=limit and offset==0:return {'audit_id':row['id'],'created':row['created'],**data}
        return {'audit_id':row['id'],'explicit_excerpt':raw[offset:offset+limit].decode('utf-8','replace'),'offset_bytes':offset,'next_offset_bytes':offset+limit if offset+limit<len(raw) else None,'total_bytes':len(raw),'full_sha256':hashlib.sha256(raw).hexdigest(),'meaning':'Byte-window of original canonical receipt, not a complete JSON object. The original remains intact.'}
    def _model_result(self,result,receipt):
        raw=json.dumps(result,ensure_ascii=False).encode()
        if len(raw)<=6500:return {**result,'client_receipt':receipt}
        return {'ok':result.get('ok'),'tool':result.get('tool'),'result':{**{k:v for k,v in (result.get('result') or {}).items() if k in ('returncode','status','evidence_id')},'explicit_excerpt':raw[:3500].decode('utf-8','replace'),'full_sha256':hashlib.sha256(raw).hexdigest(),'full_result_bytes':len(raw),'full_receipt_audit_id':receipt['audit_id'],'meaning':'Original complete result archived, not inferred absent; page jarvis_receipt or request a targeted observation.'},'client_receipt':receipt}
    def call(self,name,arguments,request_id=None):
        if not isinstance(arguments,dict):raise ValueError('arguments must be a JSON object')
        self.schema(name);reg=self.registry();ident=request_id or uuid.uuid4().hex
        signature=fingerprint({'tool':name,'arguments':arguments,'origin':self.origin,'mission':self.mission,'task':self.task})
        if self.mission and self.store.get(self.mission)['state']!='running':
            raise ValueError('Parent mission is not running; no delegated operation dispatched')
        with self.memory.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            # Scope JSON extraction: old audit targets are ordinary strings.
            prior=c.execute("SELECT id,target FROM audit WHERE operation='client_tool_result' AND json_extract(CASE WHEN json_valid(target) THEN target ELSE '{}' END,'$.request_id')=? ORDER BY id DESC LIMIT 1",(ident,)).fetchone()
            if prior:
                previous=json.loads(prior['target'])
                if previous['signature']!=signature:raise ValueError('request_id already binds a different invocation')
                return self._model_result(previous['result'],{'audit_id':prior['id'],'request_id':ident,'cached':True,'call_completed':previous['call_completed'],'application_result_independently_verified':False})
            pending=c.execute("SELECT id,target FROM audit WHERE operation='client_tool_started' AND json_extract(CASE WHEN json_valid(target) THEN target ELSE '{}' END,'$.request_id')=? ORDER BY id DESC LIMIT 1",(ident,)).fetchone()
            if pending:
                if json.loads(pending['target'])['signature']!=signature:raise ValueError('request_id already binds a different pending invocation')
                return {'ok':False,'error':'Existing dispatch has no final receipt: observe real effects before any retry','client_receipt':{'request_id':ident,'start_audit_id':pending['id'],'state':'UNKNOWN','call_completed':False}}
            payload={'request_id':ident,'origin':self.origin,'signature':signature,'tool':name,'mission':self.mission,'task':self.task}
            start=c.execute('INSERT INTO audit(operation,target,created) VALUES(?,?,?)',('client_tool_started',json.dumps(payload,ensure_ascii=False),now())).lastrowid
        token=self.store.begin_call(self.mission,self.task,name,arguments) if self.mission else None;began=time.monotonic()
        with invocation_scope(token):result=reg.execute(name,arguments)
        if token:self.store.finish_call(token,result,time.monotonic()-began)
        # Keep a completed negative systemd read distinct from a transport refusal.
        from .operational_policy import service_read_completed
        call_completed=bool(result.get('ok') or name=='host_service' and service_read_completed(result))
        audit=self._audit('client_tool_result',{'request_id':ident,'start_audit_id':start,'origin':self.origin,'signature':signature,'tool':name,'arguments':arguments,'mission':self.mission,'task':self.task,'result':result,'call_completed':call_completed,'application_result_independently_verified':False})
        return self._model_result(result,{'audit_id':audit,'request_id':ident,'mission_id':self.mission,'invocation_id':token,'origin':self.origin,'call_completed':call_completed,'application_result_independently_verified':False})
    def missions(self,action='list',ident=None,goal=None,after=0,profile='standard'):
        if action=='create':
            if not isinstance(goal,str) or not 1<=len(goal)<=3000:raise ValueError('Explicit owner goal of1..3000characters required')
            if profile not in ('standard','service_observation'):raise ValueError('Unknown existing mission profile')
            spec=dict(CLIENT_MISSION_PROFILE)
            if profile=='service_observation':spec.update(CLIENT_SERVICE_REPORT_PROFILE)
            value=CanonicalAPI(self.root).request('/api/missions',{'goal':goal,'model':'qwen3-coder-next:q4_K_M','project':'IntegratedClients','request_kind':'mission','spec':spec})
            if not re.fullmatch('[0-9a-f]{32}',str(value.get('id',''))):
                return {'created':None,'state':'UNKNOWN','error':'No valid canonical mission receipt; inspect existing missions before resubmitting'}
            return {'created':True,'source':'canonical existing Mission Engine',**value}
        if action=='list':
            with self.store.db() as c:return {'created':False,'missions':[dict(r) for r in c.execute('SELECT id,goal,state,updated FROM missions ORDER BY updated DESC LIMIT 20')]}
        if action!='read' or not ident:raise ValueError('Use list, read with id, or create with goal')
        row=self.store.get(ident);events=self.store.events(ident,after=int(after),limit=6)
        # Return operational details, not full old conversations or giant payloads.
        def bounded(value):
            text=json.dumps(value,ensure_ascii=False)
            return value if len(text)<=1000 else {'explicit_excerpt':text[:600],'full_sha256':hashlib.sha256(text.encode()).hexdigest(),'full_event_available_in_canonical_store':True}
        return {'created':False,'id':ident,'goal':row['goal'],'state':row['state'],'tasks':[{k:t.get(k) for k in ('id','title','state','artifact','report_sha256')} for t in self.store.tasks(ident)],'events':[{k:e.get(k) for k in ('id','kind','actor','tool','created')}|{'arguments':bounded(e.get('arguments')),'result':bounded(e.get('result'))} for e in events],'next_after':events[-1]['id'] if events else int(after)}
