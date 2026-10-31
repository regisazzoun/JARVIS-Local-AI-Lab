"""Local stdio MCP interoperability backed by the actual JARVIS Registry."""
import asyncio
import json
import os
from pathlib import Path
import sys

ROOT = Path('/opt/jarvis/conversation')
# Explicit useful slice, derived schemas and execution from the same registry.
EXPOSED = {'capability_status','host_service','host_logs','host_read_file','host_remote','host_ansible','skill_list','skill_run','google_mcp'}


def is_mutating(arguments):
    if arguments.get('action')!='call':return False
    name=arguments.get('name')
    value=json.loads(arguments.get('arguments','{}'))
    if not isinstance(value,dict):raise ValueError('MCP arguments must be a JSON object')
    if name=='skill_run':return True
    if name=='google_mcp':
        from .google_mcp import is_mutating as google_mutation
        return google_mutation(value)
    if name=='host_service':return value.get('action') not in ('status','is-active','is-enabled')
    if name=='host_ansible':return value.get('action') not in ('ping','resources')
    if name=='host_remote':return value.get('action') not in ('identity','resources','services','proof','read_file','tailscale_status')
    return False


def build_registry():
    from .tools import Registry
    from .memory import Memory
    config=json.loads((ROOT/'config/13e.json').read_text())
    registry=Registry(Memory(ROOT/'runtime/memory.sqlite'),ROOT,config)
    registry.context={'host_target':True,'mission_id':os.environ.get('JARVIS_MCP_MISSION')}
    return registry


async def serve():
    from mcp.server.lowlevel import Server
    from mcp.server.stdio import stdio_server
    from mcp import types
    registry=build_registry();server=Server('jarvis-registry-25')

    @server.list_tools()
    async def listing():
        return [types.Tool(name=s['function']['name'],description=s['function']['description'],inputSchema=s['function']['parameters']) for s in registry.schemas(True) if s['function']['name'] in EXPOSED]

    @server.call_tool()
    async def call(name,arguments):
        if name not in EXPOSED:raise ValueError('Tool not exposed by this adapter')
        result=await asyncio.to_thread(registry.execute,name,arguments or {})
        return types.CallToolResult(content=[types.TextContent(type='text',text=json.dumps(result,ensure_ascii=False))],isError=not result['ok'])

    async with stdio_server() as (read,write):
        await server.run(read,write,server.create_initialization_options())


async def client(action,name,arguments,mission=None):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    params=StdioServerParameters(command=sys.executable,args=['-m','jarvis.mcp_gateway'],cwd=str(ROOT),env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'JARVIS_MCP_MISSION':mission or ''})
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            initialized=await session.initialize()
            if action=='list':
                result=await session.list_tools()
                return {'server':initialized.serverInfo.model_dump(),'protocol_version':initialized.protocolVersion,'transport':'stdio','tools':[t.model_dump(exclude_none=True) for t in result.tools]}
            if action!='call':raise ValueError('action must be list or call')
            result=await session.call_tool(name,arguments)
            payload=[]
            for block in result.content:
                if block.type=='text':
                    try:payload.append(json.loads(block.text))
                    except (ValueError,TypeError):payload.append({'error':block.text})
            return {'returncode':1 if result.isError else 0,'transport':'stdio','server':initialized.serverInfo.model_dump(),'isError':result.isError,'responses':payload}


def register(registry):
    def invoke(a):
        if a['action']=='call' and not a.get('name'):raise ValueError('MCP call requires name')
        value=asyncio.run(asyncio.wait_for(client(a['action'],a.get('name'),json.loads(a.get('arguments','{}')),registry.context.get('mission_id')),timeout=600))
        # MCP subreceipts retain their broker evidence IDs. Import into the same
        # durable ledger so verifiers/cockpit see executions rather than prose.
        store=getattr(registry,'mission_store',None)
        if store:
            def collect(v):
                if isinstance(v,list):
                    for x in v:collect(x)
                elif isinstance(v,dict):
                    if v.get('tool') and 'ok' in v and v.get('result',{}).get('evidence_id'):
                        store.event(registry.context['mission_id'],'mcp_broker_receipt',registry.context.get('task_id'),'JARVIS-MCP',v['tool'],result=v)
                    for x in v.values():collect(x)
            collect(value.get('responses',[]))
        return value
    registry.specs['mcp_tools']=('Use installed local MCP adapter over real stdio: action=list discovers actual schemas; action=call requires name and arguments JSON STRING object. Same broker/policy, no arbitrary server. Exposes capability_status, host_service/logs/read_file/remote/ansible, skill_list/run and google_mcp. Returns real protocol version and structured receipts; errors are not success.',{'action':{'type':'string','enum':['list','call']},'name':{'type':'string'},'arguments':{'type':'string','maxLength':16000}},['action'],'host_authorized',invoke)


if __name__=='__main__':asyncio.run(serve())
