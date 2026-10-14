"""Own CPU-only worker: existing 13A resources are read only."""
import os,json,sys,wave,resource
from pathlib import Path
os.environ.update(CUDA_VISIBLE_DEVICES='-1',OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2',HF_HUB_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONDONTWRITEBYTECODE='1',XDG_CACHE_HOME=os.environ['JARVIS_CACHE'])
os.nice(10)
resource.setrlimit(resource.RLIMIT_CPU,(110,115))
root=Path(sys.argv[2]);mode=sys.argv[1];path=sys.argv[3]
if mode=='stt':
    import av,numpy as np
    from faster_whisper import WhisperModel
    # Decode before model load; enforce actual duration and silence, including compressed uploads.
    samples=[];count=0; rate=16000; limit=float(sys.argv[4])
    with av.open(path) as audio:
        resampler=av.AudioResampler(format='s16',layout='mono',rate=rate)
        for frame in audio.decode(audio=0):
            for f in resampler.resample(frame):
                a=f.to_ndarray().reshape(-1); count+=len(a)
                if count>rate*limit:raise ValueError('Enregistrement trop long')
                samples.append(a)
        for f in resampler.resample(None):
            a=f.to_ndarray().reshape(-1);count+=len(a);samples.append(a)
    if count>rate*limit:raise ValueError('Enregistrement trop long')
    if count<rate*.2:raise ValueError('Enregistrement vide ou trop court')
    data=np.concatenate(samples).astype(np.float32)/32768
    if float(np.sqrt(np.mean(data*data)))<0.003:raise ValueError('Silence détecté')
    model=WhisperModel(str(root/'models/stt/whisper-small'),device='cpu',compute_type='int8',cpu_threads=2,num_workers=1,local_files_only=True)
    segments,_=model.transcribe(data,language='fr',beam_size=1,vad_filter=True,condition_on_previous_text=False)
    text=' '.join(s.text.strip() for s in segments)
    if not text:raise ValueError('Aucune parole reconnue')
    print(json.dumps({'text':text},ensure_ascii=False))
else:
    import onnxruntime as ort
    from piper import PiperVoice
    from piper.config import PiperConfig
    opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
    model=root/'models/tts/fr_FR-tom-medium.onnx'
    voice=PiperVoice(session=ort.InferenceSession(str(model),sess_options=opts,providers=['CPUExecutionProvider']),config=PiperConfig.from_dict(json.loads(Path(str(model)+'.json').read_text())),download_dir=Path(os.environ['JARVIS_CACHE']),use_tashkeel=False)
    text=sys.stdin.read()
    with wave.open(path,'wb') as wav:voice.synthesize_wav(text,wav)
