#!/usr/bin/env python3
"""Independent pinned-key SSH authentication in disposable RAM guest, no disk."""
import pathlib,subprocess,time,socket
b=pathlib.Path(__file__).resolve().parents[1]/'private/reinstall-02'
key=(b/'host_key.pub').read_text().split();known=b/'smoke-known';known.write_text(f'[127.0.0.1]:22222 {key[0]} {key[1]}\n')
commands='''mount -t proc proc /proc
mount -t sysfs sys /sys
mount -t devtmpfs devtmpfs /dev
modprobe e1000
ip link set eth0 up
ip addr add 10.0.2.15/24 dev eth0
mkdir -p /run/sshd /root/.ssh
cp /jarvis/authorized_keys /root/.ssh/authorized_keys
chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys
h=$(cat /jarvis/root.hash)
awk -F: -v h="$h" 'BEGIN{OFS=":"} $1=="root"{$2=h} {print}' /etc/passwd > /tmp/passwd
cat /tmp/passwd > /etc/passwd
echo 'sshd:*:102:65534:sshd:/run/sshd:/bin/false' >> /etc/passwd
/usr/sbin/sshd -f /dev/null -p 2222 -o HostKey=/jarvis/host_key -o AuthorizedKeysFile=/root/.ssh/authorized_keys -o PasswordAuthentication=no -o PermitRootLogin=prohibit-password -o PidFile=/run/test.pid
blkid -h
mkfs.ext4 -V
'''
with (b/'ssh-smoke.log').open('w') as f:
 p=subprocess.Popen(['qemu-system-x86_64','-machine','accel=tcg','-m','768','-nodefaults','-no-reboot','-display','none','-serial','stdio','-netdev','user,id=n0,hostfwd=tcp:127.0.0.1:22222-:2222','-device','e1000,netdev=n0','-kernel',str(b/'http/linux'),'-initrd',str(b/'http/initrd.gz'),'-append','console=ttyS0 rdinit=/bin/sh'],stdin=subprocess.PIPE,stdout=f,stderr=subprocess.STDOUT)
 try:
  end=time.monotonic()+35
  while time.monotonic()<end:
   if 'job control turned off' in (b/'ssh-smoke.log').read_text(errors='replace'):break
   time.sleep(.5)
  p.stdin.write(commands.encode());p.stdin.flush();time.sleep(3)
  args=['ssh','-F','/dev/null','-p','22222','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o',f'UserKnownHostsFile={known}','-o','GlobalKnownHostsFile=/dev/null','-o','IdentitiesOnly=yes','-o','ConnectTimeout=5','-i',str(b/'identity'),'root@127.0.0.1','id; echo JARVIS_SSH_AUTH_OK']
  r=subprocess.run(args,capture_output=True,text=True,timeout=15)
  print(r.stdout,r.stderr);assert r.returncode==0 and 'uid=0' in r.stdout
  (b/'ssh-auth-verified.txt').write_text(r.stdout)
 finally:
  p.terminate();p.wait(timeout=10)
print('SSH_AUTH_SMOKE_PASS')
