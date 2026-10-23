"""Fixed independent reads; no model-supplied source code or shell fragments."""
import shlex


PROBES={
 'gpu_inventory':('python3','''import json,subprocess,platform
r=subprocess.run(['nvidia-smi','--query-gpu=name,driver_version,memory.total,memory.used','--format=csv,noheader,nounits'],capture_output=True,text=True,check=True)
gpu,driver,total,used=[x.strip() for x in r.stdout.splitlines()[0].split(',')]
print(json.dumps({'gpu':gpu,'driver_version':driver,'vram_total_mib':int(total),'vram_used_mib':int(used),'python':platform.python_version(),'kernel':platform.release()}))
'''),
 'tts_runtime':('venv/bin/python','''import json,torch,importlib.util
available=torch.cuda.is_available()
value=torch.tensor([1.,2.,3.],device='cuda').sum().item() if available else None
print(json.dumps({'cuda_available':available,'cuda_tensor_sum':value,'torch_version':torch.__version__,'cuda_runtime':torch.version.cuda,'tts_engine_importable':any(importlib.util.find_spec(x) is not None for x in ['qwen_tts','chatterbox'])}))
'''),
 'archive_inventory':('python3','''import json,zipfile,hashlib,pathlib,wave,io,array,math,sys
p=pathlib.Path('references.zip');z=zipfile.ZipFile(p)
names=[n for n in z.namelist() if n.lower().endswith('.wav') and not n.startswith('__MACOSX/') and not n.split('/')[-1].startswith('._')]
records=[]
for name in names:
 raw=z.read(name)
 with wave.open(io.BytesIO(raw)) as w:
  rate=w.getframerate();channels=w.getnchannels();width=w.getsampwidth();frames=w.getnframes();body=w.readframes(frames)
 if width==2:
  values=array.array('h',body)
  if sys.byteorder!='little':values.byteswap()
 elif width==1:values=[v-128 for v in body]
 else:values=[int.from_bytes(body[i:i+width],'little',signed=True) for i in range(0,len(body),width)]
 scale=2**(width*8-1);rms=math.sqrt(sum(v*v for v in values)/len(values)) if values else 0;peak=max((abs(v) for v in values),default=0);full=sum(v in (-scale,scale-1) for v in values)
 records.append({'name':name,'sample_rate':rate,'channels':channels,'sample_width_bytes':width,'duration_s':frames/rate,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pcm_bit_rate_bps':rate*channels*width*8,'rms_dbfs':20*math.log10(rms/scale) if rms else None,'peak_dbfs':20*math.log10(peak/scale) if peak else None,'full_scale_samples':full,'full_scale_fraction':full/len(values) if values else 0})
print(json.dumps({'valid_zip':z.testzip() is None,'wav_files':len(records),'archive_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'total_duration_s':sum(r['duration_s'] for r in records),'wav_bytes_total':sum(r['bytes'] for r in records),'full_scale_samples_total':sum(r['full_scale_samples'] for r in records),'mean_duration_s':sum(r['duration_s'] for r in records)/len(records) if records else None,'files':records}))
'''),
 'script_syntax':('python3','''import json,subprocess
paths=['lancer_tts.sh','desinstaller_tts.sh']
checks=[subprocess.run(['bash','-n',p],capture_output=True).returncode==0 for p in paths]
print(json.dumps({'launch_syntax_ok':checks[0],'uninstall_syntax_ok':checks[1]}))
''')
}


def probe_command(root,name):
    if name not in PROBES:raise ValueError('Unknown fixed probe')
    executable,source=PROBES[name]
    if '/' in executable:executable=root+'/'+executable
    return shlex.join([executable,'-c',source])
