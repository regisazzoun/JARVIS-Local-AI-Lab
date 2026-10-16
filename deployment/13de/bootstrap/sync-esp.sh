#!/bin/sh
# Installed Dell only, called after package upgrades. Never formats or repartitions.
set -eu
[ "$(cat /sys/class/dmi/id/sys_vendor)" = 'Dell Inc.' ]
[ -d /sys/firmware/efi ]
mountpoint -q /boot/efi
mountpoint -q /boot/efi-secondary || mount /boot/efi-secondary
expected=$(awk '$2=="/boot/efi-secondary" {print $1}' /etc/fstab)
case "$expected" in UUID=*) ;; *) exit 1;; esac
[ "$(findmnt -n -o UUID /boot/efi-secondary)" = "${expected#UUID=}" ]
[ "$(findmnt -n -o UUID /boot/efi)" != "${expected#UUID=}" ]
test -f /boot/efi/EFI/debian/shimx64.efi
test -f /boot/efi/EFI/debian/grubx64.efi
cp -a /boot/efi/EFI/debian/. /boot/efi-secondary/EFI/debian/
for esp in /boot/efi /boot/efi-secondary; do
 mkdir -p "$esp/EFI/BOOT"
 cp "$esp/EFI/debian/shimx64.efi" "$esp/EFI/BOOT/BOOTX64.EFI"
 cp "$esp/EFI/debian/grubx64.efi" "$esp/EFI/BOOT/grubx64.efi"
 cp "$esp/EFI/debian/grub.cfg" "$esp/EFI/BOOT/grub.cfg"
 if [ -f "$esp/EFI/debian/mmx64.efi" ]; then cp "$esp/EFI/debian/mmx64.efi" "$esp/EFI/BOOT/mmx64.efi"; fi
done
sync
