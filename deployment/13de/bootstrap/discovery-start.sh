#!/bin/sh
# Embedded early_command: NEVER returns to the installer, including on failure.
set -u
# preseed commands run under log-output; also mirror status to the physical VT.
exec >/dev/tty1 2>&1
printf '\033[2J\033[H'
echo 'JARVIS DISCOVERY: debut (lecture seule)'
stop_forever() { echo "JARVIS: $* - aucun partitionnement autorise"; while :; do sleep 3600; done; }
[ -d /sys/firmware/efi ] || stop_forever 'UEFI absent'
[ "$(cat /sys/class/dmi/id/sys_vendor)" = 'Dell Inc.' ] || stop_forever 'vendor incorrect'
# Load only network-class PCI drivers by kernel modalias; no block-device writes.
for device in /sys/bus/pci/devices/*; do
 case "$(cat "$device/class" 2>/dev/null)" in
  0x02*) modprobe "$(cat "$device/modalias")" 2>/dev/null || :;;
 esac
done
echo 'JARVIS DISCOVERY: chargement pilotes NVMe verifies'
for module in nvme-auth nvme-core nvme; do
 name=$(printf '%s' "$module" | tr '-' '_')
 if [ ! -d "/sys/module/$name" ]; then
  insmod "/jarvis-drivers/$module.ko" || stop_forever "pilote $module indisponible"
 fi
done
udevadm trigger --subsystem-match=net 2>/dev/null || :
udevadm settle 2>/dev/null || :
# Use the existing installer DHCP client; no Bbox changes.
echo 'JARVIS DISCOVERY: selection Ethernet et DHCP BusyBox'
for interface in /sys/class/net/*; do
 [ "${interface##*/}" = lo ] && continue
 ip link set "${interface##*/}" up 2>/dev/null || :
done
selected=
for attempt in 1 2 3 4 5 6 7 8 9 10; do
 selected=
 for interface in /sys/class/net/*; do
  [ "${interface##*/}" = lo ] && continue
  if [ "$(cat "$interface/carrier" 2>/dev/null)" = 1 ]; then
   [ -z "$selected" ] || stop_forever 'plusieurs interfaces actives'
   selected=${interface##*/}
  fi
 done
 [ -z "$selected" ] || break
 sleep 1
done
[ -n "$selected" ] || stop_forever 'aucun lien Ethernet'
# Avoid invoking cdebconf/netcfg recursively from preseed/early_command.
# This existing Debian RAM script applies the Bbox lease, without touching disks.
udhcpc -n -q -t 5 -T 3 -i "$selected" -s /etc/udhcpc/default.script || stop_forever 'DHCP Linux echoue'
echo 'JARVIS DISCOVERY: collecte et transmission'
/bin/sh /jarvis-collect.sh || stop_forever 'rapport non confirme'
stop_forever 'rapport envoye ; attente de revue humaine sur JARVIS'
