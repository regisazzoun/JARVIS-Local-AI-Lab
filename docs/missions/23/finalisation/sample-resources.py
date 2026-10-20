#!/usr/bin/env python3
"""Independent operator measurements correlated with real verifier invocations.
No application implementation or credentials; uses the existing read-only broker.
"""
import argparse,datetime,json,os,sqlite3,sys,time
from pathlib import Path
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.host_client import request
p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=300);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
mission='7971ec0311124fb4be9e3125dcb291fd'
def cpu():
 values=list(map(int,Path('/proc/stat').read_text().splitlines()[0].split()[1:9]));return sum(values),values[3]+values[4]
def phase():
 c=sqlite3.connect('file:/opt/jarvis/conversation/runtime/missions.sqlite?mode=ro',uri=True);c.row_factory=sqlite3.Row
 rows=c.execute("SELECT id,state,arguments FROM tool_calls WHERE mission=? AND tool='host_exec' ORDER BY created DESC LIMIT 20",(mission,)).fetchall();c.close()
 for r in rows:
  cmd=json.loads(r['arguments']).get('command','')
  if '/usr/local/lib/jarvis-host/verify_livekit_' in cmd:
   if r['state']!='started':return None
   kind='voice' if 'verify_livekit_voice.py' in cmd else 'components' if 'verify_livekit_components.py' in cmd else 'llm' if '--part llm' in cmd else 'adapters'
   return {'invocation':r['id'],'phase':kind}
 return None
records=[];previous=cpu();until=time.monotonic()+args.seconds
while time.monotonic()<until:
 time.sleep(2);current=cpu();total=current[0]-previous[0];idle=current[1]-previous[1];previous=current
 memory={line.split(':')[0]:int(line.split()[1]) for line in Path('/proc/meminfo').read_text().splitlines() if line.startswith(('MemTotal:','MemAvailable:'))}
 active=phase();row={'time':time.time(),'cpu_percent':round(100*(1-idle/total),2) if total else None,'ram_used_mb':round((memory['MemTotal']-memory['MemAvailable'])/1024,2),'verifier':active}
 if active:
  try:
   response=request('host_remote',{'host':'dell-observe','action':'telemetry'});data=json.loads(response['result']['stdout']);row['dell']={k:data.get(k) for k in ['cpu_percent','ram_used_mb','ram_total_mb','gpu','active_models']};row['broker_evidence']=response.get('evidence_id')
  except Exception as e:row['measurement_error']=str(e)[:400]
 records.append(row)
 result={'author':'Codex independent operator','mission':mission,'samples':records,'scope':'Host CPU/RAM and Dell telemetry during exact runtime verifier calls; distinguish failed/successful invocations and concurrent load. Not physical microphone evidence.'}
 args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');args.output.chmod(0o600)
print(json.dumps({'samples':len(records),'during_verifier':sum(bool(r['verifier']) for r in records)}))
