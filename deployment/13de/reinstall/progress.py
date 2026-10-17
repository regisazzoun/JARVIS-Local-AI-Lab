#!/usr/bin/env python3
"""Private event ledger and console view. No inferred success from elapsed time."""
import argparse,json,pathlib,time,os
TASKS=['pxe','identity','storage','debian','accounts','ssh-password','ssh-key','ansible','nvidia','cuda','ollama','models','integration','tests','reboot','acceptance','cleanup']
p=argparse.ArgumentParser();p.add_argument('state',type=pathlib.Path);p.add_argument('--task',choices=TASKS);p.add_argument('--status',choices=['pending','running','validated','failed','blocked']);p.add_argument('--percent',type=float);p.add_argument('--measured',action='store_true');p.add_argument('--detail',default='');a=p.parse_args();os.umask(0o077)
s=json.loads(a.state.read_text()) if a.state.exists() else {t:{'status':'pending'} for t in TASKS}
if a.task:
 assert a.status
 if a.status=='validated':assert a.detail,'Validation requires recorded evidence'
 d=s[a.task]
 if a.status=='running' and d.get('status') in ['failed','blocked']:
  d.setdefault('previous_runs',[]).append({k:d.get(k) for k in ['started','finished','detail']});d['started']=int(time.time());d.pop('finished',None)
 d.setdefault('started',int(time.time()));d.update(status=a.status,updated=int(time.time()),detail=a.detail)
 if a.status in ['validated','failed','blocked']:d['finished']=int(time.time())
 d['percent']=100 if a.status=='validated' else a.percent;d['measured']=a.measured
 tmp=a.state.with_suffix('.tmp');tmp.write_text(json.dumps(s,indent=2)+'\n');tmp.replace(a.state)
count=sum(d['status']=='validated' for d in s.values());print('['+'#'*(30*count//len(TASKS))+'-'*(30-30*count//len(TASKS))+']');print(f'Progression globale : {count}/{len(TASKS)} tâches validées (pondération par tâche, pas mesure du temps restant)')
for t,d in s.items():
 mark={'validated':'✓','running':'→','failed':'✗','blocked':'!','pending':' '}.get(d['status'],' ')
 pct=d.get('percent');bar='activité non mesurée' if pct is None else f'{pct:g}% '+('mesuré' if d.get('measured') else 'estimé par étape')
 elapsed=d.get('finished',int(time.time()))-d['started'] if 'started' in d else 0
 visual='['+('#'*(int(pct)//10)+'-'*(10-int(pct)//10) if pct is not None else '   ~~~    ')+']'
 last=time.strftime('%H:%M:%S',time.localtime(d['updated'])) if 'updated' in d else '--:--:--'
 print(f'[{mark}] {visual} {t:14s} {d["status"]:10s} {bar:28s} {elapsed}s activité {last} {d.get("detail", "")}')
