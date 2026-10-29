"""Scoped reception tools inside the existing durable engine; Qwen supplies actions."""
import json,os,time,hashlib,uuid
from pathlib import Path
from .attempt_execution import AttemptExecutor
from .attempt_ledger import digest

TOOL_NAMES={'p2_execute','p2_observe','p2_status','p2_resume','p2_reverify'}
def context(reg):
 store=reg.mission_store;m=reg.context['mission_id'];spec=json.loads(store.get(m)['spec']);cfg=spec.get('p2_reception') or {}
 if not cfg.get('active'):raise ValueError('Reception capability not assigned by owner')
 return store,m,spec,cfg,AttemptExecutor(store,m,spec['authority_workspace']['project'])
def scope(case):return 'M26-P2-reception/'+('S07' if case=='S10' else case)
def descriptor(case):return {'component':scope(case),'criterion':'owner10case-reception-v1','project':'mission26-phase2'}
def execute(reg,a):
 store,m,spec,cfg,runner=context(reg);case=a['scenario']
 if case!=cfg['case']:raise ValueError('Only current owner-assigned scenario may execute')
 if case not in ('S01','S02','S03','S04','S05','S06','S07','S10'):raise ValueError('This case is observation-only')
 row=runner.run(scope(case),descriptor(case),uuid.uuid4().hex,a['executor'],'correction_test' if case in ('S07','S10') else 'test' if case=='S02' else 'execute',a['command'],a.get('verification',''),{'S03':'policy_denied','S04':'worker_unavailable','S05':'drop_reply'}.get(case),['reception/negative.json'] if case in ('S07','S10') else [],{'kind':'json','expected':{'/value':42},'types':{'/value':'integer'}} if case in ('S07','S10') else None)
 store.event(m,'p2_scenario_action',actor='JARVIS/Qwen80B',arguments=a,result={'case':case,'epoch':cfg['epoch'],'worker_pid':os.getpid(),'observed':row,'reception_accepted':False})
 return {'case':case,'observed':row,'reception_accepted':False}
def observe(reg,a):
 store,m,spec,cfg,runner=context(reg)
 if cfg['case'] not in ('S05','S09'):raise ValueError('Only assigned recovery observation allowed')
 if cfg['case']=='S09':
  observed=[e for e in store.events(m,limit=100000) if e['kind']=='p2_restart_observed' and e['result'].get('epoch')==cfg['epoch'] and e['result'].get('same_ledger') and e['result'].get('new_worker_process')]
  if not observed:raise ValueError('Call p2_resume before observing the lost outcome')
 snapshot=runner.ledger.snapshot();problem=runner.ledger.problem(scope('S05'),descriptor('S05'))
 row=next((r for r in snapshot['attempts'] if r['problem']==problem),None)
 if not row:raise ValueError('No existing lost-response attempt')
 result=runner.observe(row['id'])
 store.event(m,'p2_scenario_observation',actor='JARVIS/Qwen80B',result={'case':cfg['case'],'epoch':cfg['epoch'],'worker_pid':os.getpid(),'observed':result})
 return result
def reverify(reg,a):
 store,m,spec,cfg,runner=context(reg)
 if cfg['case'] not in ('S06','S07','S09'):raise ValueError('Verification repair not currently assigned')
 target='S05' if cfg['case']=='S09' else cfg['case']
 problem=runner.ledger.problem(scope(target),descriptor(target));snapshot=runner.ledger.snapshot()
 row=next(r for r in snapshot['attempts'] if r['problem']==problem)
 result=runner.observe(row['id'],a['verification'],{'kind':'json','expected':{'/value':42},'types':{'/value':'integer'}} if cfg['case']=='S07' else None)
 store.event(m,'p2_scenario_reverification',actor='JARVIS/Qwen80B',result={'case':cfg['case'],'epoch':cfg['epoch'],'worker_pid':os.getpid(),'observed':result,'no_original_command_reexecution':True})
 return result
def status(reg,a):
 store,m,spec,cfg,runner=context(reg);snapshot=runner.ledger.snapshot()
 result={'problems':[{k:r[k] for k in ('scope','failed_cycles','infra_incidents','state','escalation_event')} for r in snapshot['problems']],'attempts':[{k:r[k] for k in ('id','executor','phase','state','unknown_outcome')} for r in snapshot['attempts']]}
 store.event(m,'p2_scenario_status',actor='JARVIS/Qwen80B',result={'case':cfg['case'],'epoch':cfg['epoch'],'snapshot':result,'worker_pid':os.getpid()})
 return result
def resume(reg,a):
 store,m,spec,cfg,runner=context(reg)
 if cfg['case']!='S09':raise ValueError('Restart verification not assigned')
 with store.db() as c:row=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND kind='p2_restart_checkpoint' ORDER BY id DESC LIMIT 1",(m,)).fetchone()
 if not row:raise ValueError('No checkpoint')
 checkpoint=json.loads(row['result']);snapshot=runner.ledger.snapshot()
 previous=[e for e in store.events(m,limit=100000) if e['kind']=='p2_restart_observed' and e['result'].get('checkpoint_event')==row['id'] and e['result'].get('same_ledger') and e['result'].get('new_worker_process')]
 if previous:
  result={**previous[0]['result'],'epoch':cfg['epoch'],'reused_initial_restart_observation':previous[0]['id'],'current_worker_pid':os.getpid(),'new_worker_process':os.getpid()!=checkpoint['old_worker_pid'],'comparison_scope':'initial restart observation, before subsequent recovery','unknown_attempts_at_restart':previous[0]['result']['unknown_attempts'],'unknown_attempts':[r['id'] for r in snapshot['attempts'] if r['unknown_outcome']]}
  store.event(m,'p2_restart_observed',actor='JARVIS/Qwen80B',result=result)
  return result
 result={'checkpoint_event':row['id'],'same_ledger':digest(snapshot)==checkpoint['ledger_sha256'],'old_worker_pid':checkpoint['old_worker_pid'],'current_worker_pid':os.getpid(),'new_worker_process':os.getpid()!=checkpoint['old_worker_pid'],'failed_cycles':{r['scope']:r['failed_cycles'] for r in snapshot['problems']},'unknown_attempts':[r['id'] for r in snapshot['attempts'] if r['unknown_outcome']]}
 store.event(m,'p2_restart_observed',actor='JARVIS/Qwen80B',result={'epoch':cfg['epoch'],**result})
 return result
def register(reg):
 string={'type':'string','maxLength':6500}
 reg.specs['p2_execute']=('Execute YOUR current P2 reception operation on a Dell. Choose command and real independent verification. Infrastructure records actual start/result, injects assigned real channel faults, and enforces persistent counters. No code is run on Mac. Negative expected cases remain failures, not business success.',{'scenario':{'type':'string','enum':['S01','S02','S03','S04','S05','S06','S07','S10']},'executor':{'type':'string','enum':['Dell1','Dell2']},'command':string,'verification':string,'diagnosis':string,'task_alias':string},['scenario','executor','command','diagnosis'],'host_authorized',lambda a:execute(reg,a))
 reg.specs['p2_reverify']=('Correct ONLY the verifier for the existing S06/S07 result; preserve the original action and read its existing receipt. Supply a real independent verification command, not a declaration.',{'verification':string},['verification'],'host_authorized',lambda a:reverify(reg,a))
 reg.specs['p2_observe']=('Read actual existing lost-response receipt independently; never rerun its command.',{},[],'read_only',lambda a:observe(reg,a))
 reg.specs['p2_status']=('Read actual counters, states and escalation event from canonical SQLite.',{},[],'read_only',lambda a:status(reg,a))
 reg.specs['p2_resume']=('Verify checkpoint against canonical persisted ledger from the new native worker process.',{},[],'read_only',lambda a:resume(reg,a))
def case_ready(store,m,case,epoch):
 events=[e for e in store.events(m,limit=100000) if e['result'].get('epoch')==epoch]
 actions=[e for e in events if e['kind']=='p2_scenario_action']
 if case=='S06':return any(e['kind'] in ('p2_scenario_action','p2_scenario_reverification') and e['result']['observed'].get('result',{}).get('verification',{}).get('verdict')=='INSUFFICIENT' and 'PermissionError' in e['result']['observed']['result']['verification'].get('reason','') for e in events)
 if case=='S07':return any(e['result']['observed'].get('problem_state')=='ESCALATED' for e in actions)
 if case=='S08':return any(e['kind']=='p2_scenario_status' and any(p['state']=='ESCALATED' for p in e['result']['snapshot']['problems']) for e in events)
 if case=='S09':return any(e['kind']=='p2_restart_observed' and e['result'].get('same_ledger') and e['result'].get('new_worker_process') for e in events) and any(e['kind'] in ('p2_scenario_observation','p2_scenario_reverification') and e['result']['observed'].get('state')=='SUCCESS' for e in events)
 if case=='S10':return any(e['result']['observed'].get('blocked') for e in actions)
 return bool(actions)
def run_cycle(core,store,mission):
 m=mission['id'];spec=json.loads(mission['spec']);cfg=spec['p2_reception'];case=cfg['case'];epoch=cfg['epoch']
 core.tools.mission_store=store;core.tools.context={'mission_id':m,'task_id':'step-1','conversation':mission['conversation'],'project':mission['project'],'compute_role':'mission','host_target':True}
 if case_ready(store,m,case,epoch):
  store.transition(m,'waiting_external',result={'reason':'Scenario observations ready for independent Codex reception','case':case,'human_approval_required':False});return {'progress':True,'external_block':True,'report':None}
 names={'p2_execute'} if case not in ('S08','S09') else {'p2_status'} if case=='S08' else {'p2_resume','p2_observe'}
 if case=='S09':names={'p2_resume','p2_reverify'}
 if case=='S07':names={'p2_execute','p2_reverify'}
 if case=='S06':names={'p2_reverify'} if cfg.get('verify_only') else {'p2_execute','p2_reverify'}
 schemas=[s for s in core.tools.schemas() if s['function']['name'] in names]
 messages=[{'role':'system','content':"Tu es JARVIS/Qwen80B, responsable technique. Exécute seulement le scénario P2 courant avec les outils proposés. Choisis tes commandes, la machine et analyse chaque résultat. Aucune validation humaine. Les fichiers/outils imaginaires n’existent pas. Cwd Dell /opt/jarvis-lab/mission26-phase2, dossier reception/ présent, Python3. Un négatif attendu doit rester FAIL/NOT_EXECUTED/INSUFFICIENT dans le journal. L’infrastructure Codex a écrit le protocole, pas toi; tes actions restent traçables. Pas de lecture générale ni mission_plan/authority_finish. Utilise maintenant les outils proposés, pas un simple texte."},{'role':'user','content':cfg['instruction']}]
 with store.db() as c:
  prior=c.execute("SELECT result FROM mission_events WHERE mission=? AND kind='p2_model_checkpoint' ORDER BY id DESC LIMIT 1",(m,)).fetchone()
 if prior:
  prior=json.loads(prior['result'])
  if prior.get('epoch')==epoch:messages=prior['messages']
 errors=0
 for turn in range(6):
  if store.get(m)['state']=='interrupted':return {'progress':True,'external_block':True,'report':None}
  payload={'model':mission['model'],'messages':messages,'tools':schemas,'stream':False,'options':{'num_ctx':16384,'num_predict':2048,'temperature':0.1}}
  start=time.monotonic();response=core.transport(payload);metrics=core.metrics[-1] if core.metrics else {}
  store.event(m,'inference_finished',actor='JARVIS-engine',result={'metrics':metrics,'scope':'Native durable P2 reception','case':case,'epoch':epoch},duration=time.monotonic()-start)
  if metrics.get('node')!='Dell1' or metrics.get('effective_model')!='qwen3-coder-next:q4_K_M':raise ValueError('Reception decision not from actual Qwen80B/Dell1')
  from .protocol import normalize_message
  response=normalize_message(response,core.tools.specs);messages.append(response)
  calls=response.get('tool_calls') or []
  if not calls:
   errors+=1;messages.append({'role':'user','content':'Aucune opération exécutée par ce texte. Utilise un outil proposé; les preuves réelles sont nécessaires.'})
  for call in calls:
   name=call['function']['name'];args=call['function']['arguments']
   if isinstance(args,str):args=json.loads(args)
   token=store.begin_call(m,'step-1',name,args);started=time.monotonic()
   if name not in names:result={'ok':False,'error':'Only current reception tools are assigned'}
   else:result=core.tools.execute(name,args)
   store.finish_call(token,result,time.monotonic()-started)
   messages.append({'role':'tool','tool_name':name,'content':json.dumps(result,ensure_ascii=False)})
   if not result.get('ok'):errors+=1
   if case_ready(store,m,case,epoch):
    store.event(m,'p2_case_observations_ready',actor='JARVIS-engine',result={'case':case,'epoch':epoch,'worker_pid':os.getpid(),'reception_accepted':False})
    store.transition(m,'waiting_external',result={'reason':'Actual scenario evidence ready; Codex verifies, no human approval','case':case});return {'progress':True,'external_block':True,'report':None}
  store.event(m,'p2_model_checkpoint',actor='JARVIS-engine',result={'epoch':epoch,'case':case,'messages':messages})
  if errors>=3:break
 store.event(m,'p2_reception_escalation',actor='JARVIS-engine',result={'case':case,'epoch':epoch,'reason':'Bounded reception task did not produce required observations','errors':errors})
 store.transition(m,'interrupted',result={'case':case,'reason':'Targeted technical assistance needed; no automatic fourth repetition'})
 return {'progress':True,'external_block':True,'report':None}
