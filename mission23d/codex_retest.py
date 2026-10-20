"""Restartable retest coordinator via persistent gateway; run by JARVIS."""
import hashlib,json,sys,time,urllib.request
from pathlib import Path
root=Path(__file__).parent;file=root/'reports/retest-summary.json'
def request(path,data=None):
 r=urllib.request.Request('http://127.0.0.1:8783'+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(r,timeout=15) as response:return json.load(response)
def main():
 value=json.loads(file.read_text()) if file.exists() else {'actor':'Codex retest coordinator invoked by JARVIS','completed':False,'runs':[],'active':None,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'agent_sha256':hashlib.sha256((root.parent/'livekit-agent/agent.py').read_bytes()).hexdigest()}
 if '--verify' in sys.argv:
  assert value['completed'] and len(value['runs'])==3
  for run in value['runs']:assert run['result'] is not None
  print(json.dumps(value,ensure_ascii=False));return 0
 deadline=time.monotonic()+120
 scenarios=['barge-early','barge-early','barge-late']
 while len(value['runs'])<3 and time.monotonic()<deadline:
  if value['active'] is None:
   value['active']=request('/test',{'scenario':scenarios[len(value['runs'])]});file.write_text(json.dumps(value,indent=2)+'\n')
  job=request('/test/'+value['active']['id'])
  if job['done']:
   value['runs'].append({'name':scenarios[len(value['runs'])],'id':value['active']['id'],'returncode':job['returncode'],'result':job['result'],'audio':job['audio']});value['active']=None
   file.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
  else:time.sleep(.5)
 value['completed']=len(value['runs'])==3;value['voice_received']=value['completed'] and all(r['result'].get('passed') for r in value['runs'])
 file.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'completed':value['completed'],'runs':len(value['runs']),'active':value['active'],'voice_received':value['voice_received']},ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
