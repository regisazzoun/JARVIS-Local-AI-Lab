"""P3: bounded active (blue) context, canonical operational (green) journal.

No second conversation memory. Full archived prompts and original receipts remain
in MissionStore; a checkpoint is structured evidence, not a model-only summary.
"""
import copy,hashlib,json,time,urllib.request,os,socket
from .mission_store import encoded

class ContextCapacityError(ValueError):pass

def sha(value):return hashlib.sha256(encoded(value).encode()).hexdigest()
def serialized_bytes(value):return len(encoded(value).encode())
def result_objective(config):
 """Owner resource criterion written before planning/delegation; no network IO."""
 hybrid=config.get('hybrid_compute',{});nodes=hybrid.get('nodes',{})
 node=next((nodes[n] for n in hybrid.get('routes',{}).get('mission',[]) if nodes.get(n,{}).get('enabled')), {})
 ceiling=node.get('hard_context_limit')
 if not ceiling:return None
 reply=hybrid.get('mission_segment_tokens',4096);margin=node.get('context_template_margin',1024)
 return {'total_context_tokens_max':ceiling,'response_tokens_reserved':reply,'template_tokens_reserved':margin,
         'input_tokens_max':ceiling-reply-margin,
         'result_required':'Chaque sous-tâche doit tenir dans cette fenêtre avant transmission. Sinon découper, archiver et référencer ; ne pas tronquer les exigences.',
         'admission_measure':'UTF-8 serialized bytes used as conservative token upper estimate, NOT exact tokenizer count'}
def preview(value,limit=700):
 text=value if isinstance(value,str) else encoded(value)
 return value if len(text)<=limit else {'excerpt':text[:limit],'original_chars':len(text),'sha256':sha(value),'full_source':'canonical event/tool receipt; use context_recall'}

def capacity(config,model):
 hybrid=config.get('hybrid_compute',{});nodes=hybrid.get('nodes',{})
 name=next((n for n in hybrid.get('routes',{}).get('mission',[]) if nodes.get(n,{}).get('enabled')),None)
 node=nodes.get(name,{})
 configured=int(node.get('inference_num_ctx') or config.get('durable_num_ctx') or config.get('num_ctx') or 0)
 if configured<=0:raise ContextCapacityError('No configured mission context capacity; discover actual backend before inference')
 observed=None;error=None
 if node.get('url'):
  try:
   with urllib.request.urlopen(node['url'].rstrip('/')+'/api/ps',timeout=3) as response:data=json.load(response)
   match=next((m for m in data.get('models',[]) if m.get('name')==node.get('mission_model',model)),None)
   if match and type(match.get('context_length')) is int:observed=match['context_length']
  except (OSError,ValueError,KeyError) as exc:error=type(exc).__name__
 hard=node.get('hard_context_limit',configured)
 return {'limit':min(configured,observed or configured,hard),'configured_limit':configured,'hard_context_limit':hard,'observed_loaded_limit':observed,'source':'configured limit and actual api/ps' if observed else 'configured fallback pending loaded observation','observation_error':error,'node':name,'model':node.get('mission_model',model),'observed_at':time.time()}

def observation_view(o):
 wrapper=o.get('result') or {};value=wrapper.get('result') or {};execution=value.get('execution') or {}
 return {'reference':o.get('event_reference'),'invocation_id':o['id'],'tool':o['tool'],'ok':wrapper.get('ok'),'error':preview(wrapper.get('error'),250),'parameters':{k:v for k,v in o['arguments'].items() if k in ('path','host','action','issue','kind','operation_id')},'parameters_sha256':sha(o['arguments']),'result':{k:value[k] for k in ('reference','source_reference','version','state','status','returncode','verification_event','failed_cycles','test_executed','new_process','same_task','counters_preserved','counters_unchanged','interface_counters_unchanged','authority_counters_unchanged','previous_reference','excerpt_is_not_complete_source','next_offset','total_chars') if k in value}|({'content':preview(value['content'],900)} if 'content' in value else {})|({'execution_returncode':execution.get('returncode'),'stdout':preview(execution.get('stdout'),600),'stderr':preview(execution.get('stderr'),350)} if execution else {})}

class ContextBudget:
 def __init__(self,store,mission,task=None):self.store=store;self.m=mission;self.task=task
 def latest(self,kind,limit=1):
  scoped=bool(self.task and kind in ('working_note','authority_model_decision'))
  boundary=json.loads(self.store.get(self.m)['spec']).get('authority_evidence_after_event',0) if scoped else 0
  with self.store.db() as c:rows=c.execute('SELECT id,actor,created,result FROM mission_events WHERE mission=? AND kind=?'+(' AND task=? AND id>?' if scoped else '')+' ORDER BY id DESC LIMIT ?',((self.m,kind,self.task,boundary,limit) if scoped else (self.m,kind,limit))).fetchall()
  return [{**dict(r),'result':json.loads(r['result'] or '{}')} for r in rows]
 def checkpoint(self,reason,automatic=False):
  mission=self.store.get(self.m);spec=json.loads(mission['spec']);task=next((t for t in self.store.tasks(self.m) if t['id']==self.task),None)
  with self.store.db() as c:
   plan=c.execute('SELECT version,sha256 FROM mission_plans WHERE mission=? ORDER BY version DESC LIMIT 1',(self.m,)).fetchone()
  self.store.attempt_ledger(self.m)
  with self.store.db() as c:
   counters=[dict(r) for r in c.execute('SELECT scope,fingerprint,failed_cycles,infra_incidents,state,escalation_event FROM mission_problems_v2 WHERE mission=? ORDER BY scope',(self.m,))]
   pending=[dict(r) for r in c.execute("SELECT id,problem,executor,phase,state,unknown_outcome FROM mission_attempts_v2 WHERE mission=? AND state IN ('PENDING','DISPATCHED','RUNNING','VALIDATION_INCONCLUSIVE') ORDER BY created,id",(self.m,))]
   rows=c.execute("SELECT t.id,t.tool,t.arguments,t.result,(SELECT max(e.id) FROM mission_events e WHERE e.mission=t.mission AND e.invocation=t.id AND e.kind='tool_finished') event_reference FROM tool_calls t WHERE t.mission=? AND (? IS NULL OR t.task=?) ORDER BY t.created DESC,t.rowid DESC LIMIT 3",(self.m,self.task,self.task)).fetchall()
  observations=[{**dict(o),'arguments':json.loads(o['arguments']),'result':json.loads(o['result'] or '{}')} for o in reversed(rows)]
  authority=self.latest('authority_state');executions=list(authority[0]['result'].get('executions',{}).items()) if authority else []
  if spec.get('authority_task_scoped_evidence'):
   with self.store.db() as c:refs={str(r[0]) for r in c.execute("SELECT id FROM mission_events WHERE mission=? AND task=? AND kind='authority_execution' AND id>?",(self.m,self.task,spec.get('authority_evidence_after_event',0)))}
   executions=[(ref,e) for ref,e in executions if ref in refs]
  modifications=[{'reference':ref,'executor':e['host'],'kind':e['kind'],'source_version':sha(e.get('after',{})),'changed_files':[p for p in set(e.get('before',{}))|set(e.get('after',{})) if e.get('before',{}).get(p)!=e.get('after',{}).get(p)]} for ref,e in executions if e.get('kind')=='correct'][-8:]
  tests=[{'reference':int(ref),'executor':e['host'],'returncode':e['execution']['returncode'],'source_version':sha(e.get('after',{}))} for ref,e in executions if e.get('kind')=='test'][-8:]
  # Keep substantive evidence independently of the last failed reader calls.
  # Process exit zero remains a process fact, never a semantic verdict.
  observed_evidence=[{'reference':int(ref),'executor':e['host'],'kind':e['kind'],'observed_process_returncode':e['execution']['returncode'],'stdout':preview(e['execution'].get('stdout',''),1200),'stderr':preview(e['execution'].get('stderr',''),300),'source_version':sha(e.get('after',{})),'adequacy':'not inferred from process return code'} for ref,e in executions if e.get('kind') in ('test','inspect')][-2:]
  reserved_operation_ids=sorted(authority[0]['result'].get('operations',{})) if authority else []
  authority_counters={issue:{k:v.get(k,0) for k in ('failed_cycles','delegation_failures','correction_resolved_through','delegation_resolved_through','correction_resolution_event')} for issue,v in (authority[0]['result'].get('issues',{}) if authority else {}).items()}
  with self.store.db() as c:
   interfaces=[dict(r) for r in c.execute("SELECT json_extract(result,'$.epoch') epoch,json_extract(result,'$.category') category,max(json_extract(result,'$.count')) count FROM mission_events WHERE mission=? AND kind='authority_interface_failure' GROUP BY epoch,category ORDER BY epoch,category",(self.m,))]
  route=self.latest('compute_route_observed');last_inference={k:route[0]['result'].get(k) for k in ('node','effective_model','num_ctx','prompt_eval_count')} if route else None
  checkpoint={'version':1,'automatic':automatic,'coordinator_host':socket.gethostname(),'process_id':os.getpid(),'mission':self.m,'parent_mission':spec.get('parent_mission'),'priority':spec.get('owner_priority'),'task':self.task,'objective':(task.get('objective') or task.get('title')) if task else mission['goal'],'owner_goal':mission['goal'],'mission_state':mission['state'],'task_state':task.get('state') if task else None,'task_contract':task.get('contract',{}) if task else {},'task_dependencies':task.get('deps',[]) if task else [],'plan':dict(plan) if plan else None,'workspace':spec.get('authority_workspace'),'model':mission['model'],'counters':counters,'authority_counters':authority_counters,'reserved_operation_ids':reserved_operation_ids,'interface_counters':interfaces,'last_inference':last_inference,'pending_effects':pending,'decisions':self.latest('authority_model_decision',2),'model_notes':self.latest('working_note',3),'verified_api_observations':self.latest('coordinator_verified_api',2),'coordinator_instructions':self.latest('coordinator_instruction',1),'modifications':modifications,'tests':tests,'observed_evidence':observed_evidence,'last_observations':[observation_view(o) for o in observations],'next_authorized_action':'Continue current owner task with offered tools; observe unknown effects before any replay','reason':reason}
  e=self.store.event(self.m,'operational_checkpoint',self.task,'JARVIS-engine',result={'sha256':sha(checkpoint),'checkpoint':checkpoint})
  return e,checkpoint
 def recall(self,reference,offset=0,limit=1800):
  if offset<0 or not 1<=limit<=4000:raise ValueError('offset >=0; limit1..4000')
  parent=json.loads(self.store.get(self.m)['spec']).get('parent_mission')
  with self.store.db() as c:r=c.execute('SELECT mission,kind,actor,result FROM mission_events WHERE id=?',(reference,)).fetchone()
  linked=False
  if r and parent:
   target=self.store.get(r['mission']);linked=target.get('project')==self.store.get(self.m).get('project') and json.loads(target['spec']).get('parent_mission')==parent
  if not r or r['mission'] not in (self.m,parent) and not linked:raise ValueError('Reference not in current mission or explicitly linked parent')
  raw=r['result'];return {'reference':reference,'kind':r['kind'],'actor':r['actor'],'sha256':hashlib.sha256(raw.encode()).hexdigest(),'content':raw[offset:offset+limit],'offset':offset,'next_offset':offset+limit if offset+limit<len(raw) else None,'total_chars':len(raw),'excerpt_is_not_complete_source':offset>0 or len(raw)>limit}
 def archive(self,payload,reason):
  return self.store.event(self.m,'context_archive',self.task,'JARVIS-engine',result={'sha256':sha(payload),'payload':payload,'reason':reason,'not_conversation_memory':True})
 def prepare(self,payload,observed,response_default=4096):
  # UTF-8 serialized bytes are deliberately conservative, explicitly labelled.
  # An actual model tokenizer can replace this estimate; never call it measured
  # tokens. Include schemas/format and a separate template/control-token margin.
  limit=observed['limit'];reply=payload.get('options',{}).get('num_predict',response_default)
  if type(reply) is not int or reply<=0:reply=response_default
  margin=1024;budget=limit-reply-margin
  measurement={'capacity':observed,'response_reserved':reply,'template_margin':margin,'input_budget_estimate':budget,'estimator':'conservative UTF-8 serialized bytes, NOT measured tokens','original_bytes':serialized_bytes(payload),'compacted':False}
  if budget<=0:
   archive=self.archive(copy.deepcopy(payload),'response reservation exhausts effective capacity');checkpoint_id,_=self.checkpoint('response reservation capacity block',automatic=True)
   self.store.event(self.m,'context_capacity_blocked',self.task,'JARVIS-engine',result={**measurement,'archive':archive,'checkpoint':checkpoint_id,'reason':'Response reservation exhausts effective capacity'})
   raise ContextCapacityError('Response reservation exhausts observed context capacity; checkpoint retained')
  if serialized_bytes(payload)<=budget:
   self.store.event(self.m,'context_budget_checked',self.task,'JARVIS-engine',result={**measurement,'sent_bytes':serialized_bytes(payload),'within_budget':True});return payload
  archive=self.archive(copy.deepcopy(payload),'active input approaches effective context capacity')
  checkpoint_id,checkpoint=self.checkpoint('automatic pre-inference checkpoint',automatic=True)
  if payload.get('format'):
   self.store.event(self.m,'context_capacity_blocked',self.task,'JARVIS-engine',result={**measurement,'archive':archive,'checkpoint':checkpoint_id,'reason':'Structured review evidence cannot be silently discarded; reduce report/claim scope or fetch targeted evidence'})
   raise ContextCapacityError('Structured review exceeds conservative input budget; original evidence archived, no inference dispatched')
  original=payload['messages'];system=copy.deepcopy(next((x for x in original if x.get('role')=='system'),{'role':'system','content':'Authorized mission; original owner constraints remain canonical.'}))
  system['content']+='\nLe checkpoint ci-dessous contient déjà l’état utile. Les références archive/checkpoint automatiques prouvent le stockage ; ne les recharge pas récursivement. Applique la dernière instruction coordinateur, puis décide une action dans la tâche. context_recall sert à un ancien incident précis, context_resume à une reprise manuelle.'
  active={k:checkpoint[k] for k in ('mission','parent_mission','priority','task','objective','task_contract','task_dependencies','plan','workspace','model','authority_counters','reserved_operation_ids','interface_counters','last_inference','pending_effects','modifications','tests','observed_evidence','next_authorized_action')}
  active['operation_identity_rule']='All reserved_operation_ids belong to durable operations. A different intended operation needs an unused id; retry requires ALL original arguments unchanged. Never replay unknown effects. Counters and backend refusals remain authoritative.'
  active['offered_tools']=[t['function']['name'] for t in payload.get('tools',[])];active['owner_goal']=checkpoint['owner_goal'];active['checkpoint_reference']=checkpoint_id;active['archive_reference']=archive
  active['counters']=[x for x in checkpoint['counters'] if x['failed_cycles'] or x['infra_incidents'] or x['state']!='OPEN']
  active['decisions']=[{'reference':e['id'],'actor':e['actor'],'instruction':preview(e['result'].get('instruction'),600)} for e in checkpoint['decisions']]
  active['model_notes']=[{'reference':e['id'],'content':preview(e['result'],500),'verification':'model note, not independently established fact'} for e in checkpoint['model_notes']]
  active['coordinator_instructions']=[{'reference':e['id'],'instruction':preview(e['result'].get('instruction',e['result']),900)} for e in checkpoint['coordinator_instructions']]
  active['verified_api_observations']=[{'reference':e['id'],'actor':e['actor'],'observed_at':e['created'],'observation':preview(e['result'],700)} for e in checkpoint['verified_api_observations']]
  active['last_observations']=checkpoint['last_observations']
  if self.task:
   # Compaction must not hide already verified criteria or a written report.
   # These are canonical backend facts, not a model-authored progress summary.
   status=self.store.contract_status(self.m,self.task)
   active['active_task_contract_status']={k:v for k,v in status.items() if k!='semantic'}
   active['active_task_contract_status']['semantic']=[
    {**{k:v for k,v in item.items() if k!='contract'},'contract':'active:'+str(i)}
    for i,item in enumerate(status.get('semantic',[]))]
   passed=[item for item in status.get('semantic',[]) if item.get('status')=='PASS' and item.get('invocation_id')]
   if status.get('all_satisfied') and status.get('report_written') and passed:
    active['active_task_contract_status']['completion_request']={
     'id':self.task,'report_path':status['report_path'],'evidence_id':passed[-1]['invocation_id']}
    active['active_task_contract_status']['next_action']='Call mission_task_complete with completion_request. Server rechecks freshness and reads the report; do not rewrite it or replay PASS criteria.'
  if json.loads(self.store.get(self.m)['spec']).get('compact_semantic_references'):
   # Exact predicates stay immutable in canonical task/plan/checkpoint. The
   # server resolves active:N; the active model need not repeat transfer paths.
   contract=checkpoint['task_contract']
   active['task_contract']={k:v for k,v in contract.items() if k!='semantic'}
   active['task_contract']['semantic']=[{'contract':'active:'+str(i),'sha256':sha(c),'kind':c['kind']} for i,c in enumerate(contract.get('semantic',[]))]
   active['task_contract']['binding']='Exact stored predicates resolved by mission_verify active:N; completion enforces every original criterion.'
   active['interface_counters']=[{'category_sha256':sha([c['epoch'],c['category']]),'count':c['count']} for c in checkpoint['interface_counters']]
   active['counters']=[{k:c[k] for k in ('fingerprint','failed_cycles','infra_incidents','state','escalation_event')} for c in active['counters']]
   active['observed_evidence']=[{k:e[k] for k in ('reference','executor','kind','observed_process_returncode','source_version')} for e in checkpoint['observed_evidence']]
  blue=[system,{'role':'user','content':encoded({'operational_state':active,'history':'Complete journal and archives retained. Use context_recall on references; do not repeat received actions.'})}]
  # Keep one complete native assistant/tool exchange when it fits. Do not alter
  # executed arguments to manufacture a different historical command.
  start=next((i for i in range(len(original)-1,-1,-1) if original[i].get('role')=='assistant' and original[i].get('tool_calls')),None)
  tail=copy.deepcopy(original[start:]) if start is not None else []
  candidate={**payload,'messages':blue+tail}
  if serialized_bytes(candidate)>budget:
   # Preserve the last actual reply over redundant historical previews. A
   # reference without its latest result can otherwise cause recall loops.
   for key in ('decisions','model_notes','last_observations','verified_api_observations'):
    active.pop(key,None)
   active['coordinator_instructions']=active['coordinator_instructions'][:1]
   candidate['messages']=[system,{'role':'user','content':encoded(active)}]+tail
  if serialized_bytes(candidate)>budget:candidate['messages']=[system,{'role':'user','content':encoded(active|{'last_observations':checkpoint['last_observations'][-1:]})}]
  if serialized_bytes(candidate)>budget:
   # Preview lengths shrink, never owner objective, predicates or system policy.
   active['last_observations']=[{'reference':o['reference'],'tool':o['tool'],'result':preview(o.get('result'),350)} for o in checkpoint['last_observations'][-2:]]
   active['coordinator_instructions']=active['coordinator_instructions'][:1]
   active['decisions']=active.get('decisions',[])[:1];active['model_notes']=active.get('model_notes',[])[:1]
   candidate['messages']=[system,{'role':'user','content':encoded(active)}]
  if serialized_bytes(candidate)>budget:
   self.store.event(self.m,'context_capacity_blocked',self.task,'JARVIS-engine',result={**measurement,'archive':archive,'checkpoint':checkpoint_id,'reason':'Mandatory policy/objective/contracts/tool schema exceed capacity; coordinator must split the task, not silently truncate constraints'})
   raise ContextCapacityError('Mandatory active task does not fit: checkpoint saved, no inference dispatched')
  original[:]=candidate['messages'];payload['messages']=original
  self.store.event(self.m,'context_budget_checked',self.task,'JARVIS-engine',result={**measurement,'compacted':True,'archive':archive,'checkpoint':checkpoint_id,'sent_bytes':serialized_bytes(payload),'within_budget':True})
  return payload

def register(reg):
 def budget():
  store=getattr(reg,'mission_store',None);ctx=reg.context
  if not store or not ctx.get('mission_id'):raise ValueError('Canonical mission required')
  return ContextBudget(store,ctx['mission_id'],ctx.get('task_id'))
 def checkpoint(a):
  b=budget();e,value=b.checkpoint(a['reason'])
  if a.get('pause_for_restart'):
   b.store.event(b.m,'context_restart_requested',b.task,'JARVIS',result={'checkpoint_reference':e,'old_process_id':value['process_id'],'reason':a['reason'],'human_approval_required':False})
   b.store.transition(b.m,'interrupted',result={'reason':'Controlled worker restart requested; coordinator continues autonomously','checkpoint_reference':e})
  return {'reference':e,'sha256':sha(value),'mission':value['mission'],'task':value['task'],'process_id':value['process_id'],'pending_effects':value['pending_effects'],'counters':value['counters'],'authority_counters':value['authority_counters'],'interface_counters':value['interface_counters'],'next_authorized_action':value['next_authorized_action']}
 def resume(a):
  b=budget()
  with b.store.db() as c:
   if a.get('reference'):
    row=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND id=? AND kind='operational_checkpoint'",(b.m,a['reference'])).fetchone()
   else:
    row=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND kind='operational_checkpoint' AND coalesce(json_extract(result,'$.checkpoint.automatic'),0)=0 ORDER BY id DESC LIMIT 1",(b.m,)).fetchone()
  if not row:raise ValueError('No manual operational checkpoint; supply an existing checkpoint reference')
  prior={'id':row['id'],'result':json.loads(row['result'])}
  old=prior['result']['checkpoint'];e,current=b.checkpoint('resume from persistent operational state',automatic=True)
  b.store.event(b.m,'context_resumed',b.task,'JARVIS',result={'previous_reference':prior['id'],'current_reference':e,'old_process_id':old['process_id'],'current_process_id':current['process_id'],'counters_preserved':all(any(n['fingerprint']==p['fingerprint'] and n['failed_cycles']>=p['failed_cycles'] and n['infra_incidents']>=p['infra_incidents'] for n in current['counters']) for p in old['counters']),'authority_counters_unchanged':old['authority_counters']==current['authority_counters'],'interface_counters_unchanged':old['interface_counters']==current['interface_counters']})
  return {'reference':e,'previous_reference':prior['id'],'same_task':old['task']==current['task'],'counters_unchanged':old['counters']==current['counters'],'new_process':old['process_id']!=current['process_id'],'plan_unchanged':old['plan']==current['plan'],'counters_preserved':all(any(n['fingerprint']==p['fingerprint'] and n['failed_cycles']>=p['failed_cycles'] and n['infra_incidents']>=p['infra_incidents'] for n in current['counters']) for p in old['counters']),'authority_counters_unchanged':old['authority_counters']==current['authority_counters'],'interface_counters_unchanged':old['interface_counters']==current['interface_counters'],'pending_effects':current['pending_effects'],'state':{k:current[k] for k in ('mission','task','objective','task_state','plan','last_observations','next_authorized_action')}}
 reg.specs['context_checkpoint']=('Persist structured operational state in canonical SQLite: task, decisions, real observations, counters, dependencies and next authorized action; no model-only summary.',{'reason':{'type':'string','maxLength':500},'pause_for_restart':{'type':'boolean','description':'If true, save and pause this mission for an already authorized worker restart; Codex resumes automatically, no human approval.'}},['reason'],'read_only',checkpoint)
 reg.specs['context_resume']=('Resume a manual checkpoint (latest by default) after interruption. Automatic budget snapshots never shadow the manual waypoint. Return actual process/counter comparisons without reloading conversation.',{'reference':{'type':'integer','minimum':1}},[],'read_only',resume)
 reg.specs['context_recall']=('Read a targeted canonical event/archive from this mission or linked parent. offset starts at0; returned fragment is explicitly incomplete. Never treats model notes as established facts.',{'reference':{'type':'integer','minimum':1},'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':4000}},['reference'],'read_only',lambda a:budget().recall(a['reference'],a.get('offset',0),a.get('limit',1800)))
