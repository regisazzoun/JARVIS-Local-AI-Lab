#!/bin/sh
# Installer context only. Invoked after the existing scoped identity/erase guard.
set -eu
command -v in-target >/dev/null
/bin/sh /guard-physical.sh
test -d /target/boot/efi/EFI/debian
# Require exactly the approved RAID members and a clean mirror.
root_source=$(awk '$2=="/target" {print $1}' /proc/mounts)
test -n "$root_source"
in-target python3 /usr/local/lib/jarvis/verify-storage.py /etc/jarvis/approved.json --root-source "$root_source" --wait-seconds 7200
# ESP1 must already be the filesystem mounted by Debian Installer.
first=$(awk -F '\t' '$1=="disk" {print $2;exit}' /approved.tsv)
second=$(awk -F '\t' '$1=="disk" {n++;if(n==2)print $2}' /approved.tsv)
root_source=$(in-target findmnt -n -o SOURCE /boot/efi)
test "$(readlink -f "$root_source")" = "/dev/${first}p1"
# Both ESPs were created/formatted by partman, never format here.
for disk in "$first" "$second"; do
 test "$(blkid -s TYPE -o value "/dev/${disk}p1")" = vfat
 test "$(blkid -s PART_ENTRY_TYPE -o value "/dev/${disk}p1")" = c12a7328-f81f-11d2-ba4b-00a0c93ec93b
 done
mkdir -p /target/boot/efi-secondary
mount "/dev/${second}p1" /target/boot/efi-secondary
trap 'umount /target/boot/efi-secondary' EXIT
# Copy Debian's SAME installed signed EFI payload; no grub binary download/build.
for esp in /target/boot/efi /target/boot/efi-secondary; do
 mkdir -p "$esp/EFI/debian" "$esp/EFI/BOOT"
 if [ "$esp" != /target/boot/efi ]; then cp -a /target/boot/efi/EFI/debian/. "$esp/EFI/debian/"; fi
 test -f "$esp/EFI/debian/shimx64.efi"
 test -f "$esp/EFI/debian/grubx64.efi"
 test -f "$esp/EFI/debian/grub.cfg"
 cp "$esp/EFI/debian/shimx64.efi" "$esp/EFI/BOOT/BOOTX64.EFI"
 cp "$esp/EFI/debian/grubx64.efi" "$esp/EFI/BOOT/grubx64.efi"
 cp "$esp/EFI/debian/grub.cfg" "$esp/EFI/BOOT/grub.cfg"
 if [ -f "$esp/EFI/debian/mmx64.efi" ]; then cp "$esp/EFI/debian/mmx64.efi" "$esp/EFI/BOOT/mmx64.efi"; fi
 done
in-target efibootmgr --create --disk "/dev/$second" --part 1 --label 'JARVIS Debian secondary' --loader '\EFI\debian\shimx64.efi'
# Mount the secondary ESP by UUID for future package-update synchronization.
uuid=$(blkid -s UUID -o value "/dev/${second}p1")
printf 'UUID=%s /boot/efi-secondary vfat defaults,nofail,umask=0077 0 1\n' "$uuid" >> /target/etc/fstab
in-target mdadm --detail --scan > /target/etc/mdadm/mdadm.conf
in-target update-initramfs -u -k all
sync
