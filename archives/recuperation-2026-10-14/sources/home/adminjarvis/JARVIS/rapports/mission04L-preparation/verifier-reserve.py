#!/usr/bin/env python3
"""Analyse hors ligne des preuves. Aucun accès PCI ni modification du système."""
from pathlib import Path
import sys,json,re
if len(sys.argv)!=2:sys.exit('Usage : python3 verifier-reserve.py DOSSIER_PREUVES')
p=Path(sys.argv[1]);s=json.loads((p/'pci-sysfs.json').read_text());result={'dossier':str(p),'checks':[]}
def check(name,ok,detail):result['checks'].append({'controle':name,'ok':bool(ok),'detail':detail})
def res(b,i):
 try:return tuple(int(x,16) for x in s[b]['resource'].splitlines()[i].split())
 except Exception:return (0,0,0)
def active(r):return bool(r[2]&0x200) and r[0]<=r[1] and not(r[2]&0x30000000)
def decoded(b,i):
 d=bytes.fromhex(s[b]['config64']['hex'])
 if i==14:return ((int.from_bytes(d[32:34],'little')&0xfff0)<<16,((int.from_bytes(d[34:36],'little')&0xfff0)<<16)|0xfffff)
 a=int.from_bytes(d[36:38],'little');z=int.from_bytes(d[38:40],'little')
 start=(a&0xfff0)<<16;end=((z&0xfff0)<<16)|0xfffff
 if a&15==1:start|=int.from_bytes(d[40:44],'little')<<32
 if z&15==1:end|=int.from_bytes(d[44:48],'little')<<32
 return start,end
bridges=['0000:00:01.2','0000:7b:00.0','0000:7c:01.0'];wins=[]
for b in bridges:
 if b not in s:check(b,False,'pont absent');continue
 d=bytes.fromhex(s[b]['config64']['hex']);check(b+' décodage mémoire',int.from_bytes(d[4:6],'little')&2,'COMMAND.MEM')
 for i,label in [(14,'NP'),(15,'PREF')]:
  r=res(b,i);check(b+' '+label+' attribuée',active(r),[hex(x) for x in r])
  check(b+' '+label+' registres/sysfs',decoded(b,i)==r[:2],{'registres':[hex(x) for x in decoded(b,i)],'sysfs':[hex(x) for x in r[:2]]})
 wins.append(res(b,15));check(b+' PREF64',(d[36]&15)==1 and (d[38]&15)==1,'type des registres base et limite')
for parent,child in zip(bridges,bridges[1:]):
 for i,label in [(14,'NP'),(15,'PREF')]:
  a,z,_=res(parent,i);ca,cz,_=res(child,i);check(child+' couvert '+label,a<=ca<=cz<=z,parent)
free=[]
if len(wins)==3 and all(active(r) for r in wins):
 a=max(r[0] for r in wins);z=min(r[1] for r in wins);free=[(a,z)] if a<=z else []
 # Retirer les BAR/ROM déjà attribués des descendants du port cible.
 path=s[bridges[-1]]['path']+'/'
 for b,r in s.items():
  if not r['path'].startswith(path):continue
  for i in range(7):
   ca,cz,fl=res(b,i)
   if not active((ca,cz,fl)):continue
   new=[]
   for lo,hi in free:
    if cz<lo or ca>hi:new.append((lo,hi));continue
    if lo<ca:new.append((lo,ca-1))
    if cz<hi:new.append((cz+1,hi))
   free=new
check('réserve PREF libre contiguë 512 Mio',any(z-a+1>=512*1048576 for a,z in free),[[hex(a),hex(z)] for a,z in free])
placements=[]
for a,z in free:
 b1=(a+0xfffffff)&~0xfffffff;b3=(b1+0x10000000+0x1ffffff)&~0x1ffffff
 if b3+0x2000000-1<=z:placements.append({'bar1':[hex(b1),hex(b1+0xfffffff)],'bar3':[hex(b3),hex(b3+0x1ffffff)]})
check('placement aligné simultané BAR1/BAR3',bool(placements),placements)
iomem=(p/'proc_iomem.txt').read_text();roots=[]
for line in iomem.splitlines():
 m=re.fullmatch(r'([0-9a-f]+)-([0-9a-f]+) : PCI Bus 0000:00',line)
 if m:roots.append(tuple(int(x,16) for x in m.groups()))
check('apertures hôte non masquées',bool(roots) and any(z>0 for a,z in roots),[[hex(a),hex(z)] for a,z in roots])
if wins:check('PREF racine dans aperture hôte',any(a<=wins[0][0]<=wins[0][1]<=z for a,z in roots),[hex(x) for x in wins[0][:2]])
# Fenêtres de branches sœurs : aucune intersection entre fenêtres actives du même type.
for parent in bridges[:2]:
 children=[b for b,r in s.items() if Path(r['path']).parent.name==parent and r.get('class','').strip().startswith('0x0604')]
 for i,label in [(14,'NP'),(15,'PREF')]:
  overlaps=[]
  for n,b in enumerate(children):
   for c in children[n+1:]:
    rb,rc=res(b,i),res(c,i)
    if active(rb) and active(rc) and max(rb[0],rc[0])<=min(rb[1],rc[1]):overlaps.append([b,c])
  check(parent+' branches sœurs '+label+' disjointes',not overlaps,overlaps)
check('GPU NVIDIA absent',not any(r.get('vendor','').strip()=='0x10de' for r in s.values()),'contrôle pré-branchement')
result['verdict_automatique']='ARRET' if any(not c['ok'] for c in result['checks']) else 'CONTROLES_RESERVE_OK_VALIDATIONS_COMPLEMENTAIRES_REQUISES'
result['limites']='Ne valide pas seul santé système, nouveaux journaux, ACPI, descendants complets, absence de collisions globales ou autorisation de branchement. Voir rapport 04L.'
print(json.dumps(result,indent=2,ensure_ascii=False))
