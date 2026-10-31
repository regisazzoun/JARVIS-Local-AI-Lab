"""Pinned upstream Workspace MCP, using existing Registry/client receipts.

No credentials are returned to models; browser authentication is a separate CLI.
Per-profile directories anchor upstream encrypted storage, without changing HOME.
"""
import asyncio,fcntl,json,os,subprocess
from pathlib import Path

INSTALL=Path('/opt/jarvis/google-workspace-mcp')
PROFILES=Path('/home/adminjarvis/.config/jarvis/google-mcp')
FEATURES='chat.read:off,chat.write:off,people.read:off,slides.read:off,slides.write:off,tasks.read:off,tasks.write:off,gmail.send:off,gmail.sendDraft:off,calendar.deleteEvent:off,calendar.respondToEvent:off,drive.trashFile:off'
ALLOWED={'docs.create','docs.getText','docs.getSuggestions','docs.writeText','docs.replaceText','docs.formatText',
 'drive.search','drive.findFolder','drive.getComments','drive.downloadFile','drive.createFolder','drive.moveFile','drive.renameFile',
 'calendar.list','calendar.listEvents','calendar.getEvent','calendar.findFreeTime','calendar.createEvent','calendar.updateEvent',
 'gmail.search','gmail.get','gmail.downloadAttachment','gmail.listLabels','gmail.createDraft',
 'sheets.getText','sheets.getRange','sheets.getMetadata','time.getCurrentDate','time.getCurrentTime','time.getTimeZone'}

ADDITIONS={
 'sheets.create':{'name':'sheets.create','description':'JARVIS additive bridge, not an upstream MCP method. Create a spreadsheet using upstream OAuth and its existing Drive scope. Requires authenticated reception.','inputSchema':{'type':'object','properties':{'title':{'type':'string','minLength':1,'maxLength':200}},'required':['title'],'additionalProperties':False}},
 'sheets.writeRange':{'name':'sheets.writeRange','description':'JARVIS additive bridge, not an upstream MCP method. Write RAW cell values using upstream OAuth/Drive scope, then independently read via sheets.getRange.','inputSchema':{'type':'object','properties':{'spreadsheetId':{'type':'string','pattern':'^[a-zA-Z0-9_-]{1,256}$'},'range':{'type':'string','minLength':1,'maxLength':300},'values':{'type':'array','maxItems':1000,'items':{'type':'array','maxItems':100,'items':{'type':['string','number','boolean','null']}}}},'required':['spreadsheetId','range','values'],'additionalProperties':False}}
}

def profile_dir(profile,root=PROFILES):
    if profile not in ('personal','education'):raise ValueError('Use personal or education')
    directory=Path(root)/profile
    if directory.is_symlink():raise ValueError('Profile directory must not be a symlink')
    return directory

def environment():
    return {**os.environ,'GEMINI_CLI_WORKSPACE_FORCE_FILE_STORAGE':'true','WORKSPACE_FEATURE_OVERRIDES':FEATURES,'BROWSER':'www-browser','CI':'1'}

def credential_status(profile,root=PROFILES):
    directory=profile_dir(profile,root)
    if not (directory/'auth-bridge.js').is_file():return {'profile':profile,'installed':False,'state':'NOT_INSTALLED','remote_access_verified':False}
    proc=subprocess.run(['/usr/bin/node',str(directory/'auth-bridge.js'),'status'],env=environment(),capture_output=True,text=True,timeout=15)
    if proc.returncode:return {'profile':profile,'installed':True,'state':'CREDENTIAL_ERROR','remote_access_verified':False}
    value=json.loads(proc.stdout)
    return {'profile':profile,'installed':True,**value,'state':'CONFIGURED_NOT_TESTED' if value['configured'] else 'AUTH_REQUIRED',
       'setup':'google-mcp-connect --profile '+profile,'setup_execution_location':'Terminal du MacBook via SSH avec transfert local8769 ; cette commande ne va pas dans la barre d’adresse du navigateur.','browser_step':'Ouvrir uniquement l’URL Google ensuite affichée par la commande.','owner_cloud_project_required':False}

def confined_download(path,root):
    root=Path(root);dest=Path(path)
    if root.resolve()!=root or not dest.is_absolute() or not dest.resolve().is_relative_to(root):raise ValueError('Download destination must remain under '+str(root))

def validate_call(name,arguments,profile):
    if name not in ALLOWED and name not in ADDITIONS:raise ValueError('Tool not exposed; email sending and destructive operations require a separate explicit owner action')
    if not isinstance(arguments,dict):raise ValueError('arguments must be an object')
    if name in ADDITIONS:
        from jsonschema import validate
        validate(arguments,ADDITIONS[name]['inputSchema'])
    if name in ('calendar.createEvent','calendar.updateEvent') and arguments.get('attendees'):raise ValueError('No invitations in this reception; omit attendees')
    if name=='gmail.createDraft':
        for attachment in arguments.get('attachments',[]):
            confined_download(attachment['filePath'],Path('/var/lib/jarvis/projects/google-mcp')/profile/'downloads')
    # Upstream download tools bypass the host broker: constrain their destinations.
    if name in ('drive.downloadFile','gmail.downloadAttachment'):
        root=Path('/var/lib/jarvis/projects/google-mcp')/profile/'downloads'
        for key in ('localPath','outputPath','filePath','downloadPath'):
            if key in arguments:
                confined_download(arguments[key],root)
        if not any(k in arguments for k in ('localPath','outputPath','filePath','downloadPath')):raise ValueError('Explicit confined download destination required')

async def upstream(profile,action,name=None,arguments=None,root=PROFILES):
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    directory=profile_dir(profile,root)
    params=StdioServerParameters(command='/usr/bin/node',args=[str(directory/'index.js'),'--use-dot-names'],cwd=str(directory),env=environment())
    if action=='call' and name in ADDITIONS:
        proc=await asyncio.create_subprocess_exec('/usr/bin/node',str(directory/'auth-bridge.js'),'sheets-api',env=environment(),stdin=asyncio.subprocess.PIPE,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        try:out,err=await proc.communicate(json.dumps({'name':name,'arguments':arguments}).encode())
        except BaseException:
            if proc.returncode is None:proc.kill();await proc.wait()
            raise
        if proc.returncode:
            return {'mcp_is_error':True,'content':[{'error':'Sheets bridge rejected request; no credentials printed.','outcome':'UNKNOWN'}],'implementation':'Codex additive bridge with upstream AuthManager'}
        return {'mcp_is_error':False,'content':[json.loads(out)],'implementation':'Codex additive bridge with upstream AuthManager'}
    log=directory/'mcp-stderr.log'
    with log.open('a') as errlog:
        log.chmod(0o600)
        async with stdio_client(params,errlog=errlog) as (read,write):
            async with ClientSession(read,write) as session:
                init=await session.initialize()
                if action in ('list','schema'):
                    response=await session.list_tools()
                    return {'server':init.serverInfo.model_dump(),'protocol_version':init.protocolVersion,'tools':[t.model_dump(exclude_none=True) for t in response.tools if t.name in ALLOWED]}
                response=await session.call_tool(name,arguments or {})
                blocks=[]
                for block in response.content:
                    if block.type=='text':
                        try:blocks.append(json.loads(block.text))
                        except ValueError:blocks.append({'text':block.text})
                return {'server':init.serverInfo.model_dump(),'protocol_version':init.protocolVersion,'mcp_is_error':bool(response.isError),'content':blocks}

def perform(profile,action='status',name=None,arguments=None,query='',offset=0,root=PROFILES):
    directory=profile_dir(profile,root)
    if action=='status':return credential_status(profile,root)
    if action not in ('list','schema','call'):raise ValueError('Use status, list, schema or call')
    if not (directory/'index.js').is_file():return {'profile':profile,'state':'NOT_INSTALLED','operation_executed':False}
    if action=='call':
        validate_call(name,arguments or {},profile)
        status=credential_status(profile,root)
        if not status.get('configured') and not name.startswith('time.'):
            return {**status,'returncode':1,'operation_executed':False,'mcp_tool_dispatched':False}
    directory.mkdir(mode=0o700,parents=True,exist_ok=True)
    with (directory/'operation.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return {'profile':profile,'state':'BUSY','operation_executed':False,'retry_requires_observation':True}
        try:value=asyncio.run(asyncio.wait_for(upstream(profile,action,name,arguments,root),timeout=90))
        except (TimeoutError,OSError):
            return {'profile':profile,'state':'UNKNOWN','returncode':75,'operation_executed':'UNKNOWN','retry_requires_observation':True,'reason':'Transport interrupted or timed out; inspect remote state before any repeated write'}
    if action in ('list','schema'):
        if any(t['name'] in ADDITIONS for t in value['tools']):raise ValueError('Upstream/addon name collision; review pinned version')
        value['tools']+=list(ADDITIONS.values())
    if action=='schema':
        tool=next((t for t in value['tools'] if t['name']==name),None)
        if not tool:raise ValueError('Tool absent in active upstream catalog')
        return {'profile':profile,'tool':tool,'transport':'stdio','remote_access_verified':False}
    if action=='list':
        tools=[t for t in value['tools'] if not query or query.lower() in (t['name']+' '+t.get('description','')).lower()]
        start=max(0,int(offset));page=tools[start:start+6]
        return {'profile':profile,'server':value['server'],'transport':'stdio','count':len(tools),'tools':[{'name':t['name'],'description':t.get('description','')[:140]} for t in page],'next_offset':start+len(page) if start+len(page)<len(tools) else None,'remote_access_verified':False}
    failed=bool(value.get('mcp_is_error') or any(isinstance(x,dict) and x.get('error') for x in value.get('content',[])))
    return {'profile':profile,'tool':name,'transport':'stdio',**value,'returncode':1 if failed else 0,'mcp_tool_dispatched':True,'operation_executed':'UNKNOWN' if failed and is_mutating({'action':'call','name':name}) else not failed,'remote_access_verified':not failed and not name.startswith('time.'),'application_result_independently_verified':False,'verification_scope':'This Google call only; independently read back writes. Credential status is a local cache check, and time.* is local computation, never Google API proof.'}

def is_mutating(arguments):
    return arguments.get('action')=='call' and arguments.get('name') not in {'docs.getText','docs.getSuggestions','drive.search','drive.findFolder','drive.getComments','calendar.list','calendar.listEvents','calendar.getEvent','calendar.findFreeTime','gmail.search','gmail.get','gmail.listLabels','sheets.getText','sheets.getRange','sheets.getMetadata','time.getCurrentDate','time.getCurrentTime','time.getTimeZone'}

def register(registry):
    registry.specs['google_mcp']=('Google Workspace upstream MCP with publisher OAuth client: personal/education profiles. status reports real cached credentials; list(query,offset) discovers tools, schema(name) gives exact arguments, call(name,arguments) invokes the upstream server. Browser login via google-mcp-connect, never tokens in prompts. No owner Cloud project. AUTH_REQUIRED means no Google operation executed. Sheets upstream is read-only; sheets.create/writeRange are explicitly Codex additive bridges reusing upstream OAuth/Drive scope. No email sending exposed. Verify tool errors/content and independently read back writes.',
      {'profile':{'type':'string','enum':['personal','education']},'action':{'type':'string','enum':['status','list','schema','call']},'name':{'type':'string'},'arguments':{'type':'object'},'query':{'type':'string'},'offset':{'type':'integer','minimum':0}},['profile','action'],'host_authorized',lambda a:perform(**a))
