"""Apply the two configuration corrections to a stopped PRIVATE COPY only."""
import json
import pathlib
import sqlite3
import sys
import time
import uuid

root = pathlib.Path(sys.argv[1]).resolve()
if root.name != 'mission24a-correctifs-private-20261114' or not (root/'control/preparation-proof.json').is_file():
    raise SystemExit('Private fixture identity required')
c = sqlite3.connect(root/'data/webui.db')
alias = 'jarvis-conversation-utilisateurs'
base = c.execute('select base_model_id from model where id=?', (alias,)).fetchone()[0]
grants = c.execute("select principal_type,principal_id from access_grant where resource_type='model' and resource_id=? and permission='read'", (alias,)).fetchall()
inserted = 0
for kind, principal in grants:
    if kind != 'user' or not c.execute("select 1 from user where id=? and role='user'", (principal,)).fetchone():
        raise SystemExit('Only explicit fixture standard-user grants expected')
    exists = c.execute("select 1 from access_grant where resource_type='model' and resource_id=? and principal_type=? and principal_id=? and permission='read'", (base,kind,principal)).fetchone()
    if not exists:
        c.execute('insert into access_grant values(?,?,?,?,?,?,?)', (str(uuid.uuid4()),'model',base,kind,principal,'read',int(time.time())))
        inserted += 1
prompt = pathlib.Path(__file__).with_name('synthese-dates.md').read_text()
for ident in ('jarvis-tools-conversation', alias):
    params = json.loads(c.execute('select params from model where id=?', (ident,)).fetchone()[0])
    if prompt not in params.get('system', ''):
        original = params.get('system','').split('\n\n## Provenance et rapprochement des états documentés', 1)[0]
        params['system'] = original + '\n\n' + prompt
    c.execute('update model set params=? where id=?', (json.dumps(params,ensure_ascii=False),ident))
c.commit()
out = {'explicit_standard_user_base_grants_added': inserted, 'alias_principals': len(grants),
       'base_direct_inference_becomes_allowed': True, 'admin_role_added': False,
       'tool_connection_permissions_changed': False, 'production_modified': False,
       'prompt_contains_reference_answer': False, 'source_content_filter_added': False}
(root/'control/config-correction-proof.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
