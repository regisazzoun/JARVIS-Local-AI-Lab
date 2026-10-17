#!/bin/sh
# Run on the identified Dell after SSH validation; existing networkd remains authoritative.
set -eu
export DEBIAN_FRONTEND=noninteractive
[ ! -e /usr/sbin/policy-rc.d ] || { echo 'STOP: existing service-start policy requires inspection';exit 1; }
cat > /usr/sbin/policy-rc.d <<'EOF'
#!/bin/sh
# JARVIS_PLASMA_INSTALL_POLICY
case "$1" in sddm|display-manager) exit 101;; *) exit 0;; esac
EOF
chmod 755 /usr/sbin/policy-rc.d
cleanup() { if grep -q JARVIS_PLASMA_INSTALL_POLICY /usr/sbin/policy-rc.d 2>/dev/null;then rm /usr/sbin/policy-rc.d;fi; }
trap cleanup EXIT
printf '%s\n' 'sddm shared/default-x-display-manager select sddm' | debconf-set-selections
apt-get install -y --no-install-recommends kde-plasma-desktop sddm xserver-xorg kwin-x11 konsole dolphin dbus-x11 xserver-xorg-input-libinput
mkdir -p /etc/sddm.conf.d
chmod 755 /etc/sddm.conf.d
cat > /etc/sddm.conf.d/10-jarvis.conf <<'EOF'
[General]
DisplayServer=x11
[Users]
RememberLastUser=true
RememberLastSession=true
EOF
chmod 644 /etc/sddm.conf.d/10-jarvis.conf
# Preserve password authentication: no autologin is configured.
printf '/usr/bin/sddm\n' > /etc/X11/default-display-manager
chmod 644 /etc/X11/default-display-manager
systemctl enable sddm.service
systemctl set-default graphical.target
# SDDM records the chosen session; select the installed X11 Plasma entry for first use.
session=$(find /usr/share/xsessions -maxdepth 1 -name '*plasma*.desktop' -print | head -1)
[ -n "$session" ]
install -d -o sddm -g sddm -m 750 /var/lib/sddm
printf '[Last]\nUser=adminjarvis\nSession=%s\n' "$session" > /var/lib/sddm/state.conf
chown sddm:sddm /var/lib/sddm/state.conf
chmod 600 /var/lib/sddm/state.conf
# Keep the French map active on physical and graphical consoles.
setupcon --force --keyboard-only
mkdir -p /etc/X11/xorg.conf.d
cat > /etc/X11/xorg.conf.d/00-keyboard.conf <<'EOF'
Section "InputClass"
    Identifier "JARVIS French keyboard"
    MatchIsKeyboard "on"
    Option "XkbModel" "pc105"
    Option "XkbLayout" "fr"
EndSection
EOF
chmod 644 /etc/X11/xorg.conf.d/00-keyboard.conf
dpkg-query -W kde-plasma-desktop plasma-desktop plasma-workspace kwin-x11 sddm konsole dolphin
systemctl is-enabled sddm.service
test -s "$session"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
systemctl is-active ssh jarvis-ollama
printf 'JARVIS_PLASMA_INSTALLED_READY_FOR_REBOOT\n'
