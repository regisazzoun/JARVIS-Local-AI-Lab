#!/usr/bin/env python3
"""Validation hors ligne ; ne lit que les preuves fournies, aucune opération PCI."""
import json,sys,subprocess
from pathlib import Path
p=Path(sys.argv[1]);s=json.loads((p/'pci-sysfs.json').read_text());checks=[]
def res(b,i):return tuple(int(x,16) for x in s[b]['resource'].splitlines()[i].split())
def active(t):return bool(t[2]&0x200) and not t[2]&0x30000000 and t[0]<=t[1]
def add(n,ok,d):checks.append({'check':n,'ok':bool(ok),'detail':d})
for b in ['0000:00:01.2','0000:7b:00.0','0000:7c:01.0','0000:7c:04.0']:
 if b not in s:add(b,False,'absent');continue
 a,z,f=res(b,14);size=z-a+1 if active((a,z,f)) else 0
 minimum=(66 if b in ['0000:00:01.2','0000:7b:00.0'] else 32)*1048576
 add(b+' NP dimensionnement candidat',size>=minimum,{'start':hex(a),'end':hex(z),'bytes':size,'expected_min':minimum})
 if b=='0000:7c:01.0':
  descendants=[d for d,r in s.items() if r['path'].startswith(s[b]['path']+'/')];add('port cible vide',not descendants,descendants)
  # Modèle conservateur : BAR0 16M aligné, puis ROM/audio/UCSI/USB internes dans 1M,
  # et 1M séparé pour la branche USB du boîtier. Ce modèle valide les besoins connus,
  # pas les futures demandes de réserves des ponts externes.
  gpu=(a+0xffffff)&~0xffffff;gpu_end=gpu+17*1048576-1;usb_start=gpu_end+1;usb_end=usb_start+1048576-1
  add('placement NP connu aligné BAR0 et fonctions Core',active((a,z,f)) and usb_end<=z,{'GPU_window':[hex(gpu),hex(gpu_end)],'USB_window':[hex(usb_start),hex(usb_end)],'BAR0':[hex(gpu),hex(gpu+0xffffff)]})
print(json.dumps({'checks':checks,'decision':'ARRET' if any(not x['ok'] for x in checks) else 'NP_MODELE_OK_VALIDATIONS_COMPLEMENTAIRES_REQUISES','limits':'Doit compléter analyseur 04L, inclusions/collisions de tous les descendants et iomem, journaux et validations humaines. Pas de prédiction exacte du hotplug externe.'},indent=2))
