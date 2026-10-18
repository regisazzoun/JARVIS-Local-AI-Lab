"""Single-user local login; secrets never enter logs or source control."""
import json,hashlib,hmac,secrets,time,threading,sqlite3
from contextlib import contextmanager
from http.cookies import SimpleCookie
from pathlib import Path
class Auth:
    def __init__(self,file,secure=False,session_db=None):
        self.credentials=json.loads(Path(file).read_text());self.secure=secure;self.sessions={};self.attempts=[];self.lock=threading.Lock();self.session_db=session_db
        if session_db:
            with self.db() as c:c.execute('CREATE TABLE IF NOT EXISTS auth_sessions(digest TEXT PRIMARY KEY,expires REAL NOT NULL)')
    @contextmanager
    def db(self):
        c=sqlite3.connect(self.session_db,timeout=10)
        try:
            with c:yield c
        finally:c.close()
    def login(self,user,password):
        if not isinstance(user,str) or not isinstance(password,str) or len(password)>256:raise ValueError('Identifiants invalides')
        with self.lock:
            now=time.monotonic();self.attempts=[t for t in self.attempts if now-t<60]
            if len(self.attempts)>=8:raise PermissionError('Trop de tentatives. Attendre une minute.')
            self.attempts.append(now)
            hashed=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(self.credentials['salt']),300000).hex()
            if not hmac.compare_digest(user,self.credentials['username']) or not hmac.compare_digest(hashed,self.credentials['hash']):raise PermissionError('Identifiants incorrects')
            self.sessions={k:v for k,v in self.sessions.items() if v>now}
            if len(self.sessions)>=32:self.sessions.pop(next(iter(self.sessions)))
            token=secrets.token_urlsafe(32);self.sessions[token]=now+28800
            if self.session_db:
                with self.db() as c:
                    c.execute('DELETE FROM auth_sessions WHERE expires<=?',(time.time(),))
                    c.execute('INSERT INTO auth_sessions VALUES(?,?)',(hashlib.sha256(token.encode()).hexdigest(),time.time()+28800))
                    c.execute('DELETE FROM auth_sessions WHERE digest NOT IN (SELECT digest FROM auth_sessions ORDER BY expires DESC LIMIT 32)')
            self.attempts=[];return token
    def token(self,headers):
        try:
            cookie=SimpleCookie();cookie.load(headers.get('Cookie',''));return cookie['jarvis_session'].value
        except Exception:return ''
    def valid(self,headers):
        token=self.token(headers)
        with self.lock:
            if self.sessions.get(token,0)>time.monotonic():return True
            if not self.session_db:return False
            with self.db() as c:
                row=c.execute('SELECT expires FROM auth_sessions WHERE digest=?',(hashlib.sha256(token.encode()).hexdigest(),)).fetchone()
            return bool(row and row[0]>time.time())
    def logout(self,headers):
        with self.lock:
            token=self.token(headers);self.sessions.pop(token,None)
            if self.session_db:
                with self.db() as c:c.execute('DELETE FROM auth_sessions WHERE digest=?',(hashlib.sha256(token.encode()).hexdigest(),))
    def cookie(self,token):return 'jarvis_session='+token+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800'+('; Secure' if self.secure else '')
