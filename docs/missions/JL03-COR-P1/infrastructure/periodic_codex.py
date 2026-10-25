"""Bounded periodic Codex coordinator; JARVIS execution stays in canonical engine."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

PRIVATE = Path('/home/adminjarvis/JARVIS/jl03-cor-p1-private/supervision')
REGISTER = Path('/var/lib/jarvis/projects/jl03-cor-p1/REGISTRE-CODEX.json')
ROOT = '/opt/jarvis/conversation'
REPO = '/home/adminjarvis/JARVIS/jl03-cor-p1'


def main():
    os.umask(0o077)
    PRIVATE.mkdir(exist_ok=True, mode=0o700)
    with (PRIVATE/'coordinator.lock').open('a') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: return
        sys.path.insert(0, ROOT)
        from jarvis.mission_store import MissionStore
        store = MissionStore(ROOT)
        tasks = json.loads(REGISTER.read_text())['tasks']
        attention = []
        for task in tasks:
            if task['id'] not in ('D03','D04','D17'): continue
            mission = store.get(task['mission_id'])
            state = mission['state']
            stopped = state in ('interrupted','failed','waiting_external')
            review = state == 'completed' and not task.get('validated') and not task.get('technical_review_recorded')
            stalled = state in ('queued','running') and time.time() - mission['last_progress'] > 900
            # Let the explicit one-shot dispatcher consume an already reviewed repair.
            if task.get('corrective_resume',{}).get('armed'): continue
            if not (stopped or review or stalled): continue
            plans = store.plans(mission['id'])
            attention.append({'task':task['id'],'mission':mission['id'],'state':state,
                              'result':json.loads(mission.get('result') or '{}'),
                              'plan_version':plans[-1]['version'] if plans else 0})
        statefile = PRIVATE/'STATE.json'
        saved = json.loads(statefile.read_text()) if statefile.exists() else {'attempts':{}}
        if not attention:
            saved.update(checked_at=time.time(),status='WATCHING_NO_INTERVENTION_NEEDED')
            statefile.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
            print('Watching: native work progressing or reviewed resume already queued.')
            return
        key = hashlib.sha256(json.dumps(attention,sort_keys=True).encode()).hexdigest()
        tries = saved.setdefault('attempts',{}).get(key,0)
        if tries >= 3:
            saved.update(checked_at=time.time(),status='COORDINATOR_BOUNDED_STOP',unresolved=attention)
            statefile.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
            print('Same coordination condition unresolved after3 passages; dossier retained, no fourth blind retry.')
            return
        saved['attempts'][key] = tries+1
        saved.update(started_at=time.time(),status='CODEX_COORDINATING',attention=attention)
        statefile.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
        stamp = str(time.time_ns());output=PRIVATE/(stamp+'-summary.md');log=PRIVATE/(stamp+'-private.log')
        prompt=(PRIVATE/'PROMPT.md').read_text()+'\nÉTAT CIBLÉ OBSERVÉ PAR LE WATCHDOG :\n'+json.dumps(attention,ensure_ascii=False)+'\nPassage borné '+str(tries+1)+'/3 pour cet état. Une répétition inchangée ne corrige rien.'
        cmd=['/home/adminjarvis/.local/bin/codex','-a','never','exec','-s','danger-full-access','-C',REPO,
             '--ephemeral','--color','never','-o',str(output),'-']
        for row in attention:store.event(row['mission'],'coordinator_periodic_started',task=row['task'],actor='Codex-periodic',result={'attempt':tries+1,'summary_path':str(output),'scope':'One targeted coordination intervention, JARVIS retains execution'})
        with log.open('w') as stream:
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=stream,stderr=subprocess.STDOUT,text=True,start_new_session=True)
            try: proc.communicate(prompt,timeout=420);rc=proc.returncode
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGTERM)
                try:proc.wait(timeout=10)
                except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                rc=124
        saved.update(finished_at=time.time(),status='PASSAGE_FINISHED' if rc==0 else 'PASSAGE_FAILED',returncode=rc,summary_path=str(output))
        statefile.write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n')
        for row in attention:store.event(row['mission'],'coordinator_periodic_finished',task=row['task'],actor='Codex-periodic',result={'returncode':rc,'summary_path':str(output),'not_acceptance':True})
        print(json.dumps({'returncode':rc,'summary':str(output)}))


if __name__ == '__main__': main()
