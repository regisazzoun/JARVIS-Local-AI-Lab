"""Persistent publication retries; failure never discards the local deliverable."""
import hashlib
import ipaddress
import re
import json
import time
import uuid
from contextlib import nullcontext
from pathlib import Path
from .host_client import request, BrokerError


def invoke(op,args):
    response=request(op,args)
    result=response['result']
    if result.get('returncode',0):raise RuntimeError(result.get('stderr','Broker operation failed'))
    return result


def redact_public(body):
    def address(match):
        try:
            ip=ipaddress.ip_address(match.group(0))
            return '[adresse privée masquée]' if not ip.is_global and not ip.is_loopback else match.group(0)
        except ValueError:return match.group(0)
    body=re.sub(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])',address,body)
    body=re.sub(r'(?i)\b[0-9a-f]{2}(?::[0-9a-f]{2}){5}\b','[adresse matérielle masquée]',body)
    body=re.sub(r'(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b','[identifiant unique masqué]',body)
    return body


def enqueue(store,mission,task,args,verified_body=None,connection=None):
    workspace=Path(args['workspace'])
    relative=Path(args['file'])
    if not workspace.is_absolute() or relative.is_absolute() or '..' in relative.parts:
        raise ValueError('workspace absolu et file relatif sans remontée requis')
    body=verified_body if verified_body is not None else invoke('host_read_file',{'path':str(workspace/relative)})['stdout']
    sanitized=redact_public(body)
    if sanitized!=body:
        invoke('host_write_file',{'path':str(workspace/relative),'content':sanitized})
        confirmed=invoke('host_read_file',{'path':str(workspace/relative)})['stdout']
        if confirmed!=sanitized:raise ValueError('Expurgation locale non confirmée')
        body=sanitized
        store.event(mission,'publication_redacted',task,result={'file':str(relative),'editor':'JARVIS-engine','reason':'Private network/hardware identifiers omitted'})
    sha=hashlib.sha256(body.encode()).hexdigest()
    with (nullcontext(connection) if connection is not None else store.db()) as c:
        existing=c.execute('SELECT id,state FROM publication_outbox WHERE mission=? AND branch=? AND file=? AND sha256=?',
                           (mission,args['branch'],args['file'],sha)).fetchone()
        if existing:return dict(existing)
        c.execute("UPDATE publication_outbox SET state='superseded',updated=? WHERE mission=? AND branch=? AND file=? AND state IN ('pending','retrying','needs_revision')",(time.time(),mission,args['branch'],args['file']))
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
    # A new row, renamed file or report body cannot reset a failed target.
    ledger=store.attempt_ledger(row['mission'])
    problem=ledger.problem('publication:'+row['repository']+':'+row['branch'],{'component':'publication','repository':row['repository'],'branch':row['branch']})
    with store.db() as c:
        p=c.execute('SELECT * FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(row['mission'],problem)).fetchone()
        count=max(p['infra_incidents'],row['attempts'])
        if count!=p['infra_incidents']:
            c.execute('UPDATE mission_problems_v2 SET infra_incidents=? WHERE mission=? AND fingerprint=?',(count,row['mission'],problem))
            store.event(row['mission'],'publication_counter_migrated',actor='JARVIS-engine',result={'problem':problem,'legacy_attempts':row['attempts'],'counter':count},connection=c)
        if count>=3 or p['state']=='ESCALATED':
            c.execute("UPDATE publication_outbox SET state='needs_revision',updated=? WHERE id=?",(time.time(),row['id']))
            e=store.event(row['mission'],'p2_escalation',actor='JARVIS-engine',result={'problem':problem,'reason':'Three publication incidents; target blocked before another push','request_to':'Codex','infra_incidents':count},connection=c)
            c.execute("UPDATE mission_problems_v2 SET state='ESCALATED',escalation_event=? WHERE mission=? AND fingerprint=?",(e,row['mission'],problem))
            return
    try:
        local=invoke('host_read_file',{'path':str(Path(row['workspace'])/row['file'])})['stdout']
        if hashlib.sha256(local.encode()).hexdigest()!=row['sha256']:
            raise ValueError('Le fichier local a changé : conserver cette livraison et enregistrer une nouvelle version explicitement')
        if row['attempts']:
            # After a lost reply, observe the actual branch before any mutation.
            # An unavailable read is insufficient and never authorizes replay.
            try:
                prior=invoke('host_github',{'repository':row['repository'],'action':'file','path':row['file'],'branch':row['branch']})
                existing=json.loads(prior['stdout'])
            except Exception as error:
                raise ValueError('Remote outcome cannot be observed before retry; no push dispatched: '+str(error)) from error
            if isinstance(existing,dict) and hashlib.sha256(existing.get('content','').encode()).hexdigest()==row['sha256']:
                with store.db() as c:
                    c.execute("UPDATE publication_outbox SET state='verified',last_error=NULL,updated=? WHERE id=? AND state!='superseded'",(time.time(),row['id']))
                    store.event(row['mission'],'publication_verified',row['task'],actor='JARVIS-engine',result={'file':row['file'],'sha256':row['sha256'],'mode':'independent read after uncertain attempt, no repeated push','commit_observed':False},connection=c)
                return
        pushed=invoke('host_github',{'repository':row['repository'],'action':'push','path':row['workspace'],'file':row['file'],'branch':row['branch']})
        commit=pushed['stdout'].strip()
        if not re.fullmatch(r'[0-9a-f]{40,64}',commit):raise ValueError('Commit GitHub invalide')
        remote=invoke('host_github',{'repository':row['repository'],'action':'file','path':row['file'],'branch':row['branch']})
        value=json.loads(remote['stdout'])
        if not isinstance(value,dict) or hashlib.sha256(value['content'].encode()).hexdigest()!=row['sha256']:
            raise ValueError('Contenu distant différent du rapport local')
        with store.db() as c:
            c.execute("UPDATE publication_outbox SET state='verified',attempts=attempts+1,commit_sha=?,last_error=NULL,updated=? WHERE id=? AND state!='superseded'",(commit,time.time(),row['id']))
            store.event(row['mission'],'publication_verified',row['task'],result={'file':row['file'],'commit':commit,'sha256':row['sha256']},connection=c)
    except Exception as exc:
        attempts=row['attempts']+1
        with store.db() as c:
            needs_revision=isinstance(exc,(ValueError,BrokerError))
            if isinstance(exc,BrokerError):needs_revision=exc.response.get('error_code') in ('PublicationRevisionRequired','PermissionError')
            c.execute('UPDATE mission_problems_v2 SET infra_incidents=infra_incidents+1 WHERE mission=? AND fingerprint=?',(row['mission'],problem))
            incidents=c.execute('SELECT infra_incidents FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(row['mission'],problem)).fetchone()[0]
            if incidents>=3:
                needs_revision=True
                e=store.event(row['mission'],'p2_escalation',actor='JARVIS-engine',result={'problem':problem,'reason':'Three comparable publication incidents','request_to':'Codex','infra_incidents':incidents},connection=c)
                c.execute("UPDATE mission_problems_v2 SET state='ESCALATED',escalation_event=? WHERE mission=? AND fingerprint=?",(e,row['mission'],problem))
            state='needs_revision' if needs_revision else 'retrying'
            c.execute("UPDATE publication_outbox SET state=?,attempts=?,last_error=?,next_run=?,updated=? WHERE id=? AND state!='superseded'",(state,attempts,str(exc),0 if needs_revision else time.time()+min(300,2**min(attempts,8)),time.time(),row['id']))
            store.event(row['mission'],'publication_needs_revision' if needs_revision else 'publication_retry',row['task'],result={'file':row['file'],'error':str(exc)},connection=c)
