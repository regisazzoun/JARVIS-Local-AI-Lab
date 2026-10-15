from pathlib import Path
import urllib.request,json,subprocess,hashlib,tarfile,io,concurrent.futures
p=Path(__file__).parent;records=json.loads((p/'transaction-exacte.json').read_text());(p/'debs').mkdir(exist_ok=True);(p/'controles').mkdir(exist_ok=True)
def inspect(d):
 name=d['Package'];f=p/'debs'/Path(d['Filename']).name
 base='https://developer.download.nvidia.com/compute/cuda/repos/debian13/x86_64/' if d['Filename'].startswith('./') else 'https://deb.debian.org/debian/'
 b=f.read_bytes() if f.exists() else urllib.request.urlopen(base+d['Filename'],timeout=60).read();assert hashlib.sha256(b).hexdigest()==d['SHA256'];f.write_bytes(b)
 c=p/'controles'/name;subprocess.run(['dpkg-deb','-e',str(f),str(c)],check=True)
 data=subprocess.run(['dpkg-deb','--fsys-tarfile',str(f)],capture_output=True,check=True).stdout;t=tarfile.open(fileobj=io.BytesIO(data));texts=[];files=[]
 for x in t.getmembers():
  files.append(x.name)
  if x.isfile() and (any(x.name.startswith(q) for q in ['./etc/','./usr/lib/udev/','./usr/lib/systemd/','./usr/share/initramfs-tools/']) or x.name.endswith('dkms.conf')):
   texts.append(x.name+'\n'+t.extractfile(x).read().decode(errors='replace'))
 (p/'controles'/name/'fichiers.txt').write_text('\n'.join(files));(p/'controles'/name/'configuration-donnees.txt').write_text('\n\n'.join(texts))
 if name=='nvidia-kernel-open-dkms':
  for suffix in ['kernel-open/conftest.sh','kernel-open/Kbuild','kernel-open/nvidia-uvm/uvm_hmm.c','kernel-open/nvidia/nv-clk.c']:
   match=next((x for x in t.getmembers() if x.isfile() and x.name.endswith(suffix)),None)
   if match:(p/('source-'+suffix.replace('/','-'))).write_bytes(t.extractfile(match).read())
 return {'Package':name,'Version':d['Version'],'SHA256':d['SHA256'],'verified':True,'URL':base+d['Filename']}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:result=list(ex.map(inspect,records))
(p/'inspection-paquets.json').write_text(json.dumps(result,indent=2));print('Inspection et SHA256 OK:',len(result),'paquets')
