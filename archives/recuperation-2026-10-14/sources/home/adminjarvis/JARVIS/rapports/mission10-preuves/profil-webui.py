import json, pathlib, urllib.request

P = pathlib.Path(__file__).parent
B = pathlib.Path('/home/adminjarvis/JARVIS')
URL = 'http://192.168.1.99:3000'
MODEL = 'qwen3.5:27b-q4_K_M'

def req(path, data=None, token=None):
    headers = {'Content-Type':'application/json'}
    if token:
        headers['Authorization'] = 'Bearer '+token
    r = urllib.request.Request(URL+path, data=None if data is None else json.dumps(data).encode(), headers=headers)
    with urllib.request.urlopen(r, timeout=180) as f:
        return json.load(f)

password = (B/'open-webui/identifiants-admin.txt').read_text().splitlines()[1].split(': ',1)[1]
token = req('/api/v1/auths/signin', dict(email='admin@jarvis.local', password=password))['token']
before = json.loads((P/'profils-avant.json').read_text())
current = req('/api/v1/models/all', token=token)
assert all(x in current for x in before), 'Un profil existant a changé depuis la sauvegarde'
assert not any(x['id'] == MODEL for x in current), 'Profil Qwen déjà présent'
profile = dict(id=MODEL, base_model_id=None, name='JARVIS — Qwen 3.5 27B Qualité',
    meta=dict(description='Qwen 3.5 27B Q4_K_M, raisonnement natif, contexte 8192. Vérification humaine des propositions techniques.'),
    params=dict(system=(B/'rapports/mission08-preuves/instruction-mistral-finale.txt').read_text(),
        num_ctx=8192, num_predict=4096, temperature=1.0, top_p=.95, top_k=20,
        min_p=0.0, presence_penalty=1.5, repeat_penalty=1.0, think=True), is_active=True)
(P/'profil-qwen-requete.json').write_text(json.dumps(profile, ensure_ascii=False, indent=2))
created = req('/api/v1/models/create', profile, token)
(P/'profil-qwen-cree.json').write_text(json.dumps(created, ensure_ascii=False, indent=2))
after = req('/api/v1/models/all', token=token)
assert all(x in after for x in before), 'Un profil existant a changé'
(P/'profils-apres.json').write_text(json.dumps(after, ensure_ascii=False, indent=2))
models = req('/api/models', token=token)
(P/'modeles-webui.json').write_text(json.dumps(models, ensure_ascii=False, indent=2))
test = req('/api/chat/completions', dict(model=MODEL,
    messages=[dict(role='user', content='Réponds en français en une phrase : combien font 17 multiplié par 23 ?')],
    params=dict(num_predict=64, think=False), stream=False), token)
(P/'validation-webui.json').write_text(json.dumps(test, ensure_ascii=False, indent=2))
print('Profil créé, profils existants identiques ; réponse WebUI :', test)
