from pathlib import Path
import json,shutil,os
H=Path.home();R=H/'JARVIS/modules-standard-20261101';T=R/'connection-templates'
AN=T/'ansible';(AN/'group_vars').mkdir(parents=True,exist_ok=True)
(AN/'inventory.yml').write_text('''# Aucun hôte : remplir au lycée à partir de la liste autorisée.
all:
  children:
    linux:
      hosts: {}
    windows:
      hosts: {}
    cisco:
      hosts: {}
    pfsense:
      hosts: {}
    nagios:
      hosts: {}
    netbox:
      hosts: {}
''')
(AN/'ansible.cfg').write_text('[defaults]\ninventory = ./inventory.yml\ncollections_path = '+str(R/'collections')+'\nhost_key_checking = True\nretry_files_enabled = False\n')
(AN/'group_vars/linux.yml.example').write_text('ansible_connection: ssh\n# ansible_user: à renseigner\n# Réutiliser les identités SSH existantes, aucun secret ici.\n')
(AN/'group_vars/windows-ssh.yml.example').write_text('ansible_connection: ssh\nansible_shell_type: powershell\n# ansible_user: à renseigner\n# Vérifier OpenSSH Server, version Windows et shell distant avant activation.\n')
(AN/'group_vars/windows-winrm.yml.example').write_text('ansible_connection: winrm\nansible_winrm_transport: kerberos\nansible_winrm_server_cert_validation: validate\n# Exemple alternatif ; transport/authentification à choisir selon le domaine.\n')
(AN/'group_vars/cisco.yml.example').write_text('ansible_connection: ansible.netcommon.network_cli\nansible_network_os: cisco.ios.ios\n# ansible_user et mode enable à renseigner selon les droits réellement accordés.\n')
(T/'infrastructure.csv').write_text('nom,role,os_version,adresse_dns,port,transport,compte,reference_secret_prive,empreinte_ou_ca,perimetre_autorise,etat_raccordement\n')
(T/'cisco-testbed.yml.example').write_text('testbed:\n  name: lycee-a-renseigner\ndevices: {}\n# Copier la structure credentials/connections du fichier amont après réception des cibles.\n')
shutil.copy2(R/'sources/cisco-pyats/testbed/testbed.example.yaml',T/'cisco-testbed-upstream.yml.example')
(T/'nagios-config.yml.example').write_text('nagios_url: ""\nnagios_user: ""\nnagios_pass: ""\nca_cert_path: ""\n# Éditer seulement une copie privée ; Nagios Core et CGI à confirmer.\n')
(T/'netbox.env.example').write_text('NETBOX_URL=\nNETBOX_TOKEN=\nVERIFY_SSL=true\n# Jeton privé avec permissions précises ; aucun secret dans ce modèle.\n')
(T/'pfsense.env.example').write_text('PFSENSE_URL=\nPFSENSE_VERSION=\nAUTH_METHOD=api_key\nPFSENSE_API_KEY=\nVERIFY_SSL=true\n# PFSENSE_CA_FILE=\n# Vérifier REST API v2 et la version du pare-feu ; aucun paquet sur cible installé ici.\n')
path=str(R/'node-runtime/node_modules/.bin')+':'+str(R/'venvs/ansible/bin')+':'+str(R/'venvs/bootstrap/bin')+':/usr/local/bin:/usr/bin:/bin'
ansible={'command':str(R/'npm/ansible-mcp/node_modules/.bin/ansible-mcp-server'),'args':['--stdio'],'env':{'PATH':path,'WORKSPACE_ROOT':str(AN),'ANSIBLE_CONFIG':str(AN/'ansible.cfg'),'ANSIBLE_COLLECTIONS_PATH':str(R/'collections')}}
q=H/'.qwen-standard/mcp.json';d=json.loads(q.read_text());d['mcpServers']['standard-ansible']=ansible;q.write_text(json.dumps(d,indent=2));q.chmod(0o600)
for f in ['qwen-local-mcp-added.json','connection-templates/mcpo-local.pending.json']:
 p=R/f;x=json.loads(p.read_text());x['mcpServers']['standard-ansible']=ansible;p.write_text(json.dumps(x,indent=2))
pending=[
 {'name':'netbox-enhanced','missing':['URL NetBox','référence privée du jeton','droits objets'],'client_config':{'command':str(R/'venvs/netbox-enhanced/bin/netbox-mcp-server'),'args':[],'env':{'NETBOX_URL':'A_RENSEIGNER','NETBOX_TOKEN':'REFERENCE_PRIVEE_A_RENSEIGNER','VERIFY_SSL':'true'}}},
 {'name':'nagios','missing':['URL Nagios Core','compte','certificat et CGI'],'client_config':{'command':str(R/'venvs/nagios/bin/nagios-mcp'),'args':['--config','FICHIER_PRIVE_A_RENSEIGNER']}},
 {'name':'cisco-pyats','missing':['testbed réel','comptes','liste de devices autorisés'],'client_config':{'command':str(R/'venvs/cisco-pyats/bin/cisco-pyats-mcp'),'args':[],'env':{'PYATS_TESTBED':'FICHIER_PRIVE_A_RENSEIGNER','PYATS_MCP_ALLOWED_DEVICES':'A_RENSEIGNER'}}},
 {'name':'pfsense','missing':['URL et version','REST API v2','identité API et CA'],'client_config':{'command':str(R/'venvs/pfsense/bin/pfsense-mcp-server'),'args':[],'env':{'PFSENSE_URL':'A_RENSEIGNER','PFSENSE_VERSION':'A_RENSEIGNER','AUTH_METHOD':'api_key','PFSENSE_API_KEY':'REFERENCE_PRIVEE_A_RENSEIGNER','VERIFY_SSL':'true'}}},
 {'name':'github-official-optional','missing':['décider si remplacement utile du connecteur JARVIS déjà actif','réutilisation du secret existant sans copie publique'],'client_config':{'command':str(R/'bin/github-mcp-server'),'args':['stdio'],'env':{'GITHUB_PERSONAL_ACCESS_TOKEN':'REFERENCE_PRIVEE_A_RENSEIGNER'}}},
]
for x in pending:x['enabled']=False
(T/'mcp-lycee.pending.json').write_text(json.dumps({'NOT_A_LIVE_CLIENT_CONFIG':True,'candidates':pending},ensure_ascii=False,indent=2))
(T/'RACCORDEMENT-LYCEE.md').write_text('''# À compléter au lycée — aucune cible active

1. Régis fournit les machines et le périmètre de découverte autorisé. Renseigner infrastructure.csv, aucun scan avant cette définition.
2. Après déplacement : adresses, routes, DNS, comptes et empreintes/certificats. Garder les secrets dans des fichiers privés, jamais dans Git.
3. Ansible : inventory.yml est vide. Les group_vars en .example sont inactifs ; ne copier que le transport adapté après contrôle de l’OS et des droits. ansible.cfg pointe vers les collections isolées et conserve le contrôle des clés d’hôte.
4. Cisco : compléter le testbed à partir de l’exemple amont, remplacer ses exemples par les vrais équipements et définir la liste de devices autorisés.
5. NetBox : choisir Enhanced pour lecture/écriture, renseigner URL et droits. Nagios : Core/CGI et CA. pfSense : version réelle, REST API v2 et CA ; aucune installation automatique sur le pare-feu.
6. mcp-lycee.pending.json est un dossier de candidats, pas une configuration importée. Les secrets doivent remplacer les références seulement dans une copie privée.
7. mcpo-local.pending.json prépare un éventuel raccordement HTTP des six MCP locaux pour WebUI. Il n’est pas ajouté au MCPO actif ; aucun service démarré/rechargé et aucun endpoint fictif enregistré dans WebUI. Les Skills WebUI utilisent déjà la voie native Open Terminal.
8. Référentiels français CIEL/BTS et gabarits : à fournir. Les ressources pédagogiques CC BY-SA nécessitent attribution et respect de leur licence.
9. Tests réels et réception : différés. Prévoir des objets/fichiers dédiés et vérifier codes retour, contenu, arrêt après résultat et rendu visuel. Aucune mission historique à reprendre.
''')
m=R/'native-connection-manifest.json';x=json.loads(m.read_text());x['qwen_mcp_added'].append('standard-ansible');x['pending_candidates']=[p['name'] for p in pending];x['ansible_inventory']='empty';x['mcpo_http']='prepared-only-not-loaded';m.write_text(json.dumps(x,ensure_ascii=False,indent=2))
print(json.dumps({'native_qwen_mcp_count':len(x['qwen_mcp_added']),'pending_candidates':x['pending_candidates'],'inventory_hosts':0,'tests_run':False}))
