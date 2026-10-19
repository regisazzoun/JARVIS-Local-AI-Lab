import json,threading,unittest,urllib.request
from types import SimpleNamespace
from http.server import ThreadingHTTPServer
from jarvis.server import make_handler
class Store:
 def get(self,ident):return {'id':ident,'state':'waiting_external','conversation':'original','active_task':'t12_code_github','updated':1}
 def tasks(self,ident):return [{'state':'validated'}]*11+[{'state':'pending'}]*2
class Controller:
 def __init__(self):self.store=Store();self.submissions=[];self.resumes=[]
 def submit(self,goal,*args):self.submissions.append(goal);return {'id':'new-memory-request','conversation':'memory'}
 def resume(self,ident):self.resumes.append(ident);return {'id':ident,'state':'queued'}
class HttpIntent(unittest.TestCase):
 def test_question_resume_and_memory_routing(self):
  control=Controller();core=SimpleNamespace(config={},missions=control,memory=SimpleNamespace())
  core.config.update(max_audio_bytes=100000,max_text_chars=100000)
  server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(core));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  def post(goal):
   req=urllib.request.Request('http://127.0.0.1:'+str(server.server_port)+'/api/missions',data=json.dumps({'goal':goal,'model':'test'}).encode(),headers={'Content-Type':'application/json','X-Jarvis-Request':'1'})
   return json.load(urllib.request.urlopen(req))
  try:
   q=post("Quel est l'état de la mission 23 ?");self.assertNotIn('id',q);self.assertEqual(control.submissions,[])
   r=post('Reprends la mission 23 et termine les tâches restantes');self.assertEqual(r['id'],'7971ec0311124fb4be9e3125dcb291fd');self.assertEqual(len(control.resumes),1);self.assertEqual(control.submissions,[])
   post('Lance la mission 24 — Mémoire enrichie');self.assertEqual(control.submissions,['Lance la mission 24 — Mémoire enrichie'])
  finally:server.shutdown();server.server_close();thread.join()
