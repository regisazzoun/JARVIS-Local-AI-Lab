"""Add isolated executor scopes, never stage or reset application sources.
Run as root with --apply; without it, inspect only. Uses existing pinned SSH profiles.
"""
import argparse,json,os,shlex,shutil,subprocess,time
from pathlib import Path
PROJECT='mission26-phase1'
REMOTE='/opt/jarvis-lab/'+PROJECT
LOCAL=Path('/var/lib/jarvis/projects')/PROJECT
OPTIONS={'root':REMOTE,'gpu':False,'root_readonly':True,'transfer':True,'transfer_local_root':str(LOCAL)}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
 policy=Path('/etc/jarvis/host-policy.json');cfg=json.loads(policy.read_text());original=json.loads(policy.read_text())
 for name in ['dell-observe','dell2']:
  host=cfg['remote_hosts'][name];existing=host.get('project_exec_options',{}).get(PROJECT)
  if existing and existing!=OPTIONS:raise SystemExit('Existing project options differ; preserve them and diagnose')
  print(name,'scope configured' if existing else 'scope absent')
  if args.apply:
   ssh=['ssh','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+host['known_hosts'],'-i',host['identity'],host['user']+'@'+host['address']]
   command=shlex.join(['sudo','install','-d','-m','700','-o',host['user'],REMOTE])
   result=subprocess.run(ssh+[command],capture_output=True,text=True)
   if result.returncode:raise SystemExit('Remote provisioning failed on profile '+name+'; inspect private SSH diagnostic')
   projects=host.setdefault('project_exec_projects',[])
   if PROJECT not in projects:projects.append(PROJECT)
   host.setdefault('project_exec_options',{})[PROJECT]=OPTIONS.copy()
 if not args.apply:return
 LOCAL.mkdir(parents=True,exist_ok=True);shutil.chown(LOCAL,user=cfg['user']);LOCAL.chmod(0o700)
 if str(LOCAL) not in cfg['write_roots']:cfg['write_roots'].append(str(LOCAL))
 # Write roots already permit reads. A later ro-bind of the same path masks RW.
 cfg['read_roots']=[p for p in cfg['read_roots'] if p!=str(LOCAL)]
 if cfg!=original:
  backup=Path('/root')/('jarvis-host-policy-before-'+PROJECT+'-'+str(time.time_ns())+'.json')
  backup.write_text(policy.read_text());backup.chmod(0o600)
  temp=policy.with_name('.host-policy-'+PROJECT+'.tmp');fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
  with os.fdopen(fd,'w') as f:json.dump(cfg,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
  os.replace(temp,policy);print('Additive policy update installed; private backup retained')
 else:print('Policy unchanged; application files and checkpoints preserved')
if __name__=='__main__':main()
