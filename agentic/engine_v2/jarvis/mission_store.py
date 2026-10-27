"""Transactional mission journal, in the existing mission database (not a memory clone)."""
from contextlib import contextmanager
from pathlib import Path
import hashlib
import json
import re
import sqlite3
import time
import uuid


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def signature(tool, arguments):
    return hashlib.sha256((tool + encoded(arguments)).encode()).hexdigest()


def arguments_match(actual, expected):
    def normalized(key,value):
        if key=='command' and isinstance(value,str):return re.sub(r'\s+2>&1\s*$','',value).strip()
        return value
    def matches(key,value):
        if key=='files':
            try:
                wanted=json.loads(value) if isinstance(value,str) else value
                supplied=actual.get(key,[]);supplied=json.loads(supplied) if isinstance(supplied,str) else supplied
                return isinstance(wanted,list) and isinstance(supplied,list) and set(wanted)<=set(supplied)
            except (ValueError,TypeError):return False
        return normalized(key,actual.get(key))==normalized(key,value)
    return all(matches(k,v) for k,v in expected.items())


class MissionStore:
    def attempt_ledger(self, mission):
        from .attempt_ledger import AttemptLedger
        return AttemptLedger(self, mission)

    def attempt_state(self, mission, state, reference=None, connection=None):
        if state not in (
            'PENDING', 'DISPATCHED', 'RUNNING', 'NOT_EXECUTED',
            'EXECUTION_FAILED', 'EXECUTED_TEST_FAILED', 'VALIDATION_INCONCLUSIVE',
            'SUCCESS', 'BLOCKED', 'ESCALATED'
        ):
            raise ValueError(f"Invalid attempt state: {state}")
        if state == 'SUCCESS':
            if reference is None:
                raise ValueError("SUCCESS attempt must include a reference to an observed event")
            if not isinstance(reference, int):
                raise ValueError("SUCCESS reference must be an integer event ID")
            with self.db() as db:
                row = db.execute("SELECT kind,tool,result FROM mission_events WHERE mission=? AND id=?", (mission, reference)).fetchone()
            if row is None:
                raise ValueError("SUCCESS reference not found in the same mission")
            observation = json.loads(row['result'])
            if row['kind'] == 'authority_execution':
                execution = observation.get('execution', {})
            elif row['kind'] == 'tool_finished' and row['tool'] == 'host_remote' and observation.get('ok') is True:
                payload = observation.get('result', {})
                execution = payload.get('execution', payload)
                if payload.get('returncode', 0) != 0:
                    raise ValueError("SUCCESS reference has a failed transport")
            else:
                raise ValueError("SUCCESS requires an observed execution, not a plan")
            code = execution.get('returncode')
            if type(code) is not int or code != 0:
                raise ValueError("SUCCESS requires an observed successful child process")
        if reference is not None:
            result = {"state": state, "reference": str(reference)}
        else:
            result = {"state": state}
        return self.event(
            mission, 'ATTEMPT_STATE', task=None, actor='JARVIS-engine',
            tool='mission_store', arguments={}, result=result,
            duration=None, invocation=None, connection=connection
        )

    def __init__(self, root):
        self.root = Path(root)
        self.path = self.root / 'runtime/missions.sqlite'
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.db() as c:
            c.execute('PRAGMA journal_mode=WAL')
            c.executescript('''
            CREATE TABLE IF NOT EXISTS missions(id TEXT PRIMARY KEY,goal TEXT,model TEXT,state TEXT,conversation TEXT,attempts INTEGER DEFAULT 0,result TEXT,updated REAL);
            CREATE TABLE IF NOT EXISTS checkpoints(id INTEGER PRIMARY KEY,mission TEXT,tool TEXT,result TEXT,created REAL);
            CREATE TABLE IF NOT EXISTS tasks(mission TEXT,id TEXT,title TEXT,deps TEXT,state TEXT,evidence TEXT,updated REAL,PRIMARY KEY(mission,id));
            CREATE TABLE IF NOT EXISTS procedures(id INTEGER PRIMARY KEY,title TEXT,content TEXT,evidence TEXT,created REAL);
            CREATE TABLE IF NOT EXISTS mission_events(id INTEGER PRIMARY KEY AUTOINCREMENT,mission TEXT NOT NULL,task TEXT,actor TEXT NOT NULL,kind TEXT NOT NULL,tool TEXT,arguments TEXT,result TEXT,created REAL NOT NULL,duration REAL,invocation TEXT);
            CREATE INDEX IF NOT EXISTS mission_event_cursor ON mission_events(mission,id);
            CREATE TABLE IF NOT EXISTS tool_calls(id TEXT PRIMARY KEY,mission TEXT NOT NULL,task TEXT,signature TEXT NOT NULL,tool TEXT NOT NULL,arguments TEXT NOT NULL,state TEXT NOT NULL,result TEXT,created REAL,updated REAL);
            CREATE INDEX IF NOT EXISTS mission_call_lookup ON tool_calls(mission,task,signature,state);
            CREATE TABLE IF NOT EXISTS mission_plans(mission TEXT,version INTEGER,author TEXT,reason TEXT,plan TEXT,sha256 TEXT,created REAL,PRIMARY KEY(mission,version));
            CREATE TABLE IF NOT EXISTS mission_context(mission TEXT PRIMARY KEY,task TEXT,messages TEXT,updated REAL);
            CREATE TABLE IF NOT EXISTS mission_context_archives(id INTEGER PRIMARY KEY,mission TEXT,task TEXT,messages TEXT,reason TEXT,created REAL);
            CREATE TABLE IF NOT EXISTS publication_outbox(id TEXT PRIMARY KEY,mission TEXT,task TEXT,repository TEXT,branch TEXT,workspace TEXT,file TEXT,sha256 TEXT,state TEXT,attempts INTEGER DEFAULT 0,next_run REAL DEFAULT 0,last_error TEXT,commit_sha TEXT,updated REAL);
            ''')
            for table, columns in {
                'missions': {'project': "TEXT DEFAULT ''", 'created': 'REAL', 'next_run': 'REAL DEFAULT 0',
                             'lease_owner': 'TEXT', 'lease_until': 'REAL', 'last_progress': 'REAL',
                             'stagnant_cycles': 'INTEGER DEFAULT 0', 'report_path': 'TEXT',
                             'spec': "TEXT DEFAULT '{}'", 'active_task': 'TEXT', 'origin': "TEXT DEFAULT 'legacy'"},
                'tasks': {'objective': 'TEXT', 'contract': "TEXT DEFAULT '{}'", 'started': 'REAL',
                          'attempts': 'INTEGER DEFAULT 0', 'last_error': 'TEXT', 'artifact': 'TEXT',
                          'report_sha256': 'TEXT', 'stage': "TEXT DEFAULT 'execute'"}
            }.items():
                present = {r['name'] for r in c.execute('PRAGMA table_info(' + table + ')')}
                for name, declaration in columns.items():
                    if name not in present:
                        c.execute('ALTER TABLE ' + table + ' ADD COLUMN ' + name + ' ' + declaration)
            c.execute('UPDATE missions SET created=coalesce(created,updated),last_progress=coalesce(last_progress,updated)')

    @contextmanager
    def db(self):
        c = sqlite3.connect(self.path, timeout=30)
        c.row_factory = sqlite3.Row
        c.execute('PRAGMA foreign_keys=ON')
        c.execute('PRAGMA synchronous=FULL')
        try:
            with c:
                yield c
        finally:
            c.close()

    def event(self, mission, kind, task=None, actor='JARVIS-engine', tool=None, arguments=None, result=None, duration=None, invocation=None, connection=None):
        values = (mission, task, actor, kind, tool, encoded(arguments or {}), encoded(result or {}), time.time(), duration, invocation)
        query = 'INSERT INTO mission_events(mission,task,actor,kind,tool,arguments,result,created,duration,invocation) VALUES(?,?,?,?,?,?,?,?,?,?)'
        if connection is not None:
            return connection.execute(query, values).lastrowid
        with self.db() as c:
            return c.execute(query, values).lastrowid

    def create(self, goal, model, conversation, project='', spec=None, origin='conversation'):
        ident = uuid.uuid4().hex
        now = time.time()
        with self.db() as c:
            c.execute('INSERT INTO missions(id,goal,model,state,conversation,updated,created,last_progress,project,spec,origin) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                      (ident, goal, model, 'draft' if (spec or {}).get('tasks') else 'queued', conversation, now, now, now, project, encoded(spec or {}), origin))
            self.event(ident, 'mission_created', result={'origin': origin}, connection=c)
        return ident

    def get(self, ident):
        with self.db() as c:
            row = c.execute('SELECT * FROM missions WHERE id=?', (ident,)).fetchone()
            if not row:
                raise ValueError('Mission absente')
            return dict(row)

    def tasks(self, ident):
        with self.db() as c:
            result = []
            for row in c.execute('SELECT * FROM tasks WHERE mission=? ORDER BY rowid', (ident,)):
                d = dict(row)
                for k in ('deps', 'evidence', 'contract'):
                    d[k] = json.loads(d[k] or ('{}' if k == 'contract' else '[]'))
                result.append(d)
            return result

    def plan(self, ident, tasks, author="operator", metadata=None, reason="initial plan", expected_version=None, append=False, patch=False):
        if isinstance(tasks, str):
            tasks = json.loads(tasks)
        if not isinstance(tasks, list) or not tasks:
            raise ValueError('Plan non vide requis')
        if append and patch:raise ValueError('Choose append or patch, not both')
        if append or patch:
            history=self.plans(ident)
            if not history:raise ValueError('append requires an existing plan')
            saved=history[-1]['plan']
            existing_ids={t['id'] for t in saved['tasks']}
            if append:
                if any(t.get('id') in existing_ids for t in tasks):
                    raise ValueError('append accepts only NEW task ids; use patch:true to update existing pending tasks without resending received tasks')
                tasks=saved['tasks']+tasks
            else:
                if any(t.get('id') not in existing_ids for t in tasks):
                    raise ValueError('patch requires existing ids; use append:true for new tasks')
                if len({t['id'] for t in tasks})!=len(tasks):raise ValueError('Duplicate patch task ids')
                replacements={t['id']:t for t in tasks}
                tasks=[replacements.get(t['id'],t) for t in saved['tasks']]
            metadata=metadata or {k:v for k,v in saved.items() if k!='tasks'}
        normalized = []
        resource_objective=json.loads(self.get(ident)['spec']).get('context_result_objective')
        received={t['id'] for t in self.tasks(ident) if t['state']=='validated'}
        for t in tasks:
            if not isinstance(t, dict) or not isinstance(t.get('id'), str) or not isinstance(t.get('title'), str):
                raise ValueError('Chaque tâche exige id et title textuels')
            deps = t.get('depends', t.get('deps', []))
            if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps):
                raise ValueError('depends doit être une liste d’identifiants')
            item={**t, 'depends': deps}
            if resource_objective and t['id'] not in received:
                item['contract']={**t.get('contract',{}),'context_result_objective':resource_objective}
            normalized.append(item)
        mapping = {t['id']: t for t in normalized}
        if len(mapping) != len(normalized):
            raise ValueError('Identifiants dupliqués')
        visited = set()
        def visit(ident, chain):
            if ident in chain or ident not in mapping:
                raise ValueError('Dépendance cyclique ou absente')
            if ident in visited:
                return
            for dep in mapping[ident]['depends']:
                visit(dep, chain | {ident})
            visited.add(ident)
        for key in mapping:
            visit(key, set())
        strict = json.loads(self.get(ident)['spec']).get('autonomous', False)
        metadata = metadata or {}
        if strict:
            for field in ('objective', 'success_criteria', 'artifacts', 'stop_conditions'):
                if not metadata.get(field):
                    raise ValueError('Autonomous plan metadata required: '+field)
            for t in normalized:
                if not t.get('contract',{}).get('semantic') or not t.get('contract',{}).get('report_path'):
                    raise ValueError('Autonomous task '+t['id']+' requires contract.report_path and nonempty contract.semantic')
                from .verification import validate_contract, validate_report_source
                contract_errors=[]
                for candidate in normalized:
                    for criterion in candidate.get('contract',{}).get('semantic',[]):
                        try:
                            validate_contract(criterion)
                            validate_report_source(candidate,criterion)
                        except ValueError as exc:contract_errors.append('Task '+candidate['id']+': '+str(exc))
                if contract_errors:raise ValueError(' | '.join(contract_errors)+'. Active examples in mission_plan schema and mission_progress; source={tool:host_read_file,arguments:{path:...}}, JSON expected/types keys start with /; CSV uses text equals; hash manifest uses digest with baseline_source, free prose uses kind report with broker read source (no predetermined hash). No plan saved; current version unchanged.')
                for field in ('objective', 'tools', 'observations', 'verification', 'recovery', 'artifacts'):
                    if not t.get(field):
                        raise ValueError('Task '+t['id']+' requires '+field)
        document = {**metadata, 'tasks': normalized}
        text = encoded(document)
        sha = hashlib.sha256(text.encode()).hexdigest()
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            latest = c.execute('SELECT * FROM mission_plans WHERE mission=? ORDER BY version DESC LIMIT 1', (ident,)).fetchone()
            version = latest['version'] if latest else 0
            if latest and latest['sha256'] == sha:
                return self.tasks(ident)
            existing = self.tasks(ident)
            if existing and expected_version is None:
                if not strict:
                    return existing
                raise ValueError('Revision requires expected_version and reason; inspect mission_progress')
            if expected_version is not None and expected_version != version:
                raise ValueError('Stale plan version: expected_version must equal CURRENT saved version '+str(version)+'; received '+str(expected_version)+'. Next version '+str(version+1)+' is assigned automatically. Failed proposals do not increment version.')
            if existing and not reason.strip():
                raise ValueError('Revision reason required')
            old = {t['id']: t for t in existing}
            previous = {t['id']: t for t in json.loads(latest['plan'])['tasks']} if latest else {}
            # Acceptance predicates cannot disappear in a revision; add checks or
            # fix implementation instead. Owner criteria also survive replanning.
            required = json.loads(self.get(ident)['spec']).get('acceptance', [])
            semantic = [x for t in normalized for x in t.get('contract',{}).get('semantic',[])]
            from .verification import exact
            for requirement in required:
                if not any(exact(requirement, x) for x in semantic):
                    raise ValueError('Plan must cover owner acceptance predicate: '+encoded(requirement))
            for key, t in old.items():
                # A not-yet-attempted 26B candidate may contain a validly shaped
                # but incorrect criterion. Its new coverage audit must run before
                # any effect. Owner predicates and received tasks remain immutable.
                unattempted_candidate=(json.loads(self.get(ident)['spec']).get('assurance') and t['state']=='pending' and not self.observations(ident,key))
                if key in mapping and not unattempted_candidate:
                    for check in t.get('contract',{}).get('semantic',[]):
                        from .verification import validate_contract, validate_report_source
                        try:
                            validate_contract(check)
                            validate_report_source(previous.get(key,{}),check)
                        except ValueError:continue  # Repair an unexecutable historical declaration; never drop valid acceptance.
                        if not any(exact(check,x) for x in mapping[key].get('contract',{}).get('semantic',[])):
                            results=[e['result'].get('status') for e in self.events(ident,limit=1000000) if e['task']==key and e['kind']=='semantic_verification' and exact(e['result'].get('contract'),check)]
                            failed_candidate=(json.loads(self.get(ident)['spec']).get('assurance') and results and results[-1]=='FAIL' and 'PASS' not in results and t['state']!='validated')
                            if not failed_candidate:raise ValueError('Cannot weaken existing semantic contract: '+key)
                            self.event(ident,'failed_criterion_revision_proposed',key,author,result={'previous_contract':check,'reason':reason,'never_passed':True,'new_coverage_review_required':True,'owner_predicates_preserved':True},connection=c)
                if t['state'] == 'validated' and (key not in mapping or (key in previous and mapping[key] != previous[key])):
                    raise ValueError('Validated task immutable: '+key+'. Copy it exactly from mission_progress or use append:true with NEW tasks only; existing tasks and metadata are retained automatically.')
                if key not in mapping and self.observations(ident, key):
                    raise ValueError('Cannot remove an attempted task; revise it preserving evidence: '+key)
            for key in old.keys() - mapping.keys():
                c.execute('DELETE FROM tasks WHERE mission=? AND id=?', (ident, key))
            for t in normalized:
                if t['id'] in old:
                    if old[t['id']]['state'] != 'validated':
                        c.execute('UPDATE tasks SET title=?,deps=?,objective=?,contract=?,updated=? WHERE mission=? AND id=?',
                                  (t['title'], encoded(t['depends']), t.get('objective',t['title']), encoded(t.get('contract',{})), time.time(), ident, t['id']))
                    continue
                c.execute('INSERT INTO tasks(mission,id,title,deps,state,evidence,updated,objective,contract) VALUES(?,?,?,?,?,?,?,?,?)',
                          (ident, t['id'], t['title'], encoded(t['depends']), 'pending', '[]', time.time(), t.get('objective', t['title']), encoded(t.get('contract', {}))))
            c.execute('INSERT INTO mission_plans VALUES(?,?,?,?,?,?,?)', (ident, version+1, author, reason, text, sha, time.time()))
            self.event(ident, 'plan_revised' if version else 'plan_saved', actor=author, result={'tasks': len(normalized), 'version':version+1,'sha256':sha,'reason':reason}, connection=c)
        return self.tasks(ident)

    def plans(self, ident):
        with self.db() as c:
            return [{**dict(r), 'plan': json.loads(r['plan'])} for r in c.execute('SELECT * FROM mission_plans WHERE mission=? ORDER BY version', (ident,))]

    def ready(self, ident):
        from .mission_assurance import enabled, coverage_state
        if enabled(self, ident) and not coverage_state(self, ident)['accepted']: return []
        tasks = self.tasks(ident)
        done = {t['id'] for t in tasks if t['state'] == 'validated'}
        return [t for t in tasks if t['state'] in ('pending', 'running', 'retrying', 'blocked') and set(t['deps']) <= done]

    def claim(self, owner, lease_seconds=120):
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            now = time.time()
            c.execute("UPDATE missions SET state='queued',lease_owner=NULL WHERE state='running' AND origin!='legacy' AND coalesce(lease_until,0)<?", (now,))
            row = c.execute("SELECT * FROM missions WHERE (state IN ('queued','retrying','publishing') OR (state='blocked' AND origin!='legacy')) AND coalesce(next_run,0)<=? ORDER BY updated LIMIT 1", (now,)).fetchone()
            if not row:
                return None
            c.execute("UPDATE missions SET state='running',attempts=attempts+1,lease_owner=?,lease_until=?,updated=? WHERE id=?",
                      (owner, now + lease_seconds, now, row['id']))
            self.event(row['id'], 'cycle_started', result={'attempt': row['attempts'] + 1}, connection=c)
            return dict(c.execute('SELECT * FROM missions WHERE id=?', (row['id'],)).fetchone())

    def heartbeat(self, ident, owner, lease_seconds=120):
        with self.db() as c:
            c.execute('UPDATE missions SET lease_until=? WHERE id=? AND lease_owner=? AND state=?',
                      (time.time() + lease_seconds, ident, owner, 'running'))

    def transition(self, ident, state, result=None, delay=0, progress=False):
        with self.db() as c:
            current = c.execute('SELECT state FROM missions WHERE id=?', (ident,)).fetchone()
            if not current:
                raise ValueError('Mission absente')
            if current['state'] == 'interrupted' and state != 'queued':
                return
            c.execute('UPDATE missions SET state=?,result=?,updated=?,next_run=?,lease_owner=NULL,lease_until=NULL WHERE id=?',
                      (state, encoded(result or {}), time.time(), time.time() + delay, ident))
            if progress:
                c.execute('UPDATE missions SET last_progress=?,stagnant_cycles=0 WHERE id=?', (time.time(), ident))
            self.event(ident, 'state_changed', result={'state': state, 'delay': delay}, connection=c)

    def begin_call(self, ident, task, tool, arguments):
        token = uuid.uuid4().hex
        now = time.time()
        with self.db() as c:
            c.execute('INSERT INTO tool_calls VALUES(?,?,?,?,?,?,?,?,?,?)',
                      (token, ident, task, signature(tool, arguments), tool, encoded(arguments), 'started', None, now, now))
            self.event(ident, 'tool_started', task, 'JARVIS', tool, arguments, invocation=token, connection=c)
        return token

    def finish_call(self, token, result, duration):
        with self.db() as c:
            row = c.execute('SELECT * FROM tool_calls WHERE id=?', (token,)).fetchone()
            c.execute('UPDATE tool_calls SET state=?,result=?,updated=? WHERE id=?', ('finished', encoded(result), time.time(), token))
            c.execute('INSERT INTO checkpoints(mission,tool,result,created) VALUES(?,?,?,?)', (row['mission'], row['tool'], encoded(result), time.time()))
            observation = self.event(row['mission'], 'tool_finished', row['task'], 'JARVIS', row['tool'], json.loads(row['arguments']), result, duration, token, c)
            # Codex-periodic: classify an observed failed child, never broker success.
            if row['tool'] == 'host_remote' and result.get('ok') is True:
                payload = result.get('result', {})
                execution = payload.get('execution', payload) if isinstance(payload, dict) else {}
                code = execution.get('returncode') if isinstance(execution, dict) else None
                if type(code) is int and code != 0:
                    self.attempt_state(row['mission'], 'EXECUTION_FAILED', reference=observation, connection=c)
            c.execute('UPDATE missions SET updated=?,last_progress=? WHERE id=?', (time.time(), time.time(), row['mission']))

    def observations(self, ident, task=None, limit=None):
        with self.db() as c:
            query = 'SELECT * FROM tool_calls WHERE mission=?'
            params = [ident]
            if task is not None:
                query += ' AND task=?'
                params.append(task)
            if limit is not None:
                if type(limit) is not int or limit<1:raise ValueError('Positive observation limit required')
                query+=' ORDER BY created DESC,rowid DESC LIMIT ?';params.append(limit)
            else:query+=' ORDER BY created,rowid'
            rows=list(c.execute(query,params))
            if limit is not None:rows.reverse()
            return [{**dict(r), 'arguments': json.loads(r['arguments'] or '{}'), 'result': json.loads(r['result'] or '{}') if r['result'] else None} for r in rows]

    def events(self, ident, after=0, limit=150):
        with self.db() as c:
            rows = [dict(r) for r in c.execute('SELECT * FROM mission_events WHERE mission=? AND id>? ORDER BY id LIMIT ?', (ident, after, limit))]
        for r in rows:
            r['arguments'] = json.loads(r['arguments'] or '{}')
            r['result'] = json.loads(r['result'] or '{}')
        return rows

    def contract_status(self, ident, task_id):
        task=next((t for t in self.tasks(ident) if t['id']==task_id),None)
        if not task:return {}
        observations=self.observations(ident,task_id)
        contract=task.get('contract',{})
        checks=contract.get('checks',[])+[{'tool':t} for t in contract.get('required_tools',[])]
        status=[]
        for check in checks:
            matches=[]
            for item in observations:
                result=item['result'] or {};args=item['arguments']
                if item['tool'] not in (check.get('tools') or [check['tool']]) or result.get('ok')!=check.get('ok',True):continue
                if check.get('action') and args.get('action')!=check['action']:continue
                if not arguments_match(args,check.get('arguments',{})):continue
                if check.get('stdout_contains') and check['stdout_contains'] not in result.get('result',{}).get('stdout',''):continue
                if any(result.get('result',{}).get(k)!=v for k,v in check.get('result_fields',{}).items()):continue
                if any(text in result.get('result',{}).get('stdout','') for text in check.get('stdout_not_contains',[])):continue
                matches.append(item['id'])
            latest=next((o for o in reversed(observations) if o['id'] in matches),None)
            fact={'created':latest['created'],'stdout':str((latest.get('result') or {}).get('result',{}).get('stdout',''))[:700]} if latest else None
            status.append({'latest_verified_fact':fact,'check':check,'satisfied':len(matches)>=check.get('minimum',1),'matching_count':len(matches),'invocations':matches[-3:]})
        path=contract.get('report_path')
        from .verification import exact
        semantic=[]
        events=[e for e in self.events(ident,limit=1000000) if e['task']==task_id and e['kind']=='semantic_verification']
        for criterion in contract.get('semantic',[]):
            matches=[e for e in events if exact(e['result'].get('contract'),criterion)]
            latest=matches[-1] if matches else None
            parent=next((o for o in reversed(observations) if latest and o['tool']=='mission_verify' and (o['result'] or {}).get('ok') and (o['result'] or {}).get('result',{}).get('verification_event')==latest['id']),None)
            semantic.append({'contract':criterion,'status':latest['result'].get('status') if latest else 'INSUFFICIENT','event':latest['id'] if latest else None,'invocation_id':parent['id'] if parent else None,'freshness':'Rechecked at task completion; mutations after observation require another read'})
        satisfied=all(s['satisfied'] for s in status) and all(s['status']=='PASS' for s in semantic)
        written=any(o['tool']=='host_write_file' and o['arguments'].get('path')==path and (o['result'] or {}).get('ok') for o in observations)
        read=any(o['tool']=='host_read_file' and o['arguments'].get('path')==path and (o['result'] or {}).get('ok') for o in observations)
        result={'requirements':status,'semantic':semantic,'all_satisfied':satisfied,'report_path':path,'report_written':written,'report_read':read}
        ids={item['invocation_id'] for item in semantic if item.get('invocation_id')}
        parent=next((o for o in reversed(observations) if o['id'] in ids),None)
        if satisfied and written and read and parent:
            result['completion_candidate']={'id':task_id,'report_path':path,'evidence_id':parent['id']}
            result['next_action']='Call mission_task_complete with completion_candidate. It still checks current evidence and rereads the report; this is not automatic validation.'
        return result

    def rebase_context(self, ident, reason, actor='JARVIS-engine'):
        with self.db() as c:
            row=c.execute('SELECT * FROM mission_context WHERE mission=?',(ident,)).fetchone()
            if not row:return False
            c.execute('INSERT INTO mission_context_archives(mission,task,messages,reason,created) VALUES(?,?,?,?,?)',(ident,row['task'],row['messages'],reason,time.time()))
            c.execute('DELETE FROM mission_context WHERE mission=?',(ident,))
            self.event(ident,'working_context_rebased',row['task'],actor,result={'reason':reason,'archive_sha256':hashlib.sha256(row['messages'].encode()).hexdigest(),'proofs_and_tasks_preserved':True},connection=c)
            return True

    def import_observation(self, ident, observation):
        """Preserve an actual earlier chat read; do not execute or fabricate it again."""
        token=uuid.uuid4().hex;created=observation['created']
        result={**observation['result'],'imported_from_chat':True,'source_created':created}
        with self.db() as c:
            c.execute('INSERT INTO tool_calls VALUES(?,?,?,?,?,?,?,?,?,?)',(token,ident,None,signature(observation['tool'],observation['arguments']),observation['tool'],encoded(observation['arguments']),'finished',encoded(result),created,time.time()))
            c.execute('INSERT INTO checkpoints(mission,tool,result,created) VALUES(?,?,?,?)',(ident,observation['tool'],encoded(result),created))
            self.event(ident,'chat_observation_imported',actor='JARVIS-engine',tool=observation['tool'],arguments=observation['arguments'],result=result,invocation=token,connection=c)
        return token
