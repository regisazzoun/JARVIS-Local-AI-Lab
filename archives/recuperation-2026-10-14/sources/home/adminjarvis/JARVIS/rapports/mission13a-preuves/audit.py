import pathlib,hashlib,json,subprocess,urllib.request,datetime,sys,os
P=pathlib.Path('/home/adminjarvis/JARVIS/rapports/mission13a-preuves')
def cmd(*a):
 p=subprocess.run(a,text=True,capture_output=True);return {'code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
configs=[pathlib.Path('/etc/systemd/system/jarvis-ollama.service'),pathlib.Path('/etc/systemd/system/jarvis-open-webui.service')]
configs+=list(pathlib.Path('/home/adminjarvis/JARVIS/open-webui').glob('*.yaml'))+list(pathlib.Path('/home/adminjarvis/JARVIS/open-webui').glob('.env*'))
configs+=list(pathlib.Path('/etc/systemd/system/jarvis-ollama.service.d').glob('*'))+list(pathlib.Path('/etc/systemd/system/jarvis-open-webui.service.d').glob('*'))
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'configs':{str(p):sha(p) for p in configs if p.is_file()},'ollama_models':{},'services':cmd('systemctl','is-active','jarvis-ollama.service','jarvis-open-webui.service'),'units':cmd('systemctl','show','jarvis-ollama.service','jarvis-open-webui.service','-p','FragmentPath','-p','DropInPaths'),'gpu':cmd('nvidia-smi','--query-gpu=name,memory.used,memory.total','--format=csv'),'gpu_processes':cmd('nvidia-smi','--query-compute-apps=pid,process_name,used_memory','--format=csv'),'listeners':cmd('ss','-ltnup'),'memory':cmd('free','-b'),'disk':cmd('df','-B1','/opt','/tmp'),'dpkg':cmd('dpkg-query','-W','-f=${binary:Package}\t${Version}\t${db:Status-Abbrev}\n'),'kernel':cmd('uname','-r'),'python':cmd('python3','--version'),'docker':cmd('docker','ps','--format','{{.Names}}\t{{.Image}}\t{{.Status}}')}
for endpoint in ('tags','ps','version'):
 with urllib.request.urlopen('http://127.0.0.1:11434/api/'+endpoint,timeout=5) as f:r['ollama_'+endpoint]=json.load(f)
for p in sorted(pathlib.Path('/home/adminjarvis/JARVIS/ollama/models').rglob('*')):
 if p.is_file():r['ollama_models'][str(p)]={'bytes':p.stat().st_size,'sha256':sha(p)}
(P/(sys.argv[1]+'.json')).write_text(json.dumps(r,indent=2))
if sys.argv[1]=='before':
 backup=P/'backup-configs';backup.mkdir(mode=0o700,exist_ok=True)
 import shutil
 for p in configs:
  if p.is_file():
   q=backup/str(p).lstrip('/');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);q.chmod(0o600)
 os.chmod(backup,0o700)
print(json.dumps({'phase':sys.argv[1],'configs':r['configs'],'model_files':len(r['ollama_models']),'services':r['services'],'gpu':r['gpu'],'ollama_ps':r['ollama_ps']},indent=2))
