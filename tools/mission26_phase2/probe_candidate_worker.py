#!/usr/bin/env python3
"""Codex integration oracle: run real candidate worker/Core/Missions in a private runtime.

No copied worker function and no mocked scheduler. The subprocess has an empty
mission database, slot2 (no publisher), and stops through its real SIGTERM handler.
This tests candidate code, never claims the canonical systemd service was tested.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import uuid

CHILD = '''import sys
from pathlib import Path
from jarvis import worker
from jarvis.core import Core
worker.ROOT=Path(sys.argv[2])
if sys.argv[3]=='changed':
 def controlled_changed_chat(*args,**kwargs):return 'controlled in-process mismatch'
 Core.chat.__code__=controlled_changed_chat.__code__
worker.run(sys.argv[1],2)
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def probe(engine, output, case, expected):
    report_path=output/(case+'-'+uuid.uuid4().hex+'.json')
    with tempfile.TemporaryDirectory(prefix='jarvis-worker-oracle-') as directory:
        runtime=Path(directory)
        cfg=json.loads((engine/'config/example.json').read_text())
        cfg['identity_file']=str(engine/'identity/JARVIS-v2.md')
        if case!='disabled':
            cfg['attestation']={'enabled':True,'candidate_directory':str(engine/'jarvis') if case!='missing' else str(runtime/'absent-candidate'),'output_file':str(report_path)}
        config_path=runtime/'config.json';config_path.write_text(json.dumps(cfg))
        env={**os.environ,'PYTHONPATH':str(engine)+os.pathsep+os.environ.get('PYTHONPATH','')}
        started=time.time()
        process=subprocess.Popen([sys.executable,'-c',CHILD,str(config_path),str(runtime),case],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        report=None;failure=None
        try:
            deadline=time.monotonic()+10
            while time.monotonic()<deadline:
                if process.poll() is not None:break
                if report_path.exists():
                    try:report=json.loads(report_path.read_text())
                    except json.JSONDecodeError:pass
                    if report is not None:break
                if case=='disabled' and time.time()-started>=2:break
                time.sleep(.05)
            if case=='disabled':
                assert process.poll() is None,'Default worker exited unexpectedly'
                assert not report_path.exists(),'Disabled feature unexpectedly emitted a report'
            else:
                assert report is not None,'Worker produced no readable report'
                assert report['pid']==process.pid,'Report not produced by the actual worker subprocess'
                assert started<=report['now']<=time.time(),'Report timestamp outside this execution'
                assert report['verification_status']==expected,(case,report)
                if case in ('match','changed'):
                    results=report['results']
                    assert set(results)=={'jarvis.worker','jarvis.core'},results
                    assert set(results['jarvis.worker']['actual_objects'])=={'run','main'}
                    assert set(results['jarvis.core']['actual_objects'])=={'Core.ollama','Core.chat'}
                    assert results['jarvis.worker']['status']=='match',results
                    assert results['jarvis.core']['status']==('mismatch' if case=='changed' else 'match'),results
                elif case=='missing':
                    assert all(r['status']=='missing' for r in report['results'].values()),report
        except Exception as exc:
            failure=exc
        finally:
            if process.poll() is None:process.send_signal(signal.SIGTERM)
            try:stdout,stderr=process.communicate(timeout=6)
            except subprocess.TimeoutExpired:
                process.kill();stdout,stderr=process.communicate()
                raise AssertionError('Real worker shutdown did not finish')
        if failure is not None:raise AssertionError({'case':case,'reason':str(failure),'stdout':stdout,'stderr':stderr}) from failure
        assert process.returncode==0,{'case':case,'returncode':process.returncode,'stdout':stdout,'stderr':stderr}
        return {'case':case,'observed_status':report['verification_status'] if report else 'NO_REPORT_DISABLED','expected_status':expected,'worker_pid':process.pid,'report_pid':report['pid'] if report else None,'report_path':str(report_path) if report else None,'report_sha256':digest(report_path) if report else None,'returncode':process.returncode,'started_at':started,'finished_at':time.time(),'canonical_service_tested':False,'real_Core_and_Missions':True,'private_runtime_and_empty_queue':True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--engine',default='engine')
    parser.add_argument('--output-dir',default='evidence/worker-attestation')
    args=parser.parse_args();engine=Path(args.engine).resolve();output=Path(args.output_dir).resolve();output.mkdir(parents=True,exist_ok=True)
    sources={name:digest(engine/'jarvis'/name) for name in ('worker.py','core.py','attest.py')}
    results=[probe(engine,output,case,expected) for case,expected in [('match','PASS'),('changed','FAIL'),('missing','INSUFFICIENT'),('disabled','NO_REPORT_DISABLED')]]
    assert sources=={name:digest(engine/'jarvis'/name) for name in sources},'Candidate source changed during verification'
    result={'suite_pass':True,'oracle_sha256':digest(Path(__file__)),'sources_sha256':sources,'cases':results,'scope':'Real candidate worker process with private runtime, no canonical systemd deployment or inference claimed'}
    result_path=output/('result-'+uuid.uuid4().hex+'.json');result_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({**result,'result_path':str(result_path)},ensure_ascii=False))


if __name__=='__main__':main()
