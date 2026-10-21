"""Install 26B in the existing service. Never change databases or host policy."""
import hashlib,json,os,shutil,sqlite3,subprocess,time
from pathlib import Path
MODULES=['missions.py','mission_store.py','durable_tools.py','durable_cycle.py','tools.py','mission_assurance.py','verification.py']
def main():
 if os.geteuid()!=0:raise SystemExit('sudo required')
 root=Path('/opt/jarvis/conversation');repo=Path(__file__).resolve().parents[2]
 c=sqlite3.connect(root/'runtime/missions.sqlite')
 if c.execute("select count(*) from missions where state='running'").fetchone()[0]:raise SystemExit('Interrupt active mission at tool boundary before installation')
 policy=Path('/etc/jarvis/host-policy.json');before=hashlib.sha256(policy.read_bytes()).hexdigest()
 source=repo/'agentic/engine_v2/jarvis'
 for name in MODULES:compile((source/name).read_text(),str(source/name),'exec')
 backup=Path('/var/backups/jarvis/mission-engine26b')/str(time.time_ns());backup.mkdir(parents=True,mode=0o700)
 rows=[]
 for name in MODULES:
  src=source/name;dst=root/'jarvis'/name
  if dst.exists():shutil.copy2(dst,backup/name)
  tmp=dst.with_suffix('.engine26b');shutil.copyfile(src,tmp);os.chmod(tmp,0o644);os.replace(tmp,dst)
  rows.append({'module':name,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
 assert hashlib.sha256(policy.read_bytes()).hexdigest()==before
 subprocess.run(['systemctl','restart','jarvis-conversation'],check=True)
 print(json.dumps({'backup':str(backup),'modules':rows,'policy_unchanged':True,'created':time.time()}))
if __name__=='__main__':main()
