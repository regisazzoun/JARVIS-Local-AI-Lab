#!/usr/bin/env python3
"""Read-only installed/late-stage storage acceptance; fail if mirror is not clean."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import argparse,json,pathlib,subprocess,sys,time
p=argparse.ArgumentParser();p.add_argument('manifest');p.add_argument('--root-source');p.add_argument('--allow-resync',action='store_true');p.add_argument('--wait-seconds',type=int,default=0);a=p.parse_args()
plan=json.loads(pathlib.Path(a.manifest).read_text()); expected={pathlib.Path(d['path']).name+'p2' for d in plan['disks']}
assert len(expected)==2,'two distinct members required'
mirrors=[]
for md in pathlib.Path('/sys/block').glob('md*'):
 if not (md/'md').is_dir():continue
 members={p.name for p in (md/'slaves').iterdir()}
 if members==expected:mirrors.append(md)
assert len(mirrors)==1,'expected RAID members missing/ambiguous'
md=mirrors[0]
deadline=time.monotonic()+a.wait_seconds
while (md/'md/sync_action').read_text().strip() != 'idle' and time.monotonic()<deadline:
 time.sleep(5)
for name,value in [('level','raid1'),('raid_disks','2'),('degraded','0')]:
 assert (md/'md'/name).read_text().strip()==value,name
action=(md/'md/sync_action').read_text().strip()
assert action=='idle' or (a.allow_resync and action=='resync'),'sync_action'
root=a.root_source or subprocess.check_output(['findmnt','-n','-o','SOURCE','/'],text=True).strip()
assert pathlib.Path(root).resolve()==pathlib.Path('/dev',md.name).resolve(),'root not on approved mirror'
uuids=[]
for d in plan['disks']:
 device=d['path']+'p1'
 def field(f):return subprocess.check_output(['blkid']+(['-p'] if f=='PART_ENTRY_TYPE' else [])+['-s',f,'-o','value',device],text=True).strip().lower()
 assert field('TYPE')=='vfat','ESP filesystem'
 assert field('PART_ENTRY_TYPE')=='c12a7328-f81f-11d2-ba4b-00a0c93ec93b','ESP GPT type'
 uuids.append(field('PARTUUID'))
assert len(set(uuids))==2 and all(uuids),'independent ESPs required'
print('STORAGE CLEAN: mirrored root, two independent ESPs; physical boot redundancy still untested' if action=='idle' else 'STORAGE ONLINE: healthy members, resync ongoing; final clean acceptance pending')
