#!/bin/sh
# SSH supervision in RAM. Never returns to partman; writes no target disk.
set -eu
exec >>/var/log/jarvis-supervision.log 2>&1
stop() { echo "STOP: $*"; echo "JARVIS STOP: $*" >/dev/tty1; while :; do sleep 60; done; }
trap 'stop erreur-initialisation' EXIT
# Overlay module metadata is supplemented with all module paths, then depmod.
# Module indexes were prepared on JARVIS against the merged initrd.
modprobe nvme || stop nvme
modprobe raid1 || stop raid1
modprobe ext4 || stop ext4
udevadm trigger; udevadm settle
/bin/loadkeys -C /dev/tty1 fr || stop clavier-fr
if ! /bin/sh /guard-physical.sh >/run/jarvis-identity.log 2>&1; then
 cat /run/jarvis-identity.log >/dev/tty1
 stop identite
fi
for d in /sys/bus/pci/devices/*; do
 case "$(cat "$d/class" 2>/dev/null)" in 0x02*) modprobe "$(cat "$d/modalias")" || :;; esac
done
for d in /sys/class/net/*; do [ "${d##*/}" = lo ] || ip link set "${d##*/}" up || :; done
selected=
for retry in 1 2 3 4 5 6 7 8 9 10; do
 for d in /sys/class/net/*; do
  [ "${d##*/}" = lo ] && continue
  if [ "$(cat "$d/carrier" 2>/dev/null)" = 1 ]; then selected=${d##*/};break;fi
 done
 [ -z "$selected" ] || break;sleep 1
done
[ -n "$selected" ] || stop ethernet
udhcpc -n -q -t 5 -T 3 -i "$selected" -s /etc/udhcpc/default.script || stop dhcp
mkdir -p /run/sshd /root/.ssh
chmod 700 /root/.ssh
cp /jarvis/authorized_keys /root/.ssh/authorized_keys;chmod 600 /root/.ssh/authorized_keys
# Unlock root for key-only SSH in disposable installer RAM, never on installed target.
root_hash=$(cat /jarvis/root.hash)
awk -F: -v h="$root_hash" 'BEGIN{OFS=":"} $1=="root"{$2=h} {print}' /etc/passwd > /tmp/passwd
cat /tmp/passwd > /etc/passwd;rm /tmp/passwd
grep -q "^sshd:" /etc/passwd || echo "sshd:*:102:65534:sshd:/run/sshd:/bin/false" >> /etc/passwd
cat > /jarvis/sshd_config <<'EOF'
Port 2222
HostKey /jarvis/host_key
PidFile /run/jarvis-sshd.pid
AuthorizedKeysFile /root/.ssh/authorized_keys
PermitRootLogin prohibit-password
PasswordAuthentication no
KbdInteractiveAuthentication no
AllowUsers root@192.168.1.99
Subsystem sftp internal-sftp
EOF
/usr/sbin/sshd -t -f /jarvis/sshd_config || stop ssh-config
/usr/sbin/sshd -f /jarvis/sshd_config -E /var/log/jarvis-sshd.log || stop ssh
printf '\033[2J\033[H%s\n' 'JARVIS : identite validee, clavier francais, SSH de supervision actif port 2222.' 'Attente du controleur JARVIS. Aucun partitionnement automatique.' >/dev/tty1
trap - EXIT
while :; do sleep 60; done
