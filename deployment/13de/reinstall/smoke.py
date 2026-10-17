#!/usr/bin/env python3
"""Targeted no-disk/no-network boot: module indexes, French map, pinned SSH daemon."""
import pathlib,subprocess,time
b=pathlib.Path(__file__).resolve().parents[1]/'private/reinstall-02'
commands='''mount -t proc proc /proc
mount -t sysfs sys /sys
mount -t devtmpfs devtmpfs /dev
modprobe nvme && modprobe raid1 && modprobe ext4 && modprobe vfat && echo JARVIS_MODULES_OK
/bin/loadkeys -C /dev/tty1 fr && echo JARVIS_KEYBOARD_FR_OK
/usr/bin/dumpkeys -C /dev/tty1 | grep -E "keycode +1[67] "
printf TOOL_CHECK | tee /tmp/tee-check
gzip --help
mkdir -p /run/sshd
echo "sshd:*:102:65534:sshd:/run/sshd:/bin/false" >> /etc/passwd
/usr/sbin/sshd -t -o HostKey=/jarvis/host_key -f /dev/null -o PidFile=/run/test.pid -o PasswordAuthentication=no && echo JARVIS_SSH_CONFIG_OK
/usr/sbin/sshd -D -e -p 2222 -o HostKey=/jarvis/host_key -f /dev/null -o PidFile=/run/test.pid -o PasswordAuthentication=no &
sleep 2
kill $(cat /run/test.pid)
/usr/sbin/debootstrap --version
poweroff -f
'''
with (b/'smoke-final.log').open('w') as f:
 p=subprocess.Popen(['qemu-system-x86_64','-machine','accel=tcg','-m','768','-nodefaults','-no-reboot','-display','none','-serial','stdio','-nic','none','-kernel',str(b/'http/linux'),'-initrd',str(b/'http/initrd.gz'),'-append','console=ttyS0 rdinit=/bin/sh'],stdin=subprocess.PIPE,stdout=f,stderr=subprocess.STDOUT)
 deadline=time.monotonic()+40
 while time.monotonic()<deadline:
  if 'job control turned off' in (b/'smoke-final.log').read_text(errors='replace'):break
  time.sleep(.5)
 p.stdin.write(commands.encode());p.stdin.flush()
 try:p.wait(timeout=40)
 except subprocess.TimeoutExpired:p.terminate();p.wait()
log=(b/'smoke-final.log').read_text(errors='replace')
for line in log.splitlines():
 if any(x in line for x in ['JARVIS_','not found','error','Error','Server listening','debootstrap','failed','Failed']):print(line)
for mark in ['JARVIS_MODULES_OK','JARVIS_KEYBOARD_FR_OK','JARVIS_SSH_CONFIG_OK']:
 assert '\n'+mark in log,mark+' missing'
assert 'Server listening on 0.0.0.0 port 2222' in log
print('SMOKE_PASS: modules, French keymap, SSH daemon and debootstrap checked; no installation or network test claimed')
