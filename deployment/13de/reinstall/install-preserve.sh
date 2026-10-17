#!/bin/sh
# Run only through the pinned installer SSH session after exact identity checks.
# Reuses approved members, never invokes partman, wipefs, mdadm --create or sgdisk.
set -eu
umask 077
export DEBIAN_FRONTEND=noninteractive
progress() { printf '%s %s\n' "$(date -Iseconds)" "$*" | tee -a /run/jarvis-install-progress.log >/dev/tty1; }
trap 'progress "FAILED installation: inspect /run/jarvis-install.log; SSH supervision preserved"' EXIT
[ ! -e /run/jarvis-reinstall-started ] || { echo 'STOP: already started; inspect before resume'; exit 1; }
/bin/sh /guard-physical.sh
set -- $(awk -F '\t' '$1=="disk"{print "/dev/"$2}' /approved.tsv)
[ "$#" = 2 ];a=$1;b=$2
# GPT/ESP/member checks precede any filesystem write.
for disk in "$a" "$b"; do
 [ "$(blkid -p -s PTTYPE -o value "$disk")" = gpt ]
 [ "$(blkid -p -s TYPE -o value "${disk}p1")" = vfat ]
 [ "$(blkid -p -s PART_ENTRY_TYPE -o value "${disk}p1")" = c12a7328-f81f-11d2-ba4b-00a0c93ec93b ]
 [ "$(blkid -p -s TYPE -o value "${disk}p2")" = linux_raid_member ]
done
progress 'storage RUNNING: preservation GPT/ESP et assemblage du miroir existant'
if ! ls /sys/block/md*/md/level >/dev/null 2>&1; then mdadm --assemble /dev/md0 "${a}p2" "${b}p2";fi
set -- /sys/block/md*/md
[ "$#" = 1 ];mdsys=$1;mdname=${mdsys%/md};mdname=${mdname##*/};md=/dev/$mdname
[ "$(cat "$mdsys/level")" = raid1 ];[ "$(cat "$mdsys/raid_disks")" = 2 ];[ "$(cat "$mdsys/degraded")" = 0 ]
[ "$(cat "$mdsys/sync_action")" = idle ] || { progress 'storage BLOCKED: miroir non synchronise; aucune recreation';exit 1; }
set -- /sys/block/"$mdname"/slaves/*
[ "$#" = 2 ]
for slave in "$@"; do case "${slave##*/}" in "${a##*/}p2"|"${b##*/}p2") :;; *) exit 1;;esac;done
! grep -q "^$md " /proc/mounts
mdadm --detail "$md" > /run/jarvis-storage-before.txt
blkid >> /run/jarvis-storage-before.txt
[ "$(blkid -p -s TYPE -o value "$md")" = ext4 ]
touch /run/jarvis-reinstall-started
progress 'storage VALIDATED: miroir sain conserve; formatage rapide ext4 de la racine uniquement'
mkfs.ext4 -F -L jarvis-root -E lazy_itable_init=1,lazy_journal_init=1 "$md"
mkdir -p /target;mount "$md" /target
progress 'debian RUNNING: installation Debian 13 neuve avec debootstrap'
/usr/sbin/debootstrap --arch=amd64 --variant=minbase --keyring=/usr/share/keyrings/debian-archive-keyring.gpg trixie /target http://deb.debian.org/debian
for fs in dev proc sys;do mount --rbind /$fs /target/$fs;mount --make-rslave /target/$fs;done
mkdir -p /target/run;mount -t tmpfs tmpfs /target/run
cp /etc/resolv.conf /target/etc/resolv.conf
cat > /target/usr/sbin/policy-rc.d <<'EOF'
#!/bin/sh
exit 101
EOF
chmod 755 /target/usr/sbin/policy-rc.d
cat > /target/etc/apt/sources.list <<'EOF'
deb http://deb.debian.org/debian trixie main contrib non-free non-free-firmware
deb http://deb.debian.org/debian trixie-updates main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security trixie-security main contrib non-free non-free-firmware
EOF
mkdir -p /target/boot/efi /target/boot/efi-secondary /target/etc/mdadm
mount "${a}p1" /target/boot/efi;mount "${b}p1" /target/boot/efi-secondary
mdadm --detail --scan > /target/etc/mdadm/mdadm.conf
chroot /target apt-get update
chroot /target apt-get install -y linux-image-amd64 linux-headers-amd64 openssh-server sudo python3 ca-certificates mdadm nvme-cli smartmontools efibootmgr rsync wget curl pciutils dmidecode grub-efi-amd64-signed shim-signed locales console-setup keyboard-configuration systemd-sysv systemd-timesyncd
printf 'jarvis-dell\n' > /target/etc/hostname
printf '127.0.0.1 localhost\n127.0.1.1 jarvis-dell\n' > /target/etc/hosts
printf 'fr_FR.UTF-8 UTF-8\n' > /target/etc/locale.gen
chroot /target locale-gen
printf 'LANG=fr_FR.UTF-8\n' > /target/etc/default/locale
cat > /target/etc/default/keyboard <<'EOF'
XKBMODEL="pc105"
XKBLAYOUT="fr"
XKBVARIANT=""
XKBOPTIONS=""
BACKSPACE="guess"
EOF
printf 'KEYMAP=fr\n' > /target/etc/vconsole.conf
chroot /target setupcon --save-only || :
ln -sf /usr/share/zoneinfo/Europe/Paris /target/etc/localtime
progress 'accounts RUNNING: deux comptes, mot de passe utilisateur et cle JARVIS'
for user in adminjarvis jarvis-bootstrap;do
 chroot /target useradd -m -s /bin/bash "$user"
 printf '%s:%s\n' "$user" "$(cat /jarvis/root.hash)" | chroot /target chpasswd -e
 printf '%s ALL=(ALL:ALL) NOPASSWD: ALL\n' "$user" > /target/etc/sudoers.d/"$user"
 chmod 440 /target/etc/sudoers.d/"$user"
 mkdir -p /target/home/"$user"/.ssh
 cp /jarvis/authorized_keys /target/home/"$user"/.ssh/authorized_keys
 chroot /target chown -R "$user:$user" /home/"$user"/.ssh
 chmod 700 /target/home/"$user"/.ssh;chmod 600 /target/home/"$user"/.ssh/authorized_keys
 chroot /target visudo -cf /etc/sudoers.d/"$user"
done
cp /jarvis/target_host_key /target/etc/ssh/ssh_host_ed25519_key
cp /jarvis/target_host_key.pub /target/etc/ssh/ssh_host_ed25519_key.pub
chmod 600 /target/etc/ssh/ssh_host_ed25519_key
cat > /target/etc/ssh/sshd_config.d/00-jarvis.conf <<'EOF'
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication yes
KbdInteractiveAuthentication no
AllowUsers adminjarvis jarvis-bootstrap
EOF
mkdir -p /target/run/sshd
chroot /target /usr/sbin/sshd -t
mkdir -p /target/etc/systemd/network
cat > /target/etc/systemd/network/20-wired.network <<'EOF'
[Match]
Type=ether
[Network]
DHCP=yes
EOF
chroot /target systemctl enable systemd-networkd ssh systemd-timesyncd
mkdir -p /target/boot/efi /target/boot/efi-secondary /target/etc/mdadm
rootuuid=$(blkid -s UUID -o value "$md")
printf 'UUID=%s / ext4 defaults 0 1\n' "$rootuuid" > /target/etc/fstab
printf 'UUID=%s /boot/efi vfat defaults,nofail,umask=0077 0 2\n' "$(blkid -s UUID -o value "${a}p1")" >> /target/etc/fstab
printf 'UUID=%s /boot/efi-secondary vfat defaults,nofail,umask=0077 0 2\n' "$(blkid -s UUID -o value "${b}p1")" >> /target/etc/fstab
mdadm --detail --scan > /target/etc/mdadm/mdadm.conf
printf 'GRUB_CMDLINE_LINUX_DEFAULT="nomodeset"\nGRUB_TERMINAL_OUTPUT=console\n' > /target/etc/default/grub.d/90-jarvis.cfg
chroot /target update-initramfs -u -k all
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
