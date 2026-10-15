#!/bin/sh
# Embed this file and authorized_key in installer initrd; never fetch keys over HTTP.
set -eu
test -s /authorized_key
grep -Eq '^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp256) [A-Za-z0-9+/=]+( .*)?$' /authorized_key
install -d -m 700 /target/home/jarvisadmin/.ssh
install -m 600 /authorized_key /target/home/jarvisadmin/.ssh/authorized_keys
in-target chown -R jarvisadmin:jarvisadmin /home/jarvisadmin/.ssh
# Dedicated target only. Required for unattended Ansible become; no host changes.
printf '%s\n' 'jarvisadmin ALL=(ALL:ALL) NOPASSWD: ALL' > /target/etc/sudoers.d/jarvisadmin
chmod 440 /target/etc/sudoers.d/jarvisadmin
in-target visudo -cf /etc/sudoers.d/jarvisadmin
# Unlock account without a usable password hash, retaining SSH public-key access.
in-target usermod -p '*' jarvisadmin
in-target systemctl enable ssh
