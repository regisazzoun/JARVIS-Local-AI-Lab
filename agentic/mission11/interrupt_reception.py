"""Interrupt only the dedicated reception mission after a validated checkpoint."""
import json,pathlib,sqlite3,subprocess,time,sys
from reception import OUT
ident=json.loads((OUT/((sys.argv[1] if len(sys.argv)>1 else 'project')+'.json')).read_text())['response']['id']
path=pathlib.Path('/opt/jarvis/conversation/runtime/missions.sqlite')
for attempt in range(300):
    c=sqlite3.connect(path);c.row_factory=sqlite3.Row
    row=c.execute('SELECT * FROM missions WHERE id=?',(ident,)).fetchone()
    checks=[dict(x) for x in c.execute('SELECT * FROM checkpoints WHERE mission=? ORDER BY id',(ident,))];c.close()
    ready=any(json.loads(x['result']).get('ok') and (x['tool']=='mission_task_complete' or x['tool']=='host_exec' and 'PORT_OK=8091' in json.loads(x['result']).get('result',{}).get('stdout','')) for x in checks)
    if ready and row['state']=='running':
        snapshot={'mission':dict(row),'checkpoints':checks,'interrupt_time':time.time(),'method':'systemctl restart jarvis-conversation, broker and Dell untouched'}
        (OUT/('restart-before-'+(sys.argv[1] if len(sys.argv)>1 else 'project')+'.json')).write_text(json.dumps(snapshot,ensure_ascii=False,indent=2))
        result=subprocess.run(['sudo','-n','systemctl','restart','jarvis-conversation'],capture_output=True,text=True)
        snapshot['restart_returncode']=result.returncode
        (OUT/('restart-proof-'+(sys.argv[1] if len(sys.argv)>1 else 'project')+'.json')).write_text(json.dumps(snapshot,ensure_ascii=False,indent=2))
        print(json.dumps({'interrupted':ident,'validated_checkpoint_count':len(checks),'restart_returncode':result.returncode}));break
    if row['state'] in ('completed','reported','incomplete','failed'):
        print(json.dumps({'not_interrupted':'mission already finished','state':row['state']}));break
    time.sleep(1)
else:print('NO_INTERRUPTION: no validated task checkpoint within 300s')
