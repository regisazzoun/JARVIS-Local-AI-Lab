#!/usr/bin/env python3
"""One bounded qualification of the real partman/EFI recipe on TWO disposable VM disks.
No access to host disks: all QEMU drives are freshly created files in private/session.
"""
import argparse,gzip,json,os,pathlib,subprocess,uuid
ROOT=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('session',type=pathlib.Path);a=p.parse_args();os.umask(0o077)
b=a.session.resolve();assert b.is_relative_to((ROOT/'private').resolve());b.mkdir(mode=0o700)
stage=b/'stage';stage.mkdir();drivers=stage/'jarvis-drivers';drivers.mkdir()
for f in (ROOT/'private/bootstrap-discovery-04/stage/jarvis-drivers').glob('*.ko'):(drivers/f.name).write_bytes(f.read_bytes())
(stage/'load-nvme.sh').write_text('set -eu\nfor n in nvme-auth nvme-core nvme; do\n module=$(printf %s "$n" | tr "-" "_")\n test -d "/sys/module/$module" || insmod /jarvis-drivers/$n.ko\ndone\n')
plan=dict(vendor='QEMU',product='Standard PC (Q35 + ICH9, 2009)',uuid=str(uuid.uuid4()),disks=[dict(path='/dev/nvme0n1',serial='QUALIFY-A',model='QEMU NVMe Ctrl',size=16*1024**3),dict(path='/dev/nvme1n1',serial='QUALIFY-B',model='QEMU NVMe Ctrl',size=16*1024**3)])
(stage/'approved.json').write_text(json.dumps(plan))
(stage/'approved.tsv').write_text('uuid\t'+plan['uuid']+'\n'+''.join(f"disk\tnvme{i}n1\tQUALIFY-{chr(65+i)}\tQEMU NVMe Ctrl\t33554432\n" for i in range(2)))
# This fixture cannot run on Dell or any physical target, even if the archive is misused.
(stage/'guard-physical.sh').write_text('''set -eu
test "$(cat /sys/class/dmi/id/sys_vendor)" = QEMU
test -d /sys/firmware/efi
for pair in 'nvme0n1 QUALIFY-A' 'nvme1n1 QUALIFY-B'; do
 set -- $pair
 test "$(cat /sys/block/$1/device/serial | sed 's/ *$//')" = "$2"
 test "$(cat /sys/block/$1/size)" = 33554432
done
''')
for name in ('install-bootstrap.sh','finalize-efi.sh','sync-esp.sh','verify-storage.py'):(stage/name).write_bytes((ROOT/'bootstrap'/name).read_bytes())
with (stage/'install-bootstrap.sh').open('a') as f:f.write('\n# Qualification fixture only: record real installed boot without any physical target access.\ncat > /target/etc/systemd/system/jarvis-qualification-boot.service <<\'EOF\'\n[Unit]\nDescription=Disposable VM installed boot proof\nAfter=local-fs.target\n[Service]\nType=oneshot\nExecStart=/bin/sh -c \'test "$(cat /sys/class/dmi/id/sys_vendor)" = QEMU && test -d /sys/firmware/efi && findmnt / >/dev/ttyS0 && cat /proc/mdstat >/dev/ttyS0 && echo JARVIS_INSTALLED_BOOT_OK >/dev/ttyS0\'\n[Install]\nWantedBy=multi-user.target\nEOF\nin-target systemctl enable jarvis-qualification-boot.service\n')
(stage/'jarvis-event.sh').write_text('#!/bin/sh\nexit 0\n')
(stage/'jarvis-collect.sh').write_text('#!/bin/sh\nexit 0\n')
(stage/'bootstrap-expires').write_text('2030-01-01 00:00:00 UTC\n')
hashed=subprocess.run(['openssl','passwd','-6','-stdin'],input=os.urandom(32).hex().encode()+b'\n',capture_output=True,check=True).stdout.decode().strip()
cfg=(ROOT/'debian/preseed-bootstrap.candidate.cfg').read_text().replace('@PASSWORD_HASH@',hashed).replace('@DISK_A@','/dev/nvme0n1').replace('@DISK_B@','/dev/nvme1n1')
cfg=cfg.replace('locale string fr_FR.UTF-8','locale string en_US.UTF-8')
cfg+='''
d-i preseed/early_command string /bin/sh /load-nvme.sh
d-i partman-md/confirm boolean true
d-i partman-md/confirm_nooverwrite boolean true
d-i partman-md/device_remove_md boolean true
d-i partman-lvm/device_remove_lvm boolean true
d-i partman/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true
d-i clock-setup/ntp boolean false
d-i grub-installer/bootdev string /dev/nvme0n1
d-i grub-installer/force-efi-extra-removable boolean true
d-i preseed/late_command string /bin/sh /install-bootstrap.sh && echo JARVIS_RAID_ESP_QUALIFIED >/dev/ttyS0 || echo JARVIS_RAID_ESP_FAILED >/dev/ttyS0; while :; do sleep 3600; done
'''
(stage/'preseed.cfg').write_text(cfg)
names='\n'.join(sorted(str(p.relative_to(stage)) for p in stage.rglob('*')))+'\n'
archive=subprocess.run(['cpio','-o','-H','newc','--reproducible'],cwd=stage,input=names.encode(),capture_output=True,check=True).stdout
(b/'initrd.gz').write_bytes((ROOT/'private/debian-verified/initrd.gz').read_bytes()+gzip.compress(archive,mtime=0))
for n in ('a','b'):subprocess.run(['qemu-img','create','-f','qcow2',str(b/(n+'.qcow2')),'16G'],check=True)
(b/'vars.fd').write_bytes(pathlib.Path('/usr/share/OVMF/OVMF_VARS_4M.fd').read_bytes())
(b/'console.log').touch(mode=0o600)
cmd=['sudo','-n','qemu-system-x86_64','-run-with','user=adminjarvis','-machine','q35,accel=kvm','-m','2048','-smp','2','-nodefaults','-display','none','-monitor','none','-chardev','socket,id=serial,path='+str(b/'console.sock')+',server=on,wait=off,logfile='+str(b/'console.log'),'-serial','chardev:serial','-drive','if=pflash,format=raw,readonly=on,file=/usr/share/OVMF/OVMF_CODE_4M.fd','-drive','if=pflash,format=raw,file='+str(b/'vars.fd'),'-netdev','user,id=net0','-device','e1000e,netdev=net0','-kernel',str(ROOT/'private/debian-verified/linux'),'-initrd',str(b/'initrd.gz'),'-append','auto=true priority=critical file=/preseed.cfg interface=auto console=ttyS0,115200n8 locale=en_US.UTF-8 language=en country=US keymap=fr DEBIAN_FRONTEND=noninteractive nomodeset']
for index,n in enumerate(('a','b')):cmd+=['-drive',f'if=none,id=disk{index},format=qcow2,file={b/(n+".qcow2")}','-device',f'nvme,drive=disk{index},serial=QUALIFY-{chr(65+index)}']
(b/'command.json').write_text(json.dumps(cmd,indent=2)+'\n')
print('QUALIFICATION_START',b,flush=True)
subprocess.run(cmd,check=True,timeout=1800)
