"""Codex supplied route regression. Real Handler with declared fixture dependencies."""
import sys,json,types,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'backend'))
# Standalone Dell worker: supply the broker boundary only, never a copied route.
probes=[]
fixture={'available':True,'cpu_percent':0.0,'sampled_at':1000,'gpus':[{'name':'RTX 3090','utilization':0},{'name':'RTX 3080','utilization':0}]}
client=types.ModuleType('jarvis.host_client')
def request(tool,args):
 assert tool=='host_remote' and args['action']=='telemetry_v3'
 probes.append(args['host']);return {'result':{'stdout':json.dumps(fixture)}}
client.request=request
sys.modules['jarvis']=types.ModuleType('jarvis');sys.modules['jarvis.host_client']=client
import telemetry_probe
telemetry_probe.collect=lambda:{'available':True,'cpu_percent':0}
import server
h=object.__new__(server.Handler);h.path='/api/launcher/resources';h.headers={'Host':'localhost:8766'}
def upstream(path,*args):
 body={'authenticated':True} if path=='/api/session' else {'machines':{'mac-mini':{},'dell-1':{},'dell-2':{'available':False}}}
 return 200,{},json.dumps(body).encode()
h.upstream=upstream;responses=[];h.send=lambda body,status=200,*a,**kw:responses.append((body,status))
h.do_GET()
assert responses and responses[-1][1]==200,responses
assert 'dell2' in probes,'Actual resources route never called the Dell2 probe'
assert responses[-1][0]['machines']['dell-2']['cpu_percent']==0.0
assert responses[-1][0]['machines']['dell-2']['gpus']==fixture['gpus']
print('Real resources Handler consumed injected Dell2 probe; fixture boundary, not network acceptance')
