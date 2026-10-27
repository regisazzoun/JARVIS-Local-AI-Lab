"""Read-only Python code-object attestation, candidate phase M26-P4.

Original AttestRuntime interface by JARVIS. Code-object comparison corrected by
Codex after the file-hash false positive. Candidate code is compiled, NEVER run.
Attests Python function/method code, not module globals, native code or behavior.
"""
import hashlib
import inspect
import json
import os
from pathlib import Path
import sys
import time
import types


def _constant(value):
    if isinstance(value, types.CodeType):
        return ['code', _code(value)]
    if value is None or value is Ellipsis:
        return [type(value).__name__]
    if isinstance(value, (bool, int, str)):
        return [type(value).__name__, value]
    if isinstance(value, bytes):
        return ['bytes', value.hex()]
    if isinstance(value, float):
        return ['float', value.hex()]
    if isinstance(value, complex):
        return ['complex', value.real.hex(), value.imag.hex()]
    if isinstance(value, tuple):
        return ['tuple', [_constant(v) for v in value]]
    if isinstance(value, frozenset):
        return ['frozenset', sorted((_constant(v) for v in value), key=_json)]
    raise TypeError('Unsupported code constant: '+type(value).__name__)


def _json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(',', ':'))


def _code(code):
    # Exclude filename and line/debug tables: candidate and deployment paths
    # differ. Preserve executable bytecode, nested constants and exception table.
    fields=('co_argcount','co_posonlyargcount','co_kwonlyargcount','co_nlocals',
            'co_stacksize','co_flags','co_name','co_qualname','co_names',
            'co_varnames','co_freevars','co_cellvars')
    return {**{k:getattr(code,k) for k in fields},
            'co_code':code.co_code.hex(),
            'co_exceptiontable':code.co_exceptiontable.hex(),
            'co_consts':[_constant(v) for v in code.co_consts]}


def get_object_code_hash(obj):
    """Hash the live code object; no disk/source/name-only fallback."""
    if inspect.ismethod(obj):
        obj=obj.__func__
    code=obj if isinstance(obj,types.CodeType) else getattr(obj,'__code__',None)
    if not isinstance(code,types.CodeType):
        raise TypeError('Actual Python code object required')
    return hashlib.sha256(_json(_code(code)).encode()).hexdigest()


def _live_objects(module):
    objects={};unsupported=[]
    def collect(namespace, prefix=''):
        for name,obj in namespace.items():
            key=prefix+name
            if isinstance(obj,property):
                unsupported.append(key);continue
            if isinstance(obj,(staticmethod,classmethod)):
                obj=obj.__func__
            if getattr(obj,'__module__',None)!=module.__name__:
                continue
            if inspect.isfunction(obj):
                if hasattr(obj,'__wrapped__'):unsupported.append(key)
                objects[key]=get_object_code_hash(obj)
            elif inspect.isclass(obj):
                collect(vars(obj),key+'.')
            elif isinstance(obj,property):
                for suffix,fn in [('get',obj.fget),('set',obj.fset),('del',obj.fdel)]:
                    if fn is not None:
                        objects[key+'.'+suffix]=get_object_code_hash(fn)
    collect(vars(module))
    return objects,unsupported


def _compiled_objects(source, filename):
    root=compile(source,filename,'exec',dont_inherit=True)
    objects={}
    def collect(code):
        for value in code.co_consts:
            if isinstance(value,types.CodeType):
                # Class bodies contain construction instructions, not a live
                # function. Only compare declarations with their function code.
                if value.co_flags & inspect.CO_NEWLOCALS and '.<locals>.' not in value.co_qualname:
                    key=value.co_qualname
                    objects[key]=None if key in objects else get_object_code_hash(value)
                collect(value)
    collect(root)
    # Nested functions are included recursively in their parent's fingerprint;
    # they are not necessarily instantiated/exported as live module members.
    return {k:v for k,v in objects.items() if '.<locals>.' not in k}


class AttestRuntime:
    def __init__(self,root,max_age_seconds=30):
        self.root=Path(root).resolve()
        self.max_age_seconds=max_age_seconds
        self._measurements={}
        self._start_time=time.time()

    def _hash_file(self,path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def _hash_object_code(self,obj):
        return get_object_code_hash(obj)

    def _gather_module_info(self,module_name):
        mod=sys.modules.get(module_name)
        if mod is None or not getattr(mod,'__file__',None):
            return None
        path=Path(mod.__file__).resolve()
        objects,unsupported=_live_objects(mod)
        return {'path':str(path),'file_hash':self._hash_file(path) if path.is_file() else None,
                'observed_at':time.time(),'pid':os.getpid(),
                'objects':[{'name':k,'code_hash':v} for k,v in sorted(objects.items())],'unsupported_symbols':unsupported,
                'scope':'Python __code__ only; excludes globals, defaults, closure values, decorators and native code'}

    def measure_module(self,module_name,symbols=None):
        info=self._gather_module_info(module_name)
        if not info:
            return False
        if symbols is not None:
            info['selected_symbols']=list(symbols)
        self._measurements[module_name]=info
        return True

    def verify_against_candidate(self,candidate_path):
        if not self._measurements:
            return {'__attestation__':{'status':'insufficient','reason':'No measured module'}}
        results={}
        for name,stored in self._measurements.items():
            candidate=Path(candidate_path).resolve()/Path(stored['path']).name
            base={'candidate_path':str(candidate),'stored_path':stored['path'],
                  'pid':os.getpid(),'observed_at':time.time(),'objects_match':None}
            age=time.time()-stored['observed_at']
            if age<0 or age>self.max_age_seconds:
                results[name]={**base,'status':'insufficient','reason':'Measurement expired or future-dated'}
                continue
            if not candidate.is_file():
                results[name]={**base,'status':'missing','reason':'Candidate absent'}
                continue
            try:
                # Reobserve to catch in-process monkey patches after measurement.
                live=self._gather_module_info(name)
                if not live:
                    raise ValueError('Measured module no longer loaded')
                actual={item['name']:item['code_hash'] for item in live['objects']}
                expected=_compiled_objects(candidate.read_bytes(),str(candidate))
                selected=stored.get('selected_symbols')
                if selected is not None:
                    if not selected or any(k not in actual or k not in expected for k in selected):
                        raise ValueError('Requested Python code symbol absent or unsupported')
                    actual={k:actual[k] for k in selected}
                    expected={k:expected[k] for k in selected}
                if any(k in live['unsupported_symbols'] for k in (selected if selected is not None else actual)) or any(v is None for v in expected.values()):
                    raise ValueError('Decorated/descriptor or ambiguous candidate symbol requires explicit supported symbol selection')
                if not actual or not expected:
                    raise ValueError('No comparable Python function code objects')
                same=actual==expected
                results[name]={**base,'status':'match' if same else 'mismatch',
                               'objects_match':same,'actual_objects':actual,
                               'expected_objects':expected,'candidate_hash':self._hash_file(candidate),
                               'observed_disk_hash':live['file_hash'],'scope':live['scope'],'selected_symbols':selected}
            except (OSError,ValueError,TypeError,SyntaxError) as exc:
                results[name]={**base,'status':'insufficient','reason':str(exc)}
        return results

    def to_report(self):
        return {'start_time':self._start_time,'start_time_meaning':'measurement session, NOT process birth','now':time.time(),'pid':os.getpid(),
                'python':sys.version,'measurements':self._measurements,
                'scope':'Current process only; remote worker/service integration not implied'}


def attestation_report(module_names,candidate_path,max_age_seconds=30):
    runtime=AttestRuntime(candidate_path,max_age_seconds)
    absent=[name for name in module_names if not runtime.measure_module(name)]
    results=runtime.verify_against_candidate(candidate_path)
    statuses=[r['status'] for r in results.values()]
    verdict=('FAIL' if 'mismatch' in statuses else 'PASS' if statuses and all(v=='match' for v in statuses) and not absent else 'PARTIAL' if 'match' in statuses else 'INSUFFICIENT')
    return {**runtime.to_report(),'results':results,'verification_status':verdict,
            'unavailable_modules':absent}
