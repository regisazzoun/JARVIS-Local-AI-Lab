"""SQLite repository. No implicit promotion. All IDs are application UUIDs."""
import sqlite3, json, uuid, datetime, os
from pathlib import Path
from contextlib import contextmanager,closing

def uid(): return str(uuid.uuid4())
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

MIGRATIONS = [(1, '''
CREATE TABLE conversations(id TEXT PRIMARY KEY, project TEXT NOT NULL, created TEXT NOT NULL);
CREATE TABLE messages(id TEXT PRIMARY KEY, conversation TEXT REFERENCES conversations(id) ON DELETE CASCADE, role TEXT NOT NULL CHECK(role IN ('user','assistant')), content TEXT NOT NULL, model TEXT NOT NULL, created TEXT NOT NULL);
CREATE VIRTUAL TABLE messages_fts USING fts5(id UNINDEXED,content);
CREATE TABLE memories(id TEXT PRIMARY KEY, kind TEXT NOT NULL CHECK(kind IN ('persistent','temporary','project')), project TEXT NOT NULL, conversation TEXT, content TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('pending','approved','rejected')), created TEXT NOT NULL, updated TEXT NOT NULL);
CREATE VIRTUAL TABLE memories_fts USING fts5(id UNINDEXED,content);
CREATE TABLE audit(id INTEGER PRIMARY KEY, operation TEXT NOT NULL, target TEXT NOT NULL, created TEXT NOT NULL);
'''), (2, '''
ALTER TABLE memories ADD COLUMN active INTEGER NOT NULL DEFAULT 1;
ALTER TABLE memories ADD COLUMN expires TEXT;
CREATE TABLE documents(id TEXT PRIMARY KEY,project TEXT NOT NULL,source TEXT NOT NULL,content TEXT NOT NULL,created TEXT NOT NULL);
CREATE VIRTUAL TABLE documents_fts USING fts5(id UNINDEXED,content);
CREATE TABLE tool_audit(id INTEGER PRIMARY KEY,tool TEXT NOT NULL,risk TEXT NOT NULL,ok INTEGER NOT NULL,elapsed REAL NOT NULL,created TEXT NOT NULL);
''')]

class Memory:
    def __init__(self,path):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as c:
            c.execute('CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY)')
            version=c.execute('SELECT COALESCE(MAX(version),0) FROM schema_version').fetchone()[0]
            if version>len(MIGRATIONS): raise ValueError('Schéma plus récent : ouverture refusée')
            for v,sql in MIGRATIONS:
                if v>version:
                    c.executescript('BEGIN IMMEDIATE;'+sql+f'INSERT INTO schema_version VALUES({v}); COMMIT;')
        os.chmod(self.path,0o600)
    @contextmanager
    def connect(self):
        c=sqlite3.connect(self.path,timeout=10);c.row_factory=sqlite3.Row
        c.execute('PRAGMA foreign_keys=ON')
        try:
            with c:yield c
        finally:c.close()
    def log(self,c,op,target): c.execute('INSERT INTO audit(operation,target,created) VALUES(?,?,?)',(op,target,now()))
    def conversation(self,project=''):
        id=uid()
        with self.connect() as c:c.execute('INSERT INTO conversations VALUES(?,?,?)',(id,project,now()))
        return id
    def history(self,id):
        with self.connect() as c:return [dict(r) for r in c.execute('SELECT * FROM messages WHERE conversation=? ORDER BY created,rowid',(id,))]
    def list_conversations(self):
        with self.connect() as c:return [dict(r) for r in c.execute('SELECT * FROM conversations ORDER BY created DESC')]
    def exchange(self,id,user,answer,model):
        with self.connect() as c:
            for role,text in [('user',user),('assistant',answer)]:
                mid=uid();c.execute('INSERT INTO messages VALUES(?,?,?,?,?,?)',(mid,id,role,text,model,now()))
                c.execute('INSERT INTO messages_fts VALUES(?,?)',(mid,text))
    def propose(self,content,kind='persistent',project='',conversation=None):
        if kind not in ('persistent','project','temporary'):raise ValueError('Type de mémoire invalide')
        if kind=='temporary' and not conversation:raise ValueError('Session requise pour une mémoire temporaire')
        if kind!='temporary':conversation=None
        if not isinstance(content,str):raise ValueError('Texte requis')
        content=' '.join(content.split())
        if not content or len(content)>8000:raise ValueError('Souvenir vide ou trop long')
        id=uid();status='approved' if kind=='temporary' else 'pending'
        with self.connect() as c:
            c.execute('BEGIN IMMEDIATE')
            for row in c.execute("SELECT id,content FROM memories WHERE kind=? AND project=? AND COALESCE(conversation,'')=? AND status IN ('pending','approved') AND active=1",(kind,project,conversation or '')):
                if row['content'].casefold()==content.casefold():return row['id']
            c.execute('INSERT INTO memories(id,kind,project,conversation,content,status,created,updated) VALUES(?,?,?,?,?,?,?,?)',(id,kind,project,conversation,content,status,now(),now()))
            if status=='approved':c.execute('INSERT INTO memories_fts VALUES(?,?)',(id,content))
            self.log(c,'propose',id)
        return id
    def decide(self,id,approve,explicit=False):
        if approve and explicit is not True:raise ValueError('Validation explicite requise')
        with self.connect() as c:
            r=c.execute('SELECT * FROM memories WHERE id=?',(id,)).fetchone()
            if not r or r['status']!='pending':raise ValueError('Proposition absente ou déjà traitée')
            c.execute('UPDATE memories SET status=?,updated=? WHERE id=?',('approved' if approve else 'rejected',now(),id))
            if approve:c.execute('INSERT INTO memories_fts VALUES(?,?)',(id,r['content']))
            self.log(c,'approve' if approve else 'reject',id)
    def edit(self,id,content,project,explicit=False):
        if explicit is not True:raise ValueError('Validation explicite requise')
        if not isinstance(content,str) or not content.strip() or len(content)>8000:raise ValueError('Souvenir vide ou trop long')
        with self.connect() as c:
            r=c.execute("SELECT id FROM memories WHERE id=? AND status='approved'",(id,)).fetchone()
            if not r:raise ValueError('Souvenir validé absent')
            for other in c.execute("SELECT content FROM memories WHERE id!=? AND project=? AND active=1 AND status IN ('approved','pending')",(id,project)):
                if ' '.join(other['content'].split()).casefold()==' '.join(content.split()).casefold():raise ValueError('Souvenir identique déjà présent')
            c.execute('UPDATE memories SET content=?,project=?,updated=? WHERE id=?',(content,project,now(),id))
            c.execute('DELETE FROM memories_fts WHERE id=?',(id,));c.execute('INSERT INTO memories_fts VALUES(?,?)',(id,content));self.log(c,'edit',id)
    def delete(self,id):
        with self.connect() as c:
            c.execute('DELETE FROM memories WHERE id=?',(id,));c.execute('DELETE FROM memories_fts WHERE id=?',(id,));self.log(c,'delete',id)
    def list_memories(self):
        with self.connect() as c:return [dict(r) for r in c.execute('SELECT * FROM memories ORDER BY created DESC')]
    def search(self,query,project=None,conversation=None,messages=False):
        # Treat search as literal terms, never expose raw MATCH operators.
        import re
        terms=re.findall(r'\w+',query,flags=re.UNICODE)[:12]
        if not terms:return []
        match=' OR '.join('"'+t+'"' for t in terms)
        with self.connect() as c:
            if messages:
                sql='SELECT m.* FROM messages m JOIN messages_fts f ON m.id=f.id JOIN conversations a ON a.id=m.conversation WHERE messages_fts MATCH ?'
                params=[match]
                if project is not None:sql+=' AND a.project=?';params.append(project)
            else:
                sql="SELECT m.* FROM memories m JOIN memories_fts f ON m.id=f.id WHERE memories_fts MATCH ? AND m.status='approved' AND m.active=1 AND (m.expires IS NULL OR m.expires>?) AND (m.kind!='temporary' OR m.conversation=?)"
                params=[match,now(),conversation]
                if project is not None:sql+=" AND (m.project='' OR m.project=?)";params.append(project)
            return [dict(r) for r in c.execute(sql+' LIMIT 12',params)]
    def prune(self,days):
        cutoff=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(days=days)).isoformat()
        with self.connect() as c:
            c.execute('DELETE FROM messages_fts WHERE id IN (SELECT id FROM messages WHERE created<?)',(cutoff,))
            c.execute('DELETE FROM messages WHERE created<?',(cutoff,))
    def export(self):
        with self.connect() as c:return {t:[dict(r) for r in c.execute('SELECT * FROM '+t)] for t in ['schema_version','conversations','messages','memories','audit','documents','tool_audit']}
    def backup(self,target):
        target=Path(target)
        if target.exists():raise ValueError('Destination existante refusée')
        with self.connect() as src,closing(sqlite3.connect(target)) as dest:src.backup(dest)
        os.chmod(target,0o600)
    @staticmethod
    def restore(source,target):
        if Path(target).exists():raise ValueError('Restauration uniquement vers un nouveau fichier de test')
        with closing(sqlite3.connect(f'file:{Path(source).resolve()}?mode=ro',uri=True)) as src:
            if src.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('Sauvegarde invalide')
            with closing(sqlite3.connect(target)) as dest:src.backup(dest)
        os.chmod(target,0o600)
        return Memory(target)

    def obsolete(self,id,explicit=False):
        if explicit is not True:raise ValueError('Validation explicite requise')
        with self.connect() as c:
            c.execute('UPDATE memories SET active=0,updated=? WHERE id=?',(now(),id))
            c.execute('DELETE FROM memories_fts WHERE id=?',(id,));self.log(c,'obsolete',id)
    def document(self,content,source,project=''):
        id=uid()
        with self.connect() as c:
            c.execute('INSERT INTO documents VALUES(?,?,?,?,?)',(id,project,source,content,now()));c.execute('INSERT INTO documents_fts VALUES(?,?)',(id,content))
        return id
    def document_search(self,query,project=''):
        import re
        terms=re.findall(r'\w+',query)[:10]
        if not terms:return []
        match=' OR '.join('"'+t+'"' for t in terms)
        with self.connect() as c:return [dict(r) for r in c.execute("SELECT d.* FROM documents d JOIN documents_fts f ON d.id=f.id WHERE documents_fts MATCH ? AND (project='' OR project=?) LIMIT 4",(match,project))]
