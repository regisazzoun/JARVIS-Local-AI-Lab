"""Reports derived from receipts; free model narrative is archived separately."""
import hashlib
import json
from .mission_store import encoded
from .verification import exact


def facts(store, ident):
    observations = store.observations(ident)
    events = store.events(ident, limit=1000000)
    actions = []
    for o in observations:
        receipt = o.get('result') or {}
        args = dict(o['arguments'])
        if 'content' in args:
            args['content_sha256'] = hashlib.sha256(str(args.pop('content')).encode()).hexdigest()
        actions.append({'invocation':o['id'],'task':o['task'],'initiator':'JARVIS','executor':'broker' if o['tool'].startswith('host_') else 'JARVIS-engine', 'tool':o['tool'],'parameters':args,'observed_ok':receipt.get('ok'), 'returncode':receipt.get('result',{}).get('returncode'), 'broker_evidence':receipt.get('result',{}).get('evidence_id'), 'error':receipt.get('error'), 'created':o['created']})
    return {'mission':ident,'goal':store.get(ident)['goal'],'plans':[{k:r[k] for k in ('version','author','reason','sha256')} for r in store.plans(ident)],
            'tasks':[{k:t[k] for k in ('id','state','report_sha256','artifact')} for t in store.tasks(ident)],
            'actions':actions,'inference_routes':[{'event':e['id'],'created':e['created'],**{k:e['result'].get(k) for k in ('node','effective_model','requested_model','role','compute_job')}} for e in events if e['kind']=='compute_route_observed'],
            'semantic_verifications':[{'event':e['id'],'task':e['task'],**e['result']} for e in events if e['kind']=='semantic_verification'],
            'codex_interventions':[{'event':e['id'],'kind':e['kind'],'result':e['result']} for e in events if e['actor']=='Codex'],
            'scope':'Predicates only; software tests and model declarations are not autonomy evidence.'}


def task_gate(registry, task, chosen):
    store = registry.mission_store; ident = registry.context['mission_id']
    contracts = task.get('contract',{}).get('semantic',[])
    if not contracts:
        raise ValueError('Autonomous task requires contract.semantic with at least one exact independent observation')
    events = [e for e in store.events(ident,limit=1000000) if e['kind']=='semantic_verification' and e['task']==task['id']]
    observations = store.observations(ident,task['id'])
    report = task.get('contract',{}).get('report_path')
    # Conservative freshness: a later action (including a skill) requires recheck.
    def effect(o):
        name=o['tool'];args=o['arguments'];action=args.get('action')
        if args.get('path')==report and name in ('host_write_file','host_edit_file'):
            return False
        if name in ('host_exec','host_write_file','host_edit_file','host_delete_file','skill_test','skill_run','host_ansible','mcp_tools'):
            return True
        if name=='host_service':return action not in ('status','is-active','is-enabled')
        if name=='host_project_service':return action not in ('status','logs')
        if name=='host_package':return action!='status'
        if name=='host_remote':return action in ('write_file','package_install','project_exec','service','supervision_install','desktop_configure','tailscale_configure')
        if name=='host_github':return action in ('push','push_tree','branch_create','create','enable_pages','pull_request','download','clone')
        return False
    effects = [o for o in observations if (o.get('result') or {}).get('ok') and effect(o)]
    boundary = max((o['created'] for o in effects),default=0)
    for contract in contracts:
        matching = [e for e in events if exact(e['result'].get('contract'),contract)]
        if not matching or matching[-1]['result'].get('status')!='PASS':
            raise ValueError('Semantic verification absent/failed: '+encoded(contract))
        if matching[-1]['created'] < boundary:
            raise ValueError('Semantic verification stale after action; re-read actual state')
    if chosen['tool'] != 'mission_verify' or chosen['result'].get('result',{}).get('status')!='PASS':
        raise ValueError('evidence_id must identify a successful mission_verify of active task')


def render_final(store, ident, narrative):
    data=facts(store,ident)
    lines=['# Rapport de mission — faits issus du journal', '', 'Rédaction factuelle : JARVIS-engine. Opérations et plans : acteurs des reçus. Infrastructure26 : Codex. Le texte libre original de JARVIS est conservé dans model_report_original ; il ne constitue pas une preuve.', '', 'Mission `'+ident+'`.', '', '| Tâche | État | SHA256 rapport |','| --- | --- | --- |']
    for t in data['tasks']:
        lines.append('| '+t['id']+' | '+t['state']+' | '+str(t['report_sha256'])+' |')
    lines.extend(['','Plans : '+encoded(data['plans']), '', 'Contrôles sémantiques (historique conservé) :'])
    for v in data['semantic_verifications']:
        lines.append('- Événement '+str(v['event'])+' ; tâche '+str(v['task'])+' ; '+v['status']+' ; SHA256 '+str(v.get('sha256'))+' ; observations '+encoded(v['observations']))
    lines.extend(['','Invocations journalisées : '+str(len(data['actions']))+'. Ce compte comprend contrôles, refus, macros et sous-appels ; il ne mesure pas autant de progrès autonomes.', '', 'Interventions Codex : '+encoded(data['codex_interventions']), '', 'Limites : conformité limitée aux prédicats déclarés et aux instants des lectures. Les rapports de tâches rédigés par le modèle restent à confronter aux reçus. Aucun GO14A automatique. Épreuve finale14A et24-Old non lancées.', '', 'Texte libre JARVIS original : SHA256 '+hashlib.sha256(narrative.encode()).hexdigest()+', archivé intégralement, sans promotion automatique en fait vérifié.'])
    body='\n'.join(lines)+'\n'
    store.event(ident,'report_facts_checked',result={'facts_sha256':hashlib.sha256(encoded(data).encode()).hexdigest(),'narrative_sha256':hashlib.sha256(narrative.encode()).hexdigest(),'policy':'deterministic factual final, original narrative preserved'})
    return body


def register(registry):
    def show(args):
        store=getattr(registry,'mission_store',None)
        if not store:raise ValueError('Durable mission required')
        return facts(store,registry.context['mission_id'])
    registry.specs['mission_report_facts']=('Read factual ledger: actors, tools, parameters, observed receipts, plan versions, semantic verdicts and Codex interventions. Use before report; narrative is not evidence.',{},[],'host_authorized',show)
