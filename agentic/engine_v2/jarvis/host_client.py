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
    spec('host_exec','Exécuter bash sur Debian réel comme adminjarvis dans les chemins hôte accordés. /usr réel lecture seule, secrets absents, réseau hôte disponible ; GitHub/SSH authentifiés via outils structurés. Durée 60s. Pas de sudo.', ['command'])
    spec('host_read_file','Lire un fichier réel dans les chemins accordés',['path'])
    spec('host_write_file','Écrire/remplacer un fichier réel, créer les parents',['path','content'])
    spec('host_delete_file','Supprimer un fichier réel accordé',['path'])
    spec('host_package','Paquet Debian autorisé : action status, install ou configure (reprendre dpkg après interruption). Installation réelle persistante ; ensuite tester le logiciel avec host_exec/capability_test.',['package','action'])
    spec('host_service','systemd réel ; actions et unités définies dans host_policy. Préserver déploiement Dell.',['service','action'])
    spec('host_logs','Journaux réels des services accordés',['service'])
    spec('host_resources','Ressources CPU RAM GPU et inventaire Tailscale réel',[])
    spec('host_github','GitHub authentifié sans exposer le jeton. Actions inspect, file, branches, pages, clone, push (un fichier <1Mo), pull_request brouillon, create (Launcher2 seul), enable_pages (Launcher2 branche gh-pages). file et clone acceptent branch pour lire une branche précise. push nécessite path local, branch jarvis/..., file relatif. Jamais main ; gh-pages accepté pour Launcher2 seul.',['repository','action','path','branch','file','body'],['repository','action'])
    spec('host_remote','SSH sur profil activé : identity/resources/services/proof, write_file/read_file (path/content), package_install (package), service (service/service_action). Voir host_policy. Administration Dell activée selon la politique propriétaire 11B.',['host','action','path','content','package','service','service_action'],['host','action'])
    spec('host_ansible','Ansible réel sur profil activé : ping, resources, deploy_file (path/content), package_install (package), service (service/service_action). Aucune cible implicite ; profil Dell selon politique 11B.',['host','action','path','content','package','service','service_action'],['host','action'])
    spec('capability_request','Consigner une demande durable à Codex. Ne confère aucun droit. persistent : oui/non ; fournir diagnostic réel et test concret.',['capability','mission','resource','required_access','diagnosis','solution','validation','persistent'])
    spec('capability_status','Registre persistant et demandes/résultats Codex. resource optionnel retourne le détail complet de la ressource.',['resource'],[])
    spec('capability_test','Tester réellement une capacité et enregistrer VALIDÉ/ÉCHEC. capacity host_package (resource nom paquet), host_service (unité), host_github (dépôt), host_files (dossier).',['capability','resource'])
