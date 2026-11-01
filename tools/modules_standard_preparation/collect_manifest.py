import pathlib,json,importlib.metadata,hashlib,datetime
R=pathlib.Path.home()/'JARVIS/modules-standard-20261101'
out={'date':'2026-11-01','host':'Mac mini JARVIS / Debian','root':str(R),'status':'installed-not-tested','functional_tests_run':False,'new_agent_engine':False,'services_started_or_restarted':False,'existing_missions_modified':False}
for key,file in [('sources','sources-lock.json'),('installation','installation-status.json'),('skills','skills-manifest.json'),('github_binary','github-binary-lock.json')]:out[key]=json.loads((R/file).read_text())
out['python_environments']={}
for v in (R/'venvs').iterdir():
 sites=list(v.glob('lib/python*/site-packages'))
 if not sites:continue
 out['python_environments'][v.name]=sorted([{'name':d.metadata['Name'],'version':d.version} for d in importlib.metadata.distributions(path=[str(sites[0])])],key=lambda d:d['name'].lower())
out['npm']={}
for n in (R/'npm').iterdir():
 p=n/'package.json'
 if p.exists():out['npm'][n.name]=json.loads(p.read_text()).get('dependencies',{})
out['collections']=[]
for p in (R/'collections/ansible_collections').glob('*/*/MANIFEST.json'):
 d=json.loads(p.read_text())['collection_info'];out['collections'].append({k:d.get(k) for k in ['namespace','name','version','license','repository']})
out['ocr']={'installation':'extracted-debian-packages-not-tested','packages':[{'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (R/'debs').glob('*.deb')],'root':str(R/'sysroot')}
out['playwright_browser']={'downloaded':(R/'browsers').exists(),'directories':[p.name for p in (R/'browsers').iterdir() if p.is_dir()],'tested':False}
out['reused']=['Open Terminal 0.14.7','MCPO 0.0.20','Qwen Code 0.26.4','Open WebUI','LibreOffice','SSH keys and pinned hosts']
out['pending']=['native WebUI/Qwen Code registration','authorized school inventory and infrastructure discovery','NetBox/Nagios/pfSense/Windows/AD/Cisco credentials and compatibility','functional tests and document visual review','optional marker-pdf/nano-pdf and external-model OCR not installed','draw.io desktop optional export dependency not installed']
(R/'manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
(R/'documents.env').write_text('export PY='+str(R/'venvs/documents/bin/python')+'\nexport PYPANDOC_PANDOC='+str(R/'venvs/documents/lib/python3.12/site-packages/pypandoc/files/pandoc')+'\nexport PATH='+str(R/'venvs/documents/bin')+':'+str(R/'sysroot/usr/bin')+':"$PATH"\nexport LD_LIBRARY_PATH='+str(R/'sysroot/usr/lib/x86_64-linux-gnu')+':"${LD_LIBRARY_PATH:-}"\nexport TESSDATA_PREFIX='+str(R/'sysroot/usr/share/tesseract-ocr/5/tessdata')+'\n')
bad=R/'connection-templates/targets.env.example'
if bad.exists():bad.unlink()
(R/'connection-templates/README.txt').write_text('À renseigner au lycée : cible autorisée, nom DNS/adresse, rôle, OS/version, transport, compte, référence du secret privé, droits, port, certificat/empreinte et commande de lecture de réception. Aucun secret dans Git. Reprendre les noms exacts de variables de chaque README amont ; ne pas inventer leur correspondance. Inventaire Ansible vide fourni. Aucun scan réseau autorisé par ce fichier.\n')
print('Manifest written. Skills:',len(out['skills']),'Package install failures:',[n for n,s in out['installation'].items() if s['status']!='installed-not-tested'])
print('Chromium directories:',out['playwright_browser']['directories'])
