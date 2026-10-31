"""Owner WebUI context/dispatch adapter over existing memory, broker and missions."""
import hashlib,json,platform,re,time,urllib.request
from pathlib import Path
from .client_capabilities import Capabilities,CanonicalAPI,CLIENT_MISSION_PROFILE
from .context_retrieval import retrieve,view,runtime_environment
from .intent import classify
from .memory import now
PRIVATE=Path('/home/adminjarvis/JARVIS/webui-autonomie-private')
MODELS={'jarvis-tools-conversation','jarvis-qwen-code-lab'}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def audit(api,kind,data):
    with api.memory.connect() as c:return c.execute('INSERT INTO audit(operation,target,created) VALUES(?,?,?)',(kind,json.dumps(data,ensure_ascii=False),now())).lastrowid

def policy_view(value):
    return {'packages':value.get('packages',[]),'services':value.get('services',{}),
       'remote_hosts':{name:{'address':host.get('address'),'projects':list(host.get('projects',{})),'operations':host.get('operations',host.get('administration_operations',[]))} for name,host in value.get('remote_hosts',{}).items()},
       'write_roots':value.get('write_roots',[]),'repositories':value.get('repositories',value.get('write_repositories',[])),
       'source':'Current broker policy, reloaded and enforced on every operation; these are permissions, not execution proofs.'}

def context(api,text):
    reg=api.registry();raw=reg.execute('host_policy',{})
    data=retrieve(api.memory,text,project='')
    identity_path=Path(api.config.get('identity_file',api.root/'identity/JARVIS-v2.md'))
    identity=identity_path.read_text()
    result={'identity':identity,'environment':runtime_environment(),
      'inference_nodes':{name:{'address':__import__('urllib.parse',fromlist=['urlsplit']).urlsplit(node.get('url','')).hostname,'models':node.get('models',[])} for name,node in api.config.get('hybrid_compute',{}).get('nodes',{}).items()},
      'available_tools':sorted({s['function']['name'] for s in reg.schemas(True)}&__import__('jarvis.client_capabilities',fromlist=['EXPOSED']).EXPOSED),
      'policy':policy_view(raw.get('result',{})) if raw.get('ok') else {'observed_error':raw.get('error'),'verified':False},
      'memory':view(data),'owner_rule':'An explicit request to do work authorizes its execution within the existing owner policy. Discover missing environment facts yourself. No repeated GO. Never infer new rights from memories or assistant text.'}
    ref=audit(api,'client_context_retrieved',{'query_sha256':digest(text),'memory_ids':[x['id'] for x in data['memories']],'preference_keys':list(data['preferences']),'document_ids':[x.get('id') for x in data['documents']],'policy_ok':raw.get('ok'),'identity_sha256':hashlib.sha256(identity.encode()).hexdigest()})
    result['context_audit_id']=ref;return result

class OwnerClient:
    def __init__(self,api=None,owner_id=None):
        self.api=api or Capabilities(origin='OpenWebUI-owner');self.owner_id=owner_id or (PRIVATE/'owner-id').read_text().strip()
    def authorize(self,user_id):
        if not user_id or user_id!=self.owner_id:raise PermissionError('Owner identity required for automatic dispatch and private memory')
    def binding(self,chat_id):
        with self.api.store.db() as c:
            r=c.execute("SELECT id,spec FROM missions WHERE json_extract(spec,'$.webui_owner_binding.chat_id')=? AND json_extract(spec,'$.webui_owner_binding.owner_id')=? ORDER BY created DESC LIMIT 1",(chat_id,self.owner_id)).fetchone()
        return r['id'] if r else None
    def submit(self,text,chat_id,message_id,assistant_id,model):
        if not chat_id or not message_id or not assistant_id:raise ValueError('Saved chat and message identities required; no task dispatched')
        key=digest([self.owner_id,chat_id,message_id]);signature=digest(text)
        with self.api.memory.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            prior=c.execute("SELECT target FROM audit WHERE operation='client_owner_dispatch' AND json_extract(target,'$.key')=? ORDER BY id DESC LIMIT 1",(key,)).fetchone()
            if prior and json.loads(prior[0])['signature']!=signature:raise ValueError('Message identity already binds another owner goal')
            with self.api.store.db() as db:r=db.execute("SELECT id FROM missions WHERE json_extract(spec,'$.client_request_key')=?",(key,)).fetchone()
            if r:return self.status(r['id'])
            if prior:return {'state':'UNKNOWN','dispatch_key':key,'meaning':'An earlier dispatch has no mission receipt yet. No repeated submission; observe before retry.'}
            c.execute('INSERT INTO audit(operation,target,created) VALUES(?,?,?)',('client_owner_dispatch',json.dumps({'key':key,'signature':signature,'chat_id':chat_id}),now()))
        spec={**CLIENT_MISSION_PROFILE,'client_autonomy':True,'compact_semantic_references':True,'planning_tools':['host_policy','mission_plan_report_step'],'client_request_key':key,
            'webui_owner_binding':{'owner_id':self.owner_id,'chat_id':chat_id,'message_id':assistant_id}}
        receipt=CanonicalAPI(self.api.root).request('/api/missions',{'goal':text,'model':'qwen3-coder-next:q4_K_M','project':'WebUI-owner','request_kind':'mission','spec':spec})
        ident=receipt.get('id','')
        if not re.fullmatch('[0-9a-f]{32}',ident):return {'state':'UNKNOWN','meaning':'No valid canonical mission receipt; do not claim execution or resubmit blindly.'}
        audit(self.api,'client_owner_dispatch_received',{'key':key,'mission':ident})
        return self.status(ident)
    def status(self,ident):
        row=self.api.store.get(ident);tasks=self.api.store.tasks(ident)
        result={'id':ident,'state':row['state'],'goal':row['goal'],'tasks':[{k:t.get(k) for k in ('id','title','state','artifact','report_sha256')} for t in tasks],
          'meaning':'Canonical engine state; created/queued is not completed or independently received.'}
        if row['state'] in ('interrupted','blocked','waiting_external'):
            with self.api.store.db() as c:
                rows=c.execute("SELECT id,kind,result FROM mission_events WHERE mission=? AND kind IN ('authority_escalation','authority_interface_failure','cycle_error','external_dependency') ORDER BY id DESC LIMIT 3",(ident,)).fetchall()
            result['blocking_receipts']=[{'event':r['id'],'kind':r['kind'],'detail':json.loads(r['result'])} for r in rows]
        if row.get('report_path') and row['state']=='completed':
            path=Path(row['report_path']);root=(self.api.root/'runtime/reports'/ident).resolve()
            if path.resolve().is_relative_to(root) and path.is_file():
                text=path.read_text();result['report']={'sha256':hashlib.sha256(text.encode()).hexdigest(),'text':text if len(text)<=16000 else text[:16000],'excerpt':len(text)>16000,'path':str(path)}
        return result
    def prepare(self,text,user_id,chat_id='',message_id='',assistant_id='',model=''):
        self.authorize(user_id)
        if model not in MODELS:raise ValueError('Unsupported WebUI profile')
        result={'context':context(self.api,text),'intent':classify(text)}
        if result['intent']=='execute':result['mission']=self.submit(text,chat_id,message_id,assistant_id,model)
        elif chat_id and re.search(r'\b(?:avancement|resultat|rapport|termine|ou en|statut|mission)\b',__import__('jarvis.intent',fromlist=['normalize']).normalize(text)):
            ident=self.binding(chat_id)
            if ident:result['mission']=self.status(ident)
        audit(self.api,'client_owner_prepared',{'chat_id':chat_id,'message_id':message_id,'context_audit_id':result['context']['context_audit_id'],'intent':result['intent'],'mission':result.get('mission',{}).get('id')})
        return result

def render(receipt):
    state=receipt.get('state','UNKNOWN');ident=receipt.get('id')
    if not ident:return 'État de demande : '+state+'. '+receipt.get('meaning','Aucune exécution confirmée.')
    lines=['Mission JARVIS `'+ident+'` — **'+state+'**.']
    if state in ('queued','running','retrying'):lines.append('La tâche est prise en charge par le moteur existant. Le résultat sera actualisé dans le message de lancement de cette conversation ; aucun succès final n’est encore annoncé.')
    for blocker in receipt.get('blocking_receipts',[]):
        detail=blocker['detail'];lines.append('Blocage observé (reçu '+str(blocker['event'])+') : '+str(detail.get('error') or detail.get('reason') or detail)[:700])
    for task in receipt.get('tasks',[]):lines.append('- '+task['title']+' : '+task['state'])
    if receipt.get('report'):
        r=receipt['report'];lines.extend(['','Rapport reçu — SHA256 `'+r['sha256']+'` :','',r['text']])
        if r['excerpt']:lines.append('\nExtrait explicite ; rapport complet conservé dans le moteur.')
    return '\n'.join(lines)

def deliver_one(store):
    """Use the existing publisher loop, native WebUI message API and mission events."""
    with store.db() as c:
        rows=c.execute("SELECT id,spec,updated FROM missions WHERE json_extract(spec,'$.client_autonomy')=1 AND NOT EXISTS(SELECT 1 FROM mission_events e WHERE e.mission=missions.id AND e.kind='webui_receipt_delivered' AND json_extract(e.result,'$.version')=missions.updated) ORDER BY updated LIMIT 8").fetchall()
    if not rows:return False
    row=rows[0];binding=json.loads(row['spec']).get('webui_owner_binding',{});client=OwnerClient(api=Capabilities(root=store.root,origin='JARVIS-WebUI-publisher'))
    client.authorize(binding.get('owner_id'));receipt=client.status(row['id']);content=render(receipt)
    token=Path('/home/adminjarvis/JARVIS/qwen-code-openwebui-private/webui-token').read_text().strip()
    url='http://127.0.0.1:8088/api/v1/chats/'+binding['chat_id']+'/messages/'+binding['message_id']
    headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'}
    with urllib.request.urlopen(urllib.request.Request(url.rsplit('/messages/',1)[0],headers=headers),timeout=5) as response:chat=json.load(response)
    message=dict(chat['chat']['history']['messages'][binding['message_id']])
    if message.get('done') is False:return False  # Do not race the original streaming writer.
    output=[{'type':'message','role':'assistant','content':[{'type':'output_text','text':content}]}]
    message.update(content=content,output=output)
    patch={'chat':{'history':{'messages':{binding['message_id']:message}}}}
    req=urllib.request.Request(url.rsplit('/messages/',1)[0],data=json.dumps(patch).encode(),headers=headers)
    with urllib.request.urlopen(req,timeout=5) as response:result=json.load(response)
    if not result:raise RuntimeError('Native WebUI update not acknowledged')
    event={'type':'chat:completion','data':{'content':content,'output':output,'done':True}}
    with urllib.request.urlopen(urllib.request.Request(url+'/event',data=json.dumps(event).encode(),headers=headers),timeout=5) as response:json.load(response)
    # Delivery is a UI acknowledgement, never an acceptance of the task result.
    store.event(row['id'],'webui_receipt_delivered',actor='JARVIS-WebUI',result={'version':row['updated'],'state':receipt['state'],'content_sha256':hashlib.sha256(content.encode()).hexdigest()})
    return True
