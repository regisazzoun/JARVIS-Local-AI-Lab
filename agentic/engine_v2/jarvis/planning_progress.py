"""Evidence-based planning progress in the existing journal, independent of task names."""
import json,re,hashlib
from pathlib import Path


def defect_keys(review):
    keys=set()
    for text in review.get('issues',[]):
        if text.startswith('Unordered artifact writers ') and ' both declare ' in text:
            keys.add('artifact-order:'+text.split(' both declare ',1)[1].split('. Declare',1)[0])
        elif text.startswith('Report artifact collision:') and ' share ' in text:
            keys.add('report-collision:'+text.split(' share ',1)[1].split('. Use distinct',1)[0])
        elif text.startswith('Unexecutable contract '):keys.add('unexecutable-contract')
    for row in review.get('coverage',[]):
        if row.get('covered') is False:keys.add('requirement:'+str(row.get('requirement')))
    if review.get('status')!='PASS' and not keys:keys.add('review-not-passed')
    return sorted(keys)


def assess(store,mission):
    with store.db() as c:
        rows=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND kind='coverage_review' ORDER BY id",(mission,)).fetchall()
        repairs=c.execute("SELECT id,result FROM mission_events WHERE mission=? AND kind='coordinator_planning_repair_verified' AND actor='Codex' ORDER BY id",(mission,)).fetchall()
        latest=c.execute("SELECT result FROM mission_events WHERE mission=? AND kind='planning_review_progress' ORDER BY id DESC LIMIT 1",(mission,)).fetchone()
    if not rows:return None
    # Re-evaluate a newly verified repair even when no newer review exists.
    # A cached blocked verdict must not hide actual coordinator intervention.
    runtime_repair=None
    for row in repairs:
        data=json.loads(row['result']);manifest=data.get('deployed_manifest') or {}
        if data.get('actual_interface_repair_verified') is not True or not manifest:continue
        base=(store.root/'jarvis').resolve();valid=True
        for relative,expected in manifest.items():
            path=(base/relative).resolve()
            if not path.is_relative_to(base) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                valid=False;break
        if valid:runtime_repair=row['id']
    repaired={}
    for row in repairs:
        data=json.loads(row['result'])
        if data.get('actual_task_reduction_verified') is not True:continue
        with store.db() as c:
            before=c.execute('SELECT plan,sha256 FROM mission_plans WHERE mission=? AND version=?',(mission,data.get('before_version'))).fetchone()
            after=c.execute('SELECT plan,sha256 FROM mission_plans WHERE mission=? AND version=?',(mission,data.get('plan_version'))).fetchone()
        if not before or not after or before['sha256']!=data.get('before_sha256') or after['sha256']!=data.get('after_sha256'):continue
        prior={t['id'] for t in json.loads(before['plan'])['tasks']};kept={t['id'] for t in json.loads(after['plan'])['tasks']}
        if kept<prior:repaired[data['plan_version']]=row['id']
    # A second review of one version supersedes its earlier opinion, without
    # deleting it or counting repeated reads as additional correction cycles.
    versions={}
    for row in rows:
        data=json.loads(row['result']);versions[data.get('plan_version',row['id'])]=(row['id'],data)
    previous=None;stagnant=0;failures=sum(json.loads(row['result']).get('status')=='FAIL' for row in rows);repair=None;meaningful=False
    for reference,review in sorted(versions.values()):
        if runtime_repair and reference<runtime_repair:continue
        keys=set(defect_keys(review));passed=review.get('status')=='PASS'
        workspace=json.loads(store.get(mission)['spec']).get('report_workspace')
        if workspace:
            with store.db() as c:
                plan=c.execute('SELECT plan FROM mission_plans WHERE mission=? AND version=?',(mission,review.get('plan_version'))).fetchone()
            if plan:
                from .operational_policy import report_path_allowed
                for task in json.loads(plan['plan'])['tasks']:
                    if not report_path_allowed(task.get('contract',{}).get('report_path'),None,workspace):
                        keys.add('unwritable-report:'+task['id'])

        structural_repair=repaired.get(review.get('plan_version'))
        improved=previous is not None and keys<previous
        if structural_repair:repair=structural_repair;stagnant=0
        if passed or improved:stagnant=0;meaningful=True
        else:stagnant+=1;meaningful=bool(structural_repair)
        previous=keys
    if runtime_repair:
        repair=runtime_repair
        if not any(reference>runtime_repair for reference,_ in versions.values()):
            review=json.loads(rows[-1]['result']);previous=set(defect_keys(review));stagnant=0;meaningful=False
    result={'review_event':rows[-1]['id'],'plan_version':review.get('plan_version'),'status':review.get('status'),'defects':sorted(previous),'nonimproving_reviews':stagnant,'failed_reviews_retained':failures,'runtime_repair_event':runtime_repair,'meaningful':meaningful,'verified_repair_event':repair,'blocked':stagnant>=3,'basis':'Actual review outcomes and strict reduction of stable owner/artifact defects; new IDs/plan saves alone are not progress'}
    plans=store.plans(mission)
    pending=bool(plans and plans[-1]['version']>(review.get('plan_version') or 0))
    result['current_plan_version']=plans[-1]['version'] if plans else None
    result['review_pending']=pending
    if pending:
        result['last_review_status']=result['status'];result['status']='INSUFFICIENT';result['meaningful']=False
    if latest and json.loads(latest['result'])==result:return result
    store.event(mission,'planning_review_progress',actor='JARVIS-engine',result=result)
    return result


def require_revision_capacity(store,mission):
    state=assess(store,mission)
    if state and state['blocked']:
        raise ValueError('Planning strategy escalated after three non-improving reviews; existing plan/history preserved. Codex verified technical repair required before further mutation.')


def conflicts(review):
    return any(key.startswith(('artifact-order:','report-collision:')) for key in defect_keys(review))
