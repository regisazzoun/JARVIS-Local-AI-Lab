"""CPU-only file synthesis/transcription; no listener, playback or Ollama client."""
import os,sys,time,json,wave,resource
from pathlib import Path
root=Path(__file__).resolve().parent
os.nice(10);os.sched_setaffinity(0,set(sorted(os.sched_getaffinity(0))[:2]));resource.setrlimit(resource.RLIMIT_CPU,(180,185))
os.environ.update({'CUDA_VISIBLE_DEVICES':'-1','ONNX_PROVIDER':'CPUExecutionProvider','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2','MKL_NUM_THREADS':'2','HF_HUB_OFFLINE':'1','HF_HUB_DISABLE_TELEMETRY':'1','HF_HOME':str(root/'cache/hf'),'XDG_CACHE_HOME':str(root/'cache'),'PYTHONDONTWRITEBYTECODE':'1'})
def deny_network(event,args):
 if event in ['socket.connect','socket.bind']:raise RuntimeError('Network disabled during inference')
sys.addaudithook(deny_network)
import numpy as np
import onnxruntime as ort
out=root/'audio';out.mkdir(exist_ok=True)
texts={
 'accueil':"Bonjour, je suis JARVIS. Je peux vous aider à organiser vos projets et retenir les informations que vous choisissez de me confier.",
 'memoire':"Vous préférez le café décaféiné. J'ai corrigé cette préférence. Le projet Atlas est en préparation, et sa prochaine étape est un essai sur processeur.",
 'quebec_lexique':"Ce soir, on va jaser du projet. Je passe au dépanneur après le travail. Le rendez-vous est prévu à dix-sept heures trente, le treize octobre.",
}
(root/'corpus.json').write_text(json.dumps(texts,ensure_ascii=False,indent=2))
engine=sys.argv[1];records=[];t=time.perf_counter()
options=ort.SessionOptions();options.intra_op_num_threads=2;options.inter_op_num_threads=1;options.execution_mode=ort.ExecutionMode.ORT_SEQUENTIAL
if engine.startswith('piper'):
 from piper import PiperVoice,SynthesisConfig
 voice_name=engine.split('-')[1];m=root/'models'/f'{voice_name}-fr_FR-{voice_name}-medium.onnx'
 voice=PiperVoice.load(str(m),config_path=str(m)+'.json',use_cuda=False)
 # Recreate with bounded session options; inference remains CPU only.
 voice.session=ort.InferenceSession(str(m),sess_options=options,providers=['CPUExecutionProvider'])
 load=time.perf_counter()-t
 for name,text in texts.items():
  target=out/f'{engine}-{name}.wav';started=time.perf_counter()
  with wave.open(str(target),'wb') as wav:voice.synthesize_wav(text,wav)
  elapsed=time.perf_counter()-started
  with wave.open(str(target),'rb') as wav:duration=wav.getnframes()/wav.getframerate();rate=wav.getframerate()
  records.append({'file':target.name,'text_key':name,'synthesis_s':elapsed,'audio_s':duration,'rtf':elapsed/duration,'sample_rate':rate})
elif engine=='kokoro':
 from kokoro_onnx import Kokoro
 sess=ort.InferenceSession(str(root/'models/kokoro-v1.0.int8.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
 voice=Kokoro.from_session(sess,str(root/'models/voices-v1.0.bin'));load=time.perf_counter()-t
 for name,text in texts.items():
  target=out/f'kokoro-ff_siwis-{name}.wav';started=time.perf_counter();audio,rate=voice.create(text,voice='ff_siwis',speed=1.0,lang='fr-fr');elapsed=time.perf_counter()-started
  with wave.open(str(target),'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
  duration=len(audio)/rate;records.append({'file':target.name,'text_key':name,'synthesis_s':elapsed,'audio_s':duration,'rtf':elapsed/duration,'sample_rate':rate})
elif engine in ('stt','stt-small'):
 from faster_whisper import WhisperModel
 size='small' if engine=='stt-small' else 'base'
 m=root/('models/whisper-'+size);m.mkdir(exist_ok=True)
 for name in ['config.json','model.bin','tokenizer.json','vocabulary.txt']:
  dest=m/name
  if not dest.exists():dest.symlink_to(root/'models'/('whisper-'+size+'-'+name))
 model=WhisperModel(str(m),device='cpu',compute_type='int8',cpu_threads=2,num_workers=1,local_files_only=True);load=time.perf_counter()-t
 for target in sorted(out.glob('*.wav')):
  started=time.perf_counter();segments,info=model.transcribe(str(target),language='fr',beam_size=1,vad_filter=False,condition_on_previous_text=False);text=' '.join(s.text.strip() for s in segments);elapsed=time.perf_counter()-started
  with wave.open(str(target),'rb') as wav:duration=wav.getnframes()/wav.getframerate()
  key=next((k for k in texts if target.stem.endswith(k)),None)
  records.append({'file':target.name,'text_key':key,'reference':texts.get(key),'transcript':text,'transcription_s':elapsed,'audio_s':duration,'rtf':elapsed/duration,'language':info.language})
 with wave.open(str(root/'silence-fixture.wav'),'wb') as wav:
  wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(16000);wav.writeframes(b'\0'*64000)
 started=time.perf_counter();segments,info=model.transcribe(str(root/'silence-fixture.wav'),language='fr',beam_size=1,vad_filter=False,condition_on_previous_text=False);transcript=' '.join(s.text.strip() for s in segments)
 records.append({'file':'silence-fixture.wav','kind':'silence','audio_s':2.0,'transcript':transcript,'transcription_s':time.perf_counter()-started,'passed_no_hallucination':not bool(transcript)})
else:raise ValueError(engine)
result={'engine':engine,'model_load_s':load,'cpu_affinity':sorted(os.sched_getaffinity(0)),'provider':'CPU only','network':'denied during inference','records':records}
(root/f'{engine}-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
