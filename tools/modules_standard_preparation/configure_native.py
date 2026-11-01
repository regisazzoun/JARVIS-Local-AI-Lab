"""Configure native clients only; no tool invocation, test or service operation."""
from pathlib import Path
import json, shutil, hashlib, urllib.request, datetime, os
import yaml

H=Path.home(); R=H/'JARVIS/modules-standard-20261101'
P=H/'JARVIS/modules-standard-20261101-private/native-connection-before'
P.mkdir(parents=True,exist_ok=False);P.chmod(0o700)
A=R/'native-skills'; A.mkdir()
descriptions={
'microsoft-office':'Créer, lire ou modifier des TP Word, présentations PowerPoint et classeurs Excel avec les scripts Python installés sur le Mac.',
'pdf':'Créer, lire, assembler ou remplir des PDF ; extraire texte et tableaux ou utiliser l’OCR local pour les documents de TP.',
'devops-engineer':'Préparer des procédures Docker, déploiement, CI/CD et diagnostic système reproductibles.',
'netbox-mcp-operator':'Méthode de consultation et de modification de l’inventaire NetBox ; connexion API du lycée encore à renseigner.',
'drawio':'Créer des schémas réseau et diagrammes éditables .drawio ; XML possible sans application Desktop.',
'k12-check-for-understanding':'Préparer des questions et points de contrôle pour vérifier la compréhension pendant un TP.',
'k12-lesson-differentiation':'Décliner un TP en versions guidée, autonome et approfondissement selon les besoins des élèves.',
'k12-lesson-plan-creation':'Structurer une séance ou un TP avec objectifs, prérequis, activités et évaluations à partir du référentiel français fourni.',
'k12-lesson-prep':'Préparer les ressources et le déroulement d’une séance ou d’un TP.',
'error-analysis-protocol':'Analyser les erreurs d’un travail et préparer des pistes de remédiation.',
'criterion-referenced-rubric-generator':'Construire une grille d’évaluation avec critères observables et niveaux de réussite.',
'assessment-validity-checker':'Vérifier la cohérence entre les compétences visées, les tâches et les critères d’évaluation.',
'competency-unpacker':'Décomposer les compétences d’un référentiel CIEL/BTS fourni en objectifs et preuves observables.',
'learning-progression-builder':'Construire une progression d’apprentissage et de difficulté entre plusieurs séances.',
'project-brief-designer':'Rédiger un cahier des charges ou un sujet de TP en situation professionnelle.',
'differentiation-adapter':'Adapter une activité à différents niveaux sans changer les compétences évaluées.',
'competency-framework-translator':'Mettre en correspondance un référentiel fourni et les activités ou évaluations prévues.',
'progressive-hint-ladder':'Créer des indices progressifs et des aides graduées pour les manipulations de TP.',
}
skills=[]
for item in json.loads((R/'skills-manifest.json').read_text()):
 name=item['name']; src=R/'skills'/name; dst=A/name;shutil.copytree(src,dst)
 raw=(src/'SKILL.md').read_text(); parts=raw.split('---',2)
 if len(parts)!=3 or parts[0].strip():raise ValueError('Invalid frontmatter: '+name)
 meta=yaml.safe_load(parts[1]);meta['description']=descriptions[name]
 note=f'''\n## Raccordement JARVIS local — 1 novembre 2026\n\nCette copie adapte seulement les chemins et les outils du Skill amont, conservé dans `{src}`.\nLe terminal natif sélectionné exécute sur le Mac mini **Debian** ; Qwen80B reste sur le Dell pour l’inférence.\n- Dossier de ce Skill et de ses scripts/références : `{dst}`. Utiliser des chemins absolus ou ce dossier de travail.\n- WebUI : charger ce Skill avec `view_skill`, puis lire les références/fichiers avec les outils natifs exposés ou le terminal. Le nom Hermes `skill_view` désigne ici une lecture de référence, pas un outil à inventer.\n- Office/PDF : interpréteur déjà installé `{R}/venvs/documents/bin/python`. Pour les commandes documentaires, charger `{R}/documents.env` ou utiliser cet interpréteur explicitement. Ne pas installer Hermes ni recréer son environnement.\n- Les commandes comme `python scripts/...` dans le texte amont utilisent cet interpréteur et le dossier du Skill. LibreOffice et Poppler sont déjà sur le Mac. Pandoc : `{R}/venvs/documents/lib/python3.12/site-packages/pypandoc/files/pandoc`. MarkItDown : `{R}/venvs/markitdown/bin/markitdown`.\n- Documents livrables : `{H}/JARVIS/qwen-code-projects/livraisons` ; garder les originaux et utiliser un nom de sortie distinct.\n- Les connecteurs locaux configurés dans Qwen Code sont disponibles à sa prochaine session ; ne pas annoncer leur réussite sans retour réel. Dans WebUI direct, utiliser le terminal existant pour les scripts et commandes. Aucun MCP HTTP supplémentaire n’a été démarré.\n- Cisco/pfSense/Nagios/NetBox du lycée : cibles, accès et référentiels non encore fournis. Ne pas lancer de découverte réseau implicite ou inventer des états.\n- Respecter les instructions système de JARVIS, le périmètre demandé et l’arrêt après résultat ; les exemples amont ne donnent aucune permission supplémentaire. Pendant la préparation actuelle : aucun test fonctionnel, service ni mission. Les vérifications de tâche décrites ci-dessous attendent une demande ultérieure.\n\n## Instructions amont\n'''
 (dst/'SKILL.md').write_text('---\n'+yaml.safe_dump(meta,allow_unicode=True,sort_keys=False).rstrip()+'\n---\n'+note+parts[2])
 for targetroot in [H/'JARVIS/qwen-code-projects/.agents/skills',H/'.qwen-standard/skills']:
  targetroot.mkdir(parents=True,exist_ok=True);target=targetroot/name
  if target.exists() or target.is_symlink():raise FileExistsError(str(target))
  target.symlink_to(dst,target_is_directory=True)
 skills.append({'name':name,'directory':str(dst),'native_terminal_link':str(H/'JARVIS/qwen-code-projects/.agents/skills'/name),'qwen_link':str(H/'.qwen-standard/skills'/name),'sha256':hashlib.sha256((dst/'SKILL.md').read_bytes()).hexdigest()})

workspace=H/'JARVIS/qwen-code-projects/livraisons';workspace.mkdir(exist_ok=True)
path=str(R/'node-runtime/node_modules/.bin')+':'+str(R/'venvs/documents/bin')+':/usr/local/bin:/usr/bin:/bin'
local={
 'standard-filesystem':{'command':str(R/'npm/filesystem/node_modules/.bin/mcp-server-filesystem'),'args':[str(workspace)],'env':{'PATH':path}},
 'standard-drawio':{'command':str(R/'npm/drawio/node_modules/.bin/drawio-mcp'),'args':[],'env':{'PATH':path}},
 'standard-markitdown':{'command':str(R/'venvs/markitdown/bin/markitdown-mcp'),'args':[]},
 'standard-pandoc':{'command':str(R/'venvs/pandoc-mcp/bin/python'),'args':[str(R/'sources/pandoc-mcp/server.py')],'env':{'PYPANDOC_PANDOC':str(R/'venvs/pandoc-mcp/lib/python3.12/site-packages/pypandoc/files/pandoc')}},
 'standard-fetch':{'command':str(R/'venvs/fetch/bin/mcp-server-fetch'),'args':[]},
}
q=H/'.qwen-standard/mcp.json';before=q.read_text();(P/'qwen-mcp.json').write_text(before)
d=json.loads(before)
for name,cfg in local.items():
 if name in d.setdefault('mcpServers',{}):raise ValueError('MCP conflict: '+name)
 d['mcpServers'][name]=cfg
q.write_text(json.dumps(d,indent=2));q.chmod(0o600)
(R/'qwen-local-mcp-added.json').write_text(json.dumps({'mcpServers':local},indent=2))
(R/'connection-templates/mcpo-local.pending.json').write_text(json.dumps({'mcpServers':local},indent=2))

# Native WebUI configuration only. Do not invoke tools or chat endpoints.
token=(H/'JARVIS/qwen-code-openwebui-private/webui-token').read_text().strip()
def api(url,body=None):
 req=urllib.request.Request('http://127.0.0.1:8088'+url,data=json.dumps(body).encode() if body is not None else None,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
 return json.load(urllib.request.urlopen(req,timeout=30))
profile_diff=[]
marker='Skills standard locaux — raccordement du 1 novembre 2026'
addition=f'''\n\n{marker} : les 18 Skills Office/PDF, pédagogiques, DevOps, Draw.io et méthode NetBox sont installés sur le Mac et raccordés au catalogue natif du terminal sélectionné. Activer le chargement à la demande par view_skill ; lire seulement les références nécessaires avec les outils disponibles et utiliser les scripts via run_command. Ne pas recopier tous les Skills dans le contexte. Les chemins d’exécution et l’interpréteur documentaire sont dans chaque Skill ; charger {R}/documents.env pour Office/PDF/OCR/Pandoc, ou utiliser les chemins absolus indiqués. MarkItDown est installé à {R}/venvs/markitdown/bin/markitdown. Les livrables vont dans {workspace}. Ces raccordements ne sont pas encore testés : ne pas annoncer de résultat sans sortie réelle. Les MCP locaux configurés pour Qwen Code ne sont pas de nouveaux serveurs HTTP WebUI ; WebUI direct utilise le terminal existant. Les accès et inventaires du lycée seront fournis demain ; ne pas découvrir de cibles non autorisées. Référentiels CIEL/BTS et gabarits restent à fournir. Conserver les règles d’arrêt, missions et services existants.'''
for id in ['jarvis-qwen-code-lab','jarvis-tools-conversation']:
 model=api('/api/v1/models/model?id='+id);(P/(id+'.json')).write_text(json.dumps(model,ensure_ascii=False,indent=2))
 old=model.get('meta',{}).get('builtinTools',{}).get('skills')
 model.setdefault('meta',{}).setdefault('builtinTools',{})['skills']=True
 if marker in model.setdefault('params',{}).get('system',''):raise ValueError('Already configured: '+id)
 model['params']['system']=model['params'].get('system','')+addition
 api('/api/v1/models/model/update',model)
 profile_diff.append({'id':id,'builtinTools.skills':{'before':old,'after':True},'system_append':addition,'other_fields':'preserved'})
(R/'native-connection-manifest.json').write_text(json.dumps({'date':'2026-11-01','status':'configured-not-tested','skills':skills,'profiles':profile_diff,'qwen_mcp_added':list(local),'qwen_existing_mcp_preserved':list(json.loads(before).get('mcpServers',{})),'webui_transport':'existing Open Terminal, native terminal Skills','qwen_transport':'native stdio on next session','functional_tests_run':False,'services_restarted':False,'missions_modified':False,'private_backup':str(P)},ensure_ascii=False,indent=2))
print(json.dumps({'skills_linked':len(skills),'qwen_mcp_added':list(local),'profiles_updated':[x['id'] for x in profile_diff],'status':'configured-not-tested'}))
