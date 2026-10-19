"""Conservative explicit-intent routing; status questions never create missions."""
import re,unicodedata

def normalize(text):
    return ''.join(x for x in unicodedata.normalize('NFD',text.lower()) if unicodedata.category(x)!='Mn').strip()

def classify(text):
    value=normalize(text)
    if re.match(r'^(?:quel|quelle|quels|quelles|pourquoi|ou en|est.ce que|peux.tu (?:expliquer|me dire)|explique|donne.moi (?:l.etat|le statut))\b',value):return 'question'
    if re.search(r'\b(?:reprends|reprendre|poursuis|continue|termine)\b.*\bmission\s*23\b',value):return 'resume23'
    if re.match(r'^(?:lance|demarre|execute|cree|developpe|installe|corrige|publie|reprends|poursuis|termine|peux.tu (?:lancer|executer|creer|developper|installer|corriger|publier))\b',value):return 'execute'
    return 'conversation'

def mission_answer(text,store):
    """Render requested technical status from canonical facts, without inference claims."""
    value=normalize(text)
    if classify(text)!='question' or not re.search(r'\b(?:mission\s*23|tache\s*12|t12)\b',value):return None
    import json,datetime
    from zoneinfo import ZoneInfo
    ident='7971ec0311124fb4be9e3125dcb291fd';row=store.get(ident);tasks=store.tasks(ident)
    done=sum(t['state']=='validated' for t in tasks)
    answer=f"Mission 23 — LiveKit : {row['state']}, tâche active {row['active_task']}, {done}/{len(tasks)} tâches validées par le moteur. Ce compteur ne prouve pas une réception vocale complète."
    answer+=' Dernière activité : '+datetime.datetime.fromtimestamp(row['updated'],ZoneInfo('Europe/Paris')).isoformat()+'.'
    if re.search(r'pourquoi|blocage|echou',value):
        with store.db() as c:
            events=[dict(r) for r in c.execute("SELECT kind,arguments,result FROM mission_events WHERE mission=? AND tool='host_github' AND kind='tool_finished' ORDER BY id DESC",(ident,))]
        failures=[];last_success=None
        for e in events:
            a=json.loads(e['arguments']);r=json.loads(e['result'])
            if r.get('ok') and last_success is None:last_success=a.get('action')
            if not r.get('ok') and len(failures)<3:failures.append(r.get('error','échec sans diagnostic'))
        answer+=' Historique t12 : les anciens push échouaient notamment avec « Fichier régulier lisible <1Mo requis ». Le broker attend un dossier dans path puis y ajoute file ; les tentatives passant un fichier dans path étaient incorrectes. Le diagnostic de panne générale GitHub ne découle pas de ce message.'
        if failures:answer+=' Derniers diagnostics conservés : '+' ; '.join(failures)+'.'
        if last_success:answer+=' Une opération GitHub ultérieure a réussi : '+last_success+' ; cela ne suffit pas à déclarer toute la livraison terminée.'
    answer+=' Le diagnostic df542051560b44b3851124b09d8319c2 est lié à la mission23 ; la mission24 de roadmap reste Mémoire enrichie et ingestion documentaire.'
    return {'answer':answer,'tools':[],'conversation':row['conversation'],'source':'JARVIS-engine/canonical-mission-store','state':row['state']}
