"""Executable, versioned compositions of the existing authorized tool registry.

No Python plugin loading or new authority: every step uses Registry.execute.
"""
from contextlib import contextmanager
import hashlib
import json
import re
import sqlite3
import time
import uuid
from pathlib import Path
from jsonschema import Draft202012Validator


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def digest(value):
    return hashlib.sha256(encode(value).encode()).hexdigest()


def substitute(value, params):
    if isinstance(value, dict):
        return {k: substitute(v, params) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute(v, params) for v in value]
    if isinstance(value, str) and re.fullmatch(r'\$\{[a-zA-Z_][a-zA-Z_0-9]*\}', value):
        key=value[2:-1]
        if key not in params:raise ValueError('Parameter '+key+' missing; declare it in parameters schema and supply its value')
        return params[key]
    if isinstance(value, str) and '${' in value:
        raise ValueError('Partial template unsupported: '+repr(value)[:180]+'. For parameterized commands use host_exec arguments argv as an array, for example ["python3","/path/program.py","--input","${input_file}"]. Each parameter occupies a whole array element and must be declared in parameters schema. Or use a fixed command reading a fixed job file.')
    return value


class SkillLab:
    def __init__(self, registry):
        self.registry = registry
        self.path = registry.root/'runtime/skill-lab.sqlite'
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.db() as c:
            c.executescript('''
            CREATE TABLE IF NOT EXISTS versions(name TEXT,version INTEGER,manifest TEXT,sha TEXT,actor TEXT,created REAL,PRIMARY KEY(name,version));
            CREATE TABLE IF NOT EXISTS active(name TEXT PRIMARY KEY,version INTEGER);
            CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY,name TEXT,version INTEGER,params TEXT,testing INTEGER,state TEXT,steps TEXT,created REAL,updated REAL,mission TEXT);
            ''')

    @contextmanager
    def db(self):
        c = sqlite3.connect(self.path, timeout=20)
        c.row_factory = sqlite3.Row
        try:
            with c:
                yield c
        finally:
            c.close()

    def validate(self, manifest):
        required = {'name','description','when','parameters','requires_tools','prerequisites','steps','on_error','changelog'}
        if set(manifest) != required:
            raise ValueError('Manifest fields must be exactly '+str(sorted(required)))
        if not re.fullmatch('[a-z][a-z0-9-]{1,63}', manifest['name']):
            raise ValueError('Invalid skill name')
        for k in ['description','when','on_error','changelog']:
            if not isinstance(manifest[k],str) or not manifest[k].strip():
                raise ValueError('Nonempty text required: '+k)
        schema = manifest['parameters']
        def local_refs(value):
            if isinstance(value,dict):
                if any(k in value and not str(value[k]).startswith("#") for k in ("$ref","$dynamicRef")):
                    raise ValueError("Only local JSON schema references supported")
                for item in value.values():local_refs(item)
            elif isinstance(value,list):
                for item in value:local_refs(item)
        local_refs(schema)
        Draft202012Validator.check_schema(schema)
        if schema.get('type') != 'object' or schema.get('additionalProperties') is not False:
            raise ValueError('Parameters must be object, additionalProperties=false')
        if not isinstance(manifest['prerequisites'],list):
            raise ValueError('prerequisites must be a list of observable conditions')
        steps = manifest['steps']
        if not isinstance(steps,list) or not 1 <= len(steps) <= 20:
            raise ValueError('1..20 executable steps required')
        allowed = {n for n in self.registry.specs if n.startswith('host_')} | {'web_fetch','web_search','capability_status','mission_verify'}
        used = set()
        for s in steps:
            if set(s)-{'tool','arguments','verify','checks'} or not {'tool','arguments'} <= set(s):
                raise ValueError('Step: tool, arguments, optional verify=true and checks')
            if s['tool'] not in allowed:
                raise ValueError('Unavailable or recursive tool: '+str(s['tool']))
            if not isinstance(s['arguments'],dict) or type(s.get('verify',False)) is not bool:
                raise ValueError('Step arguments object and verify boolean required')
            if s.get('verify') and not s.get('checks') and s['tool']!='mission_verify':
                raise ValueError('Verification requires independent observable checks')
            if s['tool']=='mission_verify' and not s.get('verify'):
                raise ValueError('mission_verify step must set verify:true')
            for check in s.get('checks',[]):
                if set(check) != {'path','op','value'} or check['op'] not in ('equals','contains'):
                    raise ValueError('Check: path, op equals/contains, value')
            used.add(s['tool'])
        if not any(s.get('verify') for s in steps):
            raise ValueError('At least one independent verification step required')
        if not isinstance(manifest['requires_tools'],list) or set(manifest['requires_tools']) != used:
            raise ValueError('requires_tools must exactly identify executable dependencies')

    def define(self, manifest):
        self.validate(manifest)
        store=getattr(self.registry,'mission_store',None)
        if store and json.loads(store.get(self.registry.context['mission_id'])['spec']).get('autonomous'):
            if not any(s['tool']=='mission_verify' and s.get('verify') for s in manifest['steps']):
                raise ValueError('New autonomous skills require a mission_verify step with verify:true and exact semantic contract; code0 or contains status is insufficient. Existing historical versions remain preserved.')
        text, sha = encode(manifest), digest(manifest)
        with self.db() as c:
            c.execute('BEGIN IMMEDIATE')
            last=c.execute('SELECT version,sha FROM versions WHERE name=? ORDER BY version DESC LIMIT 1',(manifest['name'],)).fetchone()
            if last and last['sha']==sha:
                return {'name':manifest['name'],'version':last['version'],'sha256':sha,'unchanged':True}
            v=last['version']+1 if last else 1
            actor='JARVIS' if self.registry.context.get('mission_id') else 'local-operator'
            c.execute('INSERT INTO versions VALUES(?,?,?,?,?,?)',(manifest['name'],v,text,sha,actor,time.time()))
        return {'name':manifest['name'],'version':v,'sha256':sha,'state':'candidate','previous_active_version_preserved':True}

    def get(self, name, version=None):
        with self.db() as c:
            r=c.execute('SELECT * FROM versions WHERE name=? '+('AND version=?' if version else 'ORDER BY version DESC LIMIT 1'),(name,version) if version else (name,)).fetchone()
        if not r: raise ValueError('Unknown skill/version')
        return dict(r)

    def listing(self, args):
        with self.db() as c:
            rows=[dict(r) for r in c.execute('SELECT v.name,v.version,v.sha,v.actor,a.version active_version FROM versions v LEFT JOIN active a ON a.name=v.name ORDER BY v.name,v.version')]
            for r in rows:
                m=json.loads(self.get(r['name'],r['version'])['manifest'])
                r.update(description=m['description'],parameters=m['parameters'],requires_tools=m['requires_tools'])
                r['unavailable_tools']=[n for n in m['requires_tools'] if n not in self.registry.specs]
                r['last_run']=dict(c.execute('SELECT id,state,testing,updated FROM runs WHERE name=? AND version=? ORDER BY updated DESC LIMIT 1',(r['name'],r['version'])).fetchone() or {})
                if args.get('name')==r['name']:r['manifest']=m
        return {'skills':[r for r in rows if not args.get('name') or r['name']==args['name']], 'authority':'existing Registry and broker owner policy; exposure is not availability'}

    def activate(self, name, enabled):
        if type(enabled) is not bool:raise ValueError('enabled must be boolean')
        with self.db() as c:
            if not enabled:
                c.execute('DELETE FROM active WHERE name=?',(name,));return {'name':name,'active':False}
            v=self.get(name)
            tested=c.execute('SELECT state FROM runs WHERE name=? AND version=? AND testing=1 ORDER BY updated DESC LIMIT 1',(name,v['version'])).fetchone()
            if not tested or tested['state']!='passed':raise ValueError('Latest candidate requires a successful current test before activation')
            c.execute('INSERT OR REPLACE INTO active VALUES(?,?)',(name,v['version']))
        return {'name':name,'version':v['version'],'active':True,'sha256':v['sha']}

    def invoke(self, tool, args):
        registry=self.registry
        store=getattr(registry,'mission_store',None)
        token=None;start=time.monotonic()
        if store:
            token=store.begin_call(registry.context['mission_id'],registry.context.get('task_id'),tool,args)
        result=registry.execute(tool,args)
        if token:store.finish_call(token,result,time.monotonic()-start)
        return result

    def execute(self, name, params, testing=False, run_id=None):
        if not self.registry.context.get('mission_id') and getattr(self.registry,'mission_controller',None):
            raise ValueError('Executable skills require a durable mission; no mutation outside mission tracking')
        with self.db() as c:
            old=c.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone() if run_id else None
            if run_id and not old:raise ValueError('Unknown checkpoint')
            if old:
                if old['name']!=name or old['params']!=encode(params) or bool(old['testing'])!=testing:
                    raise ValueError('Checkpoint name/parameters/mode mismatch')
                mission=self.registry.context.get('mission_id')
                if old['mission'] and old['mission']!=mission:raise ValueError('Checkpoint belongs to another mission')
                version=old['version']
            elif testing:version=self.get(name)['version']
            else:
                active=c.execute('SELECT version FROM active WHERE name=?',(name,)).fetchone()
                if not active:raise ValueError('Skill disabled or untested')
                version=active['version']
            if not testing:
                active=c.execute('SELECT version FROM active WHERE name=?',(name,)).fetchone()
                if not active or active['version']!=version:raise ValueError('Checkpoint version no longer active')
        record=self.get(name,version);manifest=json.loads(record['manifest']);self.validate(manifest)
        Draft202012Validator(manifest['parameters']).validate(params)
        # Expand and validate ALL arguments before the first effect.
        steps=[{**s,'arguments':substitute(s['arguments'],params),'checks':substitute(s.get('checks',[]),params)} for s in manifest['steps']]
        for s in steps:
            spec=self.registry.specs[s['tool']]
            from .tools import parameter_schema
            Draft202012Validator(parameter_schema(s['tool'],spec)).validate(s['arguments'])
        run_id=run_id or uuid.uuid4().hex
        results=json.loads(old['steps']) if old else []
        if not old:
            with self.db() as c:c.execute('INSERT INTO runs VALUES(?,?,?,?,?,?,?,?,?,?)',(run_id,name,version,encode(params),int(testing),'running','[]',time.time(),time.time(),self.registry.context.get('mission_id')))
        state='passed'
        for index,step in enumerate(steps):
            previous=next((r for r in results if r['index']==index and r['ok']),None)
            if previous and not step.get('verify'):continue
            result=self.invoke(step['tool'],step['arguments']);ok=bool(result.get('ok'));error=None
            if ok:
                try:
                    for check in step['checks']:
                        v=result
                        for key in check['path'].split('.'):v=v[int(key)] if isinstance(v,list) else v[key]
                        expected=check['value']
                        if not (v==expected if check['op']=='equals' else expected in v):
                            raise ValueError('Verification mismatch: '+check['path'])
                except (KeyError,TypeError,IndexError,ValueError) as exc:ok=False;error=str(exc)
            row={'index':index,'tool':step['tool'],'ok':ok,'verification_error':error,'result':result,'created':time.time()}
            results=[r for r in results if r['index']!=index]+[row]
            state='running' if ok and index<len(steps)-1 else 'passed' if ok else 'failed'
            with self.db() as c:c.execute('UPDATE runs SET state=?,steps=?,updated=? WHERE id=?',(state,encode(results),time.time(),run_id))
            if not ok:break
        return {'returncode':0 if state=='passed' else 1,'run_id':run_id,'name':name,'version':version,'sha256':record['sha'],'state':state,'testing':testing,'steps':results,'on_error':manifest['on_error'] if state!='passed' else None,'resumed':bool(old)}


def register(registry):
    lab=SkillLab(registry)
    def spec(name,description,props,required,fn):
        registry.specs[name]=(description,props,required,'host_authorized',fn)
    text={'type':'string','maxLength':64000}
    spec('skill_list','Discover executable skills, versions, parameters, active status, missing tools and latest real run. Optional name returns full manifests.',{'name':text},[],lab.listing)
    spec('skill_define','Create/improve an immutable candidate workflow. manifest is JSON STRING with exact fields name,description,when,parameters(JSON schema object with additionalProperties=false),requires_tools,prerequisites(list),steps(list of {tool,arguments,verify?,checks?}),on_error,changelog. For autonomous missions include {tool:"mission_verify",arguments:{contract:{kind:"json",source:{tool:"host_read_file",arguments:{path:"${output_file}"}},expected:{"/port":8091}}},verify:true}; no checks needed there. Old-style checks remain for compatibility, but alone cannot validate a new autonomous skill. Whole-value ${parameter} substitution only. Every tool executes through existing policy. New versions need skill_test before skill_activate.',{'manifest':text},['manifest'],lambda a:lab.define(json.loads(a['manifest'])))
    spec('skill_test','Execute latest candidate with REAL effects in the authorized workspace, including independent verification. parameters is a JSON STRING object. Failed test never activates. run_id resumes same revision and parameters, skips successful action steps, repeats verification.',{'name':text,'parameters':text,'run_id':text},['name','parameters'],lambda a:lab.execute(a['name'],json.loads(a['parameters']),True,a.get('run_id')))
    spec('skill_activate','Activate latest candidate only after its latest real test passed, or disable without deleting history.',{'name':text,'enabled':{'type':'boolean'}},['name','enabled'],lambda a:lab.activate(a['name'],a['enabled']))
    spec('skill_run','Execute active version with parameters JSON STRING. Each subcall and independent check is traced; stops on first failure with run_id for checkpoint resume. Never claims a failed verifier succeeded.',{'name':text,'parameters':text,'run_id':text},['name','parameters'],lambda a:lab.execute(a['name'],json.loads(a['parameters']),False,a.get('run_id')))
