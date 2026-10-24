#!/bin/sh
# Dell2 mission14B only; install Debian-packaged driver and toolkit, no inference stack.
set -eu
umask 077
progress() { printf '%s %s\n' "$(date -Iseconds)" "$*" | tee -a /run/jarvis-install-progress.log >/dev/tty1; }
trap 'progress "FAILED NVIDIA/CUDA: inspect /run/jarvis-gpu-install.log; do not reinstall Debian"' EXIT
/bin/sh /guard-physical.sh
[ -e /run/jarvis-install-complete ]
[ ! -e /run/jarvis-gpu-install-started ] || { echo 'STOP: inspect existing package installation before resume'; exit 1; }
[ "$(awk '$2=="/target" {print $1}' /proc/mounts)" = /dev/md0 ]
touch /run/jarvis-gpu-install-started
progress 'gpu RUNNING: installation pilote NVIDIA et toolkit CUDA Debian, sans Ollama/routage'
chroot /target /usr/bin/env DEBIAN_FRONTEND=noninteractive apt-get update
chroot /target /usr/bin/env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nvidia-driver nvidia-smi nvidia-cuda-toolkit mokutil
chroot /target dpkg --audit
chroot /target dkms status
chroot /target update-initramfs -u -k all
mkdir -p /target/var/lib/jarvis/mission14b
chroot /target dpkg-query -W nvidia-driver nvidia-smi nvidia-cuda-toolkit > /target/var/lib/jarvis/mission14b/gpu-packages.txt
# Compilation now; execution only after real installed boot and driver load.
chroot /target /usr/bin/nvcc -O2 /var/lib/jarvis/mission14b/cuda-smoke.cu -o /var/lib/jarvis/mission14b/cuda-smoke
progress 'gpu PREPARED: paquets et test CUDA compiles; pilote/calcul a verifier apres boot'
touch /run/jarvis-gpu-packages-complete
trap - EXIT
