from pathlib import Path
import json,urllib.request
h=Path.home();r=h/'JARVIS/modules-standard-20261101';p=h/'JARVIS/modules-standard-20261101-private/reception-stop-before';p.mkdir(parents=True,exist_ok=True);p.chmod(0o700)
t=(h/'JARVIS/qwen-code-openwebui-private/webui-token').read_text().strip()
def api(path,d=None):
 q=urllib.request.Request('http://127.0.0.1:8088'+path,data=json.dumps(d).encode() if d is not None else None,headers={'Authorization':'Bearer '+t,'Content-Type':'application/json'})
 return json.load(urllib.request.urlopen(q,timeout=30))
addition='''\n\nRéception locale — commande explicitement bornée : lorsque Régis demande UNE commande exacte et aucune autre action, appeler uniquement run_command pour cette commande, sans consultation préalable list_processes, list_files, Skill, aide ou lecture. Le risque de relancer un processus ne justifie pas une recherche préalable : un processus à attendre est seulement celui dont cet appel run_command vient de renvoyer l’identifiant avec status=running. Dans ce seul cas, utiliser get_process_status sur cet identifiant jusqu’à done. Dès le résultat final, répondre avec le code retour et la sortie réelle, sans autre appel, que le code soit0 ou non. Une erreur n’autorise pas de réparation spontanée. Pour une tâche documentaire, arrêter les vérifications dès que les critères demandés sont établis ; les exemples des Skills ne sont pas une liste de commandes à exécuter entièrement.'''
for id in ['jarvis-qwen-code-lab','jarvis-tools-conversation']:
 d=api('/api/v1/models/model?id='+id);b=p/(id+'.json')
 if not b.exists():b.write_text(json.dumps(d,ensure_ascii=False,indent=2))
 if 'Réception locale — commande explicitement bornée' not in d['params'].get('system',''):
  d['params']['system']=d['params'].get('system','')+addition;api('/api/v1/models/model/update',d)
(r/'reception-stop-clarification.json').write_text(json.dumps({'profiles':['jarvis-qwen-code-lab','jarvis-tools-conversation'],'system_append':addition,'no_other_fields_changed':True,'new_engine':False},ensure_ascii=False,indent=2))
print('Bounded-command instructions updated; other profile fields preserved.')
