#!/usr/bin/env python3
"""Read-only source integrity audit, resumable application checkpoint fixture."""
from pathlib import Path
import hashlib,json,os,signal,sys,time
STOP=False

def stop(*_):
    global STOP
    STOP=True

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def atomic(p,value):
    tmp=p.with_suffix('.tmp')
    with tmp.open('w') as f:
        json.dump(value,f,sort_keys=True);f.flush();os.fsync(f.fileno())
    tmp.replace(p)

def main():
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    root=Path(__file__).resolve().parent;manifest=json.loads((root/'expected.json').read_text())
    source=Path(manifest['source_root']);checkpoint=root/'checkpoint.json'
    state=json.loads(checkpoint.read_text()) if checkpoint.exists() else {'manifest_id':manifest['manifest_id'],'done':{},'status':'running'}
    assert state['manifest_id']==manifest['manifest_id']
    for item in manifest['files']:
        if STOP:state['status']='paused';atomic(checkpoint,state);return 75
        name=item['path']
        if name in state['done']:continue
        p=source/name;p.resolve().relative_to(source.resolve())
        actual=digest(p);match=actual==item['sha256']
        state['done'][name]={'sha256':actual,'match':match};state['status']='running';atomic(checkpoint,state)
        with (root/'committed.jsonl').open('a') as f:f.write(json.dumps({'path':name,'match':match})+'\n')
        time.sleep(manifest['pace_seconds'])
    rows=[{'path':k,**v} for k,v in sorted(state['done'].items())]
    report={'manifest_id':manifest['manifest_id'],'file_count':len(rows),'expected_count':len(manifest['files']),'mismatches':[r['path'] for r in rows if not r['match']],'actual_root_sha256':hashlib.sha256(json.dumps([{'path':r['path'],'sha256':r['sha256']} for r in rows],sort_keys=True).encode()).hexdigest()}
    state['status']='completed';atomic(checkpoint,state);atomic(root/'report.json',report)
    return 0 if not report['mismatches'] and report['file_count']==report['expected_count'] else 1
if __name__=='__main__':sys.exit(main())
