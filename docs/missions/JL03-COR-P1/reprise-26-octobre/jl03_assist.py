"""Scoped Codex interface assistance. Canonical tools, evidence and gates retained."""
import hashlib,json,re,time
from pathlib import Path

MISSIONS={'16087a18f86d42b7b79296bc93b3a754':('D03',{'D03'}),
'4b96e63671e1458ba93300a0e7980e2f':('D04',{'D04-RESTITUTION'}),
'c5b81d7fa78f4fa7a5c495f30eee741e':('D17',{'D17'})}
BUNDLE_SHA='9b159fd5c8b0abf3660f583d4b5df502d92547508611f6760833270e2aea72a8'
ROOT=Path('/var/lib/jarvis/projects/jl03-cor-p1')


def scope(reg):
 c=reg.context;m=c.get('mission_id');t=c.get('task_id');pair=MISSIONS.get(m)
 if not pair or t not in pair[1]:raise ValueError('JL03 assist: this exact mission and active correction task are required')
 store=reg.mission_store
 if store.get(m)['state']=='interrupted':raise ValueError('Protocol stopped by existing guard; diagnose before resuming')
 task=next(x for x in store.tasks(m) if x['id']==t)
 if task['state']=='validated':raise ValueError('Validated task immutable')
 return m,t,pair[0],task


def native(reg,name,args):
 m,t,_,_=scope(reg);s=reg.mission_store;token=s.begin_call(m,t,name,args);start=time.monotonic()
 result={**reg.execute(name,args),'required_protocol_control':name=='host_read_file','protocol':'jl03.checked.1'};s.finish_call(token,result,time.monotonic()-start)
 return {'invocation':token,'tool':name,'arguments':args,'result':result}


def repair(reg):
 m,t,label,_=scope(reg)
 if label!='D17':raise ValueError('Only D17 has an approved executable candidate repair')
 bundle=ROOT/'D17/d17-real-code-tests.zip'
 if hashlib.sha256(bundle.read_bytes()).hexdigest()!=BUNDLE_SHA:raise ValueError('Approved regression bundle changed; inspect before staging')
 records=[]
 for host in ['dell-observe','dell2']:
  base={'host':host,'project':'jl03-cor-p1-d17'}
  r=native(reg,'host_remote',{**base,'action':'project_upload','local_path':str(bundle),'path':'/opt/jarvis-lab/jl03-cor-p1/D17/d17-real-code-tests.zip'});records.append(r)
  if not r['result'].get('ok'):return {'returncode':1,'actions':records}
  command="python3 - <<'PYCHECK'\nfrom pathlib import Path\nimport hashlib,zipfile\np=Path('d17-real-code-tests.zip')\nassert hashlib.sha256(p.read_bytes()).hexdigest()=="+repr(BUNDLE_SHA)+"\nzipfile.ZipFile(p).extractall('.')\nPYCHECK\npython3 - <<'PYROUTE'\nfrom pathlib import Path\nimport subprocess\nsource=Path('backend/server.py').read_text()\nif \"for host,machine in (('dell-observe','dell-1'),('dell2','dell-2')):\" in source:\n print('Existing two-host candidate retained; real route tests will verify behavior')\nelse:\n subprocess.run(['python3','apply-d17-route-fix.py'],check=True)\nPYROUTE"
  r=native(reg,'host_remote',{**base,'action':'project_exec','command':command});records.append(r)
  if not r['result'].get('ok'):return {'returncode':1,'actions':records}
 return {'returncode':0,'actions':records,'attribution':'Codex supplied patch and tests; JARVIS triggered real broker execution; no live deployment'}


def check(reg):
 m,t,label,task=scope(reg);records=[]
 for c in task['contract'].get('checks',[]):
  if c['tool']!='host_remote' or c.get('arguments',{}).get('host') not in ['dell-observe','dell2']:raise ValueError('Only persisted remote correction checks supported')
  r=native(reg,c['tool'],c['arguments']);records.append(r);res=r['result'];value=res.get('result',{});stdout=value.get('stdout','')
  if not res.get('ok') or (c.get('stdout_contains') and c['stdout_contains'] not in stdout) or re.search(r'^# fail [1-9]\d*\s*$',stdout,re.M):return {'returncode':1,'checks':records,'scope':'Actual remote candidate checks, not browser/acoustic acceptance'}
 summaries=[]
 for row in records:
  args=row['arguments'];v=row['result'].get('result',{});out=v.get('stdout','')
  command=args.get('command','');match=re.search(r'node --test ([^\n]+)',command)
  summaries.append({'host':args['host'],'operation':match.group(1) if match else 'production import check','returncode':v.get('returncode'),
                    'counts':{k:int(n) for k,n in re.findall(r'^# (tests|pass|fail) (\d+)\s*$',out,re.M)},'invocation':row['invocation']})
 event=reg.mission_store.event(m,'jl03_candidate_summary',task=t,actor='JARVIS',result={'status':'PASS','checks':summaries,'scope':'Mechanical summary of actual native receipts, not acoustic/browser acceptance','observed_at':time.time()})
 return {'returncode':0,'checks':records,'summary_event':event,'scope':'Actual remote candidate checks; fixture boundaries remain, no live deployment'}


def fact_report(reg):
 m,t,label,task=scope(reg);s=reg.mission_store
 obs=[o for o in s.observations(m,t) if o['tool']=='jl03_candidate_check' and (o.get('result') or {}).get('ok')]
 if not obs:raise ValueError('Execute jl03_candidate_check successfully first; no synthetic report')
 observed=obs[-1];event=observed['result']['result']['summary_event']
 summary=next(e for e in s.events(m,limit=1000000) if e['id']==event)['result']['checks']
 originals={}
 for row in observed['result']['result']['checks']:originals[row['arguments']['host']]=row['invocation']
 lines=['# '+label+' — contrôles du candidat','','Source mécanique : event:'+str(event)+'.',
        'Reçus originaux par hôte : '+', '.join(originals.values())+'.','','## Résultats actuels','']
 for row in summary:
  counts=row['counts'];suffix=', '.join(k+'='+str(v) for k,v in counts.items()) if counts else 'contrôle sans compteur TAP'
  lines.append('- '+row['host']+' : '+row['operation']+' ; code retour '+str(row['returncode'])+' ; '+suffix+'.')
 lines+=['','## Portée et réserves','',
 'Historique : les FAIL et INSUFFICIENT restent conservés dans le journal et ne sont pas requalifiés par les succès actuels.',
 'Ces contrôles du candidat isolé ne constituent pas une réception acoustique ni une preuve de conversation ou d’inférence utilisateur.',
 'Interface et aides fournies par Codex, opérations de contrôle déclenchées par JARVIS. Autonomie sans assistance non revendiquée.',
 'Aucun déploiement live n’est établi par ces seuls contrôles. Revue indépendante et réserves maintenues.','']
 body='\n'.join(lines);path=task['contract']['report_path']
 # Preserve originals through real broker calls before writing the factual candidate.
 old=native(reg,'host_read_file',{'path':path})
 if old['result'].get('ok'):
  v=old['result']['result'];content=v.get('content',v.get('stdout',''))
  if content:
   saved=native(reg,'host_write_file',{'path':str(Path(path).with_name('RAPPORT-AVANT-ASSIST-'+str(time.time_ns())+'.md')),'content':content})
   if not saved['result'].get('ok'):return {'returncode':1,'error':'Original report could not be archived'}
 written=native(reg,'host_write_file',{'path':path,'content':body})
 if not written['result'].get('ok'):return {'returncode':1,'write':written}
 read=native(reg,'host_read_file',{'path':path})
 return {'returncode':0 if read['result'].get('ok') else 1,'report_path':path,'check_invocation':observed['id'],'read_invocation':read['invocation'],'scope':'Deterministic factual report; narrative verification still required'}


def verify(reg):
 scope(reg);r=native(reg,'mission_verify',{'contract':'active:0'})
 return {'returncode':0 if r['result'].get('ok') else 1,'verification':r}


def finish(reg):
 m,t,_,_=scope(reg);status=reg.mission_store.contract_status(m,t)
 candidate=status.get('completion_candidate')
 if not candidate:return {'returncode':1,'error':'Completion withheld: current canonical prerequisites not satisfied','contract_status':status}
 r=native(reg,'mission_task_complete',candidate)
 return {'returncode':0 if r['result'].get('ok') else 1,'completion':r}


def protocol(reg):
 _,_,label,_=scope(reg)
 sequence=(['jl03_apply_candidate_fix'] if label=='D17' else [])+['jl03_candidate_check','jl03_write_fact_report','jl03_verify_report','jl03_finish_checked_task']
 receipts=[]
 for operation in sequence:
  observed=native(reg,operation,{})
  receipts.append({'operation':operation,'invocation':observed['invocation'],'ok':observed['result'].get('ok')})
  if not observed['result'].get('ok'):
   return {'returncode':1,'stopped_at':operation,'receipts':receipts,'failure':observed['result'],'scope':'No retry or bypass; JARVIS-triggered assisted protocol'}
 return {'returncode':0,'receipts':receipts,'scope':'JARVIS-triggered assisted protocol complete; no autonomous coding or live deployment claimed'}


def register(reg):
 for name,description,fn in [
 ('jl03_run_checked_protocol','Execute the scoped assisted protocol once: candidate repair if D17, actual remote checks, factual report preserving original, real semantic review, conditional canonical completion. No parameters. Stops on first failure; no retry or bypass; Codex-authored workflow triggered by JARVIS.',protocol),
 ('jl03_apply_candidate_fix','D17 only: stage approved real-code tests and apply supplied safe route patch on both Dell candidates; preserve originals, no live deployment.',repair),
 ('jl03_candidate_check','Run exact persisted candidate checks on both Dell hosts with actual broker receipts. No parameters. Does not receive browser/acoustics.',check),
 ('jl03_write_fact_report','After successful candidate check: preserve prior report, write and reread factual report from actual native receipts. No parameters. Does not bypass narrative review.',fact_report),
 ('jl03_verify_report','Run exact active:0 semantic report review through canonical verifier. No parameters. Actual PASS required.',verify),
 ('jl03_finish_checked_task','Complete ONLY when canonical completion_candidate exists after real checks, report read and semantic PASS. No parameters; never forces acceptance.',finish)]:
  reg.specs[name]=(description,{},[],'host_authorized',lambda args,f=fn:f(reg))
