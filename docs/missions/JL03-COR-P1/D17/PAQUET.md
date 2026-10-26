# D17 — synchronisation corrective v5, exécution JARVIS

Directives consultées : AGENTS.md, docs/CHARTE_DIRECTIVES_JARVIS.md, CONTINUITE.md, dernier dossier D17 et reçus36115/36128/36144. Autorisations autonomes conservées, maximum deux contextes, trois échecs comparables puis arrêt ; aucun compteur ni FAIL effacé. Écart corrigé : le projet existe ; seul tests/d17-reception.test.mjs manque sur Dell1. L'assertion a déjà été corrigée par JARVIS sur Dell2, ne pas répéter sed.
Codex a récupéré en lecture le vrai test JARVIS Dell2 et fourni une archive exacte, sans changer ni exécuter de test Dell. Le PASS 2/2 Dell2 reçu36128 porte seulement sur fixtures, aucune réception applicative.
PREMIÈRE ACTION JARVIS : host_remote avec arguments exacts :
{"host": "dell-observe", "action": "project_upload", "project": "jl03-cor-p1-d17", "path": "/opt/jarvis-lab/jl03-cor-p1/D17/d17-jarvis-baseline.zip", "local_path": "/var/lib/jarvis/projects/jl03-cor-p1/D17/d17-jarvis-baseline.zip"}
Puis host_remote project_exec host=dell-observe project=jl03-cor-p1-d17 avec command EXACT ci-dessous. Extraction bornée à un fichier, SHA vérifié, refuse un fichier divergent au lieu de l'écraser. Tu réalises toi-même ces opérations Dell :
python3 - <<'PYSYNC'
from pathlib import Path
import zipfile,hashlib
zpath=Path('d17-jarvis-baseline.zip')
assert hashlib.sha256(zpath.read_bytes()).hexdigest()=='326d01e52d298f283abee9436c2d6740b178cb1cb91ebeacbe541c8e0fd650a1'
p=Path('tests/d17-reception.test.mjs')
with zipfile.ZipFile(zpath) as z:
 assert z.namelist()==['tests/d17-reception.test.mjs']
 data=z.read('tests/d17-reception.test.mjs')
 assert hashlib.sha256(data).hexdigest()=='3675fe4690d0acce362df5bb733cd8a05943f10b97a3ab6f3d92f3f63f7d68c3'
 if p.exists():
  assert p.read_bytes()==data, 'Divergence: conserver fichier existant, ne pas ecraser'
 else:
  p.parent.mkdir(exist_ok=True);p.write_bytes(data)
 print('D17 baseline JARVIS synchronisee',hashlib.sha256(p.read_bytes()).hexdigest())
PYSYNC
Après synchronisation, lance node --test tests/d17-reception.test.mjs sur Dell1 et lis le résultat. Un PASS ne reçoit que cette synchronisation de baseline, pas D17. Ne rejoue jamais sed sur un fichier absent.
ENSUITE ta tâche réelle reste le développement JARVIS sur Dell : host_remote {host:"dell2",action:"telemetry_v3"}, comparer les champs réels à backend/server.py route /api/launcher/resources et site/telemetry.js. Le backend enrichissait Dell1 seulement. Raccorder Dell2, créer des tests important/exécutant le vrai module renderer et la vraie route avec injection explicitement fixture, cas zéro/inconnu/GPU absent/hors ligne/périmé. Retirer assert.ok(true) ; aucune fonction copiée dans le test. Documenter la limite fixtures, jamais inférence réelle. Synchroniser les fichiers effectivement modifiés entre les deux projets Dell via ZIP project_download/project_upload avec SHA, avant tests sur les deux Dell. Le test seul import node:test ne prouve pas le renderer. Exporter candidat ZIP/JSON/MD et RAPPORT.md factuel avant revue Codex. Aucune réception sur prose ou fixtures seules.
Racine distante /opt/jarvis-lab/jl03-cor-p1/D17 : PAS source/. Outils techniques host_remote uniquement ; host_write_file seulement /var/lib/jarvis/projects/jl03-cor-p1/D17/RAPPORT.md. Pas host_exec/ssh/scp, pas de mission_verify avec arguments project_exec. Trois échecs comparables arrêt/analyse et dossier ; garder tous les reçus et compteurs. ZéroGPU n'est pas panne ; 3090+3080 réelles Dell2. Aucun Ollama/modèle/routage/quota/mémoire/JL01/JL02/service modifié. Attribution : coordination et archive exacte Codex, développement/application/tests Dell JARVIS. Capture acceptée préservée ; aucune intégration live directe.
