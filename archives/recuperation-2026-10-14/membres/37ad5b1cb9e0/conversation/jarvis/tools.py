"""Bounded tool registry. Never interpolate model arguments into shell commands."""
import json,subprocess,time,platform,shutil,os
from pathlib import Path
from .memory import now

def command(argv):
    p=subprocess.run(argv,capture_output=True,text=True,timeout=8,env={**os.environ,'LC_ALL':'C'})
    return {'returncode':p.returncode,'stdout':p.stdout[:12000],'stderr':p.stderr[:2000]}

class Registry:
    def __init__(self,memory,root,config=None):
        self.memory=memory;self.root=Path(root);self.context={};self.config=config or {}
        self.specs={
          'system_status':('État réel CPU/RAM et système, lecture seule',{},[], 'read_only',lambda a:{'system':platform.system(),'release':platform.release(),'load':os.getloadavg(),'memory':command(['free','-m'])}),
          'disk_usage':('Espace disque du dossier JARVIS, lecture seule',{},[], 'read_only',lambda a:dict(zip(['total','used','free'],shutil.disk_usage(self.root)))),
          'jarvis_services':('État actuel des services JARVIS, Ollama et Open WebUI, lecture seule',{},[], 'read_only',self.services),
          'software_versions':('Versions Python, SQLite et API Ollama, lecture seule',{},[], 'read_only',self.versions),
          'propose_memory':('Proposer un souvenir durable, jamais approuver. Il reste en attente de validation humaine.',{'content':{'type':'string','maxLength':4000}},['content'],'pending_write',self.propose)
        }
    def services(self,args):
        result={'systemd':command(['systemctl','show','jarvis-conversation.service','jarvis-ollama.service','jarvis-open-webui.service','--property=Id,ActiveState,SubState,MainPID']), 'interpretation':'Open WebUI utilise une unité oneshot Docker. active/exited et MainPID=0 sont normaux et ne prouvent pas une panne ; utiliser la vérification HTTP.'}
        import urllib.request
        url=self.config.get('webui_health_url')
        if url:
            try:
                with urllib.request.urlopen(url,timeout=4) as r:result['open_webui_http']={'status':r.status,'body':json.load(r)}
            except Exception:result['open_webui_http']={'status':'non vérifiable'}
        return result
    def versions(self,args):
        import sqlite3,urllib.request
        result={'python':platform.python_version(),'sqlite':sqlite3.sqlite_version}
        try:
            with urllib.request.urlopen('http://127.0.0.1:11434/api/version',timeout=5) as r:result['ollama']=json.load(r)
        except Exception:result['ollama']='indisponible'
        return result
    def propose(self,args):
        return {'id':self.memory.propose(args['content'],project=self.context.get('project',''),conversation=self.context.get('conversation')),'status':'pending','approval_required':True}
    def schemas(self):
        return [{'type':'function','function':{'name':name,'description':s[0],'parameters':{'type':'object','properties':s[1],'required':s[2],'additionalProperties':False}}} for name,s in self.specs.items()]
    def execute(self,name,args):
        start=time.monotonic();result=None
        try:
            if name not in self.specs:raise ValueError('Outil inconnu ou non autorisé')
            description,props,required,risk,fn=self.specs[name]
            if risk not in ('read_only','pending_write'):raise ValueError('Risque non autorisé dans 13E')
            if not isinstance(args,dict) or set(args)-set(props) or any(k not in args for k in required):raise ValueError('Arguments invalides')
            for k,v in args.items():
                if props[k]['type']=='string' and (not isinstance(v,str) or not v.strip() or len(v)>props[k].get('maxLength',4000)):raise ValueError('Texte invalide')
            result={'ok':True,'result':fn(args),'risk':risk}
        except subprocess.TimeoutExpired:result={'ok':False,'error':'Délai outil dépassé'}
        except Exception as e:result={'ok':False,'error':str(e)}
        result.update(tool=name,elapsed_s=round(time.monotonic()-start,3))
        with self.memory.connect() as c:
            c.execute('INSERT INTO tool_audit(tool,risk,ok,elapsed,created) VALUES(?,?,?,?,?)',(name,self.specs[name][3] if name in self.specs else 'denied',int(result['ok']),result['elapsed_s'],now()))
        return result
