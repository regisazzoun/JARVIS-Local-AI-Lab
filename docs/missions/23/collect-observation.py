#!/usr/bin/env python3
"""Read-only reception snapshot; run with access to the canonical technical database.
Does not run application code, resume, mutate tasks or publish raw commands/secrets.
"""
import argparse,collections,hashlib,json,sqlite3,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--database',default='/opt/jarvis/conversation/runtime/missions.sqlite');p.add_argument('--mission',default='7971ec0311124fb4be9e3125dcb291fd');p.add_argument('--after-event',type=int,default=3953);p.add_argument('--output',required=True);a=p.parse_args()
c=sqlite3.connect('file:'+a.database+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
mission=dict(c.execute('select id,state,attempts,active_task,updated from missions where id=?',(a.mission,)).fetchone());events=[dict(r) for r in c.execute('select * from mission_events where mission=? and id>=? order by id',(a.mission,a.after_event))]
calls=[];compactions=[];inferences=[]
for e in events:
 r=json.loads(e['result'] or '{}');args=json.loads(e['arguments'] or '{}')
 if e['kind']=='tool_finished':
  value=r.get('result',{});stdout=value.get('stdout','');stderr=value.get('stderr','');text=stdout+'\n'+stderr
  calls.append({'event':e['id'],'invocation':e['invocation'],'actor':e['actor'],'tool':e['tool'],'ok':r.get('ok'),'action':args.get('action'),'path':args.get('path'),'created':e['created'],'command_sha256':hashlib.sha256(args['command'].encode()).hexdigest() if 'command' in args else None,'returncode':value.get('returncode'),'broker_evidence':value.get('evidence_id'),'flags':{k:k in text for k in ['RuntimeWarning','Traceback','LLM_STREAM_VERIFIED','AGENT_ADAPTERS_VERIFIED','Génération non disponible']}})
 if e['kind']=='context_compacted':compactions.append({'event':e['id'],**r})
 if e['kind']=='inference_finished':inferences.append(r.get('metrics',{}))
tasks=[dict(r) for r in c.execute('select id,title,state,artifact,report_sha256 from tasks where mission=? order by id',(a.mission,))];done=sum(t['state']=='validated' for t in tasks)
record={'collected_at':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'mission':mission,'window_start_event':a.after_event,'tasks':tasks,'validated':done,'total':len(tasks),'progress_percent':round(100*done/len(tasks)),'tool_results':dict(collections.Counter('success' if x['ok'] else 'failure' for x in calls)),'tool_receipts':calls,'inference_done_reasons':dict(collections.Counter(x.get('done_reason') for x in inferences)),'route_failure_count':sum(bool(x.get('route_failures')) for x in inferences),'compaction_receipts':compactions,'interpretation':'Flags are observations, not proof that a marker corresponds to a valid test; inspect the generated test and actual response before reception. No application text or private inventory exported.'}
Path(a.output).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'state':mission['state'],'validated':done,'total':len(tasks),'progress':record['progress_percent'],'tools':record['tool_results'],'compactions':len(compactions)}))
