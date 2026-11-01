"""Installation only. Never launches MCP servers, tests, browsers or missions."""
import pathlib, subprocess, json, os, concurrent.futures, threading
R=pathlib.Path.home()/'JARVIS/modules-standard-20261101'
UV=R/'venvs/bootstrap/bin/uv'
STATE=R/'installation-status.json'
states={}; lock=threading.Lock()
def record(name,status,**kw):
 with lock:
  states[name]={'status':status,**kw}
  STATE.write_text(json.dumps(states,indent=2))
 print(name,status,flush=True)
def run(cmd,log,env=None,timeout=1800,cwd=None):
 p=subprocess.run([str(c) for c in cmd],stdout=log,stderr=log,env=env,timeout=timeout,cwd=cwd)
 if p.returncode:raise RuntimeError('installer exit '+str(p.returncode))
def py(name,packages):
 record(name,'installing')
 try:
  with (R/'logs'/('install-'+name+'.log')).open('w') as log:
   v=R/'venvs'/name
   run([UV,'venv','--python','3.12',v],log)
   run([UV,'pip','install','--python',v/'bin/python']+packages,log)
   with (R/(name+'-packages.lock')).open('w') as out:
    subprocess.run([str(UV),'pip','freeze','--python',str(v/'bin/python')],stdout=out,stderr=log,check=True)
  record(name,'installed-not-tested',venv=str(v))
 except Exception as e:record(name,'installation-failed',error=str(e))
tasks=[
 ('documents',['python-docx==1.2.0','openpyxl==3.1.5','python-pptx==1.0.2','reportlab==5.1.0','pypdf==6.21.2','pdfplumber==0.11.10','pypdfium2==5.14.0','pymupdf','pytesseract','pypandoc_binary']),
 ('markitdown',[str(R/'sources/markitdown/packages/markitdown')+'[docx,pptx,xlsx,pdf]',str(R/'sources/markitdown/packages/markitdown-mcp')]),
 ('pfsense',[str(R/'sources/pfsense')]),
 ('nagios',[str(R/'sources/nagios')]),
 ('netbox-enhanced',[str(R/'sources/netbox-enhanced')]),
 ('netbox-official',[str(R/'sources/netbox-official')]),
 ('cisco-pyats',[str(R/'sources/cisco-pyats')]),
 ('pandoc-mcp',['mcp[cli]','pypandoc_binary']),
 ('fetch',['mcp-server-fetch']),
 ('ansible',['ansible-core','ansible-lint','ansible-navigator']),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 list(ex.map(lambda t:py(*t),tasks))
record('node24','installing')
try:
 with (R/'logs/install-node24.log').open('w') as log:
  run(['npm','install','--prefix',R/'node-runtime','--no-audit','--no-fund','node@24'],log)
 record('node24','installed-not-tested')
except Exception as e:record('node24','installation-failed',error=str(e))
env=os.environ.copy();env['PATH']=str(R/'node-runtime/node_modules/.bin')+':'+env['PATH']
npm_tasks=[('filesystem','@modelcontextprotocol/server-filesystem'),('playwright','@playwright/mcp'),('drawio','@drawio/mcp'),('ansible-mcp','@ansible/ansible-mcp-server')]
for name,pkg in npm_tasks:
 record(name,'installing')
 try:
  with (R/'logs'/('install-'+name+'.log')).open('w') as log:
   run(['npm','install','--prefix',R/'npm'/name,'--save-exact','--no-audit','--no-fund',pkg],log,env=env)
  record(name,'installed-not-tested',package=pkg)
 except Exception as e:record(name,'installation-failed',error=str(e))
if states.get('ansible',{}).get('status')=='installed-not-tested':
 record('ansible-collections','installing')
 try:
  with (R/'logs/install-ansible-collections.log').open('w') as log:
   run([R/'venvs/ansible/bin/ansible-galaxy','collection','install','ansible.windows','microsoft.ad','cisco.ios','-p',R/'collections'],log,env=env)
  record('ansible-collections','installed-not-tested')
 except Exception as e:record('ansible-collections','installation-failed',error=str(e))
