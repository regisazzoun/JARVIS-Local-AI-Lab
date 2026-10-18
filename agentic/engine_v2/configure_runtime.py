#!/usr/bin/env python3
"""Apply measured mission22 settings while preserving private credentials/URLs.
Run on the canonical Mac mini. Discovers the existing local model catalogue;
does not download models or alter the Dell, SSH, accounts or host policy.
"""
import datetime,json,os,pathlib,shutil,urllib.request
p=pathlib.Path('/opt/jarvis/conversation/config/13e.json')
if os.geteuid()!=0:raise SystemExit('Operator root required')
config=json.loads(p.read_text())
if config['ollama_url'].rstrip('/') in ('http://127.0.0.1:11434','http://localhost:11434'):raise SystemExit('An existing configured Dell endpoint is required; no remote node is invented')
with urllib.request.urlopen('http://127.0.0.1:11434/api/tags',timeout=10) as response:
    local={m['name'] for m in json.load(response).get('models',[])}
if config['default_model'] not in local:raise SystemExit('Local default model absent; retain existing routing, do not download implicitly')
backup=pathlib.Path('/var/backups/jarvis/mission22/runtime-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json')
backup.parent.mkdir(parents=True,exist_ok=True,mode=0o700);shutil.copy2(p,backup);backup.chmod(0o600)
config.setdefault('ollama_nodes',{}).update({'Mac-mini':'http://127.0.0.1:11434','Dell1':config['ollama_url']})
config['ollama_route']=['Mac-mini','Dell1'];config['mission_ollama_route']=['Dell1','Mac-mini']
config.update(num_ctx=16384,durable_num_ctx=16384,durable_num_predict=-1,ollama_timeout=None)
stat=p.stat();temporary=p.with_suffix('.mission22.tmp');temporary.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n');temporary.chmod(stat.st_mode&0o777);os.chown(temporary,stat.st_uid,stat.st_gid);os.replace(temporary,p)
print('Measured settings applied; existing private configuration retained; restart canonical service when ready.')
