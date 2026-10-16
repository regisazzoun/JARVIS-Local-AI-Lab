#!/bin/sh
# Read-only sysfs/proc discovery. Writes only temporary files in installer RAM.
set -eu
umask 077
BASE='@BASE@'
KEY='@KEY@'
read_file() {
 for f in "$@"; do
  if [ -r "$f" ]; then printf '\n--- %s ---\n' "$f"; cat "$f" 2>/dev/null || :; fi
 done
}
vendor=$(cat /sys/class/dmi/id/sys_vendor 2>/dev/null || :)
product=$(cat /sys/class/dmi/id/product_name 2>/dev/null || :)
case "$vendor:$product" in *Dell*:*5820*) ;; *) echo 'STOP: cible Dell 5820 non identifiee'; exit 1;; esac
# Refuse writing to /tmp if backed by a physical filesystem.
workroot=${JARVIS_REPORT_TMP:-/tmp}
ram=no
while read -r dev point type rest; do
 case "$point" in /|"$workroot") case "$type" in rootfs|tmpfs|ramfs) ram=yes;; *) ram=no;; esac;; esac
done < /proc/mounts
[ "$ram" = yes ] || { echo 'STOP: /tmp non confirme en RAM'; exit 1; }
work=$(mktemp -d "$workroot/jarvis-discovery.XXXXXX")
report=$work/report.txt
{
 echo 'JARVIS DISCOVERY V1 - READ ONLY'
 read_file /proc/version /proc/cmdline
 echo '\n[DMI]'
 for n in sys_vendor product_name product_version product_uuid product_serial board_vendor board_name board_version bios_vendor bios_version bios_date; do read_file "/sys/class/dmi/id/$n"; done
 echo '\n[CPU / RAM]'
 read_file /proc/cpuinfo /proc/meminfo
 echo '\n[PCI]'
 for d in /sys/bus/pci/devices/*; do
  [ -d "$d" ] || continue
  printf '\nPCI %s\n' "${d##*/}"
  read_file "$d/vendor" "$d/device" "$d/class" "$d/subsystem_vendor" "$d/subsystem_device" "$d/numa_node"
  if [ -L "$d/driver" ]; then readlink "$d/driver" || :; fi
 done
 echo '\n[NVME CONTROLLERS]'
 for d in /sys/class/nvme/nvme*; do
  [ -d "$d" ] || continue
  read_file "$d/model" "$d/serial" "$d/firmware_rev" "$d/state" "$d/transport" "$d/address"
 done
 echo '\n[BLOCK DEVICES / PARTITIONS]'
 read_file /proc/partitions /proc/mounts /proc/swaps
 for d in /sys/class/block/*; do
  [ -d "$d" ] || continue
  printf '\nBLOCK %s (size/start units: 512-byte sectors)\n' "${d##*/}"
  read_file "$d/size" "$d/start" "$d/partition" "$d/ro" "$d/device/model" "$d/device/serial" "$d/queue/logical_block_size" "$d/queue/physical_block_size"
 done
 echo '\n[UEFI]'
 if [ -d /sys/firmware/efi ]; then echo UEFI_PRESENT; else echo UEFI_NOT_OBSERVED; fi
 echo '\n[RAID - active kernel state only; no assembly or metadata scan]'
 read_file /proc/mdstat
 for d in /sys/class/block/md*/md; do
  [ -d "$d" ] || continue
  read_file "$d/level" "$d/array_state" "$d/raid_disks" "$d/degraded" "$d/sync_action"
 done
 echo '\n[NETWORK]'
 for d in /sys/class/net/*; do
  [ -d "$d" ] || continue
  printf '\nNET %s\n' "${d##*/}"
  read_file "$d/address" "$d/operstate" "$d/carrier" "$d/mtu"
 done
 if command -v ip >/dev/null 2>&1; then ip address show || :; ip route show || :; fi
 read_file /proc/net/route /proc/net/ipv6_route /proc/net/dev
 echo '\n[AVAILABLE NETWORK TOOLS]'
 for tool in wget nc curl ip; do command -v "$tool" || :; done
 echo 'JARVIS_IDENTITY_BEGIN'
 printf 'vendor\t%s\n' "$vendor"
 printf 'product\t%s\n' "$product"
 printf 'uuid\t%s\n' "$(cat /sys/class/dmi/id/product_uuid)"
 if [ -d /sys/firmware/efi ]; then printf 'uefi\ttrue\n'; else printf 'uefi\tfalse\n'; fi
 for disk in /sys/block/*; do
  n=${disk##*/}
  case "$n" in loop*|ram*|sr*|md*|dm-*) continue;; esac
  serial=$(cat "$disk/device/serial" 2>/dev/null | sed 's/^ *//;s/ *$//' || :)
  model=$(cat "$disk/device/model" 2>/dev/null | sed 's/^ *//;s/ *$//' || :)
  printf 'disk\t/dev/%s\t%s\t%s\t%s\t%s\n' "$n" "$serial" "$model" "$(cat "$disk/size")" "$(cat "$disk/ro")"
 done
 echo 'JARVIS_IDENTITY_END'
 if [ -r /etc/ssh/ssh_host_ed25519_key.pub ]; then
  echo JARVIS_HOSTKEY_BEGIN
  cat /etc/ssh/ssh_host_ed25519_key.pub
  echo JARVIS_HOSTKEY_END
 fi
 echo 'JARVIS DISCOVERY END' 
} > "$report"
echo "Rapport RAM : $report"
if command -v wget >/dev/null 2>&1 && wget --help 2>&1 | grep -q -- '--post-file'; then
 if wget --no-proxy -T 30 -t 1 -q -O "$work/ack" --post-file="$report" "$BASE/$KEY/report"; then
  if grep -q '^RECEIVED$' "$work/ack"; then echo 'Rapport recu par JARVIS'; exit 0; fi
 fi
fi
if command -v nc >/dev/null 2>&1; then
 size=$(wc -c < "$report")
 { printf 'POST /%s/report HTTP/1.0\r\nHost: @HOST@\r\nContent-Length: %s\r\nContent-Type: text/plain\r\n\r\n' "$KEY" "$size"; cat "$report"; } | nc -w 30 @HOST@ @PORT@ > "$work/ack" || :
 if grep -q '^RECEIVED$' "$work/ack"; then echo 'Rapport recu par JARVIS (nc)'; exit 0; fi
fi
echo "Envoi non confirme ; rapport conserve en RAM : $report"
exit 1
