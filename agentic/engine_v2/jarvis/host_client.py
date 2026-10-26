"""Tools shared by text, voice and durable mission worker."""
import json,socket,os
from contextvars import ContextVar
WORKLOAD_CLASS=ContextVar('host_workload_class',default=None)

SOCKET = '/run/jarvis-host/bridge.sock'

def transport_failure(operation, exc):
    if isinstance(exc, PermissionError): category='transport_denied'
    elif isinstance(exc, FileNotFoundError): category='resource_missing'
    elif isinstance(exc, TimeoutError): category='timeout'
    elif isinstance(exc, (ConnectionError, BrokenPipeError)): category='service_unavailable'
    else: category='transport_error'
    return {'ok':False,'error':str(exc),'error_code':type(exc).__name__,
            'diagnostic':{'operation':operation,'error_category':category,'stage':'before_broker_reply',
                          'endpoint':SOCKET,'policy_identity':None,'evidence_id':None,
                          'retry':'Check client confinement and broker connectivity; policy denial is not established.'}}

class BrokerError(RuntimeError):
    def __init__(self,response):
        self.response=response
        super().__init__(json.dumps(response,ensure_ascii=False))

def request(operation,arguments,workload_class=None,*,_endpoint=None):
    try:
        if _endpoint is None:return _request(operation,arguments,workload_class)
        return _request(operation,arguments,workload_class,_endpoint=_endpoint)
    except OSError as exc:
        raise BrokerError(transport_failure(operation,exc)) from exc

def _request(operation,arguments,workload_class=None,*,_endpoint=None):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        s.settimeout(660);s.connect(_endpoint or SOCKET)
        s.sendall(json.dumps({'operation':operation,'arguments':arguments,'workload_class':workload_class or WORKLOAD_CLASS.get() or os.environ.get('JARVIS_WORKLOAD_CLASS','interactive')}).encode()+b'\n')
        data=b''
        while not data.endswith(b'\n'):
            block=s.recv(65536)
            if not block:raise RuntimeError('Passerelle interrompue : vérifier état avant toute reprise')
            data+=block
            if len(data)>2000000:raise ValueError('Réponse trop grande')
    result=json.loads(data)
    if not result['ok']:raise BrokerError(result)
    return result

def register(registry):
    def spec(name,description,fields,required=None):
        props={k:{'type':'string','maxLength':16000 if k in ('content','command') else 6000} for k in fields}
        def execute(args):
            # Host authority comes from root-owned broker policy, never from agent_mode or a prompt.
            if name=='host_exec':
                if 'argv' in args:
                    import shlex
                    if 'command' in args:raise ValueError('Provide argv OR command, never both')
                    argv=args['argv']
                    if not isinstance(argv,list) or not argv or any(not isinstance(v,str) or '\x00' in v for v in argv):raise ValueError('argv must be a nonempty list of NUL-free strings')
                    args={k:v for k,v in args.items() if k!='argv'}
                    args['command']=shlex.join(argv)
                    if len(args['command'])>16000:raise ValueError('Encoded command exceeds16000 characters')
                elif 'command' not in args:raise ValueError('host_exec requires command string OR argv array')
            token=WORKLOAD_CLASS.set('mission' if getattr(registry,'context',{}).get('mission_id') else None)
            try:response=request(name,args)
            finally:WORKLOAD_CLASS.reset(token)
            result={**response['result'],'evidence_id':response['evidence_id']}
            if name=='capability_status':
                # One tool registry: derive schemas from the registry actually exposed to this model.
                scope=result.get('effective_scope')
                result['tools']=[{'name':key,'function':value[0],'parameters':value[1],
                                 'required':value[2],'mode':value[3],
                                 'availability':'unverified' if scope is not None else 'policy_visibility_unavailable',
                                 'scope_reference':'effective_scope; action and resource must be checked',
                                 'documentation':'docs/missions/23C/REGISTRE-CAPACITES.md',
                                 'test_method':'capability_test where supported; otherwise execute a scoped read and inspect its receipt'}
                                for key,value in registry.specs.items() if value[3]=='host_authorized']
                result['catalogue_summary']={
                    'tools_count':len(result['tools']),
                    'capabilities_count':len(result.get('capabilities',[])),
                    'requests_count':len(result.get('requests',[])),
                    'fields':'Structured fields tools, capabilities and requests; absence of stdout does not mean an empty registry.',
                    'availability':'Per-resource capabilities retain their observed state; tool exposure alone is not functional validation.'}
            if 'diagnostic' in response:result['diagnostic']=response['diagnostic']
            return result
        registry.specs[name]=(description,props,list(required if required is not None else fields),'host_authorized',execute)
    spec('host_policy','Lire les autorisations hôte persistantes réellement accordées ; ne peut pas les modifier',[])
    spec('host_exec','Exécuter bash sur Debian réel comme adminjarvis dans les chemins hôte accordés. timeout optionnel en secondes (défaut 60, maximum 300), pour les tests réels plus longs. /usr réel lecture seule, secrets absents, réseau hôte disponible ; GitHub/SSH authentifiés via outils structurés. Pas de bus systemd ni de périphériques /dev dans ce confinement : pour journaux/états/GPU, utilise host_diagnostics, host_logs, host_service, host_resources. Ne conclus pas une panne à partir d’un accès absent ici. /tmp est neuf et éphémère à chaque appel ; conserve les fichiers de reprise dans write_roots. Les processus de ce shell meurent à la fin de l’appel ; utilise host_project_service pour un serveur durable accordé. Pas de sudo.', ['command'])
    registry.specs['host_exec'][1]['timeout']={'type':'integer','minimum':1,'maximum':300}
    registry.specs['host_exec'][1]['argv']={'type':'array','minItems':1,'maxItems':256,'items':{'type':'string','maxLength':6000}}
    old=registry.specs['host_exec']
    registry.specs['host_exec']=(old[0]+' Alternative structurée : argv tableau de chaînes, exclusif avec command. Chaque argument est échappé littéralement ; dans un skill utiliser argv=["python3","/path/script.py","--input","${input_file}"] pour les paramètres, jamais une interpolation de fragment shell.',old[1],[],old[3],old[4])
    spec('host_read_file','Lire un fichier réel accordé. Pour source longue ou vue modèle excerptée : offset en caractères et limit=6000 ; next_offset permet la suite, source_sha256 vérifie même version. Sans pagination, lecture complète conservée pour réception des rapports. Les pages indépendantes sont admises en mission_read_batch.',['path'])
    registry.specs['host_read_file'][1].update(offset={'type':'integer'},limit={'type':'integer'})
    spec('host_write_file','Écrire/remplacer un fichier réel, créer les parents',['path','content'])
    def edit_file(args):
        response=request('host_edit_file',args)
        return {**response['result'],'evidence_id':response['evidence_id']}
    registry.specs['host_edit_file']=('Édition ciblée exacte d’un fichier accordé ; préserve le reste. path, old texte exact non vide, new remplacement (vide pour suppression), count occurrences attendu défaut1 ; expected_sha256 optionnel refuse source modifiée. Rien n’est écrit si précondition incorrecte. Retourne SHA avant/après ; retester le code ensuite.',{'path':{'type':'string'},'old':{'type':'string','maxLength':16000},'new':{'type':'string','minLength':0,'maxLength':16000},'count':{'type':'integer'},'expected_sha256':{'type':'string'}},['path','old','new'],'host_authorized',edit_file)
    spec('host_delete_file','Supprimer un fichier réel accordé',['path'])
    spec('host_package','Paquet Debian autorisé : action status, install ou configure (reprendre dpkg après interruption). Installation réelle persistante ; ensuite tester le logiciel avec host_exec/capability_test.',['package','action'])
    spec('host_service','systemd réel ; actions et unités définies dans host_policy. Préserver déploiement Dell.',['service','action'])
    spec('host_logs','Journaux réels des services accordés',['service'])
    spec('host_diagnostics','Diagnostic Mac mini réel hors confinement : action failed_units, recent_warnings, kernel_warnings, storage_state. Lecture seule, journaux root sans secret de configuration.',['action'])
    spec('host_resources','Ressources CPU RAM GPU et inventaire Tailscale réel',[])
    spec('host_github','GitHub authentifié sans exposer le jeton. Actions inspect, file, download, branches, pages, clone, push (un fichier <1Mo), pull_request brouillon, create (Launcher2 seul), enable_pages (Launcher2 branche gh-pages). file lit path (ou file) exact ; download lit path et enregistre le fichier complet dans destination absolue autorisée, sans recopier son contenu. file et clone acceptent branch pour lire une branche précise. push nécessite path DOSSIER racine local, branch jarvis/..., file relatif (pas le fichier dans path). push_tree publie un lot explicite : path dossier, files chaîne JSON de chemins relatifs ; exclure .env/secrets/binaires. Produit commit_sha et verified, reprise idempotente sans force. verify_tree reprend path dossier et files JSON et compare chaque blob distant avec les sources locales ; absent ou différent échoue. Autres actions : repositories, branch_create, commits, verify_commit, diff, prs, pr_status. Pour commits, verify_commit, diff, prs et pr_status, branch est obligatoire et doit être la branche réelle jarvis/... ou codex/... (les PR sont listées par branche head). verify_commit exige en plus le commit SHA attendu. pull_request crée ou met à jour la PR existante. Les commits locaux via host_exec restent possibles ; push_tree crée un commit distant de sources contrôlées sans exporter les secrets/historique local. Jamais main ; gh-pages accepté pour Launcher2 seul.',['repository','action','path','branch','file','body','destination','files','commit','title','message'],['repository','action'])
    spec('host_remote','SSH sur profil activé : identity/resources/services/proof, write_file/read_file (path/content), package_install (package), service (service/service_action). Opérations structurées supplémentaires si accordées : supervision_install, supervision_test, desktop_configure, desktop_test, desktop_network_test, tailscale_configure (installe le client sur Dell, réutilise uniquement une clé privée préprovisionnée), tailscale_status (état réel sans secret), desktop_gateway_configure (passerelle privée du Mac lorsque Dell n’a pas de client Tailscale). Elles exécutent une infrastructure fixe sans renvoyer de secret. Voir host_policy. project_exec(project,command) exécute dans un confinement distant du seul projet accordé, réseau hôte et /usr lecture seule, sans clés ni sudo ; pour client WebRTC de réception sur Dell1. Administration Dell activée selon la politique propriétaire 11B.',['host','action','path','content','package','service','service_action','project','command'],['host','action'])
    registry.specs['host_remote'][1]['local_path']={'type':'string','description':'project_upload/download only: local source/destination. project, path (remote absolute), local_path required; transfers bytes with SHA256 comparison. Download into /var/lib/jarvis/projects/tts-01; upload only readable allowed roots. Never returns binary contents.'}
    registry.specs['host_remote'][1]['model']={'type':'string','maxLength':128,'description':'action=model_pull (alias pull) only: exact allowed Ollama tag, e.g. qwen3:32b-q4_K_M. Bounded resumable download on the target mission service. Success requires final success AND exact catalogue readback. Other models are rejected by owner policy.'}
    registry.specs['host_remote'][1]['probe']={'type':'string','enum':['gpu_inventory','tts_runtime','archive_inventory','script_syntax','tts_samples'],'description':'action project_probe only, with project:tts-01. Fixed independent read in a read-only project mount. No command or content accepted; usable as mission_verify source.'}
    old=registry.specs['host_remote']
    registry.specs['host_remote']=(old[0]+' Model installation: action=model_pull, host=dell-observe, model=qwen3:32b-q4_K_M. The tool executes POST pull, preserves progress and verifies the exact installed tag. Repeat the same call after an incomplete timeout to resume cached blobs; do not substitute another model. hybrid_catalogue independently reads installed models. TTS-01: project_exec project=tts-01 at /opt/jarvis-lab/tts-01 with GPU; project_probe(project,probe) performs a fixed independent read usable in mission_verify; project_upload/project_download transfer a file with project,path,local_path and SHA256 verification. Archive references stay private.',old[1],old[2],old[3],old[4])
    spec('host_ansible','Ansible réel sur profil activé : ping, resources, deploy_file (path/content), package_install (package), service (service/service_action). Aucune cible implicite ; profil Dell selon politique 11B.',['host','action','path','content','package','service','service_action'],['host','action'])
    spec('capability_request','Consigner une demande durable à Codex. Ne confère aucun droit. persistent : oui/non ; fournir diagnostic réel et test concret.',['capability','mission','resource','required_access','diagnosis','solution','validation','persistent'])
    spec('capability_status','Registre persistant et demandes/résultats Codex. resource optionnel retourne le détail complet de la ressource.',['resource'],[])
    spec('capability_test','Tester réellement une capacité et enregistrer VALIDÉ/ÉCHEC. capacity host_package (resource nom paquet), host_service (unité), host_github (dépôt), host_files (dossier).',['capability','resource'])

    def project_service(args):
        response=request('host_project_service',args)
        return {**response['result'],'evidence_id':response['evidence_id']}
    registry.specs['host_project_service']=('Service de projet persistant dans le même confinement que host_exec. Actions install (argv exécutable absolu et arguments, projet accordé), status (inclut les processus hôte du cgroup du service : PID, nom et exécutable, sans arguments ni environnement), start, stop, restart, logs. Exécution comme identité technique, jamais root ; conserve le serveur entre appels et redémarrages du moteur. Pas de modification des services centraux. logs retourne les messages récents de l’activation courante ; history=true inclut les anciennes activations, toujours messages récents d’abord.',{'project':{'type':'string'},'name':{'type':'string'},'action':{'type':'string','enum':['install','status','start','stop','restart','logs','enable','disable']},'argv':{'type':'array','items':{'type':'string'}},'history':{'type':'boolean'}},['project','name','action'],'host_authorized',project_service)
