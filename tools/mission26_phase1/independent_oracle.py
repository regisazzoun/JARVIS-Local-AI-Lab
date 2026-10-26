"""Codex independent behavioral acceptance; never repairs the candidate."""
import copy
import hashlib
import json
from pathlib import Path
from labtool import normalize, group_entries

checks=[]
def check(name,fn):
 try:
  fn();checks.append({'name':name,'status':'PASS'})
 except Exception as error:
  checks.append({'name':name,'status':'FAIL','error':repr(error)})
def valid(value):
 payload={'count':value,'extra':{'keep':[1,2]}};before=copy.deepcopy(payload)
 got=normalize(payload)
 assert got==before and got is not payload
 assert payload==before
 assert type(got['count']) is int

def invalid(payload):
 before=copy.deepcopy(payload)
 try:normalize(payload)
 except ValueError:pass
 else:raise AssertionError('Expected ValueError')
 assert payload==before

for number in [0,1,10**12]:check('Q1-valid-'+str(number),lambda n=number:valid(n))
for label,payload in [('missing',{}),('bool-true',{'count':True}),('bool-false',{'count':False}),('string',{'count':'2'}),('negative',{'count':-1}),('float',{'count':2.0}),('null',{'count':None})]:check('Q1-invalid-'+label,lambda p=payload:invalid(p))

def grouped():
 rows=[{'label':'a','value':1,'extra':{'keep':True}}, {'label':'b','value':2}, {'label':'a','value':3}]
 before=copy.deepcopy(rows);result=group_entries(rows)
 assert rows==before,'Input mutated'
 assert list(result)==['a','b']
 assert result=={'a':[before[0],before[2]],'b':[before[1]]}
 assert [r['value'] for r in result['a']]==[1,3]
check('Q2-properties-order-labels-no-mutation',grouped)
check('Q2-empty',lambda: (_ for _ in ()).throw(AssertionError()) if group_entries([])!={} else None)
files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('labtool').glob('*.py'))}
print(json.dumps({'actor':'Codex independent acceptance','checks':checks,'pass':sum(c['status']=='PASS' for c in checks),'fail':sum(c['status']=='FAIL' for c in checks),'source_files':files},ensure_ascii=False))
raise SystemExit(1 if any(c['status']=='FAIL' for c in checks) else 0)
