#!/bin/sh
# Embedded early_command: NEVER returns to the installer, including on failure.
set -u
stop_forever() { echo "JARVIS: $* - aucun partitionnement autorise"; while :; do sleep 3600; done; }
[ -d /sys/firmware/efi ] || stop_forever 'UEFI absent'
[ "$(cat /sys/class/dmi/id/sys_vendor)" = 'Dell Inc.' ] || stop_forever 'vendor incorrect'
# Load only network-class PCI drivers by kernel modalias; no block-device writes.
for device in /sys/bus/pci/devices/*; do
 case "$(cat "$device/class" 2>/dev/null)" in
  0x02*) modprobe "$(cat "$device/modalias")" 2>/dev/null || :;;
 esac
done
modprobe nvme || stop_forever 'pilote NVMe indisponible'
udevadm trigger --subsystem-match=net 2>/dev/null || :
udevadm settle 2>/dev/null || :
# Use Debian Installer netcfg and its preseeded DHCP settings; no Bbox changes.
netcfg || stop_forever 'DHCP Linux echoue'
/bin/sh /jarvis-collect.sh || stop_forever 'rapport non confirme'
stop_forever 'rapport envoye ; attente de revue humaine sur JARVIS'
