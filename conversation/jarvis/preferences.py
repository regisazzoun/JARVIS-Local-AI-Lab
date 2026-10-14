"""Closed, non-sensitive preference scope; never retain arbitrary text automatically."""
import re, unicodedata

def detect(text):
    t=' '.join(unicodedata.normalize('NFKD',text.casefold()).encode('ascii','ignore').decode().split())
    # Do not interpret quoted examples, questions, negatives, or incidental diagnostic text.
    if len(t)>350 or any(x in t for x in ['?', 'ne ', 'pas ', 'exemple', '```', '"', 'secret','mot de passe','token','permission','sudo','administrateur','adresse','sante']):return []
    if not re.match(r"^(?:jarvis[, :]*|s'il te plait[, :]*|merci de )?(?:je prefere|ma preference|retiens|memorise|souviens-toi|desormais|a partir de maintenant|oublie|supprime|parle|reponds|utilise|tutoie|vouvoie|cite|verifie)",t):return []
    result=[]
    if re.search(r'vocal|oral|voix|a voix haute',t):
        if re.search(r'oublie|supprime',t):result.append(('voice_length',None))
        elif re.search(r'courte?s?|breve?s?|concis|syntheti',t):result.append(('voice_length','short'))
        elif re.search(r'detaillee?s?|longue?s?',t):result.append(('voice_length','detailed'))
        elif re.search(r'normal|moyenn',t):result.append(('voice_length','normal'))
    if re.search(r'langue|parle|reponds|conversation',t):
        if 'francais' in t:result.append(('language','fr'))
        elif 'anglais' in t:result.append(('language','en'))
    if 'presentation' in t or 'reponses' in t:
        if 'paragraph' in t:result.append(('presentation','paragraphs'))
        elif re.search(r'listes?|puces',t):result.append(('presentation','lists'))
    if 'tutoie' in t or 'tutoiement' in t:result.append(('address_style','tu'))
    elif 'vouvoie' in t or 'vouvoiement' in t:result.append(('address_style','vous'))
    if re.search(r'toujours|desormais|retiens|memorise|je prefere',t):
        if re.search(r'\b(?:cite|citer|citations?)\b',t) and 'source' in t:result.append(('sources','cite'))
        if re.search(r'verifie|verification',t) and re.search(r'resultats?|conclure|conclusion',t):result.append(('verification','always'))
        if re.search(r'metrique|unites si',t):result.append(('units','metric'))
    return result

def clean_speech(text,limit=420,language='fr'):
    detail='The details are shown on screen.' if language=='en' else 'Les détails sont affichés à l’écran.'
    text=re.sub(r'```.*?```',' '+detail+' ',text,flags=re.S)
    text=re.sub(r'`[^`]*`','',text)
    text=re.sub(r'https?://\S+|(?:/[\w.~-]+){2,}|\|[^\n]*','',text)
    text=re.sub(r'(?m)^\s*(?:[-*#]+|\d+[.)])\s*','',text)
    text=re.sub(r'\[([^]]+)\]\([^)]*\)',r'\1',text)
    text=re.sub(r'[*_#]','',text)
    text=' '.join(text.split()).strip() or detail
    if len(text)<=limit:return text
    cut=text[:limit]; boundary=max(cut.rfind('. '),cut.rfind('! '),cut.rfind('? '))
    return (cut[:boundary+1] if boundary>60 else cut.rsplit(' ',1)[0]+'.')+' '+detail
