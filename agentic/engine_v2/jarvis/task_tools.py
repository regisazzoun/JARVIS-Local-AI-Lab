"""Persistent task graph and proven procedure library; separate from personal memories."""
import json,sqlite3,time

def register(registry):
    path=registry.root/'runtime/missions.sqlite'
    def connect():
        c=sqlite3.connect(path,timeout=30);c.row_factory=sqlite3.Row
        c.executescript('''CREATE TABLE IF NOT EXISTS tasks(mission TEXT,id TEXT,title TEXT,deps TEXT,state TEXT,evidence TEXT,updated REAL,PRIMARY KEY(mission,id));
        CREATE TABLE IF NOT EXISTS procedures(id INTEGER PRIMARY KEY,title TEXT,content TEXT,evidence TEXT,created REAL);''');return c
    def key():return registry.context.get('mission_id') or registry.context.get('conversation') or 'direct'
    def plan(args):
        tasks=json.loads(args['tasks'])
        if not isinstance(tasks,list) or not 0<len(tasks)<=30:raise ValueError('Liste de 1 à 30 tâches requise')
        if any(not isinstance(t,dict) or set(t)!={'id','title','depends'} or not isinstance(t['depends'],list) for t in tasks):raise ValueError('Chaque tâche exige exactement id, title, depends (liste des identifiants ; [] si aucune dépendance)')
        byid={t['id']:t for t in tasks}
        if len(byid)!=len(tasks):raise ValueError('Identifiants dupliqués')
        def visit(ident,chain):
            if ident in chain:raise ValueError('Dépendance cyclique')
            if ident not in byid:raise ValueError('Dépendance absente')
            for dep in byid[ident].get('depends',[]):visit(dep,chain+[ident])
        for ident in byid:visit(ident,[])
        with connect() as c:
            existing=c.execute('SELECT id FROM tasks WHERE mission=?',(key(),)).fetchall()
            if existing:
                result=status({});result['note']='Plan déjà enregistré : conserve ces identifiants et reprends les tâches restantes ; ne recrée pas le plan.';return result
            for t in tasks:c.execute('INSERT OR IGNORE INTO tasks VALUES(?,?,?,?,?,?,?)',(key(),t['id'],t['title'],json.dumps(t.get('depends',[])),'pending','[]',time.time()))
        return status({})
    def status(args):
        with connect() as c:
            rows=[]
            for x in c.execute('SELECT * FROM tasks WHERE mission=?',(key(),)):
                row=dict(x);proof=json.loads(row.pop('evidence'));row['evidence_ids']=[p.get('result',{}).get('evidence_id') for p in proof];rows.append(row)
            procedures=[{'id':x['id'],'title':x['title'],'content':x['content'][:1200]} for x in c.execute('SELECT * FROM procedures ORDER BY id DESC LIMIT 5')]
        done=sum(r['state']=='validated' for r in rows)
        return {'mission':key(),'tasks':rows,'progress':{'validated':done,'total':len(rows),'percent':round(100*done/len(rows)) if rows else 0},'procedures':procedures}
    def complete(args):
        # An evidence id must correspond to a successful host result from this conversation.
        evidence=args['evidence_id'];trace=registry.root/'runtime/tool-traces.jsonl'
        matched=[];candidates=[]
        if trace.exists():
            for line in trace.read_text().splitlines():
                item=json.loads(line);r=item['result']
                if item.get('conversation')==registry.context.get('conversation') and r.get('ok') and r.get('result',{}).get('evidence_id'):candidates.append(r)
        if registry.context.get('mission_id'):
            with connect() as c:
                exists=c.execute("SELECT 1 FROM sqlite_master WHERE name='checkpoints'").fetchone()
                for row in c.execute('SELECT result FROM checkpoints WHERE mission=? ORDER BY id',(key(),)) if exists else []:
                    r=json.loads(row[0])
                    if r.get('ok') and r.get('result',{}).get('evidence_id'):candidates.append(r)
        if evidence=='last_success' and candidates:matched=[candidates[-1]]
        else:matched=[r for r in candidates if r['result']['evidence_id']==evidence]
        if not matched:raise ValueError('Preuve réussie de cette conversation absente')
        with connect() as c:
            row=c.execute('SELECT * FROM tasks WHERE mission=? AND id=?',(key(),args['id'])).fetchone()
            if not row:raise ValueError('Tâche absente')
            for dep in json.loads(row['deps']):
                other=c.execute('SELECT state FROM tasks WHERE mission=? AND id=?',(key(),dep)).fetchone()
                if not other or other['state']!='validated':raise ValueError('Dépendance non validée')
            c.execute('UPDATE tasks SET state=?,evidence=?,updated=? WHERE mission=? AND id=?',('validated',json.dumps(matched),time.time(),key(),args['id']))
        return status({})
    def learn(args):
        # Procedures are technical observations, never authorization or personal memory.
        with connect() as c:
            row=c.execute('SELECT evidence FROM tasks WHERE mission=? AND state=?',(key(),'validated')).fetchall()
            if not row:raise ValueError('Aucune tâche vérifiée pour capitaliser cette procédure')
            c.execute('INSERT INTO procedures(title,content,evidence,created) VALUES(?,?,?,?)',(args['title'],args['content'],json.dumps([json.loads(x[0]) for x in row]),time.time()))
        return {'saved':True,'authority':'Technical procedure only; never owner authorization'}
    for name,description,fields,fn in [
      ('mission_plan','Plan durable : tasks chaîne JSON liste [{id,title,depends:[id]}], dépendances sans cycles ; indépendant de la mémoire personnelle.',['tasks'],plan),
      ('mission_progress','Lire tâches, progression validée et procédures techniques précédentes.',[],status),
      ('mission_task_complete','Valider tâche par preuve hôte réussie evidence_id (ou last_success) issue de cette conversation/mission ; dépendances doivent être validées.',['id','evidence_id'],complete),
      ('procedure_save','Capitaliser une procédure technique après au moins une tâche réellement validée. Ne confère aucun droit.',['title','content'],learn)]:
        registry.specs[name]=(description,{k:{'type':'string','maxLength':10000} for k in fields},fields,'host_authorized',fn)
