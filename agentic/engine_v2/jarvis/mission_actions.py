"""Optional durable operation keys; exactly-once cannot be promised across a crash.

Successful identical operations replay receipts. Unknown outcomes require fresh
observation before explicit retry; they are never silently counted as successful.
"""
import json
import time
from .mission_store import encoded, signature


def register(registry):
    def action(args):
        store=getattr(registry,'mission_store',None)
        if not store:raise ValueError('Durable mission required')
        mission=registry.context['mission_id'];task=registry.context.get('task_id')
        name=args['tool'];params=json.loads(args['arguments']);key=args['operation_key']
        if name not in registry.specs or not (name.startswith('host_') or name in ('skill_run','skill_test')):
            raise ValueError('Existing host or skill tool required')
        sig=signature(name,params)
        with store.db() as c:
            c.execute('CREATE TABLE IF NOT EXISTS mission_operations(mission TEXT,key TEXT,signature TEXT,invocation TEXT,state TEXT,result TEXT,PRIMARY KEY(mission,key))')
            c.execute('BEGIN IMMEDIATE')
            old=c.execute('SELECT * FROM mission_operations WHERE mission=? AND key=?',(mission,key)).fetchone()
            if old:
                if old['signature']!=sig:raise ValueError('Operation key already bound to different parameters')
                if old['state']=='finished' and json.loads(old['result']).get('ok'):
                    return {'replayed':True,'original_invocation':old['invocation'],**json.loads(old['result'])['result']}
                proof=next((o for o in store.observations(mission,task) if o['id']==args.get('retry_evidence_id') and o['tool']=='mission_verify'),None)
                if not proof or (proof.get('result') or {}).get('result',{}).get('status')!='FAIL':
                    raise ValueError('Outcome failed/unknown: independently observe effect via mission_verify; explicit retry_evidence_id of fresh FAIL required')
                prior=next((o for o in store.observations(mission) if o['id']==old['invocation']),None)
                if prior and proof['created']<=prior['created']:raise ValueError('Retry observation stale')
            # Reserve key transactionally before effect; existing tool_calls holds full receipt.
            c.execute('INSERT OR REPLACE INTO mission_operations VALUES(?,?,?,?,?,?)',(mission,key,sig,None,'started',None))
        token=store.begin_call(mission,task,name,params)
        with store.db() as c:c.execute('UPDATE mission_operations SET invocation=? WHERE mission=? AND key=?',(token,mission,key))
        start=time.monotonic()
        previous_key=registry.context.get('durable_operation_key')
        registry.context['durable_operation_key']=key
        try:result=registry.execute(name,params)
        finally:
            if previous_key is None:registry.context.pop('durable_operation_key',None)
            else:registry.context['durable_operation_key']=previous_key
        store.finish_call(token,result,time.monotonic()-start)
        with store.db() as c:c.execute('UPDATE mission_operations SET state=?,result=? WHERE mission=? AND key=?',('finished',encoded(result),mission,key))
        return {'returncode':0 if result.get('ok') else 1,'original_invocation':token,'replayed':False,'observed_receipt':result}
    registry.specs['mission_action']=('Execute existing host/skill tool with durable operation_key. Identical success reuses receipt across restart; different parameters need a new key. Unknown/failed effect requires a fresh mission_verify FAIL retry_evidence_id. Verify actual state afterwards; cached success is not current state.',{'operation_key':{'type':'string'},'tool':{'type':'string'},'arguments':{'type':'string','maxLength':64000},'retry_evidence_id':{'type':'string'}},['operation_key','tool','arguments'],'host_authorized',action)
