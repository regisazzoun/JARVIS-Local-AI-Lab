"""Tools shared by text, voice and durable mission worker."""
import json,socket

class BrokerError(RuntimeError):
    def __init__(self,response):
        self.response=response
        super().__init__(json.dumps(response,ensure_ascii=False))

def request(operation,arguments):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        s.settimeout(660);s.connect('/run/jarvis-host/bridge.sock')
        s.sendall(json.dumps({'operation':operation,'arguments':arguments}).encode()+b'\n')
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
            response=request(name,args)
            return {**response['result'],'evidence_id':response['evidence_id']}
        registry.specs[name]=(description,props,list(required if required is not None else fields),'host_authorized',execute)
    spec('host_policy','Lire les autorisations hôte persistantes réellement accordées ; ne peut pas les modifier',[])
    spec('host_exec','Exécuter bash sur Debian réel comme adminjarvis dans les chemins hôte accordés. timeout optionnel en secondes (défaut 60, maximum 300), pour les tests réels plus longs. /usr réel lecture seule, secrets absents, réseau hôte disponible ; GitHub/SSH authentifiés via outils structurés. Pas de bus systemd ni de périphériques /dev dans ce confinement : pour journaux/états/GPU, utilise host_diagnostics, host_logs, host_service, host_resources. Ne conclus pas une panne à partir d’un accès absent ici. /tmp est neuf et éphémère à chaque appel ; conserve les fichiers de reprise dans write_roots. Les processus de ce shell meurent à la fin de l’appel ; utilise host_project_service pour un serveur durable accordé. Pas de sudo.', ['command'])
    registry.specs['host_exec'][1]['timeout']={'type':'integer','minimum':1,'maximum':300}
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
    spec('host_ansible','Ansible réel sur profil activé : ping, resources, deploy_file (path/content), package_install (package), service (service/service_action). Aucune cible implicite ; profil Dell selon politique 11B.',['host','action','path','content','package','service','service_action'],['host','action'])
    spec('capability_request','Consigner une demande durable à Codex. Ne confère aucun droit. persistent : oui/non ; fournir diagnostic réel et test concret.',['capability','mission','resource','required_access','diagnosis','solution','validation','persistent'])
    spec('capability_status','Registre persistant et demandes/résultats Codex. resource optionnel retourne le détail complet de la ressource.',['resource'],[])
    spec('capability_test','Tester réellement une capacité et enregistrer VALIDÉ/ÉCHEC. capacity host_package (resource nom paquet), host_service (unité), host_github (dépôt), host_files (dossier).',['capability','resource'])

    def project_service(args):
        response=request('host_project_service',args)
        return {**response['result'],'evidence_id':response['evidence_id']}
    registry.specs['host_project_service']=('Service de projet persistant dans le même confinement que host_exec. Actions install (argv exécutable absolu et arguments, projet accordé), status, start, stop, restart, logs. Exécution comme identité technique, jamais root ; conserve le serveur entre appels et redémarrages du moteur. Pas de modification des services centraux. logs retourne les messages récents de l’activation courante ; history=true inclut les anciennes activations, toujours messages récents d’abord.',{'project':{'type':'string'},'name':{'type':'string'},'action':{'type':'string','enum':['install','status','start','stop','restart','logs','enable','disable']},'argv':{'type':'array','items':{'type':'string'}},'history':{'type':'boolean'}},['project','name','action'],'host_authorized',project_service)
