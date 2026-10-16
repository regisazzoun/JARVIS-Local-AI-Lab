#!/usr/bin/env python3
"""Boot each disposable NVMe alone through OVMF, without direct kernel boot."""
import argparse,hashlib,json,pathlib,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args();b=a.session.resolve()
assert b.is_relative_to((ROOT/'private').resolve())
installation=(b/'console.log').read_text(errors='replace');assert '\nJARVIS_RAID_ESP_QUALIFIED' in installation
proofs=[]
for name,serial in [('a','QUALIFY-A'),('b','QUALIFY-B')]:
 log=b/f'boot-{name}.log';log.touch(mode=0o600)
 variables=b/f'boot-{name}-vars.fd';variables.write_bytes((b/'vars.fd').read_bytes())
 cmd=['sudo','-n','qemu-system-x86_64','-run-with','user=adminjarvis','-machine','q35,accel=kvm','-m','2048','-smp','2','-nodefaults','-display','none','-monitor','none','-serial','file:'+str(log),'-nic','none','-drive','if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd','-drive','if=pflash,format=raw,file='+str(variables),'-drive','if=none,id=disk,format=qcow2,file='+str(b/(name+'.qcow2')),'-device','nvme,drive=disk,serial='+serial]
 child=subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 try:
  deadline=time.monotonic()+210;success=False
  while time.monotonic()<deadline and child.poll() is None:
   if 'JARVIS_INSTALLED_BOOT_OK' in log.read_text(errors='replace'):success=True;break
   time.sleep(1)
  if not success:print(log.read_text(errors='replace')[-4000:],flush=True)
  assert success,'single-disk EFI boot failed: '+name
  proofs.append(dict(disk=name,only_this_nvme_attached=True,native_uefi_boot=True,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
  print('NATIVE_EFI_SINGLE_DISK_BOOT_OK',name,flush=True)
 finally:
  child.terminate()
  try:child.wait(timeout=5)
  except subprocess.TimeoutExpired:child.kill();child.wait()
record=dict(dual_esp_boot_qualified=True,recipe_sha256=hashlib.sha256((ROOT/'debian/preseed-bootstrap.candidate.cfg').read_bytes()).hexdigest(),proofs=proofs,installation_log_sha256=hashlib.sha256((b/'console.log').read_bytes()).hexdigest(),scope='disposable virtual NVMe; not a physical disk-disconnection test')
(b/'qualification.json').write_text(json.dumps(record,indent=2)+'\n')
print('DUAL_ESP_QUALIFICATION_RECORDED',b/'qualification.json',flush=True)
