from pathlib import Path
import subprocess,json,sys
p=Path(__file__).resolve().parents[2]
items=[('@lukemorales/query-key-factory','1.3.4','@lukemorales+query-key-factory+1.3.4.patch'),('@ronas-it/rtkq-entity-api','1.1.1','@ronas-it+rtkq-entity-api+1.1.1.patch')]
for name,version,file in items:
 actual=json.loads((p/'node_modules'/name/'package.json').read_text())['version']
 if actual!=version:raise RuntimeError('Unexpected dependency version: '+name)
 patch=p/'patches'/file;text=patch.read_text()
 targets=[line[6:] for line in text.splitlines() if line.startswith('+++ b/')]
 if not targets or any(not t.startswith('node_modules/'+name+'/dist/') or '..' in Path(t).parts for t in targets):raise RuntimeError('Patch target outside reviewed dependency')
 dry=subprocess.run(['patch','-p1','--batch','--forward','--dry-run'],input=text,cwd=p,text=True,capture_output=True)
 if dry.returncode==0:subprocess.run(['patch','-p1','--batch','--forward'],input=text,cwd=p,text=True,check=True)
 else:
  reverse=subprocess.run(['patch','-p1','--batch','--reverse','--dry-run'],input=text,cwd=p,text=True,capture_output=True)
  if reverse.returncode:raise RuntimeError('Patch incompatible or partially applied: '+file)
  print('Already applied:',name)
node=sys.argv[1]
for name in ['index.js','index.mjs']:subprocess.run([node,'--check',str(p/'node_modules/@ronas-it/rtkq-entity-api/dist'/name)],check=True)
print('Reviewed dependency patches and syntax verified')
