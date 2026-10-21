"""Evidence-based predicates. A new policy-controlled read is mandatory.

PASS means exactly these predicates at read time, never model intent or universal
application correctness. Partial/unavailable evidence cannot close a task.
"""
import hashlib
import json
import time
from .mission_store import encoded


def exact(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(exact(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(exact(x, y) for x, y in zip(a, b))
    return a == b


def pointer(value, path):
    if path == '':
        return value
    if not isinstance(path, str) or not path.startswith('/'):
        raise ValueError('JSON Pointer required, e.g. /port')
    for key in path[1:].split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def validate_contract(contract):
    if not isinstance(contract,dict):raise ValueError('Semantic contract object required')
    source=contract.get('source',{})
    if not isinstance(source,dict) or not isinstance(source.get('tool'),str) or not isinstance(source.get('arguments'),dict):
        raise ValueError('source requires tool and arguments object')
    kind=contract.get('kind')
    if kind=='text':
        if not isinstance(contract.get('equals'),str) and not (isinstance(contract.get('sha256'),str) and len(contract['sha256'])==64):
            raise ValueError('Text contract requires equals (entire exact content) or sha256; expected/contains is not a text proof. Revise invalid contract; final synthesis is also provided by intervention_report.')
    elif kind=='json':
        if not contract.get('expected') and not contract.get('types') and not contract.get('preserve'):
            raise ValueError('At least one JSON predicate required')
        for field in ('expected','types'):
            if not isinstance(contract.get(field,{}),dict):raise ValueError(field+' must map JSON Pointers to values/types')
        for path in list(contract.get('expected',{}))+list(contract.get('types',{}))+contract.get('preserve',[]):
            if not isinstance(path,str) or path and not path.startswith('/'):
                raise ValueError('Use JSON Pointer starting with /, e.g. /port')
        if contract.get('preserve') and not contract.get('baseline_source'):
            raise ValueError('preserve requires baseline_source')
    elif kind=='service':
        if contract.get('expected_state') not in ('active','inactive','failed'):raise ValueError('Explicit expected_state required')
    else:raise ValueError('kind must be json, text or service')


def evaluate(body, contract, baseline=None):
    """Pure predicates, also usable by skills. No stdout keyword success."""
    checks = []
    kind = contract.get('kind')
    if kind == 'json':
        try:
            value = json.loads(body)
        except json.JSONDecodeError as exc:
            return {'status':'FAIL','checks':[{'predicate':'valid_json','pass':False,'error':str(exc)}],'sha256':hashlib.sha256(body.encode()).hexdigest()}
        expected = contract.get('expected', {})
        types = contract.get('types', {})
        preserve = contract.get('preserve', [])
        if not expected and not types and not preserve:
            raise ValueError('At least one JSON predicate required')
        for path, wanted in expected.items():
            try:
                actual = pointer(value, path)
                checks.append({'path': path, 'expected': wanted, 'actual': actual, 'pass': exact(actual, wanted)})
            except (KeyError, IndexError, TypeError, ValueError):
                checks.append({'path': path, 'expected': wanted, 'missing': True, 'pass': False})
        names = {'integer': int, 'string': str, 'boolean': bool, 'object': dict, 'array': list, 'null': type(None), 'number': (int, float)}
        for path, name in types.items():
            if name not in names:
                raise ValueError('Unknown JSON type '+str(name))
            try:
                actual = pointer(value, path)
                passed = type(actual) in names[name] if isinstance(names[name], tuple) else type(actual) is names[name]
            except (KeyError, IndexError, TypeError, ValueError):
                passed = False
            checks.append({'path': path, 'type': name, 'pass': passed})
        for path in preserve:
            if baseline is None:
                checks.append({'path': path, 'unavailable': True, 'pass': False})
                continue
            try:
                passed = exact(pointer(value, path), pointer(json.loads(baseline), path))
            except (KeyError, IndexError, TypeError, ValueError):
                passed = False
            checks.append({'path': path, 'preserved': True, 'pass': passed})
    elif kind == 'text':
        if 'equals' not in contract and 'sha256' not in contract:
            raise ValueError('Exact text or SHA256 required')
        if 'equals' in contract:
            checks.append({'predicate': 'exact_content', 'pass': body == contract['equals']})
        if 'sha256' in contract:
            checks.append({'predicate': 'sha256', 'pass': hashlib.sha256(body.encode()).hexdigest() == contract['sha256']})
    elif kind == 'service':
        if contract.get('expected_state') not in ('active', 'inactive', 'failed'):
            raise ValueError('Explicit expected_state required')
        checks.append({'predicate': 'effective_service_state', 'actual': body.strip(), 'expected': contract['expected_state'], 'pass': body.strip() == contract['expected_state']})
    else:
        raise ValueError('kind must be json, text or service')
    if any(c.get('unavailable') for c in checks):
        status = 'PARTIAL' if any(c['pass'] for c in checks) else 'INSUFFICIENT'
    else:
        status = 'PASS' if all(c['pass'] for c in checks) else 'FAIL'
    return {'status': status, 'checks': checks, 'sha256': hashlib.sha256(body.encode()).hexdigest()}


class Verifier:
    def __init__(self, registry):
        self.registry = registry

    def read(self, source):
        name, args = source['tool'], source['arguments']
        allowed = name == 'host_read_file' or name == 'host_github' and args.get('action') == 'file' or name == 'host_remote' and args.get('action') == 'read_file' or name == 'host_service' and args.get('action') == 'is-active'
        if not allowed:
            raise ValueError('Independent read required: host_read_file, host_remote read_file, host_github file, host_service is-active')
        store = getattr(self.registry, 'mission_store', None)
        token = store.begin_call(self.registry.context['mission_id'], self.registry.context.get('task_id'), name, args) if store else None
        start = time.monotonic()
        receipt = self.registry.execute(name, args)
        if token:
            store.finish_call(token, receipt, time.monotonic()-start)
        result = receipt.get('result', {})
        # Explicit truncation is never accepted as complete content.
        if result.get('truncated') or result.get('stdout_truncated') or result.get('stderr_truncated') or result.get('next_offset') or result.get('stdout_model_excerpt'):
            raise ValueError('Read truncated: insufficient evidence')
        if not receipt.get('ok') and not (name == 'host_service' and result.get('stdout', '').strip() in ('inactive', 'failed')):
            raise ValueError('Independent read unavailable: '+str(receipt.get('error', result.get('stderr', ''))))
        body = result.get('stdout', result.get('content'))
        if not isinstance(body, str):
            raise ValueError('No complete textual content in read receipt')
        if name == 'host_github':
            item=json.loads(body)
            if not isinstance(item,dict) or not isinstance(item.get('content'),str):
                raise ValueError('GitHub file content absent')
            body=item['content']
        return body, {'invocation': token, 'broker_evidence': result.get('evidence_id'), 'tool': name, 'arguments': args}

    def verify(self, contract):
        refs = []
        try:
            validate_contract(contract)
            body, ref = self.read(contract['source']); refs.append(ref)
            baseline = None
            baseline_error = None
            if contract.get('baseline_source'):
                try:
                    baseline, ref = self.read(contract['baseline_source']); refs.append(ref)
                except (ValueError,KeyError,TypeError,OSError) as exc:
                    baseline_error = str(exc)
            verdict = evaluate(body, contract, baseline)
            if baseline_error:
                verdict['baseline_error'] = baseline_error
                if verdict['status']!='FAIL':
                    verdict['status']='PARTIAL' if any(c['pass'] for c in verdict['checks']) else 'INSUFFICIENT'
        except (ValueError, KeyError, TypeError, OSError) as exc:
            verdict = {'status': 'INSUFFICIENT', 'error': str(exc), 'checks': []}
        verdict.update(contract=contract, observations=refs, observed_at=time.time(), verifier='deterministic26')
        store = getattr(self.registry, 'mission_store', None)
        if store:
            verdict['verification_event'] = store.event(self.registry.context['mission_id'], 'semantic_verification', self.registry.context.get('task_id'), 'JARVIS-engine', result=verdict)
        return {'returncode': 0 if verdict['status'] == 'PASS' else 1, **verdict}


def register(registry):
    registry.specs['mission_verify'] = ('Read actual state independently and evaluate exact predicates. contract object or JSON STRING: {kind:"json",source:{tool:"host_read_file",arguments:{path:"..."}},expected:{"/port":8091},types:{"/port":"integer"},baseline_source:{tool:"host_read_file",arguments:{path:"original.json"}},preserve:["/label","/preserve"]}. kind text requires equals or sha256; service requires source host_service is-active and expected_state. PASS/FAIL/PARTIAL/INSUFFICIENT; never a keyword check. Usable from skills.', {'contract': {'type':['object','string'],'maxLength':64000}}, ['contract'], 'host_authorized', lambda a: Verifier(registry).verify(json.loads(a['contract']) if isinstance(a['contract'],str) else a['contract']))
