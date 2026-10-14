#!/bin/bash
# PROPOSITION UNIQUEMENT : NON EXECUTEE EN MISSION 05B-P
set -euo pipefail
umask 077
stage_jarvis=/home/adminjarvis/JARVIS/rapports/mission05B-sauvegarde-$(date +%Y%m%d-%H%M%S)
mkdir -m 700 "$stage_jarvis"
dpkg-query -W -f='${binary:Package}\t${db:Status-Status}\t${Version}\n' > "$stage_jarvis/paquets.tsv"
apt-mark showmanual > "$stage_jarvis/manuels.txt"
apt-mark showhold > "$stage_jarvis/holds.txt"
systemctl list-unit-files > "$stage_jarvis/services.txt"
systemctl show sddm ssh ssh.socket -p ActiveState -p UnitFileState > "$stage_jarvis/services-critiques.txt"
/usr/sbin/dkms status > "$stage_jarvis/dkms.txt"
getent passwd nvidia-persistenced > "$stage_jarvis/compte-nvidia-avant.txt" || true
getent group nvidia-persistenced > "$stage_jarvis/groupe-nvidia-avant.txt" || true
sudo cp --preserve=all /var/lib/dpkg/status "$stage_jarvis/dpkg-status"
for f_jarvis in /boot/initrd.img-*; do
    sudo cp --preserve=all "$f_jarvis" "$stage_jarvis/"
done
for path_jarvis in etc/apt etc/modprobe.d etc/modules-load.d etc/dkms etc/systemd/system etc/initramfs-tools etc/kernel etc/X11 var/lib/dkms var/lib/systemd/deb-systemd-helper-enabled var/lib/systemd/deb-systemd-helper-masked; do
    if [ -e "/$path_jarvis" ]; then printf '%s\n' "$path_jarvis"; fi
done > "$stage_jarvis/configuration-paths.txt"
sudo tar -C / -czf "$stage_jarvis/configurations.tgz" -T "$stage_jarvis/configuration-paths.txt"
sudo sha256sum /boot/grub/grub.cfg /boot/vmlinuz-* /boot/initrd.img-* > "$stage_jarvis/boot-sha256.txt"
printf '%s\n' "$stage_jarvis"
