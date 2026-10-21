"""Codex integration tool, to be run by JARVIS with attribution; keeps old drafts."""
import hashlib,json,re,time
from pathlib import Path
root=Path(__file__).parent
page=root/'index.html';before=page.read_text();history=root/'historique';history.mkdir(exist_ok=True)
sha=hashlib.sha256(before.encode()).hexdigest()
(history/('index-jarvis-'+sha[:12]+'.html')).write_text(before)
after,n=re.subn(r'<script>.*?</script>','<script src="/vendor/client-tools.js"></script>',before,flags=re.S)
if not n and '/vendor/client-tools.js' not in after:raise RuntimeError('Expected inline script missing')
page.write_text(after)
runner=root/'test_interruption_23d.py'
if runner.exists():
 old=runner.read_text();(history/'runner-jarvis-initial.py.txt').write_text(old)
runner.write_text('''#!/usr/bin/env python3
"""JARVIS entry point using the Codex RTC measurement tool; old draft archived."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).parent/'codex_capture.py'),run_name='__main__')
''')
receipt={'actor':'Codex integration tool executed by JARVIS','utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'before_html_sha256':sha,'after_html_sha256':hashlib.sha256(after.encode()).hexdigest(),'original_preserved':True,'source_of_client_logic':'Codex vendor/client-tools.js','page_markup':'JARVIS'}
(root/'reports/integration.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
