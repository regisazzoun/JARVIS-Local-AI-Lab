#!/usr/bin/env python3
"""Fixed-operation VM worker. No host shell, network bridge or physical disk input."""
import argparse, hashlib, json, os, re, shutil, subprocess, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent / 'runtime'
ASSETS = Path(__file__).resolve().parent / 'assets'

def tool(name):
    found = shutil.which(name)
    if not found: raise RuntimeError('Missing prerequisite: '+name)
    return found

def workspace(name):
    if not re.fullmatch(r'vm-[a-z0-9]{1,20}', name): raise ValueError('invalid VM identifier')
    ROOT.mkdir(mode=0o700, exist_ok=True)
    if ROOT.is_symlink(): raise ValueError('symlink root')
    p = ROOT/name
    if p.is_symlink(): raise ValueError('symlink workspace')
    return p

def manifest(p):
    m = json.loads((p/'owner.json').read_text())
    if m != {'mission':'13D-E', 'name':p.name}: raise ValueError('unowned workspace')
    if any(f.is_symlink() for f in p.rglob('*')): raise ValueError('symlink in workspace')

def command(p, accel='tcg'):
    manifest(p)
    # Only local preverified assets. No arbitrary argument/path from model.
    for f in ['OVMF_CODE.fd','ipxe.efi','boot.ipxe','debian/linux','debian/initrd.gz']:
        if not (ASSETS/f).is_file() or (ASSETS/f).is_symlink(): raise RuntimeError('missing asset '+f)
    pins=json.loads((ASSETS/'SHA256.json').read_text())
    for f in ['OVMF_CODE.fd','ipxe.efi','boot.ipxe','debian/linux','debian/initrd.gz']:
        if pins.get(f)!=hashlib.sha256((ASSETS/f).read_bytes()).hexdigest(): raise ValueError('asset hash mismatch: '+f)
    return [tool('qemu-system-x86_64'), '-machine','q35,accel='+accel,'-m','4096','-smp','2',
        '-bios',str(ASSETS/'OVMF_CODE.fd'),'-display','none','-monitor','none',
        '-serial','file:'+str(p/'serial.log'),'-nic','none',
        '-netdev','user,id=lab,restrict=on,ipv6=off,tftp='+str(ASSETS)+',bootfile=ipxe.efi',
        '-device','e1000,netdev=lab','-boot','order=n',
        '-drive','file='+str(p/'disk0.qcow2')+',if=virtio,format=qcow2',
        '-drive','file='+str(p/'disk1.qcow2')+',if=virtio,format=qcow2','-no-reboot']

def dispatch(action,name):
    p=workspace(name)
    if action=='create':
        qimg=tool('qemu-img')
        p.mkdir(mode=0o700)
        (p/'owner.json').write_text(json.dumps({'mission':'13D-E','name':name}))
        for i in range(2): subprocess.run([qimg,'create','-f','qcow2',str(p/f'disk{i}.qcow2'),'24G'],check=True,capture_output=True)
        return {'created':name}
    manifest(p)
    if action=='plan': return {'argv':command(p)}
    if action=='run':
        # Bounded synchronous worker: client must run outside the 13F 25-second shell.
        with (p/'qemu.log').open('ab') as log:
            try:
                result=subprocess.run(command(p),stdout=log,stderr=log,timeout=1800)
                state={'exit_code':result.returncode,'installation_verified':False}
            except subprocess.TimeoutExpired: state={'timeout':True,'installation_verified':False}
        (p/'result.json').write_text(json.dumps(state)); return state
    if action=='logs':
        return {f:p.joinpath(f).read_text(errors='replace')[-16000:] for f in ['serial.log','qemu.log','result.json'] if p.joinpath(f).is_file()}
    if action=='destroy':
        # CLI is single-user/single-worker. Refuse concurrent invocation using flock below.
        shutil.rmtree(p); return {'destroyed':name}
    raise ValueError('unknown action')

if __name__=='__main__':
    import fcntl
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['create','plan','run','logs','destroy'])
    parser.add_argument('name')
    a=parser.parse_args()
    if ROOT.is_symlink(): raise SystemExit('symlink root')
    ROOT.mkdir(mode=0o700,exist_ok=True)
    if (ROOT/'.lock').is_symlink() or (ROOT/'audit.jsonl').is_symlink(): raise SystemExit('symlink control file')
    with (ROOT/'.lock').open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:
            result=dispatch(a.action,a.name)
            with (ROOT/'audit.jsonl').open('a') as f: f.write(json.dumps({'time':time.time(),'action':a.action,'vm':a.name,'result':result})+'\n')
            print(json.dumps(result))
        except Exception as e:
            with (ROOT/'audit.jsonl').open('a') as f: f.write(json.dumps({'time':time.time(),'action':a.action,'vm':a.name,'error':str(e)})+'\n')
            raise SystemExit(str(e))
