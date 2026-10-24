#!/bin/sh
# Scoped one-shot continuation, invoked by JARVIS. No repeating install or forced reboot.
set -eu
progress() { printf '%s %s\n' "$(date -Iseconds)" "$*" | tee -a /run/jarvis-install-progress.log >/dev/tty1; }
/bin/sh /guard-physical.sh
[ ! -e /run/jarvis-autofinish-started ] || exit 0
touch /run/jarvis-autofinish-started
start=$(date +%s);last_done=0;last_progress=$start
while [ ! -e /run/jarvis-gpu-packages-complete ];do
 if grep -q 'FAILED NVIDIA/CUDA' /run/jarvis-install-progress.log;then progress 'autofinish BLOCKED: erreur paquets NVIDIA, correction au checkpoint requise';exit 1;fi
 [ "$(date +%s)" -lt "$((start+21600))" ] || { progress 'autofinish BLOCKED: delai maximal paquets depasse';exit 1; }
 sleep 30
done
progress 'autofinish WAITING: paquets prets; attente synchronisation RAID avant arret propre'
while [ "$(cat /sys/block/md0/md/sync_action)" != idle ];do
 [ "$(cat /sys/block/md0/md/degraded)" = 0 ] || { progress 'autofinish BLOCKED: RAID degrade';exit 1; }
 done_now=$(awk '{print $1}' /sys/block/md0/md/sync_completed)
 if [ "$done_now" != "$last_done" ];then last_progress=$(date +%s);last_done=$done_now;fi
 [ "$(date +%s)" -lt "$((last_progress+1200))" ] || { progress 'autofinish BLOCKED: synchronisation sans progression depuis20min';exit 1; }
 [ "$(date +%s)" -lt "$((start+21600))" ] || { progress 'autofinish BLOCKED: delai maximal synchronisation depasse';exit 1; }
 sleep 30
done
/bin/sh /guard-physical.sh
[ -e /run/jarvis-install-complete ]
[ "$(cat /sys/block/md0/md/degraded)" = 0 ]
chroot /target python3 /var/lib/jarvis/mission14b/verify-storage.py /var/lib/jarvis/mission14b/manifest.json --root-source /dev/md0
chroot /target /usr/sbin/sshd -t
cmp /target/boot/efi/EFI/debian/shimx64.efi /target/boot/efi-secondary/EFI/debian/shimx64.efi
cmp /target/boot/efi/EFI/debian/grubx64.efi /target/boot/efi-secondary/EFI/debian/grubx64.efi
# Freeze a final honest console before unmounting /target and stopping its mirror.
progress 'reboot READY: Debian/EFI/paquets prets, RAID synchronise; arret propre puis reboot automatique'
cp /run/jarvis-install-progress.log /target/var/lib/jarvis/mission14b/install-progress.log
cp /run/jarvis-install.log /target/var/lib/jarvis/mission14b/install-original.log
cp /run/jarvis-finalize.log /target/var/lib/jarvis/mission14b/finalize.log
cp /run/jarvis-gpu-install.log /target/var/lib/jarvis/mission14b/gpu-install.log
if [ -e /run/jarvis-screen-controller.pid ];then kill "$(cat /run/jarvis-screen-controller.pid)" || :;fi
printf '\033[2J\033[HJARVIS 14B : RAID synchronise, Debian et NVIDIA/CUDA prepares.\nRedemarrage automatique du systeme installe ; verification en cours apres boot.\n' >/dev/tty1
sync
awk '$2 ~ /^\/target(\/|$)/ {print $2}' /proc/mounts | sort -r | while read mountpoint;do umount "$mountpoint" || exit 1;done
mdadm --stop /dev/md0
sync
/jarvis/busybox-full reboot
