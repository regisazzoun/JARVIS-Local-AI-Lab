"""Export only scoped optimization receipts; keep secrets and old user chats private."""
import datetime,hashlib,json,sqlite3,subprocess,urllib.request
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'docs/missions/OPTIMISATION-INTERCONNEXIONS-IA';P=Path('/home/adminjarvis/JARVIS/optimisation-interconnexions-ia-private')
for src,dest in [('canonical-after.json','API-CONVERSATION-APRES.json'),('models-urls-after.json','PLACEMENT-MODELES.json'),('browser-default27.json','NAVIGATEUR-27B.json'),('browser-mission-launch-canonical.json','CREATION-MISSION-REELLE.json')]:
 if (P/src).exists():(D/dest).write_bytes((P/src).read_bytes())
log=[json.loads(x) for x in (P/'admission.jsonl').read_text().splitlines()];(D/'ADMISSION-REELLE.json').write_text(json.dumps(log,indent=2)+'\n')
c=sqlite3.connect('file:/opt/jarvis/conversation/runtime/missions.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
ids=[x['queue_id'] for x in log if 'queue_id' in x];rows=[]
for ident in ids:
 row=c.execute('select id,role,node,model,state,created,started,finished,metrics,error from compute_jobs where id=?',(ident,)).fetchone()
 if row:rows.append(dict(row))
(D/'ADMISSION-CANONIQUE.json').write_text(json.dumps(rows,indent=2)+'\n')
m='27fc9d276ccc435bb32fcfeaeee2969c';mission=dict(c.execute('select id,state,model,goal,attempts,active_task from missions where id=?',(m,)).fetchone());events=[]
for r in c.execute('select id,actor,kind,tool,result from mission_events where mission=? order by id',(m,)):
 e=dict(r);raw=json.loads(e.pop('result') or '{}')
 if e['kind'] in ['tool_finished','coordinator_instruction','codex_probe_escalation','codex_probe_closed']:
  e['result']={k:raw[k] for k in ['ok','error','text','scope','status','meaning','planning_failures','reason'] if k in raw};events.append(e)
 elif e['kind']=='compute_route_observed':
  e['result']={k:raw.get(k) for k in ['node','effective_model','num_ctx','prompt_eval_count','eval_count']};events.append(e)
(D/'SONDE-MOTEUR.json').write_text(json.dumps({'mission':mission,'events':events,'scope':'Creation and worker inference demonstrated; report execution not received after three planning refusals.'},ensure_ascii=False,indent=2)+'\n')
# CLI transport worked, but do not turn a limit exit into a successful final report.
f=P/'qwen-admission-check.jsonl';lines=[json.loads(x) for x in f.read_text().splitlines() if x.startswith('{')];calls=[]
for e in lines:
 for v in e.get('message',{}).get('content',[]):
  if v.get('type')=='tool_use':calls.append({'name':v['name'],'input':v.get('input')})
(D/'QWEN-CODE-RESERVE.json').write_text(json.dumps({'exit_code':53,'trace_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'tool_calls':calls,'last_event_type':lines[-1]['type'],'meaning':'Repeated passing read-only tests; process stopped at twelve turns. Not a received final report.'},ensure_ascii=False,indent=2)+'\n')
(D/'TESTS-LOGICIELS.txt').write_bytes((P/'software-final.txt').read_bytes())
r={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_hashes':[],'services':{},'old_P4':dict(c.execute('select id,state,active_task from missions where id=?',('c32347de3edf4288a4751a3e65afa7eb',)).fetchone()),'manual_hold_present':Path('/home/adminjarvis/JARVIS/mission26-phase2-private/supervision/MANUAL-HOLD').exists()}
for source,target in [('agentic/engine_v2/jarvis/server.py','/opt/jarvis/conversation/jarvis/server.py'),('agentic/engine_v2/jarvis/conversation_tools.py','/opt/jarvis/conversation/jarvis/conversation_tools.py')]:
 a=(R/source).read_bytes();b=Path(target).read_bytes();r['source_hashes'].append({'source':source,'installed':target,'equal':a==b,'sha256':hashlib.sha256(b).hexdigest()})
for unit in ['jarvis-conversation','jarvis-host-bridge','jarvis-launcher3','jarvis-mission-worker','jarvis-mission-worker@2','jarvis-qwen-guard','jarvis-webui-tools','apache2']:
 r['services'][unit]=subprocess.check_output(['systemctl','show',unit,'-p','ActiveState','-p','MainPID','-p','ExecMainStartTimestamp'],text=True).strip()
# Compare existing chat payloads without exporting their titles, messages or IDs.
code="import sqlite3,json,hashlib;c=sqlite3.connect('/app/backend/data/webui.db');print(json.dumps({r[0]:hashlib.sha256(r[1].encode()).hexdigest() for r in c.execute('select id,chat from chat')}))"
now=json.loads(subprocess.check_output(['sudo','docker','exec','jarvis-open-webui','python','-c',code],text=True));old=sqlite3.connect('file:'+str(P/'webui.db')+'?mode=ro',uri=True);before={x[0]:hashlib.sha256(x[1].encode()).hexdigest() for x in old.execute('select id,chat from chat')};r['data_preserved']={'previous_chats':len(before),'total_chats_now':len(now),'all_previous_chat_payloads_identical':all(now.get(k)==v for k,v in before.items())};old.close()
# No download/removal/move of weights; profiles are not model weights.
old_catalog=json.loads(Path('/home/adminjarvis/JARVIS/audit-interconnexions-ia-private/models-before.json').read_text());r['model_catalogues_unchanged']={}
for name,host in [('Mac','127.0.0.1:11434'),('Dell1-main','192.168.1.75:11434'),('Dell1-missions','192.168.1.75:11435')]:
 current=json.load(urllib.request.urlopen('http://'+host+'/api/tags',timeout=8));key=lambda d:sorted((x['name'],x['digest'],x['size']) for x in d['models']);r['model_catalogues_unchanged'][name]=key(current)==key(old_catalog[name]['/api/tags'])
r['unit_files']={n:{'identical_to_installed':(R/'tools/optimisation_interconnexions'/n).read_bytes()==Path('/etc/systemd/system',n).read_bytes(),'exec_start':subprocess.check_output(['systemctl','show',n,'-p','ExecStart','--value'],text=True)} for n in ['jarvis-qwen-guard.service','jarvis-webui-tools.service']}
r['integration_hashes']={str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (R/'tools/optimisation_interconnexions').glob('*.py')}
(D/'VERIFICATION-INDEPENDANTE.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('Verification exported',r['data_preserved'],r['model_catalogues_unchanged'])
