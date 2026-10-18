"""Durable execution with leases, immediate checkpoints and automatic continuation."""
import json
import threading
import time
import uuid
from .mission_store import MissionStore
from .durable_cycle import DurableCycle

class MissionInterrupted(RuntimeError):
    pass

class Missions:
    def __init__(self, core, root, start_worker=True):
        self.core = core
        self.store = MissionStore(root)
        self.path = self.store.path
        self.stop = threading.Event()
        self.owner = uuid.uuid4().hex
        self.cycle = DurableCycle(core, self.store)
        core.missions = self
        core.tools.mission_controller = self
        if start_worker:
            threading.Thread(target=self.worker, daemon=True, name='jarvis-missions-v2').start()
            threading.Thread(target=self.publisher, daemon=True, name='jarvis-publisher-v2').start()

    def connect(self):
        return self.store.db()

    def submit(self, goal, model, conversation=None, project='', spec=None):
        if not isinstance(goal, str) or not goal.strip() or len(goal) > self.core.config['max_text_chars']:
            raise ValueError('Objectif invalide')
        if model not in self.core.config['models']:
            raise ValueError('Modèle inconnu')
        conversation = conversation or self.core.memory.conversation(project)
        ident = self.store.create(goal, model, conversation, project, spec)
        return {'id': ident, 'mission_id': ident, 'conversation': conversation, 'state': 'queued'}

    def resume(self, ident):
        row = self.store.get(ident)
        if row['state'] in ('running', 'queued', 'completed'):
            raise ValueError('Mission déjà active ou terminée')
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
            except Exception: pass  # Worker survives DB contention; next poll retries persisted rows.

    def worker(self):
        while not self.stop.wait(1):
            if not self.core.lock.acquire(blocking=False):
                continue
            row = None
            done = threading.Event()
            try:
                row = self.store.claim(self.owner)
                if not row:
                    continue
                threading.Thread(target=self.heartbeat, args=(row['id'], done), daemon=True).start()
                if row.get('report_path'):
                    with self.store.db() as c:
                        pending=c.execute("SELECT count(*) FROM publication_outbox WHERE mission=? AND state!='verified'",(row['id'],)).fetchone()[0]
                    self.store.transition(row['id'],'publishing' if pending else 'completed',delay=10 if pending else 0)
                    continue
                result = self.cycle.run(row)
                tasks = self.store.tasks(row['id'])
                completed = bool(tasks) and all(t['state'] == 'validated' for t in tasks) and result.get('report')
                with self.store.db() as c:
                    pending=c.execute("SELECT count(*) FROM publication_outbox WHERE mission=? AND state!='verified'",(row['id'],)).fetchone()[0]
                if completed:
                    with self.store.db() as c:c.execute('UPDATE missions SET report_path=? WHERE id=?',(result['report']['path'],row['id']))
                state = ('publishing' if pending else 'completed') if completed else 'queued'
                self.store.transition(row['id'], state, result, delay=0 if result.get('progress') else 10,
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
                self.core.tools.context = {}
                self.core.tools.__dict__.pop('mission_store', None)
                self.core.lock.release()
