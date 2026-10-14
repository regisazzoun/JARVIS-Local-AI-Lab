"""Single-user local login; secrets never enter logs or source control."""
import json,hashlib,hmac,secrets,time,threading
from http.cookies import SimpleCookie
from pathlib import Path
class Auth:
    def __init__(self,file,secure=False):
        self.credentials=json.loads(Path(file).read_text());self.secure=secure;self.sessions={};self.attempts=[];self.lock=threading.Lock()
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
            token=secrets.token_urlsafe(32);self.sessions[token]=now+28800;self.attempts=[];return token
    def token(self,headers):
        try:
            cookie=SimpleCookie();cookie.load(headers.get('Cookie',''));return cookie['jarvis_session'].value
        except Exception:return ''
    def valid(self,headers):
        with self.lock:return self.sessions.get(self.token(headers),0)>time.monotonic()
    def logout(self,headers):
        with self.lock:self.sessions.pop(self.token(headers),None)
    def cookie(self,token):return 'jarvis_session='+token+'; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800'+('; Secure' if self.secure else '')
