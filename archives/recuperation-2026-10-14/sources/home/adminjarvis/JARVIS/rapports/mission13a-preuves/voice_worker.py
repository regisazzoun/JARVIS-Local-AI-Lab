"""Moteurs fichiers locaux CPU : aucune API, aucun microphone, aucun client Ollama."""
import os,sys,time,json,wave,resource,argparse
from pathlib import Path
ROOT=Path('/opt/jarvis/voice')
os.environ.update(CUDA_VISIBLE_DEVICES='-1',OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2',MKL_NUM_THREADS='2',HF_HUB_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',HF_HOME=str(ROOT/'logs/cache/hf'),XDG_CACHE_HOME=str(ROOT/'logs/cache'),PYTHONDONTWRITEBYTECODE='1',TOKENIZERS_PARALLELISM='false')
os.nice(10);os.sched_setaffinity(0,set(sorted(os.sched_getaffinity(0))[:2]));resource.setrlimit(resource.RLIMIT_CPU,(180,185))
def deny_network(event,args):
 if event in ('socket.connect','socket.bind'):raise RuntimeError('Réseau interdit pendant les essais')
sys.addaudithook(deny_network)
ap=argparse.ArgumentParser();ap.add_argument('engine',choices=['tts','stt']);ap.add_argument('--wav',required=True,type=Path);ap.add_argument('--result',required=True,type=Path);ap.add_argument('--text');args=ap.parse_args()
cfg=json.loads((ROOT/'config/voice.json').read_text());text=args.text or cfg['test_text']
t=time.perf_counter();cpu=time.process_time()
result={'engine':args.engine,'pid':os.getpid(),'python':sys.version,'cpu_affinity':sorted(os.sched_getaffinity(0)),'network':'kernel namespace without network + Python audit deny','reference':text,'wav':str(args.wav),'limits':{'cpu_threads':2}}
if args.engine=='tts':
 import onnxruntime as ort
 from piper import PiperVoice
 from piper.config import PiperConfig
 options=ort.SessionOptions();options.intra_op_num_threads=2;options.inter_op_num_threads=1;options.execution_mode=ort.ExecutionMode.ORT_SEQUENTIAL
 model=ROOT/cfg['tts_model'];config=ROOT/cfg['tts_config']
 # Construct one bounded CPU session, avoiding Mission12's double model load.
 voice=PiperVoice(session=ort.InferenceSession(str(model),sess_options=options,providers=['CPUExecutionProvider']),config=PiperConfig.from_dict(json.loads(config.read_text())),download_dir=ROOT/'logs/cache',use_tashkeel=False)
 result.update(model=str(model),providers=voice.session.get_providers(),model_load_s=time.perf_counter()-t)
 assert result['providers']==['CPUExecutionProvider']
 start=time.perf_counter()
 with wave.open(str(args.wav),'wb') as w:voice.synthesize_wav(text,w)
 result['synthesis_s']=time.perf_counter()-start
else:
 from faster_whisper import WhisperModel
 model=ROOT/cfg['stt_model']
 voice=WhisperModel(str(model),device='cpu',compute_type='int8',cpu_threads=2,num_workers=1,local_files_only=True)
 result.update(model=str(model),device=voice.model.device,compute_type=voice.model.compute_type,model_load_s=time.perf_counter()-t)
 assert voice.model.device=='cpu' and voice.model.compute_type in ('int8','int8_float32')
 result['requested_compute_type']='int8'
 start=time.perf_counter();segments,info=voice.transcribe(str(args.wav),language='fr',beam_size=1,vad_filter=False,condition_on_previous_text=False)
 result.update(transcript=' '.join(s.text.strip() for s in segments),language=info.language,transcription_s=time.perf_counter()-start)
 import re,difflib
 a=re.findall(r'\w+',text.lower());b=re.findall(r'\w+',result['transcript'].lower())
 result['word_differences']=[{'operation':op,'reference':a[i:j],'recognized':b[k:l]} for op,i,j,k,l in difflib.SequenceMatcher(a=a,b=b).get_opcodes() if op!='equal']
with wave.open(str(args.wav),'rb') as w:
 import array,math
 assert w.getnchannels()==1 and w.getsampwidth()==2 and w.getcomptype()=='NONE'
 samples=array.array('h',w.readframes(w.getnframes()));rms=math.sqrt(sum(x*x for x in samples)/len(samples));peak=max(abs(x) for x in samples)
 result['wav_validation']={'sample_rate':w.getframerate(),'frames':w.getnframes(),'channels':1,'sample_width':2,'duration_s':w.getnframes()/w.getframerate(),'rms':rms,'peak':peak,'non_silent':rms>1,'readable':True}
 assert rms>1 and peak>0
result['rtf']=result.get('synthesis_s',result.get('transcription_s'))/result['wav_validation']['duration_s']
result.update(total_wall_s=time.perf_counter()-t,cpu_s=time.process_time()-cpu,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
result['cpu_average_percent_one_core']=100*result['cpu_s']/result['total_wall_s']
args.result.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
