#!/bin/sh
set -eu
work="$1"
mount --rbind / /
mount --bind /boot /boot
mount --bind /run /run
mount --bind "$work" "$work"
mount --bind "$work/grub.d-test" /etc/grub.d
mount --bind "$work/locks" /run/lock/lvm
mount --bind "$work/tmp" /tmp
mount -o remount,bind,ro /
mount -o remount,bind,ro /boot
mount -o remount,bind,ro /run
/usr/sbin/grub-mkconfig -o "$work/grub.cfg-genere"
