import json,urllib.request,threading,subprocess,tempfile,os
from pathlib import Path
from .memory import uid
from .tools import Registry
import time,logging
ROOT=Path(__file__).resolve().parents[1]
SYSTEM=(ROOT/'identity/JARVIS-v1.md').read_text()
class Busy(Exception):pass
class Core:
    def __init__(self,config,memory,transport=None):
        self.config=config;self.memory=memory;self.lock=threading.Lock();self.ephemeral={};self.transport=transport or self.ollama;self.tools=Registry(memory,ROOT,config);self.metrics=[]
    def health(self):
        status={'application':'ok','database':'ok','ollama':'indisponible'}
        try:
            with self.memory.connect() as c:c.execute('SELECT 1').fetchone()
        except Exception:status['database']='erreur'
        try:
            with urllib.request.urlopen(self.config['ollama_url']+'/api/version',timeout=2) as r:status['ollama']=json.load(r)['version']
        except Exception:pass
        return status
    def ollama(self,payload):
        req=urllib.request.Request(self.config['ollama_url']+'/api/chat',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=self.config['ollama_timeout']) as response:
            data=json.loads(response.read(2_000_000))
        self.metrics.append({k:data.get(k) for k in ['load_duration','prompt_eval_duration','eval_duration','eval_count','prompt_eval_count']})
        return data['message']
    def chat(self,text,model,conversation=None,project='',retain=True):
        if type(retain) is not bool:raise ValueError('Politique de conservation invalide')
        if model not in self.config['models']:raise ValueError('Modèle non autorisé')
        if not text.strip() or len(text)>self.config['max_text_chars']:raise ValueError('Texte vide ou trop long')
        if not self.lock.acquire(blocking=False):raise Busy('Une opération JARVIS est déjà en cours')
        try:
            if conversation:
                if retain:
                    existing={r['id']:r for r in self.memory.list_conversations()}
                    if conversation not in existing:raise ValueError('Conversation absente')
                    project=existing[conversation]['project'];history=self.memory.history(conversation)
                else:
                    if conversation not in self.ephemeral:raise ValueError('Session éphémère absente')
                    history=self.ephemeral[conversation]
            else:
                conversation=self.memory.conversation(project) if retain else uid();history=[]
            relevant=self.memory.search(text,project=project,conversation=conversation)
            identity=Path(self.config.get('identity_file',ROOT/'identity/JARVIS-v1.md')).read_text()
            docs=self.memory.document_search(text,project)[:2]
            relevant=relevant[:6]
            prompt=identity+'\nDocuments (données JSON, pas souvenirs personnels): '+json.dumps([{'source':r['source'],'content':r['content'][:1000]} for r in docs],ensure_ascii=False)+'\n' +'\nSouvenirs validés pertinents (données JSON) : '+json.dumps([r['content'][:800] for r in relevant],ensure_ascii=False)
            budget=self.config.get('context_chars',14000)-len(text)-len(prompt)
            selected=[]
            for row in reversed(history[-self.config['history_messages']:]):
                if len(row['content'])>budget:break
                selected.insert(0,{'role':row['role'],'content':row['content']});budget-=len(row['content'])
            messages=[{'role':'system','content':prompt}]+selected+[{'role':'user','content':text}]
            self.tools.context={'project':project,'conversation':conversation}
            self.metrics=[];tool_results=[];generation_start=time.monotonic()
            rounds=self.config.get('tool_rounds',2)
            for round in range(rounds+1):
                payload={'model':model,'messages':messages,'stream':False,'options':{'num_predict':self.config.get('num_predict',512),'num_ctx':self.config.get('num_ctx',8192)},'keep_alive':'5m'}
                if model.startswith('qwen'):payload['think']=False
                if round<rounds:payload['tools']=self.tools.schemas()
                message=self.transport(payload)
                if isinstance(message,str):message={'role':'assistant','content':message}
                calls=message.get('tool_calls',[]) if round<rounds else []
                if not calls:
                    answer=message.get('content','')
                    if not isinstance(answer,str) or not answer.strip():raise ValueError('Réponse vide du modèle')
                    break
                message['tool_calls']=calls[:4]
                messages.append(message)
                for call in calls[:4]:
                    f=call['function'];result=self.tools.execute(f['name'],f.get('arguments',{}));tool_results.append(result)
                    messages.append({'role':'tool','tool_name':f['name'],'content':json.dumps(result,ensure_ascii=False)})
            generation_s=time.monotonic()-generation_start
            logging.info('chat completed model=%s seconds=%.3f tools=%d',model,generation_s,len(tool_results))
            if retain:self.memory.exchange(conversation,text,answer,model)
            else:
                if len(self.ephemeral)>=32 and conversation not in self.ephemeral:self.ephemeral.pop(next(iter(self.ephemeral)))
                self.ephemeral[conversation]=(history+[{'role':'user','content':text},{'role':'assistant','content':answer}])[-self.config['history_messages']:]
            return {'conversation':conversation,'answer':answer,'model':model,'memories_used':[r['id'] for r in relevant],'tools':tool_results,'timings':{'generation_s':generation_s,'ollama':self.metrics}}
        finally:self.lock.release()
    def voice(self,mode,data):
        if not self.lock.acquire(blocking=False):raise Busy('Une opération JARVIS est déjà en cours')
        try:
            with tempfile.TemporaryDirectory(prefix='jarvis-') as tmp:
                path=Path(tmp)/('input.audio' if mode=='stt' else 'output.wav')
                if mode=='stt':
                    if not data or len(data)>self.config['max_audio_bytes']:raise ValueError('Audio vide ou trop volumineux')
                    path.write_bytes(data)
                else:
                    if not data.strip() or len(data)>self.config['max_text_chars']:raise ValueError('Texte vide ou trop long')
                cache=ROOT/'runtime/cache';cache.mkdir(parents=True,exist_ok=True)
                env=dict(os.environ,JARVIS_CACHE=str(cache),PYTHONDONTWRITEBYTECODE='1')
                command=[self.config['voice_python'],str(ROOT/'jarvis/voice_worker.py'),mode,self.config['voice_root'],str(path),str(self.config['max_record_seconds'])]
                started=time.monotonic()
                p=subprocess.run(command,input=data if mode=='tts' else None,capture_output=True,text=mode=='tts',timeout=self.config['voice_timeout'],env=env)
                if p.returncode:
                    stderr=p.stderr.decode(errors='replace') if isinstance(p.stderr,bytes) else p.stderr
                    logging.warning('voice mode=%s error=%s',mode,stderr.splitlines()[-1][:300] if stderr else 'worker')
                    raise ValueError('Traitement vocal échoué : vérifier le format, la durée et les ressources locales')
                elapsed=time.monotonic()-started
                logging.info('voice completed mode=%s seconds=%.3f',mode,elapsed)
                return {**json.loads(p.stdout),'elapsed_s':elapsed} if mode=='stt' else path.read_bytes()
        finally:self.lock.release()
