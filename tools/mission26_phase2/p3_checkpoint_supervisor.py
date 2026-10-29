"""Bounded one-shot technical restart on actual JARVIS checkpoint request."""
import sys,json,time,subprocess,os
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.mission_store import MissionStore
s=MissionStore('/opt/jarvis/conversation');m='9e4a61d6faea4b73ad31251e72dcf7c1';units=['jarvis-mission-worker.service','jarvis-mission-worker@2.service']
def pids():
 return {u:subprocess.check_output(['systemctl','show',u,'-p','MainPID','--value'],text=True).strip() for u in units}
for _ in range(720):
 with s.db() as c:
  e=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND kind='context_restart_requested' ORDER BY id DESC LIMIT 1",(m,)).fetchone()
  done=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='codex_context_restart_executed'",(m,)).fetchone()
 if done:break
 if e and s.get(m)['state']=='interrupted':
  request=json.loads(e['result']);ref=request['checkpoint_reference']
  with s.db() as c:pending=c.execute("SELECT count(*) FROM tool_calls WHERE mission=? AND state='started'",(m,)).fetchone()[0]
  if pending:time.sleep(2);continue
  before=pids();result=subprocess.run(['sudo','-n','systemctl','restart',*units],capture_output=True,text=True,timeout=720)
  after=pids();ok=result.returncode==0 and all(int(after[u])>0 and after[u]!=before[u] for u in units)
  s.event(m,'codex_context_restart_executed',actor='Codex-supervisor',result={'request_event':e['id'],'checkpoint_reference':ref,'before':before,'after':after,'returncode':result.returncode,'ok':ok,'stderr':result.stderr[:1000],'no_model_restart':True,'no_human_approval':True})
  if ok:
   s.rebase_context(m,'Controlled worker restart from actual JARVIS checkpoint; resume checkpoint, do not replay effects',actor='Codex-supervisor')
   s.event(m,'coordinator_instruction',actor='Codex-supervisor',result={'instruction':f'Redémarrage technique des deuxworkers réussi ; reprends avec context_resume(reference={ref}), observe les compteurs conservés et le compteur distant égal1 sans rejouer son écriture. Puis poursuis contrôles indépendants et rapportP3. AucunP4 avant réception.'})
   s.transition(m,'queued',result={'reason':'Actual model-requested checkpoint restart complete','checkpoint_reference':ref})
  break
 if s.get(m)['state'] in ('completed','failed','cancelled'):break
 time.sleep(5)
else:s.event(m,'codex_restart_supervisor_expired',actor='Codex-supervisor',result={'duration_limit_seconds':3600,'no_restart_request_received':True})
