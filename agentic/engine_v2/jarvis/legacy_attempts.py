"""P2 guard for canonical host/skill actions, using the existing durable ledger.

A broker process success remains inconclusive until the persisted task predicates
are independently observed. This never promotes a transport rc0 to acceptance.
"""
import json
import hashlib
from .attempt_ledger import digest


def pending_report_validation(store,mission,task_id):
    """Project the known report-write lifecycle: verify, correct, or complete.

    Return only durable execution facts. Unknown executions and unrelated tasks
    never become known writes by this projection.
    """
    if not task_id:return None
    spec=json.loads(store.get(mission)['spec'])
    if not spec.get('planning_report_steps'):return None
    task=next((t for t in store.tasks(mission) if t['id']==task_id),None)
    contract=(task or {}).get('contract',{});path=contract.get('report_path')
    if not path or not any(c.get('kind')=='report' for c in contract.get('semantic',[])):return None
    with store.db() as c:
        if not c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='mission_attempts_v2'").fetchone():return None
        rows=c.execute("SELECT id,problem,state,unknown_outcome,request,result FROM mission_attempts_v2 WHERE mission=? ORDER BY created DESC",(mission,)).fetchall()
    for row in rows:
        request=json.loads(row['request']);result=json.loads(row['result']);args=request.get('arguments',{})
        if request.get('task')!=task_id or request.get('tool')!='host_write_file' or args.get('path')!=path:continue
        # Never skip a newer unknown write to present an old report as current.
        if row['unknown_outcome']:return None
        resumed=False
        if row['state'] in ('BLOCKED','ESCALATED'):
            with store.db() as c:
                problem=c.execute('SELECT state FROM mission_problems_v2 WHERE mission=? AND fingerprint=?',(mission,row['problem'])).fetchone()
            resumed=bool(problem and problem['state']=='RESOLVED' and result.get('verification',{}).get('status')=='FAIL')
        if not resumed and row['state'] not in ('VALIDATION_INCONCLUSIVE','EXECUTED_TEST_FAILED','SUCCESS'):return None
        if result.get('returncode')!=0 or not result.get('started',{}).get('child_started'):return None
        phase='correct' if resumed else {'VALIDATION_INCONCLUSIVE':'verify','EXECUTED_TEST_FAILED':'correct','SUCCESS':'complete'}[row['state']]
        verdict=result.get('verification',{})
        feedback={'verification_event':verdict.get('verification_event'),'status':verdict.get('status'),
                  'global_findings':[str(x)[-300:] for x in verdict.get('issues',[])[:4]],
                  'issue_count':len(verdict.get('issues',[])),
                  'meaning':'Reviewer findings about a prior report, not new operational facts. Inspect original proofs and correct your own prose.'}
        if phase=='correct' and verdict.get('sha256'):
            with store.db() as c:
                review=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND task=? AND kind='narrative_review' AND json_extract(result,'$.draft_sha256')=? ORDER BY id DESC LIMIT 1",(mission,task_id,verdict['sha256'])).fetchone()
            if review:
                from .mission_assurance import finding_rectifications
                original=json.loads(review['result']);reference='event:'+str(review['id'])
                erratum=finding_rectifications(store,mission).get(reference,{})
                withdrawn=erratum.get('withdrawn_findings',[])
                issues=[x for x in original['issues'] if x not in withdrawn]
                rejected=[claim for claim in original.get('claims',[]) if claim.get('verdict') in ('contradicted','insufficient')]
                feedback.update(review_reference=reference,global_findings=[str(x)[:300] for x in issues if ' => ' not in x][:4],
                    rejected_passages=[{'segment':x['segment'],'quote':x['quote'][:300],
                        'quote_is_excerpt':len(x['quote'])>300,'reason':x.get('reason',''),
                        'verdict':x['verdict'],'references':x.get('references',[])} for x in rejected[:3]],
                    rejected_passage_count=len(rejected),issue_count=len(issues),
                    erratum_reference=erratum.get('reference'),original_review_status=original['status'])
                if original.get('issues') and not issues and not rejected and erratum.get('reference'):
                    phase='verify'
                    feedback['all_findings_withdrawn_by']=erratum['reference']
        completion=None
        if phase in ('correct','verify'):
            status=store.contract_status(mission,task_id)
            if status.get('all_satisfied') and status.get('completion_candidate'):
                for semantic in status.get('semantic',[]):
                    if semantic['contract'].get('kind')!='report' or semantic['contract'].get('source',{}).get('arguments',{}).get('path')!=path:continue
                    with store.db() as c:
                        observed=c.execute('SELECT result FROM mission_events WHERE mission=? AND id=?',(mission,semantic['event'])).fetchone()
                    current=json.loads(observed['result']) if observed else {}
                    if semantic.get('invocation_id') and current.get('status')=='PASS' and current.get('sha256')==hashlib.sha256(args.get('content','').encode()).hexdigest():
                        phase='complete';completion={'verification_event':semantic['event'],'invocation_id':semantic['invocation_id'],'previous_attempt_state':row['state'],'old_failure_unchanged':True}
        observed_draft=None
        if phase=='correct':
            with store.db() as c:
                reads=c.execute("SELECT id,result FROM tool_calls WHERE mission=? AND task=? AND tool='host_read_file' AND json_extract(arguments,'$.path')=? ORDER BY created DESC LIMIT 8",(mission,task_id,path)).fetchall()
            for read in reads:
                wrapper=json.loads(read['result']);value=wrapper.get('result',{})
                content=value.get('stdout')
                if wrapper.get('ok') and value.get('returncode')==0 and isinstance(content,str) and len(content.encode())<=8000 and not value.get('stdout_truncated') and hashlib.sha256(content.encode()).hexdigest()==hashlib.sha256(args.get('content','').encode()).hexdigest():
                    observed_draft={'invocation_id':read['id'],'content':content,'sha256':hashlib.sha256(content.encode()).hexdigest(),'meaning':'Complete previously read draft matching the completed write. Correct this text; no repeated read needed. Final verification must independently read the resulting file.'}
                    break
        return {'attempt':row['id'],'phase':phase,'report_path':path,'write_returncode':0,
                **({'resumed_after_coordinator_resolution':{'original_attempt_state':row['state'],'problem_state':'RESOLVED','old_failure_and_counts_unchanged':True}} if resumed else {}),
                'expected_written_content_sha256':hashlib.sha256(args.get('content','').encode()).hexdigest(),
                'verification_calls':[{'contract':'active:'+str(i)} for i in range(len(contract['semantic']))],
                **({'review_feedback':feedback} if phase=='correct' else {}),
                **({'observed_draft':observed_draft} if observed_draft else {}),
                **({'completed_by_later_verification':completion} if completion else {}),
                'meaning':{'verify':'Completed write only; verify the persisted report before another write. A rejected rewrite draft did not replace it.',
                           'correct':'Observed report verification failed; correct the recorded findings and verify the new file. Unrelated planning/service work is not needed for this correction.',
                           'complete':'Write and verification are recorded; normal task completion still checks freshness and every original criterion.'}[phase]}
    return None


def task_contract(reg):
    store=getattr(reg,'mission_store',None);ctx=getattr(reg,'context',{})
    if not store or not ctx.get('mission_id') or not ctx.get('task_id'):return None
    spec=json.loads(store.get(ctx['mission_id'])['spec'])
    if spec.get('distributed_authority'):return None  # Authority has its own complete receipt adapter.
    task=next((t for t in store.tasks(ctx['mission_id']) if t['id']==ctx['task_id']),None)
    criteria=(task or {}).get('contract',{}).get('semantic')
    if not criteria:return None
    return {'criteria':criteria,'task':task,'mission':ctx['mission_id'],'store':store}


def observed_targets(reg,criteria):
    from .verification import Verifier
    result={}
    for criterion in criteria:
        source=criterion.get('source')
        if not source:continue
        try:
            body,proof=Verifier(reg).read(source)
            result[digest(source)]={'sha256':digest(body),'proof':proof}
        except (ValueError,KeyError,TypeError,OSError):
            result[digest(source)]={'unavailable':True}
    return result


def known_unit_file_read(name,args):
    """Exact unit observations in either public host_exec representation."""
    paths=('/etc/systemd/system/jarvis-mission-worker.service',
           '/etc/systemd/system/jarvis-mission-worker@.service')
    return name=='host_exec' and (
        set(args)=={'argv'} and args['argv'] in (['cat',p] for p in paths) or
        set(args)=={'command'} and args['command'] in ('cat '+p for p in paths))


def guarded(reg,name,args,fn,mutating):
    contract=task_contract(reg)
    # Wrapper/orchestrator tools recurse through the same Registry; guard the
    # actual host/skill/MCP operation, never count both wrapper and effect.
    selected=name.startswith('host_') or name in ('skill_run','skill_test','mcp_tools')
    if not mutating or known_unit_file_read(name,args) or not selected or not contract or getattr(reg,'_p2_inside_effect',False):return fn(args)
    if name=='host_write_file' and args.get('path')==contract['task'].get('contract',{}).get('report_path') and not any(c.get('source',{}).get('arguments',{}).get('path')==args.get('path') for c in contract['criteria']):return fn(args)
    store=contract['store'];mission=contract['mission'];ledger=store.attempt_ledger(mission)
    binding={'criteria':contract['criteria']}
    problem=ledger.problem('canonical-action:'+digest(binding),binding)
    key=str(reg.context.get('durable_operation_key') or digest({'tool':name,'arguments':args}))
    request={'tool':name,'arguments':args,'contract':contract['criteria'],'task':reg.context['task_id']}
    begin=ledger.begin(problem,key,args.get('host','canonical-broker'),'execute',request)
    if begin.get('blocked'):raise ValueError('P2: problem escalated; no fourth operation. '+json.dumps(begin))
    if begin.get('requires_observation'):raise ValueError('P2: observe existing effect with mission_verify before another mutation; no action dispatched. '+json.dumps(begin))
    if begin.get('cached'):return ledger.get(begin['attempt'])['result']['value']
    attempt=begin['attempt'];ledger.transition(attempt,'DISPATCHED')
    store.event(mission,'canonical_attempt_bound',reg.context['task_id'],'JARVIS-engine',result={'attempt':attempt,'tool':name,'arguments':args,'contract':contract['criteria']})
    before=observed_targets(reg,contract['criteria']) if hasattr(reg,'execute') else {}
    try:
        reg._p2_inside_effect=True
        value=fn(args)
    except Exception as exc:
        proof=store.event(mission,'p2_dispatch_failure_observed',actor='JARVIS-engine',result={'attempt':attempt,'known_not_executed':False,'error':str(exc),'requires_independent_observation':True})
        ledger.transition(attempt,'VALIDATION_INCONCLUSIVE',evidence=proof,result={'error':str(exc)},unknown=True)
        ledger.failure(attempt,infrastructure=True)
        raise
    finally:reg._p2_inside_effect=False
    code=value.get('returncode') if isinstance(value,dict) else None
    execution=value.get('execution',{}) if isinstance(value,dict) else {}
    if not execution and isinstance(value,dict):
        try:
            body=json.loads(value.get('stdout','{}'))
            if isinstance(body,dict) and isinstance(body.get('execution'),dict):execution=body['execution']
        except (TypeError,ValueError):pass
    if type(execution.get('returncode')) is int:code=execution['returncode']
    after=observed_targets(reg,contract['criteria']) if hasattr(reg,'execute') else {}
    changed=any(b.get('sha256') and before.get(k,{}).get('sha256') and b['sha256']!=before[k]['sha256'] for k,b in after.items())
    result={'change_observed':bool(changed),'before':before,'after':after,'value':value,'returncode':code,'verified':False,'validation_scope':'persisted task contract','execution':execution}
    if type(code) is not int:
        proof=store.event(mission,'p2_dispatch_failure_observed',actor='JARVIS-engine',result={'attempt':attempt,'known_not_executed':False,'observed_value':value})
        ledger.transition(attempt,'VALIDATION_INCONCLUSIVE',evidence=proof,result=result,unknown=True)
    else:
        marker={'child_started':True,'basis':'completed broker process receipt, not a live PID observation','broker_evidence':value.get('evidence_id')}
        proof=store.event(mission,'p2_started_observed',actor='JARVIS-engine',result={'attempt':attempt,'marker':marker})
        ledger.transition(attempt,'RUNNING',evidence=proof);result['started']=marker
        state='EXECUTION_FAILED' if code else 'VALIDATION_INCONCLUSIVE'
        proof=store.event(mission,'p2_result_observed',actor='JARVIS-engine',result={'attempt':attempt,'observation':result,'state':state})
        ledger.transition(attempt,state,evidence=proof,result=result,unknown=False)
        if code:ledger.failure(attempt,correction_changed=False)
    return value


def settle(reg,verdict):
    contract=task_contract(reg)
    if not contract or verdict.get('contract') not in contract['criteria']:return
    store=contract['store'];mission=contract['mission'];ledger=store.attempt_ledger(mission)
    binding={'criteria':contract['criteria']};problem=ledger.problem('canonical-action:'+digest(binding),binding)
    snapshot=ledger.snapshot()
    pending=[r for r in snapshot['attempts'] if r['problem']==problem and r['state']=='VALIDATION_INCONCLUSIVE']
    for raw in pending:
        attempt=ledger.get(raw['id'])
        with store.db() as c:
            bound=c.execute("SELECT id FROM mission_events WHERE mission=? AND kind='canonical_attempt_bound' AND json_extract(result,'$.attempt')=? ORDER BY id DESC LIMIT 1",(mission,raw['id'])).fetchone()
            observations=[{**json.loads(r['result']),'verification_event':r['id']} for r in c.execute("SELECT id,result FROM mission_events WHERE mission=? AND task=? AND kind='semantic_verification' AND id>? ORDER BY id",(mission,contract['task']['id'],bound['id']))]
        latest={digest(v['contract']):v for v in observations if v.get('contract') in contract['criteria']}
        if verdict['status']=='FAIL':
            result={**attempt['result'],'verification':verdict,'verified':False}
            proof=store.event(mission,'p2_result_observed',actor='JARVIS-engine',result={'attempt':raw['id'],'observation':result,'state':'EXECUTED_TEST_FAILED'})
            if result.get('started'):
                ledger.transition(raw['id'],'EXECUTED_TEST_FAILED',evidence=proof,result=result,unknown=False)
                ledger.failure(raw['id'],correction_changed=bool(result.get('change_observed')))
        elif len(latest)==len(contract['criteria']) and all(v['status']=='PASS' for v in latest.values()):
            if not attempt['result'].get('started') or attempt['unknown_outcome']:
                store.event(mission,'canonical_effect_verified_execution_unknown',actor='JARVIS-engine',result={'attempt':raw['id'],'verification':verdict,'no_execution_success_claimed':True})
                continue  # Unknown execution stays protected: never invent its child rc.
            result={**attempt['result'],'verification_events':[v['verification_event'] for v in latest.values()],'verified':True}
            proof=store.event(mission,'p2_result_observed',actor='JARVIS-engine',result={'attempt':raw['id'],'observation':result,'state':'SUCCESS'})
            ledger.transition(raw['id'],'SUCCESS',evidence=proof,result=result,unknown=False)
