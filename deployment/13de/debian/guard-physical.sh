#!/bin/sh
# Embedded in initrd alongside approved.tsv, NEVER downloaded over unauthenticated HTTP.
# Run before partman and again before late_command. All mismatches stop the installer.
set -eu
stop() { echo "STOP 13D-E: $*" >&2; exit 1; }
test -d /sys/firmware/efi || stop UEFI
test "$(cat /sys/class/dmi/id/sys_vendor)" = 'Dell Inc.' || stop vendor
actual_product=$(cat /sys/class/dmi/id/product_name)
case "$actual_product" in 'Precision 5820 Tower'|'Precision 5820 Tower X-Series') ;; *) stop product ;; esac
test -s /approved.tsv || stop manifest
# Authorization artifact is deliberately absent from repository and default builds.
test -s /approved-erase.sha256 || stop 'explicit erase approval absent'
test "$(cat /approved-erase.sha256)" = "$(sha256sum /approved.tsv | cut -d ' ' -f1)" || stop approval
count=0
uuids=0
products=0
empty_media=
while IFS="$(printf '\t')" read -r kind a b c d; do
 case "$kind" in
 uuid) uuids=$((uuids+1)); test "$(cat /sys/class/dmi/id/product_uuid)" = "$a" || stop UUID ;;
 product) products=$((products+1)); test "$actual_product" = "$a" || stop product-manifest ;;
 empty-media)
  test "$a" = sda && test "$b" = 'SD/MMC CRW' && test "$c" = 0 || stop empty-media-profile
  test -z "$empty_media" || stop duplicate-empty-media
  if test -d /sys/block/sda; then
   test "$(cat /sys/block/sda/size)" = 0 || stop media-inserted
   test "$(cat /sys/block/sda/device/model | sed 's/^ *//;s/ *$//')" = "$b" || stop reader-changed
  fi
  empty_media=sda ;;
 disk)
  case "$a" in nvme[0-9]*n[0-9]*) ;; *) stop disk-name ;; esac
  test -b "/dev/$a" || stop missing-disk
  test "$(cat /sys/block/"$a"/device/serial | sed 's/^ *//;s/ *$//')" = "$b" || stop serial
  test "$(cat /sys/block/"$a"/device/model | sed 's/^ *//;s/ *$//')" = "$c" || stop model
  test "$(cat /sys/block/"$a"/size)" = "$d" || stop size
  test "$(cat /sys/block/"$a"/ro)" = 0 || stop readonly
  count=$((count+1)) ;;
 *) stop manifest-format ;;
 esac
done < /approved.tsv
test "$uuids" = 1 || stop UUID-count
test "$count" = 2 || stop disk-count
if test "$products" = 0; then test "$actual_product" = 'Precision 5820 Tower' || stop unpinned-product; else test "$products" = 1 || stop product-count; fi
actual=0
for disk in /sys/block/*; do
 case "${disk##*/}" in loop*|ram*|sr*|md*|dm-*) continue ;; esac
 test "${disk##*/}" != "$empty_media" || continue
 actual=$((actual+1))
done
test "$actual" = 2 || stop unexpected-disk
echo '13D-E: identity and scoped erase approval match' >&2
