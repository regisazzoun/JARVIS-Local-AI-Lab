"""Task verification uses a new broker read, not a model's assertion."""
import hashlib
import json
import time
from .mission_store import encoded, arguments_match


def register(registry):
    def store():
        value = getattr(registry, 'mission_store', None)
        if value is None:
            raise ValueError('Ces outils exigent une mission durable. Lance /api/missions.')
        return value
    def key(): return registry.context['mission_id']
    def plan(args):
        return {'tasks': store().plan(key(), args['tasks'], author='JARVIS', metadata=args.get('metadata'), reason=args.get('reason','initial plan'), expected_version=args.get('expected_version'), append=args.get('append',False), patch=args.get('patch',False)), 'plans':store().plans(key())}
    def progress(args):
        current=getattr(registry,'mission_store',None)
        def summary(tasks):return [{k:t.get(k) for k in ('id','title','state','artifact','report_sha256')} for t in tasks]
        if current:return {'mission':key(),'tasks':summary(current.tasks(key())),'plans':current.plans(key()),'current_plan_version':len(current.plans(key()))}
        controller=getattr(registry,'mission_controller',None)
        if not controller:raise ValueError('Moteur durable indisponible')
        ident=args.get('id')
        if not ident:
            with controller.store.db() as c:
                row=c.execute('SELECT id FROM missions WHERE conversation=? ORDER BY updated DESC LIMIT 1',(registry.context.get('conversation'),)).fetchone()
            if not row:raise ValueError('Aucune mission pour cette conversation ; utilise mission_list')
            ident=row['id']
        mission=controller.store.get(ident)
        return {'mission':ident,'state':mission['state'],'tasks':summary(controller.store.tasks(ident))}
    def listing(args):
        controller=getattr(registry,'mission_controller',None)
        if not controller:raise ValueError('Moteur durable indisponible')
        with controller.store.db() as c:
            return {'missions':[{**dict(r),'goal':r['goal'].split('\n')[0][:300]} for r in c.execute('SELECT id,goal,state,updated,conversation FROM missions ORDER BY updated DESC LIMIT 15')]}

    def evidence(args):
        rows = store().observations(key())
        row = next((r for r in rows if r['id'] == args['id'] or (r.get('result') or {}).get('result',{}).get('evidence_id')==args['id']), None)
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
        contract=task.get('contract',{})
        if contract.get('report_path') and args['report_path']!=contract['report_path']:raise ValueError('Chemin de rapport attendu : '+contract['report_path'])
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
        if json.loads(db.get(ident)['spec']).get('autonomous'):
            from .mission_reporting import task_gate
            task_gate(registry, task, chosen)
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
            actual=[r for r in observations if r['tool'] in (check.get('tools') or [check['tool']]) and (r['result'] or {}).get('ok')==check.get('ok',True) and arguments_match(r['arguments'],check.get('arguments',{})) and (not check.get('action') or r['arguments'].get('action')==check['action']) and all((r['result'] or {}).get('result',{}).get(k)==v for k,v in check.get('result_fields',{}).items()) and (not check.get('stdout_contains') or check['stdout_contains'] in (r['result'] or {}).get('result',{}).get('stdout','')) and not any(text in (r['result'] or {}).get('result',{}).get('stdout','') for text in check.get('stdout_not_contains',[]))]
            if len(actual)<check.get('minimum',1):raise ValueError('Assertion fonctionnelle manquante : '+encoded(check))
        # A mutation must have a later independent observation, not only its write receipt.
        writes = [r for r in observations if r['tool'] in ('host_write_file', 'host_edit_file', 'host_remote', 'host_ansible')
                  and (r['tool'] in ('host_write_file','host_edit_file') or (r['arguments'].get('action') in ('write_file','deploy_file','package_install','supervision_install','desktop_configure','desktop_gateway_configure','tailscale_configure') or (r['arguments'].get('action')=='service' and r['arguments'].get('service_action') in ('start','stop','restart','enable','disable'))))
                  and (r['result'] or {}).get('ok') and r['arguments'].get('path') != args['report_path']]
        if writes and chosen['created'] <= writes[-1]['created']:
            raise ValueError('Vérification indépendante postérieure à la dernière modification requise')
        spec=json.loads(db.get(ident)['spec'])
        if spec.get('publication'):
            from .publication import redact_public,invoke
            clean=redact_public(body)
            if clean!=body:
                invoke('host_write_file',{'path':args['report_path'],'content':clean})
                body=invoke('host_read_file',{'path':args['report_path']})['stdout']
                if body!=clean:raise ValueError('Expurgation locale non confirmée')
                db.event(ident,'report_redacted',task['id'],result={'editor':'JARVIS-engine','path':args['report_path']})
        sha = hashlib.sha256(body.encode()).hexdigest()
        with db.db() as c:
            c.execute("UPDATE tasks SET state='validated',last_error=NULL,evidence=?,artifact=?,report_sha256=?,updated=? WHERE mission=? AND id=?",
                      (encoded([chosen]), args['report_path'], sha, time.time(), ident, task['id']))
            db.event(ident, 'task_verified', task['id'], 'JARVIS-engine', result={'report_path': args['report_path'], 'sha256': sha, 'evidence': chosen['id']}, connection=c)
            publication=json.loads(db.get(ident)['spec']).get('publication')
            if publication:
                from pathlib import Path
                from .publication import enqueue
                relative=str(Path(args['report_path']).relative_to(Path(publication['workspace'])))
                enqueue(db,ident,task['id'],{**publication,'file':relative},verified_body=body,connection=c)
        registry.memory.document(body, source=args['report_path'], project=registry.context.get('project', ''))
        return {'state': 'validated', 'id': task['id'], 'report_path': args['report_path'], 'sha256': sha}
    def block(args):
        db=store();ident=key();task_id=registry.context.get('task_id')
        proof=next((o for o in db.observations(ident,task_id) if (o['id']==args['evidence_id'] or (o.get('result') or {}).get('result',{}).get('evidence_id')==args['evidence_id']) and o.get('result')),None)
        if not proof or proof['tool'].startswith('mission_'):raise ValueError('Une observation réelle de la tâche est requise')
        with db.db() as c:revisions=[r['file'] for r in c.execute("SELECT file FROM publication_outbox WHERE mission=? AND state='needs_revision'",(ident,))]
        if revisions:raise ValueError('Correct recoverable document publications before waiting on external authentication: '+', '.join(revisions)+'. Preserve summaries separately, download originals, append via host_exec/Python and mission_publish again.')
        read=registry.specs['host_read_file'][4]({'path':args['report_path']})
        body=read.get('stdout','')
        if read.get('returncode',0) or len(body.strip())<80:raise ValueError('Rapport de blocage vérifiable requis')
        spec=json.loads(db.get(ident)['spec']);publication=spec.get('publication')
        if publication:
            from pathlib import Path
            from .publication import enqueue,redact_public,invoke
            clean=redact_public(body)
            if clean!=body:
                invoke('host_write_file',{'path':args['report_path'],'content':clean})
                if invoke('host_read_file',{'path':args['report_path']})['stdout']!=clean:raise ValueError('Expurgation non vérifiée')
                body=clean
            enqueue(db,ident,task_id,{**publication,'file':str(Path(args['report_path']).relative_to(publication['workspace']))},verified_body=body)
        with db.db() as c:
            c.execute("UPDATE tasks SET state='blocked',last_error=?,artifact=?,report_sha256=?,updated=? WHERE mission=? AND id=?",(args['reason'],args['report_path'],hashlib.sha256(body.encode()).hexdigest(),time.time(),ident,task_id))
            db.event(ident,'external_dependency_blocked',task_id,'JARVIS',result={'reason':args['reason'],'evidence':proof['id'],'report_path':args['report_path'],'verified_success':False},connection=c)
        db.transition(ident,'waiting_external',{'reason':args['reason'],'report_path':args['report_path']})
        return {'state':'waiting_external','task':task_id,'report_path':args['report_path'],'not_completed':True}
    def publish(args):
        from .publication import enqueue
        return enqueue(store(),key(),registry.context.get('task_id'),args)
    def batch(args):
        import concurrent.futures,os
        calls=json.loads(args['calls']) if isinstance(args['calls'],str) else args['calls']
        if not isinstance(calls,list) or not calls:raise ValueError('Liste de lectures requise')
        safe={'mission_progress','host_read_file','host_policy','host_resources','host_logs','host_diagnostics','system_status','disk_usage','jarvis_services','software_versions','hardware_inventory','service_logs','read_configuration','web_fetch','web_search'}
        def run(original):
            start=time.monotonic();invoked=False
            try:
                if not isinstance(original,dict) or not isinstance(original.get('tool'),str):raise ValueError('Chaque lecture exige tool et arguments')
                name=original['tool'];arguments=dict(original.get('arguments',{}))
                for field,value in original.items():
                    if field in ('tool','arguments'):continue
                    if field in arguments and arguments[field]!=value:raise ValueError('Argument contradictoire : '+field)
                    arguments[field]=value
                if name=='host_github' and 'action' not in arguments:arguments['action']='file' if 'path' in arguments or 'file' in arguments else 'inspect'
                allowed=name in safe or name=='host_project_service' and arguments.get('action') in ('status','logs') or name=='host_remote' and arguments.get('action') in ('identity','resources','services','desktop_status','desktop_logs','journal_recent','supervision_status','models','storage','telemetry','tailscale_status') or name=='host_github' and arguments.get('action') in ('file','inspect','branches','pages')
                if not allowed:raise ValueError('Opération batch non admise : '+name+'. Appelle cet outil directement ; download écrit un fichier et host_exec exécute une commande, ils ne sont pas des lectures batch.')
                token=store().begin_call(key(),registry.context.get('task_id'),name,arguments)
                invoked=True
                result=registry.execute(name,arguments)
                store().finish_call(token,result,time.monotonic()-start)
                return {**result,'invocation_id':token,'normalized_arguments':arguments if arguments!=original.get('arguments') else None}
            except Exception as exc:
                store().event(key(),'batch_entry_rejected',registry.context.get('task_id'),result={'error':str(exc),'tool':original.get('tool') if isinstance(original,dict) else None})
                return {'ok':False,'error':str(exc),'executed':None if invoked else False,'outcome':'unknown' if invoked else 'rejected_before_execution'}
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(calls),os.cpu_count() or 1)) as pool:
            results=list(pool.map(run,calls))
            return {'results':results,'returncode':0 if all(r.get('ok') for r in results) else 1}
    definitions = [
        ('mission_block','Consigner un blocage externe réel prouvé et son rapport. Préserve toutes les tâches acquises, publie le rapport sans déclarer de réussite et attend la résolution externe. Ne pas utiliser pour une erreur récupérable.',{k:{'type':'string'} for k in ('reason','report_path','evidence_id')},['reason','report_path','evidence_id'],block),
        ('mission_list','Lister les missions durables réelles pour répondre sur leur état en conversation.',{},[],listing),
        ('mission_read_batch','Exécuter en parallèle des lectures indépendantes réelles. Ne grouper aucune mutation ni commande host_exec.',{'calls':{'type':'array','items':{'type':'object','properties':{'tool':{'type':'string'},'arguments':{'type':'object'}},'required':['tool','arguments']}}},['calls'],batch),
        ('mission_publish', 'Enregistrer un rapport local pour publication asynchrone avec vérification distante. Échec GitHub ne perd pas le fichier local.', {k:{'type':'string'} for k in ('repository','branch','workspace','file')}, ['repository','branch','workspace','file'], publish),
        ('mission_plan', 'Enregistrer/réviser ton plan durable. tasks: id,title,depends,objective,tools,observations,verification,recovery,artifacts,contract. metadata: objective,success_criteria,artifacts,stop_conditions. Révision: expected_version et reason. Pour modifier une tâche non reçue : patch:true, tasks=[définitions complètes des seules tâches modifiées], expected_version courante. Pour ajouter des étapes sans recopier les tâches reçues : append:true, tasks=[nouvelles tâches uniquement], expected_version=version courante ; metadata conservée si omise. La synthèse finale est gérée par intervention_report après les tâches techniques. Les tâches reçues restent immuables. Pour mission autonome, contract.semantic contient les contrats mission_verify attendus (lectures indépendantes).',
         {'patch':{'type':'boolean','description':'true: tasks contains ONLY the changed existing pending tasks; saved/validated tasks and metadata are preserved automatically. expected_version is current.'},'append':{'type':'boolean','description':'true: tasks contains ONLY new tasks; prior tasks and metadata are retained automatically. expected_version is current saved version.'},'metadata':{'type':'object','properties':{'objective':{'type':'string'},'success_criteria':{'type':'array','items':{'type':'string'}},'artifacts':{'type':'array','items':{'type':'string'}},'stop_conditions':{'type':'array','items':{'type':'string'}}}}, 'reason':{'type':'string'}, 'expected_version':{'type':'integer','description':'CURRENT saved version from mission_progress, not desired next version. Failed proposals do not increment it.'}, 'tasks': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'title': {'type': 'string'}, 'objective':{'type':'string'},'tools':{'type':'array','items':{'type':'string'}},'observations':{'type':'array','items':{'type':'string'}},'verification':{'type':'string'},'recovery':{'type':'string'},'artifacts':{'type':'array','items':{'type':'string'}}, 'depends': {'type': 'array', 'items': {'type': 'string'}}, 'contract': {'type':'object','properties':{'report_path':{'type':'string'},'semantic':{'type':'array','items':{'type':'object','properties':{'kind':{'type':'string','enum':['json','text','service']},'source':{'type':'object'},'expected':{'type':'object'},'types':{'type':'object'},'baseline_source':{'type':'object'},'preserve':{'type':'array','items':{'type':'string'}},'equals':{'type':'string'},'sha256':{'type':'string'},'expected_state':{'type':'string'}}}},'checks':{'type':'array','items':{'type':'object'}}}}}, 'required': ['id', 'title', 'depends']}}}, ['tasks'], plan),
        ('mission_progress', 'Relire les tâches persistantes ; id facultatif en conversation pour une autre mission.', {'id':{'type':'string'}}, [], progress),
        ('mission_evidence', 'Relire une preuve complète persistante par invocation id, avec pagination.', {'id': {'type': 'string'}, 'offset': {'type': 'integer'}}, ['id'], evidence),
        ('mission_note', 'Conserver observations, erreurs et prochaine action avant reprise.', {'content': {'type': 'string', 'maxLength': 16000}}, ['content'], note),
        ('mission_task_complete', 'Vérifier le rapport local et la preuve réelle de la tâche active ; ne valide pas une simple affirmation.',
         {'id': {'type': 'string'}, 'evidence_id': {'type': 'string'}, 'report_path': {'type': 'string'}}, ['id', 'evidence_id', 'report_path'], complete)]
    for name, desc, props, required, fn in definitions:
        registry.specs[name] = (desc, props, required, 'host_authorized', fn)
