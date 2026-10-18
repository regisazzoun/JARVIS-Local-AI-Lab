"""Task verification uses a new broker read, not a model's assertion."""
import hashlib
import json
import time
from .mission_store import encoded


def register(registry):
    def store():
        value = getattr(registry, 'mission_store', None)
        if value is None:
            raise ValueError('Ces outils exigent une mission durable. Lance /api/missions.')
        return value
    def key(): return registry.context['mission_id']
    def plan(args):
        return {'tasks': store().plan(key(), args['tasks'])}
    def progress(args):
        return {'mission': key(), 'tasks': store().tasks(key())}
    def evidence(args):
        rows = store().observations(key())
        row = next((r for r in rows if r['id'] == args['id']), None)
        if not row: raise ValueError('Preuve absente de cette mission')
        text = encoded(row)
        offset = args.get('offset', 0)
        if not isinstance(offset, int) or offset < 0: raise ValueError('offset entier positif requis')
        return {'content': text[offset:offset+12000], 'total_chars': len(text), 'next_offset': offset+12000 if offset+12000 < len(text) else None}
    def note(args):
        return {'event': store().event(key(), 'working_note', registry.context.get('task_id'), 'JARVIS', result={'content': args['content']})}
    def complete(args):
        db = store(); ident = key()
        task = next((t for t in db.tasks(ident) if t['id'] == args['id']), None)
        if not task: raise ValueError('Tâche absente')
        if task['id'] != registry.context.get('task_id'):
            raise ValueError('Valide uniquement la tâche active, après ses dépendances')
        done = {t['id'] for t in db.tasks(ident) if t['state'] == 'validated'}
        if not set(task['deps']) <= done: raise ValueError('Dépendances non validées')
        observations = db.observations(ident, task['id'])
        matches = [r for r in observations if (r['result'] or {}).get('ok') and (
            r['id'] == args['evidence_id'] or (r['result'] or {}).get('result', {}).get('evidence_id') == args['evidence_id'])]
        if not matches: raise ValueError('Preuve réelle réussie de cette tâche absente')
        chosen = matches[-1]
        if chosen['tool'] in ('host_policy', 'mission_progress', 'mission_plan', 'mission_note', 'active_memories'):
            raise ValueError('Cette observation ne prouve pas un résultat fonctionnel')
        # Independent fresh read through the broker and the existing path policy.
        read = registry.specs['host_read_file'][4]({'path': args['report_path']})
        if read.get('returncode', 0) != 0: raise ValueError('Lecture indépendante du rapport échouée')
        body = read.get('stdout', read.get('content', ''))
        if not isinstance(body, str) or len(body.strip()) < 80:
            raise ValueError('Rapport absent ou insuffisant (80 caractères minimum)')
        contract = task.get('contract', {})
        for required in contract.get('required_tools', []):
            if not any(r['tool'] == required and (r['result'] or {}).get('ok') for r in observations):
                raise ValueError('Contrat non satisfait : outil réussi requis '+required)
        for check in contract.get('checks',[]):
            actual=[r for r in observations if r['tool']==check['tool'] and (r['result'] or {}).get('ok') and (not check.get('action') or r['arguments'].get('action')==check['action']) and (not check.get('stdout_contains') or check['stdout_contains'] in (r['result'] or {}).get('result',{}).get('stdout',''))]
            if len(actual)<check.get('minimum',1):raise ValueError('Assertion fonctionnelle manquante : '+encoded(check))
        # A mutation must have a later independent observation, not only its write receipt.
        writes = [r for r in observations if r['tool'] in ('host_write_file', 'host_remote', 'host_ansible')
                  and (r['tool'] == 'host_write_file' or r['arguments'].get('action') in ('write_file', 'deploy_file', 'package_install', 'service'))
                  and (r['result'] or {}).get('ok') and r['arguments'].get('path') != args['report_path']]
        if writes and chosen['created'] <= writes[-1]['created']:
            raise ValueError('Vérification indépendante postérieure à la dernière modification requise')
        sha = hashlib.sha256(body.encode()).hexdigest()
        with db.db() as c:
            c.execute("UPDATE tasks SET state='validated',evidence=?,artifact=?,report_sha256=?,updated=? WHERE mission=? AND id=?",
                      (encoded([chosen]), args['report_path'], sha, time.time(), ident, task['id']))
            db.event(ident, 'task_verified', task['id'], 'JARVIS-engine', result={'report_path': args['report_path'], 'sha256': sha, 'evidence': chosen['id']}, connection=c)
        registry.memory.document(body, source=args['report_path'], project=registry.context.get('project', ''))
        return {'state': 'validated', 'id': task['id'], 'report_path': args['report_path'], 'sha256': sha}
    def publish(args):
        from .publication import enqueue
        return enqueue(store(),key(),registry.context.get('task_id'),args)
    definitions = [
        ('mission_publish', 'Enregistrer un rapport local pour publication asynchrone avec vérification distante. Échec GitHub ne perd pas le fichier local.', {k:{'type':'string'} for k in ('repository','branch','workspace','file')}, ['repository','branch','workspace','file'], publish),
        ('mission_plan', 'Enregistrer le plan durable avant exécution. Liste de tâches avec id,title,depends et contract optionnel.',
         {'tasks': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'title': {'type': 'string'}, 'depends': {'type': 'array', 'items': {'type': 'string'}}}, 'required': ['id', 'title', 'depends']}}}, ['tasks'], plan),
        ('mission_progress', 'Relire les tâches persistantes et leur état vérifié.', {}, [], progress),
        ('mission_evidence', 'Relire une preuve complète persistante par invocation id, avec pagination.', {'id': {'type': 'string'}, 'offset': {'type': 'integer'}}, ['id'], evidence),
        ('mission_note', 'Conserver observations, erreurs et prochaine action avant reprise.', {'content': {'type': 'string', 'maxLength': 16000}}, ['content'], note),
        ('mission_task_complete', 'Vérifier le rapport local et la preuve réelle de la tâche active ; ne valide pas une simple affirmation.',
         {'id': {'type': 'string'}, 'evidence_id': {'type': 'string'}, 'report_path': {'type': 'string'}}, ['id', 'evidence_id', 'report_path'], complete)]
    for name, desc, props, required, fn in definitions:
        registry.specs[name] = (desc, props, required, 'host_authorized', fn)
