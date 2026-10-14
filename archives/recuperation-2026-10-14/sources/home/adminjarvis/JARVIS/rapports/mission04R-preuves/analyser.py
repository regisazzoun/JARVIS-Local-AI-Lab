from pathlib import Path
import json,re,struct
p=Path(__file__).resolve().parent
raw=(p/'dmesg.txt').read_text();cur=(p/'journal-noyau.txt').read_text()
def messages(s):
 return [l.split('kernel: ',1)[-1] if 'kernel: ' in l else re.sub(r'^\[\s*[\d.]+\]\s*','',l) for l in s.splitlines()]
cm=messages(cur)
old={}
for m in ['04O','04P']:
 j=json.loads((p.parent/('mission'+m+'-preuves')/'initial'/'journal-noyau.json').read_text());old[m]=messages(j['stdout'])
root=lambda ls:[l for l in ls if re.search(r'root bus resource|PCI host bridge|Using host bridge windows|ECAM .*only partially',l)]
norm=lambda l:re.sub(r'0x[Ff][Ff][Ff][Ff][0-9a-fA-F]+','<adresse>',l)
errors=lambda ls:sorted(set(norm(l) for l in ls if re.search(r'ACPI (?:Error|Warning|BIOS Error)|DMAR.*\b(?:fault|error|failed|failure)\b|IOMMU.*\b(?:fault|error|failed|failure)\b|AER.*(?:error|fatal)|DPC.*(?:containment|trigger)',l,re.I)))
result={'intel_mentions_exactes_dmesg':len(re.findall(r'0000:00:02\.0',raw)), 'intel_mentions_exactes_journal':len(re.findall(r'0000:00:02\.0',cur)),'racine_actuelle':root(cm),'comparaison_racine':{},'erreurs_signatures':{}}
for m,ls in old.items():
 result['comparaison_racine'][m]={'identique':root(cm)==root(ls),'avant':root(ls)}
 result['erreurs_signatures'][m]={'nouvelles':sorted(set(errors(cm))-set(errors(ls))),'disparues':sorted(set(errors(ls))-set(errors(cm))),'actuelles':errors(cm)}
# Check the three historical Intel BAR ranges against all current memory or I/O resources.
pci=json.loads((p/'pci-sysfs.json').read_text());bars=[('BAR0',0x80000000,0x80ffffff,0x200),('BAR2',0xa0000000,0xafffffff,0x200),('BAR4',0x3000,0x303f,0x100)]
result['collisions_BAR_Intel_historiques']={}
for name,a,b,kind in bars:
 hits=[]
 for dev,v in pci.items():
  for idx,line in enumerate(v['resource'].splitlines()):
   s,e,flags=map(lambda x:int(x,16),line.split())
   if flags&kind and e>=s and (s or e) and max(a,s)<=min(b,e):hits.append({'bdf':dev,'index':idx,'debut':hex(s),'fin':hex(e),'flags':hex(flags)})
 result['collisions_BAR_Intel_historiques'][name]=hits
# Decode length-checked DMAR structures and numeric scope paths; no hardware method execution.
b=(p/'acpi-DMAR.bin').read_bytes();ds=[];off=48
while off+4<=len(b):
 typ,n=struct.unpack_from('<HH',b,off)
 if n<4 or off+n>len(b):raise ValueError('DMAR invalid length')
 entry={'type':typ,'length':n}
 if typ==0:
  flags,seg,base=struct.unpack_from('<BxHQ',b,off+4);entry.update(flags=flags,segment=seg,base=hex(base));scopeoff=off+16
 elif typ==1:
  seg,base,end=struct.unpack_from('<HQQ',b,off+6);entry.update(segment=seg,base=hex(base),end=hex(end));scopeoff=off+24
 else:scopeoff=off+n
 scopes=[]
 while scopeoff+6<=off+n:
  st,sl=struct.unpack_from('<BB',b,scopeoff)
  if sl<6 or scopeoff+sl>off+n:raise ValueError('DMAR invalid scope')
  scopes.append({'type':st,'bus_initial':b[scopeoff+5],'path':[{'device':b[i],'function':b[i+1]} for i in range(scopeoff+6,scopeoff+sl,2)]});scopeoff+=sl
 entry['scopes']=scopes;ds.append(entry);off+=n
result['DMAR']=ds
result['chronologie_dmesg']=[l for l in raw.splitlines() if re.search(r'PCI host bridge|00:00.0: \[|00:01.2: \[|00:01.2: bridge window.*assigned|vgaarb|efifb: |81:00.0: \[|No i915 binding|00:02\.0',l)]
(p/'analyse.json').write_text(json.dumps(result,indent=2))
for m in old:print(m,'root identique',result['comparaison_racine'][m]['identique'],'nouvelles erreurs ACPI/DMAR',result['erreurs_signatures'][m]['nouvelles'])
print('Collisions Intel:',result['collisions_BAR_Intel_historiques']);print('DMAR:',json.dumps(ds))
