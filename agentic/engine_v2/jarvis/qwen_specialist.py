"""Delegate one programming task to the existing Qwen Code adapter."""
import json,urllib.request,urllib.error
from pathlib import Path

def register(registry):
    def execute(args):
        context=getattr(registry,'context',{})
        if str(context.get('client_origin','')).startswith('QwenCode'):
            raise ValueError('Recursive Qwen Code delegation is not permitted; use programming tools directly')
        key=Path('/home/adminjarvis/JARVIS/qwen-code-openwebui-private/adapter-key').read_text().strip()
        data={**args,'namespace':'shared','parent_mission':context.get('mission_id'),'parent_task':context.get('task_id'),'trigger':'JARVIS canonical Registry'}
        request=urllib.request.Request('http://127.0.0.1:8092/tools/qwen_code',data=json.dumps(data).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+key})
        try:
            with urllib.request.urlopen(request,timeout=690) as response:return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code!=409:raise
            detail=json.loads(exc.read())
            return {'returncode':75,'execution_state':'NOT_EXECUTED','reason':detail.get('error'),'retry_condition':'Use qwen_code_status; wait for observed completion of the existing call. No duplicate was dispatched.'}
    def status(args):
        key=Path('/home/adminjarvis/JARVIS/qwen-code-openwebui-private/adapter-key').read_text().strip()
        request=urllib.request.Request('http://127.0.0.1:8092/tools/qwen_code_status',data=b'{}',headers={'Content-Type':'application/json','Authorization':'Bearer '+key})
        with urllib.request.urlopen(request,timeout=10) as response:return json.load(response)
    registry.specs['qwen_code_run']=('Déléguer une tâche de programmation à Qwen Code / Qwen80B Dell1, dans un projet existant sous /var/lib/jarvis/projects/qwen-code. Outils locaux et MCP JARVIS réels. Budget technique par appel 660s, sans plafond de tours de session. Conserver le reçu ; vérifier indépendamment le code et le test. Ne pas relancer une issue UNKNOWN sans observer ses effets.',{'task':{'type':'string','minLength':1,'maxLength':3000},'project':{'type':'string','pattern':'^[a-zA-Z0-9_-]{1,48}$'}},['task','project'],'host_authorized',execute)
    registry.specs['qwen_code_status']=('État observé du spécialiste Qwen Code et derniers reçus. busy=true : attendre sa fin, sans lancer de doublon. Un code retour nul ne vaut pas réception indépendante.',{},[],'host_authorized',status)
