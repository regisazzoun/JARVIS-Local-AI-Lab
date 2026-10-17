"""Independent acceptance assertions. Reads evidence; performs no repair or model action."""
import datetime,hashlib,json,pathlib,sqlite3,subprocess
P=pathlib.Path
OUT=P('/home/adminjarvis/JARVIS/mission11-private')
PUBLIC=P('/home/adminjarvis/JARVIS/mission11/docs/missions/11')
traces=[json.loads(x) for x in P('/opt/jarvis/conversation/runtime/tool-traces.jsonl').read_text().splitlines()]
checks=[]
def check(name,value,detail=''):
    checks.append({'check':name,'passed':bool(value),'detail':detail})
def receipt(name):
    p=OUT/(name+'.json')
    return json.loads(p.read_text()).get('response',{}) if p.exists() else {}
def selected(name):
    conv=receipt(name).get('conversation')
    return [x for x in traces if conv and x.get('conversation')==conv]
def success(name,tool,condition=lambda x:True):
    return [x for x in selected(name) if x['result']['tool']==tool and x['result']['ok'] and condition(x)]
host=receipt('host')
check('1_host_file_persistent',P('/var/lib/jarvis/projects/m11-reception/preuve.txt').read_text().strip()=='étape2-persistant')
check('1_Qwen_write_read_modify',len(success('host','host_write_file'))>=3 and len(success('host','host_read_file'))>=2)
check('2_Qwen_systemd_start_restart',all(success('host','host_service',lambda x:x['arguments'].get('action')==a) for a in ('start','restart')))
check('2_Qwen_service_active_and_logs',bool(success('service','host_service',lambda x:x['arguments'].get('action')=='is-active' and x['result']['result']['stdout'].strip()=='active')) and bool(success('service','host_logs')))
check('3_Qwen_installed_hello',bool(success('host','host_package',lambda x:x['arguments']=={'package':'hello','action':'install'})))
check('3_Qwen_executed_hello',bool(success('host','host_exec',lambda x:'Hello, world!' in x['result']['result'].get('stdout',''))))
sha=[]
for name in ('host','smoke-attempt1'):
    for x in success(name,'host_github',lambda x:x['arguments'].get('action')=='push'):
        value=x['result']['result']['stdout'].strip()
        if len(value)==40:sha.append(value)
check('4_Qwen_private_GitHub_read_commit_push',bool(success('host','host_github',lambda x:x['arguments'].get('action')=='file')) and bool(sha), 'Dedicated jarvis/mission11-proof-20261017; broker verifies pushed SHA through GitHub API')
check('4_final_implementation_updates_existing_branch',bool(success('smoke-attempt1','host_github',lambda x:x['arguments'].get('action')=='push')) and len(set(sha))>=2)
state=sqlite3.connect('/var/lib/jarvis-agent/state.sqlite');state.row_factory=sqlite3.Row
row=state.execute("SELECT state FROM capabilities WHERE capability='host_package' AND resource='tree'").fetchone()
check('5_capability_tree_validated',row and row[0]=='VALIDÉ')
request=state.execute("SELECT state FROM requests WHERE id='953c204922d74c07b6819419b16677f6'").fetchone()
check('5_persistent_request_resolved_by_real_test',request and request[0]=='VALIDÉ')
create_request=state.execute("SELECT state FROM requests WHERE id='ceb1c0e182d64acfb81c2bbb84a5bb85'").fetchone()
check('5_repository_request_resolved_by_Qwen_probe',create_request and create_request[0]=='VALIDÉ' and bool(success('jl02_repo','capability_test',lambda x:x['arguments'].get('resource')=='regisazzoun/JARVIS-Launcher2')))
repair_request=state.execute("SELECT state FROM requests WHERE id='fce4b2a1e93f4c7fbfaccb904893318f'").fetchone()
check('5_package_repair_request_resolved_by_Qwen_probe',repair_request and repair_request[0]=='VALIDÉ' and bool(success('repair_npm','capability_test',lambda x:x['arguments'].get('resource')=='npm')))
pages_request=state.execute("SELECT state FROM requests WHERE id='db4d3ae4fb5a496a8d89385d006d4a60'").fetchone()
check('5_pages_request_deferred_for_JL02',pages_request and pages_request[0]=='DEMANDÉ')
check('5_Qwen_install_and_probe',bool(success('grant','host_package',lambda x:x['arguments'].get('package')=='tree')) and bool(success('grant','capability_test',lambda x:x['arguments'].get('resource')=='tree')))
check('5_reuse_after_service_restart',bool(success('reuse','host_exec',lambda x:'tree' in x['arguments']['command'])) and not success('reuse','host_package'))
mission=sqlite3.connect('/opt/jarvis/conversation/runtime/missions.sqlite');mission.row_factory=sqlite3.Row
ident=json.loads((OUT/'project2.json').read_text())['response']['id']
record=mission.execute('SELECT * FROM missions WHERE id=?',(ident,)).fetchone()
tasks=[dict(x) for x in mission.execute('SELECT id,deps,state FROM tasks WHERE mission=?',(ident,))]
check('6_Qwen_task_graph_completed',len(tasks)==3 and all(t['state']=='validated' for t in tasks),json.dumps(tasks))
check('6_dependencies_preserved',any(json.loads(t['deps']) for t in tasks))
check('6_validated_procedure_saved',mission.execute('SELECT count(*) FROM procedures').fetchone()[0]>0)
check('6_durable_mission_completed',record['state']=='completed',record['state'])
first_ident=json.loads((OUT/'project.json').read_text())['response']['id']
first=[json.loads(x[0]) for x in mission.execute('SELECT result FROM checkpoints WHERE mission=?',(first_ident,))]
check('6_real_error_then_fix',any(x['tool']=='host_exec' and not x['ok'] and 'ValueError' in x.get('error','') for x in first) and any(x['tool']=='host_exec' and x['ok'] and 'PORT_OK=8091' in x.get('result',{}).get('stdout','') for x in first))
restart=json.loads((OUT/'restart-proof-project2.json').read_text())
check('7_actual_service_restart',restart['restart_returncode']==0 and record['attempts']>=2)
post=[json.loads(x[0]) for x in mission.execute('SELECT result FROM checkpoints WHERE mission=? AND created>?',(ident,restart['interrupt_time']))]
check('7_Qwen_reobserved_real_host',any(x['tool']=='host_read_file' and x['ok'] for x in post) and any(x['tool']=='host_exec' and x['ok'] and 'PORT_OK=8091' in x.get('result',{}).get('stdout','') for x in post))
check('7_host_scope_preserved_after_restart',not any(x['tool']=='lab_terminal' for x in post))
check('voice_synthetic_STT_Qwen_host_write_read',bool(success('voice','host_write_file')) and bool(success('voice','host_read_file')),'Synthetic speech, not physical microphone')
check('SSH_and_Ansible_real_local_transport',bool(success('remote','host_remote')) and bool(success('remote','host_ansible',lambda x:x['arguments'].get('action')=='deploy_file')) and P('/var/lib/jarvis/projects/ansible-agent-proof.txt').read_text().strip()=='ANSIBLE_AGENT_OK','Loopback profile, no distinct-machine claim')
observer=receipt('observer')
check('Dell_distinct_machine_read_only_via_Qwen',len(success('observer','host_remote'))>=3 and bool(success('observer','intervention_report')),'Dell 13D-E read-only profile; no mutation, deployment remains in progress')
check('Ansible_privileged_package_operation',bool(success('remote_admin','host_ansible',lambda x:x['arguments'].get('action')=='package_install')))
check('config_write_delete_from_normal_chat',bool(success('smoke-attempt1','host_delete_file')) and P('/etc/jarvis/managed/m11.conf').read_text().strip()=='agentic=true' and not P('/var/lib/jarvis/projects/m11-a-supprimer.txt').exists())
chat=receipt('chat_lifecycle')
check('normal_chat_mutation_lifecycle_reported',bool(success('chat_lifecycle','host_write_file')) and bool(success('chat_lifecycle','host_read_file')) and bool(success('chat_lifecycle','intervention_report')) and P('/var/lib/jarvis/projects/m11-chat-normal.txt').read_text().strip()=='chat-normal-ok')
check('npm_and_node_usable_by_Qwen',bool(success('repair_npm','capability_test',lambda x:x['arguments'].get('resource')=='npm')) or bool(success('smoke-attempt1','host_exec',lambda x:'npm' in x['arguments']['command'])))
audit=subprocess.run(['/usr/bin/dpkg','--audit'],capture_output=True,text=True)
check('dpkg_clean',audit.returncode==0 and not audit.stdout.strip() and not audit.stderr.strip())
for package in ('hello','tree','nodejs','npm'):
    r=subprocess.run(['/usr/bin/dpkg-query','-W','-f=${Status}',package],capture_output=True,text=True)
    check('installed_configured_'+package,r.returncode==0 and r.stdout=='install ok installed')
check('JL02_objective_transmitted',P('/var/lib/jarvis/projects/JL-02-OBJECTIF.md').exists() and bool(success('jl02_handoff','host_read_file')))
check('JL02_repo_access_validated',bool(success('jl02_repo','capability_test',lambda x:x['arguments'].get('resource')=='regisazzoun/JARVIS-Launcher2')))
# Verify pre-existing personal rows without exporting their content.
before=sqlite3.connect(OUT/'memory-before.sqlite');before.row_factory=sqlite3.Row
active=sqlite3.connect('/opt/jarvis/conversation/runtime/memory.sqlite');active.row_factory=sqlite3.Row
preserved={}
for table in ('memories','preferences','conversations','messages'):
    columns=before.execute('PRAGMA table_info('+table+')').fetchall();keys=[x[1] for x in columns if x[5]]
    if not keys:continue
    old=before.execute('SELECT * FROM '+table).fetchall();ok=True
    for row in old:
        found=active.execute('SELECT * FROM '+table+' WHERE '+' AND '.join(k+'=?' for k in keys),tuple(row[k] for k in keys)).fetchone()
        if found is None or tuple(found)!=tuple(row):ok=False
    preserved[table]={'rows_before':len(old),'identical':ok};check('preserved_'+table,ok,str(len(old))+' pre-existing rows')
check('canonical_SQLite_integrity',active.execute('PRAGMA quick_check').fetchone()[0]=='ok' and not active.execute('PRAGMA foreign_key_check').fetchall())
registry=[]
for x in state.execute('SELECT * FROM capabilities'):
    t=json.loads(x['last_test']);inner=t.get('result',t)
    registry.append({k:x[k] for k in ('capability','resource','machine','scope','mode','state','granted','mission','revocation')}|{'last_test':{'returncode':inner.get('returncode'),'evidence_id':t.get('evidence_id'),'caller':t.get('caller')}})
(PUBLIC/'CAPACITES.json').write_text(json.dumps({'generated':datetime.datetime.now(datetime.timezone.utc).isoformat(),'capabilities':registry,'note':'Snapshot, not authority. Effective root policy and private SQLite remain authoritative.'},ensure_ascii=False,indent=2))
requests=[]
for x in state.execute('SELECT id,payload,state,resolution,created FROM requests'):
    p=json.loads(x['payload']);r=json.loads(x['resolution']) if x['resolution'] and x['resolution'].startswith('{') else {'summary':x['resolution']}
    requests.append({'id':x['id'],'created':x['created'],'state':x['state']}|{k:p.get(k) for k in ('capability','mission','resource','required_access','persistent')}|{'resolution':r})
(PUBLIC/'DEMANDES.json').write_text(json.dumps({'generated':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requests':requests,'note':'Expurgé : état et preuves de demande, sans données d’authentification.'},ensure_ascii=False,indent=2))
result={'generated':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'Independent file/SQLite checks against real Qwen API and host broker receipts; no simulated acceptance','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'GitHub_test_commits':sha,'memory_preserved':preserved,'not_tested':['Full host reboot','Mutating administration on Dell during its active deployment','Physical microphone/speakers','GitHub Pages publication','Automatic delivery into a Codex session']}
(PUBLIC/'PREUVES-EXPURGEES.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[x['check'] for x in checks if not x['passed']]},ensure_ascii=False))
