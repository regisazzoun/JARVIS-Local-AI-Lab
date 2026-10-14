from pathlib import Path
import json,time,datetime
p=Path(__file__).parent
start=json.loads((p/'debut-observation.json').read_text())['monotonic']
while True:
 r={'date':datetime.datetime.now().astimezone().isoformat(),'elapsed':time.monotonic()-start,'boot':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'reads':{}}
 paths=[Path('/sys/class/nvme/nvme0/state'),Path('/sys/class/net/enp4s0/carrier'),Path('/sys/class/net/enp4s0/speed'),Path('/sys/class/drm/card0-DP-3/status'),Path('/sys/class/drm/card0-DP-3/enabled')]
 paths+=list(Path('/sys/bus/pci/devices').glob('*/aer_*'))+list(Path('/sys/bus/pci/devices').glob('*/resource'))
 for f in paths:
  try:r['reads'][str(f)]=f.read_text()
  except Exception as e:r['reads'][str(f)]={'error':str(e)}
 with (p/'observation.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 print(r['date'],round(r['elapsed'],1),flush=True)
 if r['elapsed']>=305:break
 time.sleep(min(30,306-r['elapsed']))
