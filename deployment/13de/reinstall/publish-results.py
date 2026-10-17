#!/usr/bin/env python3
"""Publish only a redacted evidence summary, never private inventories or credentials."""
import argparse,json,pathlib,subprocess,time
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);p.add_argument('--watch',action='store_true');a=p.parse_args();b=a.session.resolve();root=pathlib.Path(__file__).resolve().parents[3]
if a.watch:
 end=time.monotonic()+30000
 while time.monotonic()<end:
  if any((b/n).exists() for n in ['complete.json','ai-error.txt','controller-error.txt']):break
  time.sleep(5)
 else:raise RuntimeError('No terminal evidence to publish')
state=json.loads((b/'progress.json').read_text());complete=(b/'complete.json').exists();metadata=json.loads((b/'complete.json').read_text()) if complete else {}
status='RÉCEPTION COMPLÈTE VALIDÉE' if complete else 'INCOMPLET — consulter les preuves privées et reprendre sans réinstallation aveugle'
text='# Mission 13D-E / 14 — réception de la nouvelle tentative\n\nDate : '+time.strftime('%Y-%m-%d %H:%M %Z')+'\n\n**'+status+'**\n\nChaque validation ci-dessous provient des contrôles exécutés, pas de la présence de code.\n\n| Tâche | État | Preuve / réserve |\n| --- | --- | --- |\n'
for task,d in state.items():text+='| '+task+' | '+d['status']+' | '+d.get('detail','Non exécutée ou non encore validée').replace('|','/').replace('\n',' ')+' |\n'
text+='\n## Périmètre et réserves\n\nComptes demandés : adminjarvis et jarvis-bootstrap, mot de passe utilisateur privé identique ; secours par mot de passe conservé. Réinstallation de la racine uniquement prévue sur miroir/GPT/ESP existants, sans recréation volontaire du RAID. Les étapes non validées dans le tableau ne sont pas réputées réussies. Aucun essai physique de retrait des disques ni de seconde RTX 3090 alimentée. Aucun test de microphone physique ; les essais vocaux utilisent un WAV synthétique. Voix, outils et mémoire SQLite/FTS5 restent sur le Mac mini, sans base parallèle.\n'
if complete:text+='\nPilote NVIDIA : '+metadata['driver']+' ; Ollama : '+metadata['ollama']+' ; modèles réellement testés : '+', '.join(metadata['models'])+'.\n'
text+='\nLes journaux, inventaires, UUID, clés et secrets restent sous deployment/13de/private/reinstall-02, hors Git. Les éventuelles erreurs détaillées et données de test sont privées. Aucune fusion main.\n'
report=root/'docs/missions/13D-E/RECEPTION-MISSION14.md';report.write_text(text)
for rel in ['SUIVI.md','ROADMAP.md']:
 path=root/rel;withtext='\n\n## Réception nouvelle tentative Dell 13D-E / 14\n\n'+status+'. Voir [réception de mission](docs/missions/13D-E/RECEPTION-MISSION14.md) pour les preuves et réserves par tâche.\n'
 path.write_text(path.read_text()+withtext)
path=root/'docs/missions/13D-E/RAPPORT-FINAL.md';path.write_text('# Dernière réception 13D-E / 14\n\n'+status+'. Référence : [réception de la nouvelle tentative](RECEPTION-MISSION14.md). Les sections suivantes sont historiques.\n\n'+path.read_text())
files=['docs/missions/13D-E/RECEPTION-MISSION14.md','docs/missions/13D-E/RAPPORT-FINAL.md','SUIVI.md','ROADMAP.md']
secret=(root/'deployment/13de/private/reprise-user-password.txt').read_text().strip()
assert all(secret not in (root/f).read_text() for f in files),'Secret found in proposed publication'
assert subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()=='codex/mission-13de-preparation'
subprocess.run(['git','diff','--check'],cwd=root,check=True)
subprocess.run(['git','add','--']+files,cwd=root,check=True)
subprocess.run(['git','commit','-m','docs(14): publier les résultats observés du déploiement Dell'],cwd=root,check=True)
subprocess.run(['git','push','origin','codex/mission-13de-preparation'],cwd=root,check=True)
print('OBSERVED_RESULTS_PUBLISHED_NO_MERGE')
