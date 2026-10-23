#!/usr/bin/env python3
"""Actual bounded paired screening, not a claim of general agent autonomy."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import threading
import time
import urllib.request

CASES=[
 ('reasoning','Réponds uniquement en JSON : une archive contient28entrées, dont14WAV et14AppleDouble. Les14WAV totalisent88.71175secondes. Combien de fichiers audio exploitables y a-t-il, et quelle est la durée moyenne en secondes ? Champs audio_count entier et mean_seconds nombre.'),
 ('facts','Réponds uniquement en JSON. Preuves : Codex développe une sonde, JARVIS l’exécute ; résultat FAIL au premier essai puis PASS après correction. Aucun second lancement identique effectué. Champs developer,executor,first_result,final_result,idempotence_proven(booléen). Ne transforme pas une absence de preuve en réussite.'),
 ('units','Réponds uniquement en JSON. Une carte expose24576MiB de VRAM. Donne les champs vram_gib et vram_gb_decimal sous forme de nombres exacts. Deux cartes ainsi équipées constituent-elles automatiquement un seul espace mémoire contigu48GiB ? Champ contiguous_pool(booléen).'),
 ('diagnosis','Réponds uniquement en JSON. Un programme lit une valeur de port égale à0 (entier), puis plante avec ValueError: port must be >=1. Ce n’est pas une chaîne. Champs original_type,original_value,cause,repair. cause vaut hors_plage ou type_invalide ; repair vaut remplacer_par_8091 ou convertir_chaine.'),
 ('coverage','Réponds uniquement en JSON avec steps tableau d’objets {id,depends,deliverables}. Objectif : produire un JSON à partir d’un CSV en conservant le CSV, publier un manifeste SHA256 du JSON puis un rapport expliquant les vérifications. Liste les livrables par noms symboliques csv_preserved,json,manifest,report,verification. Les identifiants et dépendances doivent être cohérents, la vérification après production des artefacts concernés.'),
 ('code','Réponds uniquement en JSON {code:CHAINE}. Écris une fonction normalize(value) Python sans import. Si value est un booléen, une chaîne ou un flottant, lever ValueError. Si value est un entier entre1et65535 inclus, le retourner. Pour un entier hors de cette plage, retourner8091. Pas d’entrée/sortie de fichier ni réseau.')]


def evaluate(name,text):
    cleaned=text.strip()
    if cleaned.startswith('```'):cleaned='\n'.join(cleaned.splitlines()[1:-1])
    try:v=json.loads(cleaned)
    except ValueError:return {'pass':False,'reason':'Output is not complete JSON'}
    try:
        if name=='reasoning':passed=type(v['audio_count']) is int and v['audio_count']==14 and abs(v['mean_seconds']-88.71175/14)<1e-5
        elif name=='facts':passed=v['developer']=='Codex' and v['executor']=='JARVIS' and v['first_result']=='FAIL' and v['final_result']=='PASS' and v['idempotence_proven'] is False
        elif name=='units':passed=v['vram_gib']==24 and abs(v['vram_gb_decimal']-25.769803776)<1e-9 and v['contiguous_pool'] is False
        elif name=='diagnosis':passed=v['original_type'] in ('int','integer','entier') and type(v['original_value']) is int and v['original_value']==0 and v['cause']=='hors_plage' and v['repair']=='remplacer_par_8091'
        elif name=='coverage':
            steps=v['steps'];positions={s['id']:i for i,s in enumerate(steps)};delivered=set();passed=bool(steps) and len(positions)==len(steps)
            for index,step in enumerate(steps):
                passed=passed and all(dep in positions and positions[dep]<index for dep in step['depends']);delivered.update(step['deliverables'])
            passed=passed and {'csv_preserved','json','manifest','report','verification'}<=delivered
            produced={d:min(i for i,s in enumerate(steps) if d in s['deliverables']) for d in delivered}
            passed=passed and produced['json']<=produced['manifest']<=produced['verification']<=produced['report']
        else:
            # Restricted AST for this pure function screening. The real mission
            # demonstration later uses the actual broker and skills separately.
            tree=ast.parse(v['code']);bad=(ast.Import,ast.ImportFrom,ast.Attribute,ast.While,ast.For,ast.With,ast.Try,ast.ClassDef,ast.Lambda,ast.Global,ast.Nonlocal)
            if any(isinstance(n,bad) for n in ast.walk(tree)):raise ValueError('Unsafe or unnecessary syntax outside pure screening scope')
            allowed={'isinstance','type','int','bool','ValueError'}
            if any(isinstance(n,ast.Call) and (not isinstance(n.func,ast.Name) or n.func.id not in allowed) for n in ast.walk(tree)):raise ValueError('Unexpected call in generated pure function')
            scope={'__builtins__':{'isinstance':isinstance,'type':type,'int':int,'bool':bool,'str':str,'float':float,'ValueError':ValueError}}
            exec(compile(tree,'<candidate pure function>','exec'),scope);f=scope['normalize'];passed=True
            for item,expected in [(0,8091),(-1,8091),(1,1),(65535,65535),(65536,8091),(8091,8091)]:passed=passed and f(item)==expected
            for item in (True,False,'8091',1.0):
                try:f(item);passed=False
                except ValueError:pass
        return {'pass':bool(passed),'parsed':v}
    except Exception as exc:return {'pass':False,'reason':type(exc).__name__+': '+str(exc),'parsed':v}


def sample():
    mem={x.split(':')[0]:int(x.split()[1])*1024 for x in Path('/proc/meminfo').read_text().splitlines()}
    r=subprocess.run(['nvidia-smi','--query-gpu=index,memory.used,utilization.gpu,temperature.gpu,power.draw','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=5)
    return {'at':time.time(),'memory_available_bytes':mem['MemAvailable'],'gpu_csv':r.stdout,'probe_returncode':r.returncode}

def inference(url,model,prompt):
    values=[];stop=threading.Event()
    def monitor():
        while not stop.is_set():
            try:values.append(sample())
            except Exception as exc:values.append({'error':str(exc)})
            stop.wait(.5)
    thread=threading.Thread(target=monitor,daemon=True);thread.start();started=time.monotonic();first=None;text='';done=None;error=None
    try:
        body={'model':model,'messages':[{'role':'user','content':prompt}],'stream':True,'think':False,'keep_alive':'15m','options':{'num_ctx':4096,'num_predict':768,'seed':7,'temperature':0}}
        if not model.startswith('qwen') or model.startswith('qwen3-coder-next'):body.pop('think',None)
        request=urllib.request.Request(url+'/api/chat',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(request,timeout=180) as r:
            for line in r:
                item=json.loads(line)
                if item.get('error'):raise RuntimeError(item['error'])
                part=item.get('message',{}).get('content','')
                if part and first is None:first=time.monotonic()-started
                text+=part
                if item.get('done'):done=item
        if done is None:raise RuntimeError('Missing final metrics receipt')
    except Exception as exc:error={'type':type(exc).__name__,'message':str(exc)}
    finally:elapsed=time.monotonic()-started;stop.set();thread.join(7)
    done=done or {};done.pop('message',None)
    try:
        with urllib.request.urlopen(url+'/api/ps',timeout=5) as r:resident=json.load(r)
    except Exception as exc:resident={'unavailable':type(exc).__name__}
    return {'model':model,'text':text,'error':error,'elapsed_s':elapsed,'first_content_s':first,'server_metrics':done,'tokens_per_second':done['eval_count']*1e9/done['eval_duration'] if done.get('eval_duration') else None,'resources':values,'resident':resident}

def recheck(source,output):
    """Retest actual saved responses, retaining prior verdicts and source bytes."""
    if source.resolve()==output.resolve():raise ValueError('Recheck must preserve original artifact')
    raw=source.read_bytes();result=json.loads(raw)
    for row in result['cases']:
        row.setdefault('previous_evaluations',[]).append(row['evaluation'])
        row['evaluation']=evaluate(row['case'],row['text']) if not row['error'] else {'pass':False,'reason':'Actual inference error'}
    result['recheck']={'judge_version':'28a.screening.2','source_sha256':hashlib.sha256(raw).hexdigest(),'created':time.time(),'new_inference':False}
    result['summary']={model:{'passed':sum(r['evaluation']['pass'] for r in result['cases'] if r['model']==model),'total':sum(r['model']==model for r in result['cases'])} for model in {r['model'] for r in result['cases']}}
    with output.open('x') as target:target.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result['summary']


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--url');p.add_argument('--recheck',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--models',nargs='+',default=['qwen3.5:27b-q4_K_M','qwen3:32b-q4_K_M','llama3.3:70b-instruct-q4_K_M']);args=p.parse_args()
    if args.recheck:
        print(json.dumps(recheck(args.recheck,args.output)));raise SystemExit(0)
    if not args.url:p.error('--url required for real inference')
    result=json.loads(args.output.read_text()) if args.output.exists() else {'created':time.time(),'judge_version':'28a.screening.2','scope':'Six paired technical screening tasks, not general autonomy/quality certification','cases':[]}
    for model in args.models:
        for name,prompt in CASES:
            digest=hashlib.sha256(prompt.encode()).hexdigest()
            if any(v['model']==model and v['case']==name and v['prompt_sha256']==digest for v in result['cases']):continue
            row=inference(args.url.rstrip('/'),model,prompt);row.update(case=name,prompt_sha256=digest,evaluation=evaluate(name,row['text']) if not row['error'] else {'pass':False,'reason':'Actual inference error'})
            result['cases'].append(row);args.output.parent.mkdir(parents=True,exist_ok=True);tmp=args.output.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');tmp.replace(args.output)
            print(json.dumps({'case':name,'model':model,'pass':row['evaluation']['pass'],'elapsed_s':row['elapsed_s'],'error':row['error']}),flush=True)
    result['summary']={model:{'passed':sum(v['evaluation']['pass'] for v in result['cases'] if v['model']==model),'total':sum(v['model']==model for v in result['cases'])} for model in args.models}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result['summary']))
