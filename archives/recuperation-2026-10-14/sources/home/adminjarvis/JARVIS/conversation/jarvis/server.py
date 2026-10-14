import json,os,urllib.parse,argparse,signal,fcntl
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from .core import ROOT,Core,Busy
from .memory import Memory

def make_handler(core):
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup();self.connection.settimeout(15)
        def log_message(self,*args):pass # Do not log personal text or query strings.
        def send(self,data,status=200,mime='application/json'):
            body=data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False).encode()
            self.send_response(status);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; media-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'");self.end_headers();self.wfile.write(body)
        def guarded(self):
            host=self.headers.get('Host','')
            if host not in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'):raise PermissionError('Hôte refusé')
            origin=self.headers.get('Origin')
            if origin and origin not in (f'http://localhost:{self.server.server_port}',f'http://127.0.0.1:{self.server.server_port}'):raise PermissionError('Origine refusée')
        def do_GET(self):
            try:
                self.guarded();url=urllib.parse.urlparse(self.path);p=url.path;q=urllib.parse.parse_qs(url.query);m=core.memory
                if p=='/api/config':self.send({k:core.config[k] for k in ['models','default_model','max_record_seconds']})
                elif p=='/api/health':self.send({'application':'ok','database':'ok','ollama':'non vérifié'})
                elif p=='/api/conversations':self.send(m.list_conversations())
                elif p=='/api/history':self.send(m.history(q.get('id',[''])[0]))
                elif p=='/api/memories':self.send(m.list_memories())
                elif p=='/api/search':self.send(m.search(q.get('q',[''])[0],project=q.get('project',[None])[0],messages=q.get('type',[''])[0]=='messages'))
                elif p=='/api/export':self.send(m.export())
                elif p in ('/','/app.js','/style.css'):
                    path=ROOT/'static'/('index.html' if p=='/' else p[1:]);self.send(path.read_bytes(),mime={'/':'text/html; charset=utf-8','/app.js':'text/javascript; charset=utf-8','/style.css':'text/css; charset=utf-8'}[p])
                else:self.send({'error':'Introuvable'},404)
            except PermissionError as e:self.send({'error':str(e)},403)
            except Exception:self.send({'error':'Lecture impossible'},500)
        def do_POST(self):
            try:
                self.guarded()
                # Custom header prevents cross-origin simple-form mutation; no CORS enabled.
                if self.headers.get('X-Jarvis-Request')!='1':raise PermissionError('En-tête requis')
                size=int(self.headers.get('Content-Length','0'));audio=self.path=='/api/stt'
                if size<=0 or size>(core.config['max_audio_bytes'] if audio else 100000):raise ValueError('Requête vide ou trop volumineuse')
                raw=self.rfile.read(size);d={} if audio else json.loads(raw);p=self.path;m=core.memory
                if p=='/api/chat':self.send(core.chat(d['text'],d['model'],d.get('conversation'),d.get('project',''),d.get('retain',True)))
                elif p=='/api/stt':self.send(core.voice('stt',raw))
                elif p=='/api/tts':self.send(core.voice('tts',d['text']),mime='audio/wav')
                elif p=='/api/memory/propose':
                    if not isinstance(d.get('content'),str) or not d['content'].strip() or len(d['content'])>8000:raise ValueError('Souvenir vide ou trop long')
                    self.send({'id':m.propose(d['content'],d.get('kind','persistent'),d.get('project',''),d.get('conversation'))})
                elif p=='/api/memory/approve':m.decide(d['id'],True,d.get('explicit'));self.send({'ok':True})
                elif p=='/api/memory/reject':m.decide(d['id'],False);self.send({'ok':True})
                elif p=='/api/memory/delete':m.delete(d['id']);self.send({'ok':True})
                elif p=='/api/memory/edit':m.edit(d['id'],d['content'],d.get('project',''),d.get('explicit'));self.send({'ok':True})
                else:self.send({'error':'Introuvable'},404)
            except PermissionError as e:self.send({'error':str(e)},403)
            except Busy as e:self.send({'error':str(e)},409)
            except (ValueError,KeyError,json.JSONDecodeError) as e:self.send({'error':str(e)},400)
            except Exception:self.send({'error':'Service indisponible ou délai dépassé. Réessayer après vérification locale.'},503)
    return Handler

def main():
    os.umask(0o077)
    ap=argparse.ArgumentParser();ap.add_argument('--config',default=str(ROOT/'config/example.json'));ap.add_argument('--db',default=str(ROOT/'runtime/memory.sqlite'));args=ap.parse_args()
    runtime=ROOT/'runtime';runtime.mkdir(exist_ok=True)
    lock=open(runtime/'application.lock','w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    config=json.loads(open(args.config).read());m=Memory(args.db);m.prune(config['retention_days']);core=Core(config,m)
    # Bind is the definitive free-port check. Failure exits without affecting any existing listener.
    server=ThreadingHTTPServer(('127.0.0.1',config['port']),make_handler(core));server.daemon_threads=False
    pidfile=runtime/'application.pid';pidfile.write_text(str(os.getpid()))
    def terminate(signum,frame):raise KeyboardInterrupt
    signal.signal(signal.SIGTERM,terminate)
    print(f'JARVIS http://127.0.0.1:{server.server_port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:
        server.server_close();pidfile.unlink(missing_ok=True);lock.close()
if __name__=='__main__':main()
