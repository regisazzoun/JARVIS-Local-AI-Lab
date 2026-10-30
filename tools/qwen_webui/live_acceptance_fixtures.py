"""Create controlled live acceptance sources in a NEW authorized project.

This prepares fixtures, never claims that JARVIS ran or passed them.
"""
import argparse,json,subprocess,hashlib
from pathlib import Path

SEQUENTIAL="import json,sys,secrets,time\nfrom pathlib import Path\nstate=Path('progress.json');journal=Path('steps.jsonl')\nif not state.exists():state.write_text(json.dumps({'step':0,'nonce':'START'}))\nx=json.loads(state.read_text())\nif len(sys.argv)==1:\n print(json.dumps({'next_step':x['step']+1,'nonce':x['nonce'],'status':'DONE' if x['step']==14 else 'CONTINUE'}));raise SystemExit(0)\nif len(sys.argv)!=3 or int(sys.argv[1])!=x['step']+1 or sys.argv[2]!=x['nonce'] or x['step']>=14:raise SystemExit('Wrong step/nonce or already done')\nr={'step':int(sys.argv[1]),'previous_nonce':x['nonce'],'next_nonce':secrets.token_hex(6),'created':time.time()}\nwith journal.open('a') as f:f.write(json.dumps(r)+'\\n')\nstate.write_text(json.dumps({'step':r['step'],'nonce':r['next_nonce']}))\nprint(json.dumps({'observed_step':r['step'],'next_step':r['step']+1,'nonce':r['next_nonce'],'status':'DONE' if r['step']==14 else 'CONTINUE'}))\n"
PRICE='def total(items):\n    return sum(items) - 1\n'
PRICE_TEST='import unittest\nfrom price import total\nclass Price(unittest.TestCase):\n def test_total(self):\n  self.assertEqual(total([2,3,4]),9)\n  self.assertEqual(total([]),0)\nif __name__=="__main__":unittest.main()\n'

def create(destination,kind):
    path=Path(destination).resolve()
    roots=[Path('/home/adminjarvis/JARVIS/qwen-code-projects'),Path('/var/lib/jarvis/projects/qwen-code')]
    if not any(path.is_relative_to(root) and path!=root for root in roots):raise ValueError('Dedicated authorized project required')
    if path.exists() and (not path.is_dir() or any(path.iterdir())):raise ValueError('Refusing to overwrite an existing project')
    path.mkdir(parents=True,exist_ok=True)
    files={'steps.py':SEQUENTIAL} if kind=='sequential' else {'price.py':PRICE,'test_price.py':PRICE_TEST}
    for name,text in files.items():path.joinpath(name).write_text(text)
    for command in [['git','init','-q'],['git','add','--',*files],['git','-c','user.name=Codex','-c','user.email=codex@jarvis.local','commit','-qm','Controlled acceptance fixture']]:
        subprocess.run(command,cwd=path,check=True)
    return {'prepared_by':'Codex','agent_execution':'NOT_RUN','kind':kind,'destination':str(path),'sha256':{name:hashlib.sha256(text.encode()).hexdigest() for name,text in files.items()}}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--destination',required=True);parser.add_argument('--kind',choices=['sequential','coding'],required=True);args=parser.parse_args();print(json.dumps(create(args.destination,args.kind),indent=2))
