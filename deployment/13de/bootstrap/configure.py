#!/usr/bin/env python3
"""Run takeover + explicitly accepted storage + two Ansible passes. Never self-authorizes."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import argparse,hashlib,json,os,pathlib,re,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('takeover_settings',type=pathlib.Path);p.add_argument('storage_receipt',type=pathlib.Path);a=p.parse_args()
os.umask(0o077)
s=json.loads(a.takeover_settings.read_text());receipt=json.loads(a.storage_receipt.read_text())
assert s.get('administration_authorized') is True,'administrative authorization required'
assert receipt.get('storage_acceptance_complete') is True,'storage receipt missing'
assert receipt['manifest_sha256']==hashlib.sha256(pathlib.Path(s['manifest']).read_bytes()).hexdigest(),'receipt manifest'
assert receipt.get('dual_esp_boot_qualified') is True,'dual ESP boot not qualified'
subprocess.run(['python3',str(ROOT/'bootstrap/takeover.py'),str(a.takeover_settings)],check=True)
b=a.takeover_settings.parent;inventory=b/'inventory.json';data=json.loads(inventory.read_text())
host=data['all']['children']['dell']['hosts']['dell-precision'];host['storage_acceptance_complete']=True
inventory.write_text(json.dumps(data,indent=2)+'\n')
command=['ansible-playbook','-i',str(inventory.resolve()),str(ROOT/'ansible/dell.yml')]
for index in (1,2):
 result=subprocess.run(command,capture_output=True,text=True,cwd=ROOT/'ansible')
 (b/f'ansible-pass-{index}.txt').write_text(result.stdout+'\n'+result.stderr)
 assert result.returncode==0,f'Ansible pass {index} failed; inspect private log'
 if index==2:
  recaps=re.findall(r'\bok=\d+\s+changed=(\d+)\s+unreachable=(\d+)\s+failed=(\d+)',result.stdout)
  assert recaps and all(all(int(v)==0 for v in row) for row in recaps),'second pass not idempotent'
print('Base Ansible configured; second pass changed=0. GPU/AI roles remain excluded.')
