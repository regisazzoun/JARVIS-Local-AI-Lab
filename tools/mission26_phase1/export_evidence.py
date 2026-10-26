"""Export scoped operational evidence, not conversations, memory or policy secrets."""
import argparse,hashlib,json,re,sys,time
from pathlib import Path

def main():
 parser=argparse.ArgumentParser();parser.add_argument('mission');parser.add_argument('--root',default='/opt/jarvis/conversation');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 sys.path.insert(0,args.root)
 from jarvis.mission_store import MissionStore
 s=MissionStore(args.root);m=s.get(args.mission);spec=json.loads(m['spec'])
 if not spec.get('distributed_authority'):raise SystemExit('Only opt-in distributed demonstration may be exported')
 events=s.events(args.mission,limit=100000)
 state=next((e['result'] for e in reversed(events) if e['kind']=='authority_state'),{})
 selected=[]
 for e in events:
  if e['kind']=='authority_state':continue
  if e['kind'].startswith(('authority_','codex_')) or e['kind'] in ('coordinator_instruction','plan_saved','plan_revised','task_verified','state_changed','inference_finished','mission_created','model_report_original','report_created','working_context_rebased','report_revision_requested','context_compacted','cycle_error'):
   row=dict(e)
   if e['kind']=='inference_finished':
    row['result']={'metrics':{k:v for k,v in e['result'].get('metrics',{}).items() if k in ('node','effective_model','role','num_ctx','prompt_eval_count','eval_count','compute_job','end_to_end_s','load_duration','eval_duration','prompt_eval_duration','queue_wait_s')}}
   selected.append(row)
 calls=[]
 for o in s.observations(args.mission):
  if o['tool']=='mission_evidence':
   # Original recursively quoted evidence remains canonical, no need to republish copies.
   calls.append({k:o[k] for k in ('id','tool','task','arguments','state','created')});continue
  calls.append(o)
 metrics=[e['result'].get('metrics',{}) for e in events if e['kind']=='inference_finished']
 executions=[e for e in events if e['kind']=='authority_execution']
 data={'contract_version':'26-P1.evidence.1','captured_at':time.time(),'mission':{k:m[k] for k in ('id','goal','state','created','updated','project','report_path')},'spec':spec,
       'plans':s.plans(args.mission),'tasks':s.tasks(args.mission),'current_counters':state.get('issues',{}),'synchronizations':state.get('syncs',[]),
       'stats':{'observed_inferences':len(metrics),'max_prompt_eval_count':max([x.get('prompt_eval_count',0) for x in metrics] or [0]),'max_prompt_plus_generation':max([x.get('prompt_eval_count',0)+x.get('eval_count',0) for x in metrics] or [0]),'context_compactions':sum(e['kind']=='context_compacted' for e in events),'cycle_errors':sum(e['kind']=='cycle_error' for e in events),'observed_context_sizes':sorted({x.get('num_ctx',0) for x in metrics}),'model_decisions':sum(e['kind']=='authority_model_decision' for e in events),'real_executions':len(executions),'executions_by_host':{h:sum(e['result']['host']==h for e in executions) for h in ('Dell1','Dell2')},'nonzero_test_processes':sum(e['result']['kind']=='test' and e['result']['execution']['returncode']!=0 for e in executions),'nonzero_executions_all_declared_kinds':sum(e['result']['execution']['returncode']!=0 for e in executions),'actual_file_modifications':sum(e['result']['before']!=e['result']['after'] for e in executions)},
       'events':selected,'tool_receipts':calls,'preservation':'Complete originals, repetitive state snapshots and recursive evidence views remain in canonical missions.sqlite. No private memory, owner conversations, host policy or SSH identities exported.'}
 body=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
 if re.search(r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY|github_pat_|ghp_[A-Za-z0-9]{20}|Authorization: Bearer',body):raise SystemExit('Potential secret marker; inspect privately before publication')
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(body)
 print(json.dumps({'mission':args.mission,'state':m['state'],'bytes':len(body.encode()),'sha256':hashlib.sha256(body.encode()).hexdigest(),'stats':data['stats']},ensure_ascii=False))
if __name__=='__main__':main()
