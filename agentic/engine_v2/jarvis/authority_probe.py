"""Model-selected declared regression probes, through existing Authority execution.

Probe argv/source contract is authored by its declared owner, not by the model.
"""
import hashlib,json,shlex,time
from .authority_draft import canonical_call
from .authority_identity import invocation_scope


def declaration_digest(probe):
 return hashlib.sha256(json.dumps(probe,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def probe_command(probe):
 argv=probe['argv'];env=probe.get('env',{});sources=probe['sources']
 if not isinstance(argv,list) or not argv or not all(isinstance(x,str) for x in argv):raise ValueError('Declared probe argv must be a nonempty string array')
 if not isinstance(env,dict) or not all(isinstance(k,str) and isinstance(v,str) for k,v in env.items()):raise ValueError('Invalid declared probe environment')
 program='''import hashlib,pathlib,os,subprocess,sys
for name,expected in SOURCES.items():
 p=pathlib.Path(name)
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
  print('JARVIS_PROBE_NOT_STARTED: immutable source absent or changed',file=sys.stderr);sys.exit(125)
env=os.environ.copy();env.update(ENV)
raise SystemExit(subprocess.run(ARGV,env=env).returncode)
'''
 import re
 replacements={'SOURCES':sources,'ENV':env,'ARGV':argv}
 program=re.sub(r'\b(SOURCES|ENV|ARGV)\b',lambda m:repr(replacements[m[0]]),program)
 return 'python3 -c '+shlex.quote(program)


def run_probe(authority,args):
 parent=canonical_call(authority,'authority_run_probe',args)
 probe=authority.spec.get('authority_probes',{}).get(args['probe_id'])
 if not probe:raise ValueError('Unknown owner-declared probe')
 authority.decision({'selected_probe':args['probe_id'],'executor':args['executor'],'summary':args['summary'],'command_author':probe.get('author','owner probe declaration')})
 command=probe_command(probe)
 request={'issue':args['issue'],'kind':'test','executor':args['executor'],'summary':args['summary'],'command':command}
 token=authority.store.begin_call(authority.m,authority.t,'authority_work',request)
 selection={'parent':parent,'probe_id':args['probe_id'],'declaration_sha256':declaration_digest(probe),'command_author':probe.get('author','owner probe declaration')}
 authority.event('authority_declared_probe_expanded',{**selection,'execution_invocation':token,'model_chooses':'probe id and executor','argv_authored_by_model':False},actor='JARVIS-engine')
 previous=authority.reg.context.get('_authority_declared_probe');authority.reg.context['_authority_declared_probe']=selection
 start=time.monotonic()
 try:
  with invocation_scope(token):result=authority.reg.execute('authority_work',request)
 except Exception as exc:
  authority.store.finish_call(token,{'ok':False,'error':str(exc)},time.monotonic()-start);raise
 finally:
  if previous is None:authority.reg.context.pop('_authority_declared_probe',None)
  else:authority.reg.context['_authority_declared_probe']=previous
 authority.store.finish_call(token,result,time.monotonic()-start)
 if not result.get('ok'):raise ValueError(result.get('error','Declared probe not executed'))
 return {**result['result'],'probe_id':args['probe_id'],'probe_command_author':probe.get('author','owner probe declaration')}


def matrix(spec,state,manifest):
 probes=spec.get('authority_probes',{});out={host:{key:{'status':'NOT_EXECUTED'} for key in probes} for host in ('Dell1','Dell2')}
 for reference,row in sorted(state.get('executions',{}).items(),key=lambda item:int(item[0])):
  host=row.get('host');key=row.get('probe_id')
  if host not in out or key not in probes or row.get('before')!=manifest or row.get('after')!=manifest:continue
  if row.get('probe_declaration_sha256')!=declaration_digest(probes[key]):continue
  execution=row['execution'];status='NOT_EXECUTED' if row.get('test_execution_status')=='NOT_EXECUTED' else 'PASS' if execution['returncode']==0 and not execution.get('output_truncated') else 'FAIL'
  out[host][key]={'status':status,'reference':int(reference),'process_returncode':execution['returncode']}
 return out
