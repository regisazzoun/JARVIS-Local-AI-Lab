#!/usr/bin/env python3
"""Protected reception of an agent-authored program on real and varied inputs.

Only the program is agent-authored. Expected results come from original case
evaluations, never the candidate's declared summary or a successful exit code.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import pwd
import shlex
import shutil
import subprocess
import tempfile
import time

MODEL='qwen3-coder-next:q4_K_M'
ROOT=Path('/opt/jarvis-lab/mission28a')


def expected_scores(comparative,corrected32):
    scores={}
    for row in comparative['cases']+corrected32['cases']:
        passed=row['evaluation']['pass']
        if type(passed) is not bool:raise ValueError('Source evaluation must be Boolean')
        score=scores.setdefault(row['model'],{'passed':0,'total':0})
        score['passed']+=int(passed);score['total']+=1
    return {'mission':'28A','selected_model':MODEL,'model_count':len(scores),'scores':scores}


def variants(comparative,corrected32):
    result=[('original',copy.deepcopy(comparative),copy.deepcopy(corrected32))]
    a,b=copy.deepcopy(comparative),copy.deepcopy(corrected32)
    a['cases'][0]['evaluation']['pass']=not a['cases'][0]['evaluation']['pass']
    b['cases'][0]['evaluation']['pass']=not b['cases'][0]['evaluation']['pass']
    result.append(('changed_evaluations_stale_summaries',a,b))
    a,b=copy.deepcopy(comparative),copy.deepcopy(corrected32)
    a['cases'].pop();result.append(('removed_case_stale_summary',a,b))
    a,b=copy.deepcopy(comparative),copy.deepcopy(corrected32)
    extra=copy.deepcopy(a['cases'][0]);extra['case']='independent_extra_case'
    a['cases'].append(extra);result.append(('added_case_stale_summary',a,b))
    return result


def grade(output,manifest,expected):
    for path in [output,manifest]:
        if path.is_symlink() or not path.is_file() or path.stat().st_size>1000000:
            raise ValueError('Missing, symlinked or oversized result: '+path.name)
    raw=output.read_bytes();actual=json.loads(raw);digest=json.loads(manifest.read_text()).get('sha256')
    exact=all(actual.get(k)==v for k,v in expected.items())
    typed=type(actual.get('model_count')) is int and all(type(v.get(k)) is int for v in actual.get('scores',{}).values() for k in ('passed','total'))
    return {'pass':exact and typed and digest==hashlib.sha256(raw).hexdigest(),
            'scores_match':exact,'integer_counts':typed,'manifest_matches':digest==hashlib.sha256(raw).hexdigest(),
            'expected':expected,'actual':actual,'output_sha256':hashlib.sha256(raw).hexdigest()}


def run():
    source=ROOT/'consolider.py';paths=[ROOT/'quality-comparative.json',ROOT/'quality-32-corrected.json']
    report={'created':time.time(),'verifier':'Codex protected varied-input checker28A','pass':False,'cases_checked':0,'checks':[]}
    if not source.is_file() or source.is_symlink():
        return {**report,'status':'INSUFFICIENT','error':'Missing actual program: /opt/jarvis-lab/mission28a/consolider.py'}
    if source.stat().st_size>256000:raise ValueError('Program too large for targeted reception')
    raw=[p.read_bytes() for p in paths];program=source.read_bytes()
    report['source_sha256']={p.name:hashlib.sha256(v).hexdigest() for p,v in zip(paths,raw)}
    report['program_sha256']=hashlib.sha256(program).hexdigest()
    parent=ROOT/'.independent-reception';parent.mkdir(mode=0o755,exist_ok=True)
    if parent.is_symlink() or parent.stat().st_uid!=0:raise ValueError('Checker workspace must be protected')
    work=Path(tempfile.mkdtemp(prefix='run-',dir=parent));work.chmod(0o755)
    snapshot=work/'program.py';snapshot.write_bytes(program);snapshot.chmod(0o444)
    account=pwd.getpwnam('adminjarvis')
    from remote_project import project_program
    for index,(name,a,b) in enumerate(variants(*map(json.loads,raw))):
        case=work/str(index);case.mkdir(mode=0o755);inputs=case/'inputs';inputs.mkdir(mode=0o755)
        for filename,data in [('comparative.json',a),('corrected32.json',b)]:
            p=inputs/filename;p.write_text(json.dumps(data));p.chmod(0o444)
        inputs.chmod(0o555);outputs=case/'out';outputs.mkdir(mode=0o750);os.chown(outputs,account.pw_uid,account.pw_gid)
        command=shlex.join(['python3',str(snapshot),'--comparative',str(inputs/'comparative.json'),'--corrected32',str(inputs/'corrected32.json'),'--output',str(outputs/'result.json'),'--manifest',str(outputs/'manifest.json')])
        wrapped=project_program(str(ROOT),command,False,root_readonly=True)
        try:
            execution=subprocess.run(['runuser','-u','adminjarvis','--','python3','-c',wrapped],capture_output=True,text=True,timeout=30)
            check=grade(outputs/'result.json',outputs/'manifest.json',expected_scores(a,b)) if execution.returncode==0 else {'pass':False,'error':'Program exited nonzero'}
            check.update(returncode=execution.returncode,stdout=execution.stdout[-1500:],stderr=execution.stderr[-1500:])
        except Exception as error:check={'pass':False,'error':type(error).__name__+': '+str(error)}
        report['checks'].append({'case':name,**check})
    report['cases_checked']=len(report['checks'])
    report['original_sources_unchanged']=all(p.read_bytes()==v for p,v in zip(paths,raw))
    report['pass']=all(c['pass'] for c in report['checks']) and report['original_sources_unchanged']
    report['status']='PASS' if report['pass'] else 'FAIL'
    return report


if __name__=='__main__':
    try:result=run()
    except Exception as error:result={'pass':False,'status':'INSUFFICIENT','cases_checked':0,'error':type(error).__name__+': '+str(error)}
    # Exit0 means the observation was collected; the JSON verdict decides success.
    store=Path('/var/lib/jarvis-program-checks');store.mkdir(mode=0o750,exist_ok=True)
    path=store/('28a-'+str(time.time_ns())+'.json');path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    result['protected_receipt']=str(path);print(json.dumps(result,ensure_ascii=False))
