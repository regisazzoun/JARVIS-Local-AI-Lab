import os,json,time,importlib.util,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
private=Path(__file__).parent;os.environ['MISSION11_EVIDENCE']=str(private/'auth');(private/'auth').mkdir(exist_ok=True,mode=0o700)
spec=importlib.util.spec_from_file_location('auth','/home/adminjarvis/JARVIS/mission11/agentic/mission11/reception.py');auth=importlib.util.module_from_spec(spec);spec.loader.exec_module(auth)
def once(path,data=None):
 req=urllib.request.Request('http://localhost:8765'+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json','X-Jarvis-Request':'1'})
 with auth.client.open(req,timeout=30) as r:return json.load(r)
auth.call=once;auth.login();jar=next(h.cookiejar for h in auth.client.handlers if hasattr(h,'cookiejar'))
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/home/adminjarvis/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell',headless=True,args=['--use-gl=angle','--use-angle=swiftshader'])
 context=browser.new_context();context.add_cookies([{'name':c.name,'value':c.value,'domain':'localhost','path':c.path,'httpOnly':True,'sameSite':'Strict'} for c in jar]);page=context.new_page();page.set_default_timeout(90000);faults=[];page.on('pageerror',lambda e:faults.append(str(e)))
 page.goto('http://localhost:8766/')
 for attempt in range(30):
  if page.evaluate('Boolean(window.jl03?.state.currentConversation?.id && document.querySelectorAll(".machine-card").length===3)'):break
  page.wait_for_timeout(500)
 else:raise AssertionError('App initialization not observed')
 telemetry=page.evaluate('''async()=>{const data=await window.jl03.api('/api/launcher/resources');const {renderTelemetry}=await import('/telemetry.js');const el=document.createElement('div');renderTelemetry(el,data);const node=data.machines['dell-2'];return {available:node.available,cpu_percent:node.cpu_percent,gpus:node.gpus?.map(g=>g.name),rendered:el.textContent,actualTopbar:document.querySelector('#telemetry').textContent};}''')
 assert telemetry['available'] and len(telemetry['gpus'])==2,telemetry
 assert 'RTX 3090' in telemetry['rendered'] and 'RTX 3080' in telemetry['rendered'],telemetry
 page.route('**/api/chat',lambda route:route.fulfill(status=200,content_type='application/json',body='{"answer":""}'))
 failure=page.evaluate('''async()=>{window.jl03.state.history=[];window.jl03.state.autoplay=false;await window.jl03.sendPrompt('fixture réponse vide');return {messages:[...document.querySelectorAll('.msg')].map(e=>({role:e.className,text:e.textContent})),input:document.querySelector('#prompt-input').value};}''')
 assert len(failure['messages'])==2 and sum('Aucune réponse reçue' in m['text'] for m in failure['messages'])==1,failure
 assert failure['input']=='fixture réponse vide',failure
 page.unroute('**/api/chat')
 started=time.time()
 conversation=page.evaluate('''async()=>{const c=await window.jl03.api('/api/v3/conversation',{method:'POST',body:{project:'JL03-COR-P1-RECETTE-CODEX'}});window.jl03.state.currentConversation=c;window.jl03.state.currentProject=c.project;window.jl03.state.history=[];await window.jl03.sendPrompt('Bonjour');return {id:c.id,history:window.jl03.state.history,busy:window.jl03.state.busy};}''')
 assert len(conversation['history'])==2 and conversation['history'][1]['role']=='assistant' and conversation['history'][1]['content'].strip(),conversation
 assert not conversation['busy'],conversation
 proof={'actor':'Codex independent browser reception','at':time.time(),'checks':{'actual_authenticated_telemetry_Dell2':True,'actual_renderer_two_GPU':True,'empty_response_fixture_error_once':True,'retry_input_retained':True,'real_conversation_response':True,'no_page_errors':not faults},'telemetry':telemetry,'error_fixture':failure,'conversation':{'id':conversation['id'],'answer_chars':len(conversation['history'][1]['content']),'elapsed_s':time.time()-started},'page_errors':faults,'scope':'Real authenticated API/DOM/one conversation; empty API response deliberately injected and labelled fixture; no physical voice or autonomy reception'}
 (private/'browser-reception.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'checks':proof['checks'],'conversation':proof['conversation'],'gpus':telemetry['gpus']}));assert all(proof['checks'].values())
 browser.close()
