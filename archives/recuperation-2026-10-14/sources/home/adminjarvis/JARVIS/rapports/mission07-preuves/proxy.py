import http.server,http.client,json,pathlib,time,threading
p=pathlib.Path(__file__).parent;lock=threading.Lock()
class Handler(http.server.BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def run(self):
  body=self.rfile.read(int(self.headers.get('Content-Length','0')));record={'time':time.time(),'path':self.path,'method':self.command}
  try:record['payload']=json.loads(body) if body else None
  except:record['payload']='unparsed'
  c=http.client.HTTPConnection('127.0.0.1',11434,timeout=300)
  try:
   c.request(self.command,self.path,body,{k:v for k,v in self.headers.items() if k.lower() not in ['host','connection','content-length']});r=c.getresponse();self.send_response(r.status);self.send_header('Content-Type',r.getheader('Content-Type','application/json'));self.end_headers();chunks=[]
   while True:
    b=r.read1(65536)
    if not b:break
    chunks.append(b);self.wfile.write(b);self.wfile.flush()
   raw=b''.join(chunks).decode(errors='replace')
   try:record['response']=json.loads(raw)
   except:record['response_lines']=[json.loads(l) for l in raw.splitlines() if l.strip().startswith('{')]
  except Exception as e:record['error']=str(e)
  finally:
   c.close()
   with lock:
    with (p/'transmissions-privees.jsonl').open('a') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
 do_GET=run;do_POST=run;do_DELETE=run
http.server.ThreadingHTTPServer(('127.0.0.1',11436),Handler).serve_forever()
