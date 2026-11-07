from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit,unquote
import threading
import os
ROOT=Path(os.environ['JM01_WEB_EXPORT']).resolve()
assert (ROOT/'index.html').is_file()
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def do_GET(self):
  path=unquote(urlsplit(self.path).path)
  target=(ROOT/path.lstrip('/')).resolve()
  if not target.is_relative_to(ROOT):self.send_error(403);return
  if not target.exists() and not Path(path).suffix and not path.startswith('/selfhost/api/'):
   self.path='/index.html'
  super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',18930),Handler)
timer=threading.Timer(600,server.shutdown);timer.daemon=True;timer.start()
try:server.serve_forever()
finally:server.server_close();timer.cancel()
