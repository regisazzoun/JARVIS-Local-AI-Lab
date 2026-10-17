"""Bounded document readers/append, backed by the existing host broker.
These tools select actual text/table cells. Interpretation belongs to JARVIS.
"""
import json, pathlib, shlex
from jarvis.host_client import request
ROOT=pathlib.Path('/var/lib/jarvis/projects/mission00')

def register(registry):
    def read(a):
        path=a['path'];mode=a.get('mode','excerpt');ids=a.get('ids','')
        if mode not in ('excerpt','table','levels','inventory','outline'):raise ValueError('Mode inconnu')
        code='''from pathlib import Path
import json,hashlib
p=Path(PATH); text=p.read_text(); lines=text.splitlines(); mode=MODE
result={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'chars':len(text),'read_level':'chargement machine intégral ; sélection textuelle explicite'}
if mode=='table':
 wanted={i.strip() for i in IDS.split(',') if i.strip()}; rows=[]
 for line in lines:
  if not line.startswith('| **'): continue
  cells=[c.strip() for c in line.strip().strip('|').split('|')];ident=cells[0].strip('* ')
  if not wanted or ident in wanted: rows.append({'id':ident,'fonction':cells[1][:200],'etat':cells[2],'resultat':cells[3][:250] if len(cells)>3 else ''})
 result['rows']=rows
elif mode=='levels':
 result['quotes']=[l[:450] for l in lines if l.startswith(('## ','**Chemin','**Niveau','**Réserve'))][:60]
elif mode=='outline':
 result['quotes']=[l[:650] for l in lines if __import__('re').search(r'15[AB]\\.[1-5]',l)][:20]
elif mode=='inventory':
 d=json.loads(text);items=d.get('documents',d.get('files',[]));result['count']=len(items);result['unique_paths']=len({i.get('chemin_absolu',i.get('path')) for i in items});result['meta']=d.get('meta',d.get('summary',{}))
else:
 result['head']=text[:1500];result['tail']=text[-1000:];result['headings']=[l for l in lines if l.startswith('#')][:15]
print(json.dumps(result,ensure_ascii=False))
'''.replace('PATH',repr(path)).replace('MODE',repr(mode)).replace('IDS',repr(ids))
        response=request('host_exec',{'command':'python3 -c '+shlex.quote(code)})
        r=response['result'];return {**r,'evidence_id':response['evidence_id'],'selection_mode':mode}
    def append(a):
        p=pathlib.Path(a['path']).resolve()
        if not p.is_relative_to(ROOT) or p.suffix!='.md':raise ValueError('Livrable Markdown hors mission00')
        content=a['content']
        code='from pathlib import Path; p=Path('+repr(str(p))+'); p.parent.mkdir(parents=True,exist_ok=True); f=p.open("a"); f.write('+repr(content)+'); f.close(); print(p.stat().st_size)'
        response=request('host_exec',{'command':'python3 -c '+shlex.quote(code)})
        return {**response['result'],'path':str(p),'evidence_id':response['evidence_id']}
    def batch(a):
        paths=json.loads(a['paths'])
        if not isinstance(paths,list) or not 1<=len(paths)<=4 or not all(isinstance(p,str) and p.endswith('.md') for p in paths):raise ValueError('Un à quatre chemins Markdown requis')
        code="""from pathlib import Path
import json,hashlib,re
result=[]
for name in PATHS:
 p=Path(name);text=p.read_text();lines=text.splitlines()
 highlights=[l[:210] for l in lines if re.search(r'Objectif|Résultat|réserve|réception|GO |15[AB]\\.[1-5]',l,re.I)][:4]
 result.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'chars':len(text),'head':text[:700],'tail':text[-500:],'highlights':highlights,'read_level':'chargement machine intégral, extraits transmis au modèle'})
print(json.dumps(result,ensure_ascii=False))
""".replace('PATHS',repr(paths))
        response=request('host_exec',{'command':'python3 -c '+shlex.quote(code)})
        return {**response['result'],'evidence_id':response['evidence_id']}
    registry.specs['host_audit_read_batch']=('Charger réellement un à quatre rapports Markdown et retourner chemin, empreinte, début/fin et passages signalés. Aucun jugement de réception automatique.',{'paths':{'type':'string','maxLength':6000}},['paths'],'host_authorized',batch)
    registry.specs['host_audit_read']=('Lire réellement un document via le broker : excerpt (début/fin/titres), table (SUIVI, ids séparés par virgule), levels (titres et niveaux d’une extraction), inventory (compteJSON). Aucune interprétation automatique.',{'path':{'type':'string','maxLength':1200},'mode':{'type':'string','maxLength':30},'ids':{'type':'string','maxLength':200}},['path','mode'],'host_authorized',read)
    registry.specs['host_audit_append']=('Ajouter le texte rédigé par JARVIS à un livrableMarkdown dans le seul dossier mission00. Les originaux restent inchangés.',{'path':{'type':'string','maxLength':1200},'content':{'type':'string','maxLength':9000}},['path','content'],'host_authorized',append)
