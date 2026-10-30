"""Keep observed permissions usable across context compaction, without granting any.

The broker still reloads and enforces its policy on every real invocation.
"""
import copy,json

def observed_policy(store,mission):
 with store.db() as db:
  row=db.execute("SELECT id,created,result FROM tool_calls WHERE mission=? AND tool='host_policy' AND json_extract(result,'$.ok')=1 ORDER BY created DESC,rowid DESC LIMIT 1",(mission,)).fetchone()
 if not row:return None
 value=json.loads(row['result']).get('result',{})
 return {'invocation_id':row['id'],'observed_at':row['created'],'policy_sha256':value.get('policy_identity',{}).get('policy_sha256',value.get('diagnostic',{}).get('policy_sha256')),
         'services':value.get('services',{}),'write_roots':value.get('write_roots',[]),'report_workspace':json.loads(store.get(mission)['spec']).get('report_workspace'),
         'projection_only':True,'meaning':'Observed permissions, not observed service states. Full original policy remains at invocation_id; broker checks current policy on every call.'}

def service_schemas(schemas,policy):
 if not policy or not policy.get('services'):return schemas
 result=copy.deepcopy(schemas)
 for entry in result:
  if entry['function']['name']!='host_service':continue
  props=entry['function']['parameters']['properties']
  props['service']['enum']=sorted(policy['services'])
  props['action']['enum']=sorted({a for actions in policy['services'].values() for a in actions})
 return result

def observation_arguments(tool,args):
 if tool not in ('mission_plan','mission_plan_report_step'):return args
 return {'proposal_arguments_sha256':__import__('hashlib').sha256(json.dumps(args,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
         'expected_version':args.get('expected_version'),'proposal_is_not_an_execution_observation':True,
         'original_arguments':'Retained in the original tool invocation; the current accepted plan is provided separately.'}

def report_path_allowed(path,policy,workspace=None):
 from pathlib import PurePosixPath
 if not isinstance(path,str) or not path.startswith('/') or '..' in PurePosixPath(path).parts:return False
 roots=[workspace] if workspace else (policy or {}).get('write_roots',[])
 if not roots:return True  # No observed policy: existing broker remains the authority.
 return any(path.startswith(root.rstrip('/')+'/') for root in roots)

def report_relocation(store,mission,task,previous,replacement):
 """Relocate an unwritable, never-received report; preserve the exact verifier.

 Owner acceptance predicates are checked separately by MissionStore. This is
 not available for application/file-content predicates or a received report.
 """
 if task['state']=='validated' or previous.get('kind')!='report':return False
 old_path=task.get('contract',{}).get('report_path')
 if previous.get('source')!={'tool':'host_read_file','arguments':{'path':old_path}}:return False
 spec=json.loads(store.get(mission)['spec']);policy=observed_policy(store,mission)
 if report_path_allowed(old_path,policy,spec.get('report_workspace')):return False
 for e in store.events(mission,limit=1000000):
  if e['task']==task['id'] and e['kind']=='semantic_verification' and e['result'].get('status')=='PASS' and e['result'].get('contract')==previous:return False
 for candidate in replacement:
  path=candidate.get('source',{}).get('arguments',{}).get('path')
  expected=copy.deepcopy(previous);expected['source']['arguments']['path']=path
  if candidate==expected and report_path_allowed(path,policy,spec.get('report_workspace')):return True
 return False

def planning_state(store,mission,registered,coordinator):
 """Exact active planning inputs, without replaying rejected model proposals.

 This is a phase view of the same journal. No task or command is authored here.
 """
 from .mission_assurance import coverage_state,latest
 row=store.get(mission);spec=json.loads(row['spec']);plans=store.plans(mission)
 observations=store.observations(mission,limit=1)
 last=observations[-1] if observations else None
 return {'phase':'planning','mission':mission,'owner_goal':row['goal'],
         'owner_acceptance':spec.get('acceptance',[]),'project':row['project'],'report_workspace':spec.get('report_workspace'),'planning_feedback':planning_feedback(store,mission),
         'current_plan_version':plans[-1]['version'] if plans else 0,
         'current_plan_proposal':plans[-1]['plan'] if plans else None,
         'proposal_is_not_observed_state':True,
         'coverage':coverage_state(store,mission),'pending_plan_review':latest(store,mission,'plan_review_deferred'),
         'observed_host_policy':observed_policy(store,mission),
         'registered_execution_tool_names':sorted(registered),
         'coordinator_instructions':[json.loads(r['result']) for r in reversed(coordinator)],
         'latest_tool_result':{'invocation_id':last['id'],'tool':last['tool'],'ok':(last['result'] or {}).get('ok'),'error':(last['result'] or {}).get('error'),'original_result':'Retained in mission_evidence'} if last else None,
         'history':'All previous plans, rejected attempts, counters, original outputs and receipts remain in the canonical store. This view is not a new mission or a reset.'}

def planning_feedback(store,mission):
 """Feedback must survive rebuilt/compacted contexts, even before tool dispatch."""
 with store.db() as db:
  rejection=db.execute("SELECT id,result FROM mission_events WHERE mission=? AND kind='structured_action_rejected' ORDER BY id DESC LIMIT 1",(mission,)).fetchone()
  call=db.execute("SELECT id,result FROM tool_calls WHERE mission=? AND tool IN ('mission_plan','mission_plan_report_step') AND state='finished' ORDER BY created DESC,rowid DESC LIMIT 1",(mission,)).fetchone()
 result={}
 if rejection:
  data=json.loads(rejection['result']);result['interface_rejection']={'reference':rejection['id'],'error':data['error'],'no_tool_dispatched':True,'meaning':'Historical rejection; compare later results before treating it as unresolved.'}
 if call:
  wrapper=json.loads(call['result']);value=wrapper.get('result') or {}
  result['latest_plan_call']={'invocation_id':call['id'],'ok':wrapper.get('ok'),'error':wrapper.get('error'),'current_plan_version':value.get('current_plan_version'),'execution_allowed':value.get('execution_allowed'),'coverage':value.get('coverage'),'next_action':value.get('next_action')}
 return result

READ_SERVICE_ACTIONS={'status','show','is-active','is-enabled'}
def service_read_completed(wrapper):
 """A nonzero observed process is not a denied/unexecuted broker operation."""
 out=wrapper.get('result') or {}
 return bool(wrapper.get('ok') or ((out.get('diagnostic') or {}).get('error_category')=='application_error' and out.get('evidence_id') and type(out.get('duration_s')) in (int,float) and type(out.get('returncode')) is int))

def observed_service_reads(store,mission):
 """Original completed read outputs, including valid nonzero process exits.

 Scope is an explicit read-only snapshot mission, not continuous monitoring.
 A new owner-requested observation epoch permits new reads. No process exit
 code is promoted to a functional PASS.
 """
 with store.db() as db:
  cutoff=db.execute("SELECT coalesce(max(created),0) FROM mission_events WHERE mission=? AND kind IN ('owner_external_resolution_confirmed','external_dependency_recheck_requested','service_observation_recheck_requested')",(mission,)).fetchone()[0]
  rows=db.execute("SELECT id,created,arguments,result FROM tool_calls WHERE mission=? AND tool='host_service' AND state='finished' AND created>=? ORDER BY created,rowid",(mission,cutoff)).fetchall()
 snapshot={}
 for row in rows:
  args=json.loads(row['arguments']);wrapper=json.loads(row['result'] or '{}');out=wrapper.get('result') or {};action=args.get('action');service=args.get('service')
  if not service_read_completed(wrapper) or action not in READ_SERVICE_ACTIONS or not service or type(out.get('returncode')) is not int or not isinstance(out.get('stdout'),str) or out.get('stdout_truncated') or out.get('timeout'):continue
  from datetime import datetime
  from zoneinfo import ZoneInfo
  text=out['stdout'];item={'invocation':row['id'],'observed_at':row['created'],'observed_at_iso':datetime.fromtimestamp(row['created'],ZoneInfo('Europe/Paris')).isoformat(timespec='seconds'),'returncode':out['returncode']}
  if action in ('is-active','is-enabled') and len(text)<=120:item['observed_text']=text.strip()
  else:item['stdout_sha256']=__import__('hashlib').sha256(text.encode()).hexdigest();item['full_output']='mission_evidence at invocation'
  snapshot.setdefault(service,{})[action]=item
 return snapshot

def service_snapshot_summary(policy,reads):
 """Exact ledger counts with explicit referents, never a semantic success verdict."""
 services=set((policy or {}).get('services',{}));result={}
 for action in ('is-active','is-enabled','status','show'):
  selected={name:pairs[action] for name,pairs in reads.items() if action in pairs and name in services}
  texts={};codes={}
  for row in selected.values():
   if 'observed_text' in row:texts[row['observed_text']]=texts.get(row['observed_text'],0)+1
   code=str(row['returncode']);codes[code]=codes.get(code,0)+1
  result[action]={'observed_units':len(selected),'stdout_counts':texts,'returncode_counts':codes,'unobserved_units':sorted(services-set(selected))}
 return {'policy_invocation':(policy or {}).get('invocation_id'),'allowed_units':len(services),'by_action':result,'meaning':'Exact receipt counts by action and printed value, not health, presence, restart or deployment verification.'}

def unread_service_schemas(schemas,policy,reads):
 """Suppress duplicate snapshot reads; the model selects remaining pairs.

 Report/semantic verifiers still perform independent reads via the broker.
 This function never executes a tool or asserts a healthy service.
 """
 if not policy or not policy.get('services'):return schemas
 result=[]
 for entry in copy.deepcopy(schemas):
  if entry['function']['name']!='host_service':result.append(entry);continue
  groups={}
  for service,actions in policy['services'].items():
   remaining=tuple(sorted((set(actions)&READ_SERVICE_ACTIONS)-set(reads.get(service,{}))))
   if remaining:groups.setdefault(remaining,[]).append(service)
  if not groups:continue
  params=entry['function']['parameters'];base=copy.deepcopy(params);base.pop('oneOf',None);base.pop('allOf',None)
  branches=[]
  for actions,services in groups.items():
   branch=copy.deepcopy(base);branch['properties']['service']['enum']=sorted(services);branch['properties']['action']['enum']=list(actions);branches.append(branch)
  entry['function']['parameters']={'type':'object','oneOf':branches}
  entry['function']['description']+=' Read-only snapshot: completed service/action pairs are retained in observed_service_reads and are not offered again. Nonzero returncodes remain observations, never a PASS. New external recheck permits a fresh snapshot.'
  result.append(entry)
 return result
