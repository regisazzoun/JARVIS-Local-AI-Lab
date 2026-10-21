#!/usr/bin/env python3
"""Codex measurement scheduler; distinguishes execution from functional success."""
import argparse,datetime,hashlib,json,os,signal,subprocess,sys,time,uuid
from pathlib import Path
root=Path(__file__).parent;summary=root/'reports/suite-summary.json'
def verify():
 value=json.loads(summary.read_text());assert value['completed'] and len(value['runs'])==6
 for run in value['runs']:
  assert run['result_present'] and run['audio_present'],run['name']
 print(json.dumps(value,ensure_ascii=False));return 0
def main():
 if '--verify' in sys.argv:return verify()
 if summary.exists():
  previous=json.loads(summary.read_text())
  if not previous.get('completed'):raise RuntimeError('An incomplete campaign already exists; resume/check its process')
  archived=root/'reports'/('suite-'+previous['suite']+'-summary.json')
  if not archived.exists():archived.write_text(summary.read_text())
 ident=uuid.uuid4().hex[:10];started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 configurations=[('nominal',None,None),('barge-early-1',.6,None),('barge-early-2',.6,None),('barge-late',2.5,None),('silence',None,True),('noise',None,True)]
 value={'suite':ident,'started_utc':started,'actor':'Codex scheduler invoked by JARVIS','completed':False,'runs':[],'voice_received':False}
 summary.write_text(json.dumps(value,indent=2)+'\n')
 for name,delay,negative in configurations:
  out=root/'reports'/('suite-'+ident+'-'+name);out.mkdir(parents=True)
  wav=name if negative else 'initial'
  command=[sys.executable,str(root/'codex_capture.py'),'--wav',str(root/'fixtures'/(wav+'.wav')),'--output',str(out),'--timeout','100']
  if negative:command+=['--negative']
  if delay is not None:command+=['--interrupt-wav',str(root/'fixtures/interrupt.wav'),'--delay',str(delay),'--followup-wav',str(root/'fixtures/continuity.wav')]
  begin=time.time()
  with (out/'runner.log').open('wb') as log:
   process=subprocess.Popen(command,stdout=log,stderr=log,stdin=subprocess.DEVNULL,start_new_session=True)
   try:rc=process.wait(timeout=460)
   except subprocess.TimeoutExpired:
    os.killpg(process.pid,signal.SIGINT)
    try:rc=process.wait(timeout=10)
    except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);rc=process.wait()
  result=out/'result.json';audio=out/'received.wav'
  row={'name':name,'output':out.name,'elapsed_s':round(time.time()-begin,3),'returncode':rc,'result_present':result.exists(),'audio_present':audio.exists(),'result':json.loads(result.read_text()) if result.exists() else None}
  value['runs'].append(row);summary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps({'scenario':name,'returncode':rc,'elapsed_s':row['elapsed_s']},ensure_ascii=False),flush=True)
 value['completed']=True;value['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 value['voice_received']=all(r['result'] and r['result'].get('passed') for r in value['runs'])
 value['verdict']='GO numérique (réserves acoustiques et UI séparées)' if value['voice_received'] else 'NO-GO vocal / critères ou preuves manquants'
 summary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');(root/'reports'/('suite-'+ident+'-summary.json')).write_text(summary.read_text());print(value['verdict'],flush=True)
 return 0 if all(r['result_present'] and r['audio_present'] for r in value['runs']) else 1
if __name__=='__main__':raise SystemExit(main())
