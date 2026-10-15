#!/bin/bash
set -euo pipefail
prep=/home/adminjarvis/JARVIS/rapports/phaseC2-preparation
cd "$prep/staged"
sha256sum -c SHA256SUMS
sudo -n /usr/sbin/sshd -t
ip -4 -br address show enp4s0
sudo -n ss -lntp '( sport = :22 )'
test ! -e '/usr/lib/firmware/brcm/brcmfmac4364b2-pcie.apple,lanai.bin'
test ! -e '/usr/lib/firmware/brcm/brcmfmac4364b2-pcie.apple,lanai-HRPN-u.txt'
test ! -e '/usr/lib/firmware/brcm/brcmfmac4364b2-pcie.apple,lanai.clm_blob'
test ! -e '/usr/lib/firmware/brcm/brcmfmac4364b2-pcie.apple,lanai.txcap_blob'
sudo -n install -o root -g root -m 644 'brcmfmac4364b2-pcie.apple,lanai.bin' '/usr/lib/firmware/brcm/brcmfmac4364b2-pcie.apple,lanai.bin'
sudo -n install -o root -g root -m 644 'brcmfmac4364b2-pcie.apple,lanai-HRPN-u.txt' '/usr/lib/firmware/brcm/brcmfmac4364b2-pcie.apple,lanai-HRPN-u.txt'
sudo -n install -o root -g root -m 644 'brcmfmac4364b2-pcie.apple,lanai.clm_blob' '/usr/lib/firmware/brcm/brcmfmac4364b2-pcie.apple,lanai.clm_blob'
sudo -n install -o root -g root -m 644 'brcmfmac4364b2-pcie.apple,lanai.txcap_blob' '/usr/lib/firmware/brcm/brcmfmac4364b2-pcie.apple,lanai.txcap_blob'
sudo -n /usr/sbin/modprobe -r brcmfmac
sudo -n /usr/sbin/modprobe brcmfmac
nmcli device status
ip -4 -br address show enp4s0
sudo -n ss -lntp '( sport = :22 )'
