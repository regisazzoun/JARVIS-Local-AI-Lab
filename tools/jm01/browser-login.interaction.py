# Codex independent interaction QA of actual ExpoWeb export; simulated HTTP only.
import socket,urllib.request,json,base64,hashlib,os,struct,time
from pathlib import Path
from urllib.parse import urlsplit
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
targets=json.load(opener.open('http://127.0.0.1:18932/json/list',timeout=10))
target=next(t for t in targets if t.get('type')=='page' and t.get('url','').startswith('http://127.0.0.1:18930'))
u=urlsplit(target['webSocketDebuggerUrl']);sock=socket.create_connection((u.hostname,u.port),timeout=10);sock.settimeout(15)
key=base64.b64encode(os.urandom(16)).decode();sock.sendall(f'GET {u.path} HTTP/1.1\r\nHost: {u.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'.encode())
headers=b''
while not headers.endswith(b'\r\n\r\n'):headers+=sock.recv(1)
assert b'101' in headers.splitlines()[0]
accept=base64.b64encode(hashlib.sha1((key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest())
assert accept.lower() in headers.lower()
def exact(n):
 b=b''
 while len(b)<n:
  q=sock.recv(n-len(b))
  if not q:raise EOFError()
  b+=q
 return b
def send(payload,opcode=1):
 b=payload if isinstance(payload,bytes) else json.dumps(payload).encode();n=len(b);mask=os.urandom(4)
 h=bytes([128|opcode,128|n]) if n<126 else bytes([128|opcode,128|126])+struct.pack('!H',n) if n<65536 else bytes([128|opcode,128|127])+struct.pack('!Q',n)
 sock.sendall(h+mask+bytes(v^mask[i%4] for i,v in enumerate(b)))
def receive():
 data=b''
 while True:
  a,b=exact(2);n=b&127
  if n==126:n=struct.unpack('!H',exact(2))[0]
  if n==127:n=struct.unpack('!Q',exact(8))[0]
  mask=exact(4) if b&128 else None;part=exact(n)
  if mask:part=bytes(v^mask[i%4] for i,v in enumerate(part))
  if a&15==9:send(part,10);continue
  if a&15==8:raise EOFError()
  data+=part
  if a&128:return json.loads(data)
seq=0
def call(method,params=None):
 global seq
 seq+=1;send({'id':seq,'method':method,'params':params or {}})
 while True:
  result=receive()
  if result.get('id')==seq:
   if 'error' in result:raise RuntimeError(result['error'])
   return result.get('result',{})
requests = []
exceptions = []

def call(method, params=None):
    global seq
    seq += 1
    ident = seq
    send({'id': ident, 'method': method, 'params': params or {}})
    while True:
        result = receive()
        if result.get('method') == 'Fetch.requestPaused':
            event = result['params']
            request = event['request']
            url = request['url']
            if request['method'] == 'HEAD' and url == 'http://127.0.0.1:18930/':
                send({'id': 90000 + seq, 'method': 'Fetch.continueRequest', 'params': {'requestId': event['requestId']}})
                continue
            requests.append({'url': url, 'method': request['method'], 'postData': request.get('postData')})
            if url == 'http://127.0.0.1:18930/selfhost/api/config?skipToast=true&skipSentryReport=true':
                code = 200
                body = {'status': True, 'name': 'JM-01 LOCAL SIMULATION', 'version': '0.0-test',
                        'features': {'auth': True, 'enable_login_form': True}, 'oauth': {'providers': {}}}
            elif url == 'http://127.0.0.1:18930/selfhost/api/v1/auths/signin':
                code, body = 401, {'detail': 'Simulated invalid credentials'}
            else:
                code, body = 503, {'detail': 'Unexpected request blocked by isolated QA'}
            send({'id': 100000 + len(requests), 'method': 'Fetch.fulfillRequest', 'params': {
                'requestId': event['requestId'], 'responseCode': code,
                'responseHeaders': [{'name': 'Content-Type', 'value': 'application/json'}],
                'body': base64.b64encode(json.dumps(body).encode()).decode()}})
        if result.get('method') == 'Runtime.exceptionThrown':
            exceptions.append(result['params'])
        if result.get('id') == ident:
            if 'error' in result:
                raise RuntimeError(result['error'])
            return result.get('result', {})

def evaluate(expression):
    result = call('Runtime.evaluate', {'expression': expression, 'returnByValue': True})
    if 'exceptionDetails' in result:
        raise RuntimeError(result['exceptionDetails'])
    return result['result'].get('value')

def pump(seconds):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        evaluate('1')
        time.sleep(.1)

def enter(index, text):
    evaluate(f'(()=>{{const input=document.querySelectorAll("input")[{index}]; input.focus(); input.select();}})()')
    call('Input.insertText', {'text': text})
    evaluate(f'document.querySelectorAll("input")[{index}].blur()')

def disabled():
    return evaluate('''(()=>{const b=document.querySelector('[data-testid="sign-in-submit"]');return b ? (b.disabled || b.getAttribute('aria-disabled')==='true') : null})()''')

checks = []
output = Path(os.environ.get('JM01_QA_OUTPUT', 'interaction-simulee.json'))
try:
    call('Page.enable')
    call('Runtime.enable')
    call('Fetch.enable', {'patterns': [
        {'urlPattern': '*', 'resourceType': 'XHR', 'requestStage': 'Request'},
        {'urlPattern': '*', 'resourceType': 'Fetch', 'requestStage': 'Request'}]})
    call('Emulation.setDeviceMetricsOverride', {'width': 430, 'height': 932, 'deviceScaleFactor': 1, 'mobile': True})
    call('Page.reload', {'ignoreCache': False})
    pump(3)
    assert evaluate('document.querySelectorAll("input").length') == 3
    assert disabled() is True
    checks.append('Empty real form cannot submit')
    enter(0, 'http://127.0.0.1:18930/selfhost?token=x')
    pump(2)
    assert not requests, requests
    checks.append('Invalid query URL rejected without API request')
    enter(0, 'http://127.0.0.1:18930/selfhost/api/')
    pump(3)
    assert any(r['url'] == 'http://127.0.0.1:18930/selfhost/api/config?skipToast=true&skipSentryReport=true' for r in requests), requests
    assert evaluate('document.body.innerText.includes("JM-01 LOCAL SIMULATION")')
    checks.append('Actual config request preserves prefix and displays simulated server')
    enter(1, 'invalid')
    enter(2, 'dummy-local-only')
    pump(1)
    assert disabled() is True
    checks.append('Invalid email blocks sign-in despite server configuration')
    enter(1, 'qa@example.invalid')
    pump(1)
    assert disabled() is False, evaluate('document.body.innerText')
    checks.append('Valid dummy credentials enable real submit button')
    evaluate('''document.querySelector('[data-testid="sign-in-submit"]').click()''')
    pump(3)
    posted = [r for r in requests if r['method'] == 'POST']
    assert len(posted) == 1 and posted[0]['url'] == 'http://127.0.0.1:18930/selfhost/api/v1/auths/signin', requests
    assert json.loads(posted[0]['postData']) == {'email': 'qa@example.invalid', 'password': 'dummy-local-only'}, posted
    assert evaluate('document.querySelectorAll("input").length') == 3
    checks.append('Real submit reaches prefixed auth endpoint; simulated401 stays on login')
    assert not exceptions, exceptions
    result = {'status': 'PASS', 'scope': 'Actual ExpoWeb client; HTTP responses simulated by CDP, no real backend authentication',
              'checks': checks, 'requests': requests, 'text': evaluate('document.body.innerText'), 'exceptions': exceptions}
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False))
except Exception as error:
    output.with_name('interaction-diagnostic-' + str(time.time_ns()) + '.json').write_text(json.dumps({
        'status': 'FAIL', 'error': repr(error), 'checks_completed': checks, 'requests': requests,
        'text': evaluate('document.body.innerText'), 'inputs': evaluate('Array.from(document.querySelectorAll("input")).map(i=>i.value)'), 'exceptions': exceptions}, ensure_ascii=False, indent=2))
    raise
finally:
    try:
        call('Browser.close')
    except Exception:
        pass
    sock.close()
