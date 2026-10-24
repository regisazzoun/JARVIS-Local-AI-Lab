#!/usr/bin/env python3
"""Physical postboot dashboard: actual installed-host state, no install commands."""
import json,time,subprocess,sys
from pathlib import Path

def show():
 print('\033[2J\033[HJARVIS — MISSION 14B — DELL N°2',flush=True)
 print('Suivi installé — actualisation toutes les 5 secondes\n')
 print('[OK] Debian '+Path('/etc/debian_version').read_text().strip()+' — noyau '+subprocess.getoutput('uname -r'))
 r=subprocess.run(['systemctl','is-active','ssh'],capture_output=True,text=True)
 print(('[OK]' if r.returncode==0 else '[ERREUR]')+' SSH : '+r.stdout.strip())
 print('\nRAID réellement observé :\n'+Path('/proc/mdstat').read_text())
 p=Path('/var/lib/jarvis/mission14b/postboot.json')
 if p.exists():
  d=json.loads(p.read_text());checks=d.get('checks',{});print('Réception technique au démarrage :')
  for key,label in [('uuid_match','Identité Dell2'),('storage_clean','RAID sain, racine miroir et deux ESP'),('esp_copies_equal','Copies EFI identiques'),('driver_load','Pilote NVIDIA chargé'),('two_gpus','Deux GPU reconnus'),('cuda_all_devices','Calcul CUDA vérifié sur chaque GPU'),('clock_synchronized','Horloge synchronisée')]:print(('[OK] ' if checks.get(key) is True else '[À CONTRÔLER] ')+label)
  print('\nGPU réellement mesurés :\n'+d.get('details',{}).get('gpu',{}).get('stdout','Mesure non disponible'))
  print('CUDA :\n'+d.get('details',{}).get('cuda',{}).get('stdout','Test non disponible'))
  print('Les preuves sont conservées ; la réception finale et le contrôle SSH externe restent distincts.')
 else:print('[EN COURS] Réception après démarrage ; attente des résultats réels NVIDIA/CUDA.')
 print('\nAlt+F1 : connexion — Alt+F8 : ce suivi. Ollama/routage/charges inchangés.')
 sys.stdout.flush()
while True:
 try:show()
 except Exception as e:print('État partiel : '+str(e),flush=True)
 time.sleep(5)
