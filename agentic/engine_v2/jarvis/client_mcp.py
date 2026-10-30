"""Compact stdio client connector, backed by the existing JARVIS facade."""
import asyncio,json,os
from .client_capabilities import Capabilities

async def serve():
    from mcp.server.lowlevel import Server
    from mcp.server.stdio import stdio_server
    from mcp import types
    api=Capabilities(origin='QwenCode/MCP',mission=os.environ.get('JARVIS_MCP_MISSION'),task=os.environ.get('JARVIS_MCP_TASK'))
    server=Server('jarvis-client-capabilities')
    definitions=[('jarvis_catalog','Discover real JARVIS capabilities, paginated. query filters names/descriptions; offset follows next_offset.',{'query':{'type':'string'},'offset':{'type':'integer'}},[]),('jarvis_schema','Get exact schema for one real tool before calling it.',{'name':{'type':'string'}},['name']),('jarvis_call','Execute one real JARVIS tool. arguments is a JSON string object matching jarvis_schema. Existing broker policy and canonical audit apply. A tool receipt is not independent verification.',{'name':{'type':'string'},'arguments':{'type':'string'}},['name','arguments']),('jarvis_missions','List/read/create canonical missions. Creation only when owner requests a new mission; id for read, goal for create. after paginates events.',{'action':{'type':'string','enum':['list','read','create']},'id':{'type':'string'},'goal':{'type':'string'},'after':{'type':'integer'},'profile':{'type':'string','enum':['standard','service_observation']}},['action']),('jarvis_receipt','Read back a durable client tool receipt from canonical memory audit.',{'id':{'type':'integer'},'offset':{'type':'integer'},'limit':{'type':'integer','maximum':3000}},['id'])]
    definitions.append(('jarvis_remote_project','Execute a real remote project command on one Dell through existing host_remote/project_exec. host is mandatory; never substitute local execution for a remote result. Existing broker policy and receipts apply.',{'host':{'type':'string','enum':['dell-observe','dell2']},'project':{'type':'string'},'command':{'type':'string','maxLength':16000}},['host','project','command']))
    @server.list_tools()
    async def listing():return [types.Tool(name=n,description=d,inputSchema={'type':'object','properties':p,'required':r,'additionalProperties':False}) for n,d,p,r in definitions]
    @server.call_tool()
    async def call(name,a):
        try:
            if name=='jarvis_catalog':result=await asyncio.to_thread(api.catalog,a.get('query',''),a.get('offset',0))
            elif name=='jarvis_schema':result=await asyncio.to_thread(api.schema,a['name'])
            elif name=='jarvis_call':result=await asyncio.to_thread(api.call,a['name'],json.loads(a['arguments']))
            elif name=='jarvis_missions':result=await asyncio.to_thread(api.missions,a['action'],a.get('id'),a.get('goal'),a.get('after',0),a.get('profile','standard'))
            elif name=='jarvis_receipt':result=await asyncio.to_thread(api.receipt,a['id'],a.get('offset',0),a.get('limit',3000))
            elif name=='jarvis_remote_project':result=await asyncio.to_thread(api.call,'host_remote',{'host':a['host'],'action':'project_exec','project':a['project'],'command':a['command']})
            else:raise ValueError('Unknown tool')
            completed=result.get('client_receipt',{}).get('call_completed',result.get('ok',True))
            return types.CallToolResult(content=[types.TextContent(type='text',text=json.dumps(result,ensure_ascii=False))],isError=not completed)
        except Exception as exc:return types.CallToolResult(content=[types.TextContent(type='text',text=json.dumps({'ok':False,'error':str(exc),'operation_dispatch_not_proven':True}))],isError=True)
    async with stdio_server() as (read,write):await server.run(read,write,server.create_initialization_options())
if __name__=='__main__':asyncio.run(serve())
