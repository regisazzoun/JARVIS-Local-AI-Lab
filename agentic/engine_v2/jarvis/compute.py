"""Hybrid inference admission in the canonical mission SQLite database.

One node reservation per live request, priority between inference turns, no
migration of in-flight mutations, no canonical memory replica.
"""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sqlite3
import threading
import time
import urllib.request
import uuid


class ResourceUnavailable(RuntimeError):
    pass


class ComputeQueue:
    def __init__(self, database):
        self.path=Path(database);self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.db() as c:
            c.executescript('''CREATE TABLE IF NOT EXISTS compute_jobs(
              id TEXT PRIMARY KEY,mission TEXT,role TEXT,node TEXT,model TEXT,
              priority INTEGER,state TEXT,pid INTEGER,created REAL,started REAL,
              finished REAL,expires REAL,metrics TEXT,error TEXT);
              CREATE INDEX IF NOT EXISTS compute_pending ON compute_jobs(node,state,priority,created);''')

    @contextmanager
    def db(self):
        c=sqlite3.connect(self.path,timeout=30);c.row_factory=sqlite3.Row
        try:
            with c:yield c
        finally:c.close()

    def enter(self,node,model,role,mission=None,timeout=120):
        ident=uuid.uuid4().hex;priority=0 if role in ('conversation','critical') else 10;created=time.time()
        with self.db() as c:c.execute('INSERT INTO compute_jobs(id,mission,role,node,model,priority,state,pid,created) VALUES(?,?,?,?,?,?,?,?,?)',(ident,mission,role,node,model,priority,'queued',os.getpid(),created))
        deadline=time.monotonic()+timeout
        try:
            while True:
                with self.db() as c:
                    c.execute('BEGIN IMMEDIATE')
                    for row in c.execute("SELECT id,pid,expires FROM compute_jobs WHERE state='running' AND node=?",(node,)).fetchall():
                        try:os.kill(row['pid'],0);alive=True
                        except ProcessLookupError:alive=False
                        except PermissionError:alive=True
                        if not alive or (row['expires'] or 0)<time.time():
                            c.execute("UPDATE compute_jobs SET state='abandoned',finished=?,error=? WHERE id=?",(time.time(),'Lost inference lease; mutation checkpoints are unaffected',row['id']))
                    active=c.execute("SELECT 1 FROM compute_jobs WHERE node=? AND state='running'",(node,)).fetchone()
                    head=c.execute("SELECT id FROM compute_jobs WHERE node=? AND state='queued' ORDER BY priority,created,id LIMIT 1",(node,)).fetchone()
                    if not active and head and head['id']==ident:
                        c.execute("UPDATE compute_jobs SET state='running',started=?,expires=? WHERE id=?",(time.time(),time.time()+30,ident));return ident
                if time.monotonic()>=deadline:raise ResourceUnavailable('Inference queue timeout; retain checkpoint and retry: '+node)
                time.sleep(.05)
        except BaseException as exc:
            self.finish(ident,error=str(exc));raise

    def heartbeat(self,ident):
        with self.db() as c:c.execute("UPDATE compute_jobs SET expires=? WHERE id=? AND state='running'",(time.time()+30,ident))

    def finish(self,ident,metrics=None,error=None):
        with self.db() as c:c.execute('UPDATE compute_jobs SET state=?,finished=?,metrics=?,error=? WHERE id=?',('failed' if error else 'finished',time.time(),json.dumps(metrics or {}),error,ident))

    def recent(self,limit=20):
        with self.db() as c:return [dict(x) for x in c.execute('SELECT * FROM compute_jobs ORDER BY created DESC LIMIT ?',(limit,))]


def classify_request(text):
    lower=text.casefold()
    # Explicit costly analysis goes remote; ordinary language stays conversational.
    return 'critical' if any(term in lower for term in ('analyse approfondie','raisonnement complexe','compare en détail','démonstration mathématique','analyse complexe')) else 'conversation'


class HybridRouter:
    def __init__(self,config,database,fetch=None):
        self.config=config;self.nodes=config['nodes'];self.queue=ComputeQueue(database);self.fetch=fetch or self.http_json
        self.resource_cache={}

    def resources(self,name):
        node=self.nodes[name]
        if not node.get('resource_action'):return None
        cached=self.resource_cache.get(name)
        if cached and time.monotonic()-cached[0]<5:return cached[1]
        from .host_client import request
        if name=='Mac-mini':
            import subprocess
            r=subprocess.run(['python3',str(Path(__file__).resolve().parents[1]/'operations28a/resource_probe.py')],capture_output=True,text=True,timeout=8)
            if r.returncode:raise ResourceUnavailable('Local admission probe failed')
            value=json.loads(r.stdout)
        else:
            reply=request('host_remote',{'host':node['host_profile'],'action':node['resource_action']})
            value=json.loads(reply['result']['stdout'])
        self.resource_cache[name]=(time.monotonic(),value)
        return value

    @staticmethod
    def http_json(url,timeout=3):
        with urllib.request.urlopen(url,timeout=timeout) as r:return json.load(r)

    def discover(self):
        states=[]
        for name,node in self.nodes.items():
            row={'node':name,'enabled':bool(node.get('enabled')),'roles':node.get('roles',[])}
            if not node.get('enabled'):
                row.update(state='offline_pending',reason='Not installed/enrolled; no network request attempted');states.append(row);continue
            try:
                tags=self.fetch(node['url'].rstrip('/')+'/api/tags')
                row.update(state='ready',models=[{'name':m['name'],'size':m.get('size'),'digest':m.get('digest')} for m in tags.get('models',[])])
            except (OSError,ValueError,KeyError) as exc:row.update(state='unavailable',error_type=type(exc).__name__)
            states.append(row)
        return states

    def select(self,role,requested_model=None):
        candidates=self.config['routes'].get(role,self.config['routes']['conversation'])
        if role=='mission':
            with self.queue.db() as c:
                loads={row['node']:row['n'] for row in c.execute("SELECT node,count(*) n FROM compute_jobs WHERE state IN ('running','queued') GROUP BY node")}
            # A newly enrolled idle server can accept work without changing the
            # router. Disabled nodes are still skipped before any network call.
            candidates=sorted(candidates,key=lambda name:loads.get(name,0))
        failures=[]
        for name in candidates:
            node=self.nodes.get(name,{})
            if not node.get('enabled') or role not in node.get('roles',[]):continue
            model=node['conversation_model'] if name=='Mac-mini' else node['mission_model']
            if role=='mission' and name=='Mac-mini' and not self.config.get('allow_local_mission_fallback',False):continue
            if name=='Mac-mini':
                # A mission may not evict or silently replace the owner's conversation model.
                model=self.config['conversation_model']
                if role=='mission':
                    with self.queue.db() as c:
                        interactive=c.execute("SELECT 1 FROM compute_jobs WHERE role IN ('conversation','critical') AND state IN ('queued','running')").fetchone()
                    if interactive:failures.append({'node':name,'reason':'interactive_reserved'});continue
            try:
                tags=self.fetch(node['url'].rstrip('/')+'/api/tags')
                match=next((m for m in tags.get('models',[]) if m['name']==model),None)
                if not match:failures.append({'node':name,'reason':'model_not_installed','model':model});continue
                # The configured envelope is based on measured RAM/VRAM; runtime is
                # responsible for its exact KV/offload fit. Never count Dell2 capacity.
                if match.get('size',0)>node.get('max_model_bytes',2**63):
                    failures.append({'node':name,'reason':'model_outside_measured_envelope'});continue
                measured=self.resources(name)
                if measured:
                    available=measured['memory_available_bytes']
                    reserve=node.get('minimum_available_ram_bytes',0)
                    if available<reserve:
                        failures.append({'node':name,'reason':'RAM reserve threatened','available_bytes':available});continue
                    capacity=available-reserve+sum(max(0,g['free_mib']-2048)*2**20 for g in measured.get('gpu',[]))
                    resident=self.fetch(node['url'].rstrip('/')+'/api/ps')
                    loaded=any(m.get('name')==model for m in resident.get('models',[]))
                    if not loaded and match.get('size',0)>capacity:
                        failures.append({'node':name,'reason':'insufficient measured RAM/VRAM for weights'});continue
                return name,node,model,failures
            except (OSError,ValueError,KeyError) as exc:failures.append({'node':name,'reason':type(exc).__name__})
        raise ResourceUnavailable('No eligible inference node/model; no silent lighter substitution: '+json.dumps(failures))

    def infer(self,payload,role='conversation',mission=None):
        try:return self._infer(payload,role,mission)
        except (ResourceUnavailable,OSError,ValueError) as exc:
            if role!='critical':raise
            fallback_config={**self.config,'routes':{**self.config['routes'],'critical':['Mac-mini']}}
            fallback=HybridRouter(fallback_config,self.queue.path,self.fetch)
            message,metrics=fallback._infer(payload,role,mission)
            metrics['fallback_reason']=type(exc).__name__+': '+str(exc)
            fallback.queue.finish(metrics['compute_job'],metrics)
            return message,metrics

    def _infer(self,payload,role='conversation',mission=None):
        admission_start=time.monotonic()
        name,node,model,failures=self.select(role,payload.get('model'))
        selected_at=time.monotonic()
        timeout=self.config.get('interactive_queue_timeout',12) if role=='critical' else self.config.get('queue_timeout',120)
        ident=self.queue.enter(name,model,role,mission,timeout=timeout)
        stop=threading.Event()
        def heartbeat():
            while not stop.wait(5):self.queue.heartbeat(ident)
        thread=threading.Thread(target=heartbeat,daemon=True);thread.start();started=time.monotonic();first=None;metrics={}
        try:
            effective={**payload,'model':model,'stream':True,'keep_alive':-1 if name=='Mac-mini' else '15m'}
            if model.startswith(('llama','qwen3-coder-next')):effective.pop('think',None)
            effective['options']={**payload.get('options',{})}
            if role=='mission':effective['options']['num_predict']=self.config.get('mission_segment_tokens',4096)
            request=urllib.request.Request(node['url'].rstrip('/')+'/api/chat',data=json.dumps(effective).encode(),headers={'Content-Type':'application/json'})
            message={'role':'assistant','content':''};done=None
            with urllib.request.urlopen(request,timeout=self.config.get('inference_timeout',180)) as response:
                for raw in response:
                    item=json.loads(raw)
                    if item.get('error'):raise ResourceUnavailable(item['error'])
                    part=item.get('message',{})
                    if first is None and (part.get('content') or part.get('tool_calls')):first=time.monotonic()-started
                    message['content']+=part.get('content','')
                    if part.get('tool_calls'):message.setdefault('tool_calls',[]).extend(part['tool_calls'])
                    if item.get('done'):done=item
            if done is None:raise ResourceUnavailable('Inference stream ended without final receipt')
            metrics={key:done.get(key) for key in ('load_duration','prompt_eval_duration','eval_duration','eval_count','prompt_eval_count','total_duration','done_reason')}
            metrics.update(node=name,effective_model=model,requested_model=payload.get('model'),role=role,compute_job=ident,first_content_s=first,first_content_total_s=(started-admission_start+first) if first is not None else None,admission_s=selected_at-admission_start,queue_wait_s=started-selected_at,request_elapsed_s=time.monotonic()-started,end_to_end_s=time.monotonic()-admission_start,route_failures=failures,num_ctx=effective['options'].get('num_ctx'),admission_resources=self.resource_cache.get(name,(None,None))[1])
            self.queue.finish(ident,metrics);return message,metrics
        except BaseException as exc:
            self.queue.finish(ident,metrics,error=str(exc));raise
        finally:stop.set();thread.join(timeout=1)


def register(registry):
    if not registry.config.get('hybrid_compute'):return
    router=HybridRouter(registry.config['hybrid_compute'],registry.root/'runtime/missions.sqlite')
    registry.specs['compute_status']=('Observer les nœuds réellement disponibles, modèles installés et file partagée. Dell2 reste offline sans requête réseau tant qu’il n’est pas enrôlé.',{},[],'read_only',lambda a:{'nodes':router.discover(),'jobs':router.queue.recent(),'conversation_model':registry.config['hybrid_compute']['conversation_model']})
    def escalate(args):
        role='mission' if registry.config.get('compute_role')=='mission' else 'critical'
        message,metrics=router.infer({'model':registry.config['hybrid_compute']['conversation_model'],'messages':[{'role':'user','content':args['question']}],'options':{'num_ctx':8192,'num_predict':2048}},role=role,mission=registry.context.get('mission_id'))
        return {'answer':message.get('content',''),'inference':metrics,'scope':'Model analysis, not proof of any external operation. Tools/claims still require observations.'}
    registry.specs['compute_escalate']=('Confier une question difficile au modèle de mission du Dell et récupérer sa vraie analyse sans changer de conversation. Repli au même Qwen27 local si Dell indisponible ; aucune action système par ce seul appel.',{'question':{'type':'string','minLength':1,'maxLength':12000}},['question'],'read_only',escalate)
    def benchmark(args):
        import shlex
        allowed={'qwen3.5:27b-q4_K_M','qwen3:32b-q4_K_M','llama3.3:70b-instruct-q4_K_M','qwen3-coder-next:q4_K_M'}
        models=args['models']
        if not models or any(m not in allowed for m in models):raise ValueError('Unsupported benchmark candidate')
        name,node,model,_=router.select('mission')
        if name!='Dell1':raise ResourceUnavailable('This experimental benchmark is deployed only on Dell1')
        ident=router.queue.enter(name,'benchmark:'+','.join(models),'mission',registry.context.get('mission_id'))
        stop=threading.Event()
        def heartbeat():
            while not stop.wait(5):router.queue.heartbeat(ident)
        thread=threading.Thread(target=heartbeat,daemon=True);thread.start()
        token=None;store=getattr(registry,'mission_store',None);started=time.monotonic()
        try:
            params={'host':node['host_profile'],'action':'project_exec','project':'mission28a',
                'command':shlex.join(['python3','/opt/jarvis-lab/mission28a/quality_compare.py','--url',node['url'],
                                    '--models',*models,'--output','/opt/jarvis-lab/mission28a/quality-comparative.json'])}
            if store:token=store.begin_call(registry.context['mission_id'],registry.context.get('task_id'),'host_remote',params)
            result=registry.execute('host_remote',params)
            if token:store.finish_call(token,result,time.monotonic()-started)
            router.queue.finish(ident,{'models':models,'tool':'compute_benchmark'},error=None if result.get('ok') else str(result.get('error','Benchmark failed')))
            return {'returncode':0 if result.get('ok') else 1,'compute_job':ident,'node':name,
                    'models':models,'native_invocation':token,'observed_receipt':result,
                    'artifact':'/opt/jarvis-lab/mission28a/quality-comparative.json'}
        except BaseException as exc:
            router.queue.finish(ident,error=str(exc));raise
        finally:stop.set();thread.join(timeout=1)
    registry.specs['compute_benchmark']=('Exécuter le screening réel des candidats installés sur Dell1. Réserve sa file GPU canonique pendant le programme afin que les autres inférences ne perturbent pas les mesures ; les demandes critiques gardent le repli local. Appelle le project_exec existant avec programme/artefact fixes ; chaque cas est checkpointé et les reprises gardent les réponses déjà mesurées. models tableau de tags exacts. Ensuite project_download du fichier quality-comparative.json et vérification de son contenu. Les scores ne prouvent pas une autonomie générale.',{'models':{'type':'array','minItems':1,'maxItems':4,'items':{'type':'string','enum':['qwen3.5:27b-q4_K_M','qwen3:32b-q4_K_M','llama3.3:70b-instruct-q4_K_M','qwen3-coder-next:q4_K_M']}}},['models'],'host_authorized',benchmark)
