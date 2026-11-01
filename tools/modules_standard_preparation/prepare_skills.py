import pathlib,shutil,json,hashlib,urllib.request,tarfile
R=pathlib.Path.home()/'JARVIS/modules-standard-20261101'
S=R/'sources'; D=R/'skills';D.mkdir(exist_ok=True)
selected=[S/'hermes-skills/skills/productivity/microsoft-office',S/'hermes-skills/skills/productivity/pdf',S/'devops-skills/skills/devops-engineer',S/'netbox-enhanced/skills/netbox-mcp-operator',S/'drawio/plugins/codex/drawio/skills/drawio']
selected+=list((S/'learning-commons/skills').glob('*/'))
names=['criterion-referenced-rubric-generator','assessment-validity-checker','competency-unpacker','learning-progression-builder','project-brief-designer','differentiation-adapter','progressive-hint-ladder','error-analysis-protocol','competency-framework-translator']
selected+=[p.parent for p in (S/'education-skills/skills').rglob('SKILL.md') if p.parent.name in names]
manifest=[]
for p in selected:
 if not (p/'SKILL.md').exists():continue
 q=D/p.name
 if not q.exists():shutil.copytree(p,q)
 repo=p
 while repo.parent!=S:repo=repo.parent
 licenses=[]
 for lic in repo.glob('*LICENSE*'):
  if lic.is_file():shutil.copy2(lic,q/('UPSTREAM-'+lic.name));licenses.append(lic.name)
 origin={'source':str(p.relative_to(R)),'repository_folder':repo.name,'licenses':licenses,'activation':'staged-only-not-loaded','files':{str(f.relative_to(q)):hashlib.sha256(f.read_bytes()).hexdigest() for f in q.rglob('*') if f.is_file()}}
 manifest.append({'name':p.name,**origin})
(R/'skills-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Skills staged:',len(manifest))
# Official release only; verify published SHA256 before extracting binary.
d=json.loads((R/'github-release.json').read_text()); assets={x['name']:x for x in d['assets']}
name='github-mcp-server_Linux_x86_64.tar.gz'
checks=next(x for n,x in assets.items() if 'checksums.txt' in n)
data=urllib.request.urlopen(assets[name]['browser_download_url']).read()
sha=hashlib.sha256(data).hexdigest()
text=urllib.request.urlopen(checks['browser_download_url']).read().decode()
expected=next(line.split()[0] for line in text.splitlines() if line.split()[-1].lstrip('*')==name)
if sha!=expected:raise RuntimeError('GitHub binary checksum mismatch')
(R/'downloads').mkdir(exist_ok=True); archive=R/'downloads'/name;archive.write_bytes(data)
(R/'bin').mkdir(exist_ok=True)
with tarfile.open(archive) as tar:
 for member in tar.getmembers():
  if pathlib.PurePosixPath(member.name).name=='github-mcp-server' and member.isfile():
   target=R/'bin/github-mcp-server';target.write_bytes(tar.extractfile(member).read());target.chmod(0o755)
(R/'github-binary-lock.json').write_text(json.dumps({'version':d['tag_name'],'url':assets[name]['browser_download_url'],'sha256':sha,'checksum_match':True,'status':'installed-not-tested'},indent=2))
print('GitHub MCP binary installed; not executed.')
# A shared, explicit environment reference. No Hermes engine is installed.
(R/'documents.env').write_text('export PY='+str(R/'venvs/documents/bin/python')+'\nexport PYPANDOC_PANDOC='+str(R/'venvs/documents/lib/python3.12/site-packages/pypandoc/files/pandoc')+'\nexport PATH='+str(R/'venvs/documents/bin')+':\"$PATH\"\n')
(R/'connection-templates').mkdir(exist_ok=True)
(R/'connection-templates/inventory.yml').write_text('all:\n  children:\n    linux:\n      hosts: {}\n    windows:\n      hosts: {}\n    cisco:\n      hosts: {}\n# Renseigner uniquement les cibles fournies par Régis au lycée.\n')
(R/'connection-templates/targets.env.example').write_text('NETBOX_URL=\nNETBOX_TOKEN=\nNAGIOS_URL=\nPFSENSE_URL=\nPFSENSE_API_KEY=\n# Paramètres exacts à reprendre des documentations amont ; aucun secret ici.\n')
print('Empty connection templates created; no targets configured.')
