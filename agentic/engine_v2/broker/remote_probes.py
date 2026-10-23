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
 'archive_inventory':('python3','''import json,zipfile,hashlib,pathlib,wave,io
p=pathlib.Path('references.zip');z=zipfile.ZipFile(p)
names=[n for n in z.namelist() if n.lower().endswith('.wav') and not n.startswith('__MACOSX/') and not n.split('/')[-1].startswith('._')]
records=[]
for name in names:
 with wave.open(io.BytesIO(z.read(name))) as w:
  records.append({'name':name,'sample_rate':w.getframerate(),'channels':w.getnchannels(),'duration_s':w.getnframes()/w.getframerate()})
print(json.dumps({'valid_zip':z.testzip() is None,'wav_files':len(records),'archive_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'files':records}))
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
