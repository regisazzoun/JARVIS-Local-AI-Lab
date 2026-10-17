"""Observe the actual durable worker; never edits a mission or performs its actions."""
import json,time
from reception import login,call,OUT
login();ident=json.loads((OUT/'project2.json').read_text())['response']['id'];last=None
for attempt in range(240):
    rows=call('/api/missions');row=next(x for x in rows if x['id']==ident)
    state=(row['state'],row['attempts'])
    if state!=last:print(json.dumps({'id':ident,'state':state[0],'attempts':state[1],'progress':row.get('progress')},ensure_ascii=False),flush=True);last=state
    if row['state']=='completed':
        (OUT/'missions-final.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));break
    if row['state'] in ('failed','reported') or row['state']=='incomplete' and row['attempts']>=5:
        (OUT/'missions-final.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));raise SystemExit('Durable mission not completed; inspect saved evidence')
    time.sleep(2)
else:raise SystemExit('Durable completion timeout; state retained')
