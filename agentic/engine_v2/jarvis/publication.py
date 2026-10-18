"""Persistent publication retries; failure never discards the local deliverable."""
import hashlib
import json
import time
import uuid
from pathlib import Path
from .host_client import request


def invoke(op,args):
    response=request(op,args)
    result=response['result']
    if result.get('returncode',0):raise RuntimeError(result.get('stderr','Broker operation failed'))
    return result


def enqueue(store,mission,task,args):
    workspace=Path(args['workspace'])
    relative=Path(args['file'])
    if not workspace.is_absolute() or relative.is_absolute() or '..' in relative.parts:
        raise ValueError('workspace absolu et file relatif sans remontée requis')
    body=invoke('host_read_file',{'path':str(workspace/relative)})['stdout']
    sha=hashlib.sha256(body.encode()).hexdigest()
    with store.db() as c:
        existing=c.execute('SELECT id,state FROM publication_outbox WHERE mission=? AND branch=? AND file=? AND sha256=?',
                           (mission,args['branch'],args['file'],sha)).fetchone()
        if existing:return dict(existing)
        ident=uuid.uuid4().hex
        c.execute('INSERT INTO publication_outbox(id,mission,task,repository,branch,workspace,file,sha256,state,updated) VALUES(?,?,?,?,?,?,?,?,?,?)',
                  (ident,mission,task,args['repository'],args['branch'],str(workspace),str(relative),sha,'pending',time.time()))
        store.event(mission,'publication_queued',task,result={'id':ident,'file':str(relative),'sha256':sha},connection=c)
    return {'id':ident,'state':'pending','sha256':sha}


def deliver_one(store):
    with store.db() as c:
        row=c.execute("SELECT * FROM publication_outbox WHERE state IN ('pending','retrying') AND next_run<=? ORDER BY updated LIMIT 1",(time.time(),)).fetchone()
        if not row:return
        row=dict(row)
    try:
        local=invoke('host_read_file',{'path':str(Path(row['workspace'])/row['file'])})['stdout']
        if hashlib.sha256(local.encode()).hexdigest()!=row['sha256']:
            raise ValueError('Le fichier local a changé : conserver cette livraison et enregistrer une nouvelle version explicitement')
        pushed=invoke('host_github',{'repository':row['repository'],'action':'push','path':row['workspace'],'file':row['file'],'branch':row['branch']})
        commit=pushed['stdout'].strip()
        remote=invoke('host_github',{'repository':row['repository'],'action':'file','path':row['file'],'branch':row['branch']})
        value=json.loads(remote['stdout'])
        if not isinstance(value,dict) or hashlib.sha256(value['content'].encode()).hexdigest()!=row['sha256']:
            raise ValueError('Contenu distant différent du rapport local')
        with store.db() as c:
            c.execute("UPDATE publication_outbox SET state='verified',attempts=attempts+1,commit_sha=?,last_error=NULL,updated=? WHERE id=?",(commit,time.time(),row['id']))
            store.event(row['mission'],'publication_verified',row['task'],result={'file':row['file'],'commit':commit,'sha256':row['sha256']},connection=c)
    except Exception as exc:
        attempts=row['attempts']+1
        with store.db() as c:
            c.execute("UPDATE publication_outbox SET state='retrying',attempts=?,last_error=?,next_run=?,updated=? WHERE id=?",(attempts,str(exc),time.time()+min(300,2**min(attempts,8)),time.time(),row['id']))
            store.event(row['mission'],'publication_retry',row['task'],result={'file':row['file'],'error':str(exc)},connection=c)
