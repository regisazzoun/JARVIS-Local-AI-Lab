#!/bin/sh
# Resume only the failed finalization; no partitioning, formatting, base installation or user creation.
set -eu
progress() { printf '%s %s\n' "$(date -Iseconds)" "$*" | tee -a /run/jarvis-install-progress.log >/dev/tty1; }
trap 'progress "FAILED finalization: inspect /run/jarvis-finalize.log; SSH retained"' EXIT
/bin/sh /guard-physical.sh
[ -e /run/jarvis-reinstall-started ]
[ ! -e /run/jarvis-install-complete ] || { echo ALREADY_COMPLETE; trap - EXIT; exit 0; }
md=/dev/md0;mdname=md0;mdsys=/sys/block/md0/md
[ "$(awk '$2=="/target" {print $1}' /proc/mounts)" = "$md" ]
[ "$(cat "$mdsys/level")" = raid1 ]; [ "$(cat "$mdsys/degraded")" = 0 ]
chroot /target dpkg-query -W base-files openssh-server linux-image-amd64
chroot /target id adminjarvis
set -- $(awk -F '\t' '$1=="disk"{print "/dev/"$2}' /approved.tsv); [ "$#" = 2 ];a=$1;b=$2
progress 'finalization RUNNING: reprise apres ajout fichiers de suivi; aucune recreation du stockage'
mkdir -p /target/usr/local/bin
cp /jarvis/progress-viewer.sh /target/usr/local/bin/jarvis-progress
cp /jarvis/progress-console.service /target/etc/systemd/system/jarvis-progress-console.service
chmod 755 /target/usr/local/bin/jarvis-progress
chmod 644 /target/etc/systemd/system/jarvis-progress-console.service
chroot /target systemctl enable jarvis-progress-console.service
mkdir -p /target/boot/grub /target/boot/efi /target/boot/efi-secondary /target/etc/mdadm
rootuuid=$(blkid -s UUID -o value "$md")
printf 'UUID=%s / ext4 defaults 0 1\n' "$rootuuid" > /target/etc/fstab
printf 'UUID=%s /boot/efi vfat defaults,nofail,umask=0077 0 2\n' "$(blkid -s UUID -o value "${a}p1")" >> /target/etc/fstab
printf 'UUID=%s /boot/efi-secondary vfat defaults,nofail,umask=0077 0 2\n' "$(blkid -s UUID -o value "${b}p1")" >> /target/etc/fstab
mdadm --detail --scan > /target/etc/mdadm/mdadm.conf
printf 'GRUB_CMDLINE_LINUX_DEFAULT="nomodeset"\nGRUB_TERMINAL_OUTPUT=console\n' > /target/etc/default/grub.d/90-jarvis.cfg
printf 'vmd\nnvme\nraid1\next4\n' >> /target/etc/initramfs-tools/modules
chroot /target update-initramfs -u -k all
chroot /target grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=debian --uefi-secure-boot --no-nvram
chroot /target update-grub
# Debian signed EFI binaries; no unsigned replacement under Secure Boot.
mkdir -p /target/boot/efi/EFI/debian /target/boot/efi/EFI/BOOT
cp /target/usr/lib/shim/shimx64.efi.signed /target/boot/efi/EFI/debian/shimx64.efi
cp /target/usr/lib/grub/x86_64-efi-signed/grubx64.efi.signed /target/boot/efi/EFI/debian/grubx64.efi
printf 'search --no-floppy --fs-uuid --set=root %s\nset prefix=($root)/boot/grub\nconfigfile $prefix/grub.cfg\n' "$rootuuid" > /target/boot/efi/EFI/debian/grub.cfg
cp /target/boot/efi/EFI/debian/shimx64.efi /target/boot/efi/EFI/BOOT/BOOTX64.EFI
cp /target/boot/efi/EFI/debian/grubx64.efi /target/boot/efi/EFI/BOOT/grubx64.efi
cp /target/boot/efi/EFI/debian/grub.cfg /target/boot/efi/EFI/BOOT/grub.cfg
chroot /target rsync -a /boot/efi/EFI/ /boot/efi-secondary/EFI/
chroot /target efibootmgr --create --disk "$a" --part 1 --label 'JARVIS Debian' --loader '\EFI\debian\shimx64.efi'
chroot /target efibootmgr --create --disk "$b" --part 1 --label 'JARVIS Debian secondary' --loader '\EFI\debian\shimx64.efi'
for name in shimx64.efi grubx64.efi grub.cfg;do cmp /target/boot/efi/EFI/debian/"$name" /target/boot/efi-secondary/EFI/debian/"$name";done
chroot /target /usr/sbin/sshd -t
[ "$(cat "$mdsys/degraded")" = 0 ]
rm /target/usr/sbin/policy-rc.d
mkdir -p /target/var/lib/jarvis
cp /run/jarvis-storage-before.txt /target/var/lib/jarvis/storage-before.txt
progress 'debian VALIDATED: installation neuve terminee, ESP coherentes, comptes et SSH configures; authentifications a verifier apres reboot'
sync
trap - EXIT
# Controller retrieves evidence and explicitly reboots this same scoped target.
touch /run/jarvis-install-complete
