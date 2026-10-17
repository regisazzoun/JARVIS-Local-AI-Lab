#!/usr/bin/env python3
"""Private event ledger and console view. No inferred success from elapsed time."""
import argparse,json,pathlib,time,os,fcntl
TASKS=['pxe','identity','storage','debian','accounts','ssh-password','ssh-key','ansible','nvidia','cuda','ollama','models','integration','tests','reboot','acceptance','cleanup']
p=argparse.ArgumentParser();p.add_argument('state',type=pathlib.Path);p.add_argument('--task',choices=TASKS);p.add_argument('--status',choices=['pending','running','validated','failed','blocked']);p.add_argument('--percent',type=float);p.add_argument('--measured',action='store_true');p.add_argument('--detail',default='');p.add_argument('--details',action='store_true');a=p.parse_args();os.umask(0o077)
lock=open(str(a.state)+'.lock','a');fcntl.flock(lock,fcntl.LOCK_EX)
s=json.loads(a.state.read_text()) if a.state.exists() else {t:{'status':'pending'} for t in TASKS}
if a.task:
 assert a.status
 if a.status=='validated':assert a.detail,'Validation requires recorded evidence'
 d=s[a.task]
 if a.status=='running' and d.get('status') != 'running':
  d.setdefault('previous_runs',[]).append({k:d.get(k) for k in ['started','finished','detail']});d['started']=int(time.time());d.pop('finished',None)
 d.setdefault('started',int(time.time()));d.update(status=a.status,updated=int(time.time()),detail=a.detail)
 if a.status in ['validated','failed','blocked']:d['finished']=int(time.time())
 d['percent']=100 if a.status=='validated' else a.percent;d['measured']=a.measured
 tmp=a.state.with_suffix('.tmp');tmp.write_text(json.dumps(s,indent=2)+'\n');tmp.replace(a.state)
labels=dict(pxe='PXE',identity='Identité',storage='Stockage RAID',debian='Debian',accounts='Comptes',**{'ssh-password':'SSH mot de passe','ssh-key':'SSH par clé'},ansible='Ansible',nvidia='NVIDIA',cuda='CUDA',ollama='Ollama',models='Modèles',integration='Intégration JARVIS',tests='Tests',reboot='Redémarrage',acceptance='Réception finale',cleanup='Nettoyage')
statuses=dict(validated='validé',running='en cours',pending='à venir',failed='échec',blocked='bloqué')
count=sum(d['status']=='validated' for d in s.values());print('['+'#'*(30*count//len(TASKS))+'-'*(30-30*count//len(TASKS))+']');print(f'Progression globale : {count}/{len(TASKS)} tâches validées (pondération par tâche, pas mesure du temps restant)')
for t,d in s.items():
 mark={'validated':'✓','running':'→','failed':'✗','blocked':'!','pending':' '}.get(d['status'],' ')
 pct=d.get('percent');bar='100% validé' if d['status']=='validated' else 'activité non mesurée' if pct is None else f'{pct:g}% '+('mesuré' if d.get('measured') else 'estimé par étape')
 elapsed=d.get('finished',int(time.time()))-d['started'] if 'started' in d else 0
 visual='['+('#'*(int(pct)//10)+'-'*(10-int(pct)//10) if pct is not None else '   ~~~    ')+']'
 last=time.strftime('%H:%M:%S',time.localtime(d['updated'])) if 'updated' in d else '--:--:--'
 shown=' -- ' if pct is None else f'{pct:g}%'
 print(f'[{mark}] {labels[t]:18s} {visual} {statuses[d["status"]]:8s} {shown:6s} {elapsed//60:4d}m {last}')
 if a.details and d.get('detail'):print('    '+d['detail'])
