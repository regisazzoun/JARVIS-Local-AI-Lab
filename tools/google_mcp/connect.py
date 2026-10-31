"""Browser-only Google publisher OAuth, with loopback callback and upstream storage.

Run from an owner SSH session forwarding localhost8769. Tokens never enter stdout,
model prompts, HTTP logs or Git. The publisher handles Google code exchange/refresh.
"""
import argparse,base64,hmac,json,secrets,subprocess,sys,time
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlencode,urlparse,parse_qs
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.google_mcp import profile_dir,environment

def auth_url(settings,csrf,port):
    state=base64.b64encode(json.dumps({'manual':False,'uri':f'http://127.0.0.1:{port}/oauth2callback','csrf':csrf}).encode()).decode()
    return 'https://accounts.google.com/o/oauth2/v2/auth?'+urlencode({'client_id':settings['clientId'],'redirect_uri':settings['cloudFunctionUrl'],'response_type':'code','scope':' '.join(settings['scopes']),'access_type':'offline','prompt':'consent select_account','state':state})

def validate_callback(query,csrf):
    if not hmac.compare_digest(query.get('state',[''])[0],csrf):raise PermissionError('Invalid OAuth state')
    credentials={key:query.get(key,[''])[0] for key in ('access_token','refresh_token','expiry_date','scope','token_type')}
    if query.get('error') or not credentials['access_token'] or not credentials['refresh_token'] or not credentials['expiry_date'].isdigit():raise ValueError('Authorization incomplete')
    return credentials

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--profile',choices=['personal','education'],required=True);parser.add_argument('--port',type=int,default=8769);args=parser.parse_args()
    if not 1024<=args.port<=65535:parser.error('Use an unprivileged local port')
    directory=profile_dir(args.profile);bridge=directory/'auth-bridge.js'
    settings=json.loads(subprocess.check_output(['/usr/bin/node',str(bridge),'settings'],env=environment(),text=True,timeout=15))
    csrf=secrets.token_urlsafe(32);outcome={'saved':False,'attempts':0}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*unused):pass
        def do_GET(self):
            if urlparse(self.path).path=='/':
                self.send_response(302);self.send_header('Location',auth_url(settings,csrf,args.port));self.send_header('Cache-Control','no-store');self.send_header('Referrer-Policy','no-referrer');self.end_headers();return
            if urlparse(self.path).path!='/oauth2callback':self.send_error(404);return
            query=parse_qs(urlparse(self.path).query)
            try:credentials=validate_callback(query,csrf)
            except (PermissionError,ValueError):
                outcome['attempts']+=1;self.send_error(400,'Authorization incomplete or invalid state; no credentials saved');return
            proc=subprocess.run(['/usr/bin/node',str(bridge),'save'],input=json.dumps(credentials),env=environment(),capture_output=True,text=True,timeout=15)
            if proc.returncode:outcome['attempts']+=1;self.send_error(500,'Local credential storage failed');return
            outcome['saved']=True;self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Referrer-Policy','no-referrer');self.end_headers()
            self.wfile.write(b'<script>history.replaceState(null,"","/connected")</script><p>Compte Google raccorde. Vous pouvez fermer cet onglet.</p>')
    with HTTPServer(('127.0.0.1',args.port),Handler) as server:
        server.timeout=5
        print('Profil :',args.profile,'— OAuth fourni par le connecteur, aucun projet Cloud personnel requis.',flush=True)
        print(f'Lien court a ouvrir sur le MacBook avec le transfert SSH actif : http://127.0.0.1:{args.port}/',flush=True)
        print('Ouvre cette URL dans ton navigateur et selectionne le compte correspondant :\n'+auth_url(settings,csrf,args.port),flush=True)
        deadline=time.monotonic()+600
        while not outcome['saved'] and outcome['attempts']<3 and time.monotonic()<deadline:server.handle_request()
    if not outcome['saved']:raise SystemExit('Authentification non terminee ; aucune reussite annoncee. Relancer la commande pour un nouveau parcours.')
    print('Jetons enregistres dans le profil prive. Les tests Google distants restent a effectuer.',flush=True)
if __name__=='__main__':main()
