"""Scoped Codex coordination: dispatch only prepared P1 tasks via canonical MissionStore.

No inference/execution, retry, acceptance or competing mission database. Native workers
retain execution, checkpoints, leases and three-attempt guards. Flock prevents races.
"""
import argparse
import fcntl
import json
import sys
import time
from pathlib import Path

ACTIVE = {'queued', 'running'}
STOPPED = {'interrupted', 'failed', 'waiting_external', 'completed'}


def select_pending(entries, states, inflight):
    """A blocked context frees a slot only after its native operation has ended."""
    used = sum(states[t['id']] in ACTIVE or t['id'] in inflight for t in entries)
    return [t for t in entries if
            (t.get('status') == 'PREPARED_WAITING_SLOT' and states[t['id']] == 'draft')
            or (t.get('corrective_resume', {}).get('armed') is True
                and states[t['id']] in ('interrupted', 'waiting_external'))][:max(0, 2 - used)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--register', required=True)
    p.add_argument('--root', default='/opt/jarvis/conversation')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    register = Path(args.register)
    with register.with_suffix('.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        sys.path.insert(0, args.root)
        from jarvis.mission_store import MissionStore
        store = MissionStore(args.root)
        data = json.loads(register.read_text())
        entries = [t for t in data['tasks'] if t.get('mission_id')]
        states, inflight = {}, set()
        for t in entries:
            mission = store.get(t['mission_id'])
            states[t['id']] = mission['state']
            t['canonical_state'] = mission['state']
            t['last_observed'] = time.time()
            # Lease presence is conservative: an interrupted task can finish a call.
            with store.db() as c:
                running_call = c.execute("SELECT 1 FROM tool_calls WHERE mission=? AND state='started' LIMIT 1", (mission['id'],)).fetchone()
            if running_call or (mission.get('lease_until') or 0) > time.time():
                inflight.add(t['id'])
            if t['id'] not in ('D03', 'D04', 'D17'):
                continue
            if mission['state'] in STOPPED:
                # Observation is not reception. Never mark a blocked/complete engine
                # result as technically accepted without Codex reviewing evidence.
                t['status'] = ('ENGINE_COMPLETED_REVIEW_PENDING' if mission['state'] == 'completed'
                               else 'BLOCKED_ESCALATION_READY')
                if not t.get('coordination_notice_recorded') and not args.dry_run:
                    notice = {'task': t['id'], 'mission_id': mission['id'], 'state': mission['state'],
                              'cause_as_reported': json.loads(mission.get('result') or '{}'),
                              'evidence': 'Canonical mission_events/tool_calls retained under this mission ID',
                              'next': 'Codex reviews native evidence or diagnoses blocker. Independent prepared work continues. No blind retry; counters retained.',
                              'acceptance': 'Not automatically accepted; no live integration'}
                    path = Path(t['context_directory']) / 'COORDINATION.json'
                    path.write_text(json.dumps(notice, ensure_ascii=False, indent=2) + '\n')
                    store.event(mission['id'], 'coordinator_review_required', task=t['id'], actor='Codex-coordination', result=notice)
                    t['coordination_notice_recorded'] = str(path)
            elif mission['state'] in ACTIVE:
                t['status'] = mission['state'].upper()
        chosen = select_pending(entries, states, inflight)
        for t in chosen:
            if not args.dry_run:
                resume = t.get('corrective_resume', {})
                if resume.get('armed'):
                    # Only an explicitly reviewed, versioned intervention can arm
                    # one resume. An unchanged blocker cannot trigger auto-retries.
                    plans = store.plans(t['mission_id'])
                    events = store.events(t['mission_id'], limit=1000000)
                    approved = any(e['id'] == resume.get('strategy_event')
                                   and e['actor'] == 'Codex'
                                   and e['kind'] == 'loop_strategy_changed' for e in events)
                    if not approved or not plans or plans[-1]['version'] != resume.get('plan_version'):
                        resume['armed'] = False
                        t['status'] = 'RESUME_REQUIRES_NEW_REVIEW'
                        store.event(t['mission_id'], 'coordinator_resume_withheld', task=t['id'], actor='Codex-coordination',
                                    result={'reason': 'Reviewed plan/strategy mismatch; no blind resume'})
                        continue
                store.event(t['mission_id'], 'coordinator_handoff', task=t['id'], actor='Codex-coordination',
                            result={'reason': 'An independent context slot is available; owner authorized uninterrupted sequence',
                                    'packet': str(Path(t['context_directory']) / 'PAQUET.md'),
                                    'context_isolated': True, 'no_owner_permission_gate': True})
                store.transition(t['mission_id'], 'queued', {'reason': 'Authorized P1 sequence; separate context, maximum two'})
                if resume.get('armed'):
                    resume['armed'] = False
                    resume['dispatched_at'] = time.time()
                t['status'] = 'QUEUED'
        if not args.dry_run:
            data['updated_at'] = time.time()
            temp = register.with_suffix('.tmp')
            temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
            temp.replace(register)
        print(json.dumps({'dry_run': args.dry_run, 'states': states,
                          'inflight': sorted(inflight), 'dispatch': [t['id'] for t in chosen]}))


if __name__ == '__main__':
    main()
