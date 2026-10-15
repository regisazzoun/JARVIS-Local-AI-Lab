from pathlib import Path
import json,sys,itertools
p=Path(sys.argv[1]);s=json.loads((p/'pci-sysfs.json').read_text()); old=json.loads(Path('/home/adminjarvis/JARVIS/rapports/mission04L-preparation/hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-221729/pci-sysfs.json').read_text())
def resources(r):return [tuple(int(x,16) for x in line.split()) for line in r['resource'].splitlines()]
def active(t):return t[2]&0x200 and not t[2]&0x30000000 and t[0]<=t[1]
def contains(a,b):return active(a) and a[0]<=b[0]<=b[1]<=a[1]
checks=[]; bridges=[]; changed=[]
for b,r in s.items():
 rr=resources(r)
 if b in old and (r['resource']!=old[b]['resource'] or r['driver']!=old[b]['driver']):changed.append({'bdf':b,'before':old[b],'after':r})
 isbridge=r['class'].strip().startswith('0x0604')
 if isbridge:
  d=bytes.fromhex(r['config64']['hex']); reg={hex(i):hex(int.from_bytes(d[i:i+n],'little')) for i,n in [(4,2),(0x20,2),(0x22,2),(0x24,2),(0x26,2),(0x28,4),(0x2c,4)]}
  bridges.append({'bdf':b,'id':r['vendor'].strip()+':'+r['device'].strip(),'driver':r['driver'],'parent':Path(r['path']).parent.name,'registers':reg,'NP':rr[14],'PREF':rr[15],'PREF_type':[d[36]&15,d[38]&15]})
 for i,t in enumerate(rr):
  if not active(t) or i>6 and i not in [14,15]:continue
  for parent in Path(r['path']).parents:
   pb=parent.name
   if pb not in s or not s[pb]['class'].strip().startswith('0x0604'):continue
   pr=resources(s[pb]);allowed=[15,14] if t[2]&0x2000 else [14]
   checks.append({'bdf':b,'resource':i,'parent':pb,'range':t,'ok':any(contains(pr[j],t) for j in allowed)})
# Check BARs and bridge windows belonging to immediate children, separately for memory only.
collisions=[]
parents={Path(r['path']).parent.name for r in s.values()}
for parent in parents:
 entries=[]
 for b,r in s.items():
  if Path(r['path']).parent.name!=parent:continue
  for i,t in enumerate(resources(r)):
   if (i<=6 or i in [14,15]) and active(t):entries.append((b,i,t))
 for (b,i,a),(c,j,z) in itertools.combinations(entries,2):
  if max(a[0],z[0])<=min(a[1],z[1]):collisions.append({'parent':parent,'a':[b,i,a],'b':[c,j,z]})
result={'bridges':bridges,'inclusions':checks,'inclusion_failures':[x for x in checks if not x['ok']],'same_level_memory_collisions':collisions,'changes':changed,'limits':'Root apertures and non-PCI reserved regions cannot be checked with masked iomem. Firmware routing not tested.'}
print(json.dumps(result,indent=2))
