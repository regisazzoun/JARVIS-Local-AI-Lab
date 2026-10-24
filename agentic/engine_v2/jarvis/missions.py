"""Durable execution with leases, immediate checkpoints and automatic continuation."""
import json
import logging
from pathlib import Path
import threading
import time
import uuid
from .mission_store import MissionStore
from .durable_cycle import DurableCycle

class MissionInterrupted(RuntimeError):
    pass

class Missions:
    def __init__(self, core, root, start_worker=True, recover_exclusive=False, start_publisher=True):
        self.core = core
        self.store = MissionStore(root)
        if recover_exclusive:
            # server.main already owns runtime/application.lock: no old worker can remain.
            with self.store.db() as c:
                abandoned=[r['id'] for r in c.execute("SELECT id FROM missions WHERE state='running' AND origin!='legacy'")]
                for ident in abandoned:
                    c.execute("UPDATE missions SET state='queued',lease_owner=NULL,lease_until=NULL WHERE id=?",(ident,))
                    self.store.event(ident,'exclusive_restart_recovered',result={'basis':'Canonical process holds exclusive application flock; persisted work preserved'},connection=c)
        self.path = self.store.path
        self.stop = threading.Event()
        self.owner = uuid.uuid4().hex
        # A long durable task must not monopolize conversation/STT/TTS locks.
        from .core import Core
        self.execution_core=Core(dict(core.config),core.memory)
        self.execution_core.config['compute_role']='mission'
        self.execution_core.config['ollama_route']=core.config.get('mission_ollama_route',core.config.get('ollama_route',[]))
        self.execution_core.tools.root=core.tools.root
        self.execution_core.missions=self
        self.execution_core.tools.mission_controller=self
        self.cycle = DurableCycle(self.execution_core, self.store)
        core.missions = self
        core.tools.mission_controller = self
        if start_worker:
            threading.Thread(target=self.worker, daemon=True, name='jarvis-missions-v2').start()
            if start_publisher:threading.Thread(target=self.publisher, daemon=True, name='jarvis-publisher-v2').start()

    def connect(self):
        return self.store.db()

    def submit(self, goal, model, conversation=None, project='', spec=None):
        if not isinstance(goal, str) or not goal.strip() or len(goal) > self.core.config['max_text_chars']:
            raise ValueError('Objectif invalide')
        if model not in self.core.config['models']:
            raise ValueError('Modèle inconnu')
        if spec is not None and not isinstance(spec,dict):raise ValueError('spec doit être un objet')
        if conversation and conversation not in {r['id'] for r in self.core.memory.list_conversations()}:raise ValueError('Conversation absente')
        # New user goals use semantic/autonomous contracts by default.
        # Explicit historical task specs and persisted missions keep their mode.
        spec=dict(spec or {})
        if not spec.get('tasks'):
            spec.setdefault('autonomous',True)
            if spec.get('autonomous'): spec.setdefault('assurance',True)
        conversation = conversation or self.core.memory.conversation(project)
        ident = self.store.create(goal, model, conversation, project, spec)
        if (spec or {}).get('tasks'):
            self.store.plan(ident,spec['tasks'])
            self.store.transition(ident,'queued')
        self.core.memory.mission_message(ident,'goal',conversation,'user',goal,model)
        self.core.memory.mission_message(ident,'ack',conversation,'assistant','Mission durable enregistrée : '+ident,'JARVIS-engine')
        return {'id': ident, 'mission_id': ident, 'conversation': conversation, 'state': 'queued'}

    def resume(self, ident):
        row = self.store.get(ident)
        if row['state'] in ('running', 'queued', 'completed'):
            raise ValueError('Mission déjà active ou terminée')
        if row['state']=='waiting_external':
            self.store.rebase_context(ident,'Explicit external-dependency resume: rebuild working view from preserved proof ledger')
            self.store.event(ident,'external_dependency_recheck_requested',result={'basis':'Explicit resume requests a fresh observation; older blockers stay in history, no success inferred'})
        self.store.transition(ident, 'queued')
        return {'id': ident, 'state': 'queued'}

    def interrupt(self, ident):
        self.store.get(ident)
        self.store.transition(ident, 'interrupted')
        return {'id': ident, 'state': 'interrupted', 'note': 'La commande engagée peut se terminer ; arrêt avant le prochain outil.'}

    def is_interrupted(self, ident):
        return self.store.get(ident)['state'] == 'interrupted'

    def checkpoint(self, ident, tool, result):
        # Legacy chat path; V2 records intent + result in DurableCycle, not twice.
        if getattr(self.core.tools, 'mission_store', None) is self.store:
            return
        with self.store.db() as c:
            c.execute('INSERT INTO checkpoints(mission,tool,result,created) VALUES(?,?,?,?)',
                      (ident, tool, json.dumps(result, ensure_ascii=False), time.time()))

    def list(self):
        with self.store.db() as c:
            rows = [dict(r) for r in c.execute('SELECT * FROM missions ORDER BY updated DESC LIMIT 100')]
        for row in rows:
            tasks = self.store.tasks(row['id'])
            done = sum(t['state'] == 'validated' for t in tasks)
            row['tasks'] = tasks
            row['progress'] = {'validated': done, 'total': len(tasks), 'percent': round(done*100/len(tasks)) if tasks else None}
            row['checkpoints'] = []
        return rows

    def heartbeat(self, ident, finished):
        while not finished.wait(20):
            self.store.heartbeat(ident, self.owner)

    def publisher(self):
        from .publication import deliver_one
        while not self.stop.wait(2):
            try: deliver_one(self.store)
            except Exception: logging.exception('Persistent publisher retry after storage failure')

    def record_final(self,row):
        report=self.store.get(row['id']).get('report_path')
        if report:
            self.core.memory.mission_message(row['id'],'final',row['conversation'],'assistant',Path(report).read_text(),row['model'])

    def publish_progress(self,row):
        spec=json.loads(row['spec'])
        if not spec.get('progress_file') or not spec.get('publication'):return
        from .publication import invoke,enqueue
        publication=spec['publication'];relative=spec['progress_file']
        body='# État de mission\n\nGénéré par JARVIS-engine depuis les checkpoints réels. Les rapports sont rédigés par le modèle.\n\n| Tâche | État | Rapport vérifié |\n| --- | --- | --- |\n'
        for task in self.store.tasks(row['id']):
            body+='| '+task['id']+' — '+task['title'].replace('|','/')+' | '+task['state']+' | '+(task.get('report_sha256') or 'non reçu')+' |\n'
        body+='\nLes livraisons GitHub sont vérifiées séparément dans le Sandbox ; une tâche validée n’est pas une affirmation de livraison distante.\n'
        path=str(Path(publication['workspace'])/relative)
        invoke('host_write_file',{'path':path,'content':body})
        confirmed=invoke('host_read_file',{'path':path})['stdout']
        if body!=confirmed:raise ValueError('ETAT local non confirmé')
        enqueue(self.store,row['id'],None,{**publication,'file':relative},verified_body=body)

    def recover_final_report(self,row):
        """Recover the crash window after the durable final-tool receipt."""
        import hashlib
        from .tools import validate_final_report
        from .mission_assurance import enabled, closure_state
        if enabled(self.store,row['id']) and not closure_state(self.store,row['id'])['final_allowed']:return
        tasks=self.store.tasks(row['id'])
        if row.get('report_path') or not tasks or any(t['state']!='validated' for t in tasks):return
        with self.store.db() as c:
            revision=c.execute("SELECT coalesce(max(created),0) FROM mission_events WHERE mission=? AND kind='final_report_revision_requested'",(row['id'],)).fetchone()[0]
            since=max(revision,max(t['updated'] for t in tasks))
            calls=c.execute("SELECT id,result FROM tool_calls WHERE mission=? AND tool='intervention_report' AND state='finished' AND created>=? ORDER BY created DESC",(row['id'],since)).fetchall()
        for call in calls:
            receipt=json.loads(call['result'] or '{}')
            if not receipt.get('ok'):continue
            report=receipt.get('result',{})
            expected=self.store.root/'runtime/reports'/row['id']/'RAPPORT-FINAL.md'
            try:
                if Path(report.get('path','')).resolve()!=expected.resolve():return
                body=expected.read_bytes()
                if hashlib.sha256(body).hexdigest()!=report.get('sha256'):return
                validate_final_report(body.decode(),json.loads(row['spec']))
            except (OSError,ValueError,UnicodeError):return
            with self.store.db() as c:
                c.execute('UPDATE missions SET report_path=? WHERE id=?',(str(expected),row['id']))
                self.store.event(row['id'],'final_report_recovered',result={'invocation':call['id'],'path':str(expected),'sha256':report['sha256'],'basis':'durable successful tool receipt and unchanged file; all tasks validated'},connection=c)
            row['report_path']=str(expected)
            return

    def worker(self):
        while not self.stop.wait(1):
            if not self.execution_core.lock.acquire(blocking=False):
                continue
            row = None
            done = threading.Event()
            try:
                row = self.store.claim(self.owner)
                if not row:
                    continue
                threading.Thread(target=self.heartbeat, args=(row['id'], done), daemon=True).start()
                self.recover_final_report(row)
                if row.get('report_path'):
                    with self.store.db() as c:
                        pending=c.execute("SELECT count(*) FROM publication_outbox WHERE mission=? AND state NOT IN ('verified','superseded')",(row['id'],)).fetchone()[0]
                    if not pending:self.record_final(row)
                    self.store.transition(row['id'],'publishing' if pending else 'completed',delay=10 if pending else 0)
                    continue
                if self.defer_waiting_tasks(row):continue
                result = self.cycle.run(row)
                tasks = self.store.tasks(row['id'])
                if result.get('progress'):self.publish_progress(row)
                if result.get('external_block'):continue
                completed = bool(tasks) and all(t['state'] == 'validated' for t in tasks) and result.get('report')
                with self.store.db() as c:
                    pending=c.execute("SELECT count(*) FROM publication_outbox WHERE mission=? AND state NOT IN ('verified','superseded')",(row['id'],)).fetchone()[0]
                if completed:
                    with self.store.db() as c:c.execute('UPDATE missions SET report_path=? WHERE id=?',(result['report']['path'],row['id']))
                state = ('publishing' if pending else 'completed') if completed else 'queued'
                if not result.get('progress') and state=='queued':
                    with self.store.db() as c:
                        c.execute('UPDATE missions SET stagnant_cycles=stagnant_cycles+1 WHERE id=?',(row['id'],))
                        stagnant=c.execute('SELECT stagnant_cycles FROM missions WHERE id=?',(row['id'],)).fetchone()[0]
                    if stagnant>=3:
                        state='blocked'
                        result['blockage']='Trois cycles sans nouvelle observation utile ; reprise technique automatique après attente, sans nouvelle validation humaine.'
                if state=='completed':self.record_final(row)
                self.store.transition(row['id'], state, result, delay=60 if state=='blocked' else 0 if result.get('progress') else 10,
                                      progress=bool(result.get('progress')))
            except MissionInterrupted:
                if row: self.store.transition(row['id'], 'interrupted')
            except Exception as exc:
                if row:
                    # No fixed attempt limit: a recoverable transport failure retains all work.
                    self.store.event(row['id'], 'cycle_error', result={'error': str(exc), 'type': type(exc).__name__})
                    self.store.transition(row['id'], 'retrying', {'error': str(exc)}, delay=min(60, 2**min(row['attempts'], 6)))
            finally:
                done.set()
                self.execution_core.tools.context = {}
                self.execution_core.tools.__dict__.pop('mission_store', None)
                self.execution_core.lock.release()

    def defer_waiting_tasks(self,row):
        """A dependency wait is not an invitation to invent a new executable task."""
        tasks=self.store.tasks(row['id'])
        if not any(t['state']=='waiting_external' for t in tasks) or self.store.ready(row['id']):return False
        from .mission_assurance import enabled,coverage_state
        if enabled(self.store,row['id']) and not coverage_state(self.store,row['id'])['accepted']:return False
        pending=[{'id':t['id'],'state':t['state']} for t in tasks if t['state']!='validated']
        result={'reason':'No executable task; retain dependency checkpoint instead of invoking the model',
                'pending':pending,'human_approval_required':False}
        self.store.event(row['id'],'execution_deferred_no_ready_task',result=result)
        self.store.transition(row['id'],'waiting_external',result)
        return True
