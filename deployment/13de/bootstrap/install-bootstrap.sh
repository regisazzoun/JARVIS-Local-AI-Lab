#!/bin/sh
# late_command inside Debian Installer ONLY, never run on JARVIS.
set -eu
command -v in-target >/dev/null
/bin/sh /guard-physical.sh
test -d /target/etc
test -s /bootstrap-expires
in-target id jarvis-bootstrap >/dev/null
# Password hash was preseeded; no plaintext password is included in the initrd.
cat > /target/etc/sudoers.d/jarvis-bootstrap <<'EOF'
jarvis-bootstrap ALL=(ALL:ALL) NOPASSWD: ALL
EOF
chmod 440 /target/etc/sudoers.d/jarvis-bootstrap
in-target visudo -cf /etc/sudoers.d/jarvis-bootstrap
mkdir -p /target/etc/ssh/sshd_config.d
cat > /target/etc/ssh/sshd_config.d/00-jarvis-bootstrap.conf <<'EOF'
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
AllowUsers jarvis-bootstrap@192.168.1.99 jarvisadmin@192.168.1.99
Match User jarvis-bootstrap Address 192.168.1.99
    PasswordAuthentication yes
Match all
EOF
in-target ssh-keygen -A
in-target /usr/sbin/sshd -t
mkdir -p /target/usr/local/sbin
cat > /target/usr/local/sbin/jarvis-revoke-bootstrap <<'EOF'
#!/bin/sh
set -eu
test -s /var/lib/jarvis/permanent-key-verified
usermod -L -e 1 -s /usr/sbin/nologin jarvis-bootstrap
rm -f /etc/sudoers.d/jarvis-bootstrap
# Remove the per-user password exception; global PasswordAuthentication stays no.
sed -i '/^Match User jarvis-bootstrap/,$d' /etc/ssh/sshd_config.d/00-jarvis-bootstrap.conf
/usr/sbin/sshd -t
systemctl reload ssh
systemctl disable --now jarvis-bootstrap-expire.timer
EOF
chmod 700 /target/usr/local/sbin/jarvis-revoke-bootstrap
cat > /target/etc/systemd/system/jarvis-bootstrap-expire.service <<'EOF'
[Unit]
Description=Revoke deployment bootstrap credentials
[Service]
Type=oneshot
ExecStart=/bin/sh -c 'if test -s /var/lib/jarvis/permanent-key-verified; then exec /usr/local/sbin/jarvis-revoke-bootstrap; else logger -t jarvis-bootstrap "24h review required; account retained until independent key proof"; fi' 
EOF
{
 printf '[Unit]\nDescription=Bound bootstrap credential lifetime\n[Timer]\nOnCalendar=%s\nPersistent=true\n[Install]\nWantedBy=timers.target\n' "$(cat /bootstrap-expires)"
} > /target/etc/systemd/system/jarvis-bootstrap-expire.timer
in-target systemctl enable ssh jarvis-bootstrap-expire.timer
mkdir -p /target/usr/local/lib/jarvis /target/etc/jarvis
cp /verify-storage.py /target/usr/local/lib/jarvis/verify-storage.py
cp /approved.json /target/etc/jarvis/approved.json
chmod 600 /target/etc/jarvis/approved.json
cp /sync-esp.sh /target/usr/local/sbin/jarvis-sync-esp
chmod 700 /target/usr/local/sbin/jarvis-sync-esp
printf '%s\n' 'DPkg::Post-Invoke { "/usr/local/sbin/jarvis-sync-esp"; };' > /target/etc/apt/apt.conf.d/99jarvis-esp
cp /jarvis-collect.sh /target/usr/local/lib/jarvis/collect.sh
chmod 700 /target/usr/local/lib/jarvis/collect.sh
cat > /target/etc/systemd/system/jarvis-install-report.service <<'EOF'
[Unit]
Description=Report installed Dell identity and SSH public host key
Wants=network-online.target
After=network-online.target ssh.service
ConditionPathExists=!/var/lib/jarvis/install-report-sent
[Service]
Type=oneshot
Environment=JARVIS_REPORT_TMP=/run
ExecStart=/bin/sh /usr/local/lib/jarvis/collect.sh
ExecStartPost=/usr/bin/mkdir -p /var/lib/jarvis
ExecStartPost=/usr/bin/touch /var/lib/jarvis/install-report-sent
ExecStartPost=/usr/bin/rm -f /usr/local/lib/jarvis/collect.sh
Restart=on-failure
RestartSec=60
[Install]
WantedBy=multi-user.target
EOF
in-target systemctl enable jarvis-install-report.service
# Finalize both ESPs and validate storage BEFORE reboot may be enabled.
/bin/sh /finalize-efi.sh
# Prevent accidental interactive continuation after a late-stage failure.
