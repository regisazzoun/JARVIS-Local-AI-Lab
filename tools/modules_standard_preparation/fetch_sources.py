import json, subprocess, pathlib, datetime
root=pathlib.Path.home()/'JARVIS/modules-standard-20261101'
root.mkdir(parents=True,exist_ok=True)
(root/'sources').mkdir(exist_ok=True)
(root/'logs').mkdir(exist_ok=True)
repos={
'hermes-skills':('NousResearch/hermes-agent',['skills/productivity/microsoft-office','skills/productivity/pdf','LICENSE']),
'learning-commons':('learning-commons-org/agent-skills',None),
'education-skills':('GarethManning/education-agent-skills',None),
'devops-skills':('Jeffallan/claude-skills',['skills/devops-engineer','LICENSE']),
'mcp-reference':('modelcontextprotocol/servers',['src/filesystem','src/fetch','LICENSE','package.json','package-lock.json','tsconfig.json']),
'ansible-devtools':('ansible/vscode-ansible',None),
'cisco-pyats':('CiscoDevNet/cisco-pyats-mcp-network-automation',None),
'pfsense':('gensecaihq/pfsense-mcp-server',None),
'nagios':('equilibrise/nagios-mcp',None),
'netbox-enhanced':('skuldgerry/netbox-mcp',None),
'drawio':('jgraph/drawio-mcp',None),
'markitdown':('microsoft/markitdown',None),
'pandoc-mcp':('dullroar/pandoc_mcp',None),
'playwright':('microsoft/playwright-mcp',None),
'github-mcp':('github/github-mcp-server',None),
'netbox-official':('netboxlabs/netbox-mcp-server',None),
}
results=[]
for name,(repo,sparse) in repos.items():
 p=root/'sources'/name
 with (root/'logs'/('source-'+name+'.log')).open('w') as log:
  try:
   if not (p/'.git').exists():
    cmd=['git','clone','--depth','1']
    if sparse:cmd+=['--filter=blob:none','--sparse']
    subprocess.run(cmd+['https://github.com/'+repo+'.git',str(p)],stdout=log,stderr=log,check=True,timeout=300)
    if sparse:subprocess.run(['git','-C',str(p),'sparse-checkout','set','--no-cone']+sparse,stdout=log,stderr=log,check=True,timeout=120)
   sha=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
   results.append({'name':name,'repository':repo,'commit':sha,'source':'downloaded','path':str(p)})
   print(name,'downloaded',sha,flush=True)
  except Exception as e:
   results.append({'name':name,'repository':repo,'source':'failed','error':str(e)})
   print(name,'FAILED',str(e),flush=True)
 (root/'sources-lock.json').write_text(json.dumps(results,indent=2))
