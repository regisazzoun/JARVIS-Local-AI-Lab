#!/usr/bin/env bash
# Lancer avec bash depuis Konsole, comme utilisateur habituel, jamais avec sudo bash.
# Par défaut : diagnostics et simulations seulement.
set -Eeuo pipefail
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export LC_ALL=C
umask 077
MODE=${1:---diagnostic}
KEY_FILE=${2:-}
WORK_DIR=''
SSH_MASKED=0
die() { printf 'ARRET : %s\n' "$*" >&2; exit 1; }
on_error() {
  local rc=$?
  printf 'ERREUR ligne %s, code %s. Arrêt sans poursuite ni redémarrage.\n' "$1" "$rc" >&2
  if (( SSH_MASKED )); then
    printf 'SSH reste masqué et arrêté. Examiner le journal et la configuration avant toute activation.\n' >&2
  fi
  [[ -z $WORK_DIR ]] || printf 'Journal et sauvegardes : %s\n' "$WORK_DIR" >&2
  exit "$rc"
}
trap 'on_error "$LINENO"' ERR
trap 'printf "Interruption : aucune poursuite automatique.\n" >&2; exit 130' INT TERM
confirm() {
  local answer
  read -r -p "$1 — saisir OUI : " answer
  [[ $answer == OUI ]] || die 'Accord non donné.'
}
case "$MODE" in
  --help) printf 'Usage : bash %s --diagnostic\n        bash %s --appliquer /chemin/cle_client.pub\n' "$0" "$0"; exit 0 ;;
  --diagnostic|--appliquer) ;;
  *) die 'Mode inconnu. Utiliser --help.' ;;
esac
(( EUID != 0 )) || die 'Utiliser votre compte habituel, sans sudo bash.'
[[ $(awk '/^NoNewPrivs:/{print $2}' /proc/self/status) == 0 ]] || die 'Session restreinte : exécuter depuis Konsole sur Debian. Aucun contournement.'
# os-release est un fichier système de confiance, pas une entrée fournie au script.
. /etc/os-release
[[ $ID == debian && $VERSION_ID == 13 && $VERSION_CODENAME == trixie ]] || die 'Debian 13 trixie requis.'
[[ $(dpkg --print-architecture) == amd64 ]] || die 'Architecture amd64 requise.'
for tool in sudo ip curl getent systemctl apt-get dpkg-query findmnt ssh-keygen sha256sum grub-script-check; do
  command -v "$tool" >/dev/null || die "Outil préalable absent : $tool. Examiner avant installation."
done
sudo -v
[[ $(sudo id -u) == 0 ]] || die 'Sudo ne fournit pas les droits root attendus.'
sudo -l
systemctl show --property=Version --value >/dev/null
WORK_DIR=$(mktemp -d "${HOME}/jarvis-02B-XXXXXXXX")
exec > >(tee -a "$WORK_DIR/execution.log") 2>&1
printf 'Travail : %s\nMode : %s\nCompte : %s\n' "$WORK_DIR" "$MODE" "$(id -un)"
uname -a
ip -br address
ip route
ip -6 route
cat /etc/resolv.conf
[[ $(cat /sys/class/net/enp4s0/carrier) == 1 ]] || die 'Pas de porteuse Ethernet enp4s0.'
cat /sys/class/net/enp4s0/speed
for host in deb.debian.org security.debian.org; do
  getent ahosts "$host"
  curl --fail --head --connect-timeout 10 --max-time 30 "https://${host}/debian$( [[ $host == security.debian.org ]] && printf '%s' '-security' || true )/dists/trixie$( [[ $host == security.debian.org ]] && printf '%s' '-security' || true )/InRelease"
done
sudo journalctl -b -k -p warning --no-pager
systemctl --failed --no-pager
for mountpoint in / /boot /boot/efi; do
  findmnt --mountpoint "$mountpoint"
done
df -hT / /boot /boot/efi
[[ -d /sys/firmware/efi ]] || die 'Démarrage EFI requis.'
sudo ls -l /boot/efi/EFI/debian
sudo test -s /boot/efi/EFI/debian/shimx64.efi
sudo test -s /boot/efi/EFI/debian/grubx64.efi
sudo grub-script-check /boot/grub/grub.cfg
sudo cp /boot/grub/grub.cfg "$WORK_DIR/grub.cfg.before"
sudo chown "$(id -u):$(id -g)" "$WORK_DIR/grub.cfg.before"
audit=$(sudo dpkg --audit)
printf '%s\n' "$audit"
[[ -z $audit ]] || die 'dpkg --audit signale une anomalie.'
mapfile -t KERNEL_PACKAGES < <(dpkg-query -W -f='${binary:Package} ${db:Status-Abbrev}\n' 'linux-image-[0-9]*' | awk '$2 == "ii" {print $1}')
(( ${#KERNEL_PACKAGES[@]} > 0 )) || die 'Aucun paquet de noyau versionné identifié.'
for package in "${KERNEL_PACKAGES[@]}"; do
  version=${package#linux-image-}; version=${version%%:*}
  sudo test -s "/boot/vmlinuz-$version"
  sudo test -s "/boot/initrd.img-$version"
  sudo sha256sum "/boot/vmlinuz-$version" >> "$WORK_DIR/kernels.sha256"
done
printf 'Noyaux à conserver : %s\n' "${KERNEL_PACKAGES[*]}"
sudo apt-get -s --no-remove upgrade | tee "$WORK_DIR/upgrade.cached.txt"
sudo apt-get -s --no-remove install openssh-server dkms linux-headers-amd64 nvme-cli | tee "$WORK_DIR/install.cached.txt"
if [[ $MODE == --diagnostic ]]; then
  printf 'Diagnostic terminé. Aucun paquet, index APT ou fichier de configuration modifié.\n'
  printf 'Des journaux/sauvegardes de lecture ont été créés dans %s.\n' "$WORK_DIR"
  exit 0
fi

# Ce chemin est limité à la première installation d’OpenSSH sur la base auditée.
if dpkg-query -W -f='${db:Status-Abbrev}' openssh-server 2>/dev/null | grep -q '^ii'; then
  die 'Serveur SSH déjà installé : revue de sa configuration requise, pas de remplacement automatique.'
fi
[[ ! -e /etc/ssh/sshd_config && ! -L /etc/ssh/sshd_config ]] || die 'Configuration SSH préexistante : revue manuelle requise.'
[[ -n $KEY_FILE && -f $KEY_FILE && ! -L $KEY_FILE ]] || die 'Fournir un fichier de clé publique client ordinaire.'
[[ $(awk 'NF {n++} END {print n+0}' "$KEY_FILE") == 1 ]] || die 'Une seule clé publique est attendue.'
grep -Eq '^(ssh-ed25519|ssh-rsa|ecdsa-sha2-nistp(256|384|521)|sk-ssh-ed25519@openssh.com|sk-ecdsa-sha2-nistp256@openssh.com) [A-Za-z0-9+/=]+( .*)?$' "$KEY_FILE" || die 'Clé publique simple requise, sans options authorized_keys.'
ssh-keygen -lf "$KEY_FILE"
ADMIN_USER=$(id -un)
[[ $ADMIN_USER == adminjarvis ]] || die 'Compte adminjarvis attendu pour cette mission.'
[[ ! -L $HOME/.ssh && ! -L $HOME/.ssh/authorized_keys ]] || die 'Liens symboliques SSH refusés : vérifier les chemins.'
for unit in ssh.service ssh.socket; do
  if [[ -e /etc/systemd/system/$unit || -L /etc/systemd/system/$unit || -e /run/systemd/system/$unit || -L /run/systemd/system/$unit ]]; then
    die "Surcharge systemd préexistante pour $unit : revue manuelle requise."
  fi
done
boot_kib=$(df -Pk /boot | awk 'NR==2 {print $4}')
root_kib=$(df -Pk / | awk 'NR==2 {print $4}')
(( boot_kib >= 512000 && root_kib >= 2097152 )) || die 'Marge minimale : 500 Mio /boot et 2 Gio racine ; estimation à revoir.'
printf '\nOPÉRATIONS PROPOSÉES :\n'
printf '%s\n' \
 '1. apt-get update avec arrêt si un dépôt échoue ; nouvelles simulations affichées.' \
 '2. Marquage manuel des noyaux installés pour les préserver ; aucune suppression.' \
 '3. Masquage persistant de ssh.service/ssh.socket avant installation pour empêcher le démarrage par les scripts de paquets.' \
 '4. apt-get --no-remove upgrade ; installation des quatre paquets et dépendances.' \
 '5. Sauvegarde et remplacement de la configuration du serveur nouvellement installé.' \
 '6. SSH IPv4 sur 127.0.0.1:22 uniquement, root interdit, clés uniquement, adminjarvis seul.' \
 '7. Ajout de la clé publique approuvée à authorized_keys, sans changement des droits sudo.' \
 '8. Vérification sshd et activation ssh.service après démasquage ; socket désactivé.' \
 'Aucun dépôt T2/NVIDIA, règle réseau, partition ou redémarrage ; pas de nettoyage de noyaux.' \
 'Les mises à jour peuvent installer un noyau Debian et recharger des services. APT reste interactif.'
confirm 'Approuver ces opérations et l’empreinte de la clé affichée'
sudo apt-get -o APT::Update::Error-Mode=any update
sudo apt-get -s --no-remove upgrade | tee "$WORK_DIR/upgrade.fresh.txt"
sudo apt-get -s --no-remove install openssh-server dkms linux-headers-amd64 nvme-cli | tee "$WORK_DIR/install.fresh.txt"
confirm 'Approuver les listes actualisées, y compris les éventuels nouveaux noyaux'
sudo apt-mark manual "${KERNEL_PACKAGES[@]}"
SSH_MASKED=1
sudo systemctl mask ssh.service ssh.socket
sudo apt-get --no-remove upgrade
sudo apt-get --no-remove install openssh-server dkms linux-headers-amd64 nvme-cli
sudo cp -a /etc/ssh/sshd_config "$WORK_DIR/sshd_config.packaged"
cat > "$WORK_DIR/sshd_config.jarvis" <<'SSHCONF'
# JARVIS Mission 02B : première installation, préparation locale seulement.
Port 22
AddressFamily inet
ListenAddress 127.0.0.1
PermitRootLogin no
AllowUsers adminjarvis
PubkeyAuthentication yes
AuthenticationMethods publickey
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitEmptyPasswords no
UsePAM yes
AuthorizedKeysFile .ssh/authorized_keys
Subsystem sftp /usr/lib/openssh/sftp-server
SSHCONF
sudo install -o root -g root -m 600 "$WORK_DIR/sshd_config.jarvis" /etc/ssh/sshd_config
[[ ! -e $HOME/.ssh/authorized_keys ]] || cp -a "$HOME/.ssh/authorized_keys" "$WORK_DIR/authorized_keys.before"
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
touch "$HOME/.ssh/authorized_keys"
chmod 600 "$HOME/.ssh/authorized_keys"
public_key=$(cat "$KEY_FILE")
if ! grep -Fqx -- "$public_key" "$HOME/.ssh/authorized_keys"; then
  # Préfixe newline pour éviter de fusionner avec une ancienne dernière ligne sans newline.
  printf '\n%s\n' "$public_key" >> "$HOME/.ssh/authorized_keys"
fi
sudo /usr/sbin/sshd -t
sudo /usr/sbin/sshd -T -C user=adminjarvis,host=localhost,addr=127.0.0.1 | tee "$WORK_DIR/sshd.effective.txt"
for expected in 'permitrootlogin no' 'pubkeyauthentication yes' 'passwordauthentication no' 'kbdinteractiveauthentication no' 'authenticationmethods publickey' 'listenaddress 127.0.0.1:22'; do
  grep -Fxq "$expected" "$WORK_DIR/sshd.effective.txt" || die "Configuration effective incorrecte : $expected. SSH reste masqué."
done
sudo sha256sum -c "$WORK_DIR/kernels.sha256"
for package in "${KERNEL_PACKAGES[@]}"; do
  dpkg-query -W -f='${db:Status-Abbrev}\n' "$package" | grep -q '^ii' || die "Noyau non conservé : $package"
done
sudo grub-script-check /boot/grub/grub.cfg
sudo apt-get check
audit=$(sudo dpkg --audit)
[[ -z $audit ]] || die "Anomalie dpkg : $audit"
[[ -d /lib/modules/$(uname -r)/build ]] || die 'En-têtes du noyau actif absents : proposer les en-têtes versionnés exacts avant de poursuivre.'
dkms status
sudo systemctl unmask ssh.service ssh.socket
sudo systemctl disable --now ssh.socket
sudo systemctl enable --now ssh.service
SSH_MASKED=0
systemctl is-active ssh.service
sudo ss -lntp '( sport = :22 )' | tee "$WORK_DIR/ssh.listeners.txt"
grep -q '127.0.0.1:22' "$WORK_DIR/ssh.listeners.txt" || die 'Écoute SSH locale non observée.'
printf '\nPréparation terminée : SSH local seulement, pas encore validé par connexion authentifiée.\n'
printf 'Tester manuellement avec la clé privée correspondante : ssh -i /chemin/cle_privee adminjarvis@127.0.0.1\n'
printf 'Pour un accès LAN, demander une configuration et un filtrage ciblés après revue du réseau/routeur.\n'
printf 'T2Linux non installé ; signatures, dépendances et en-têtes T2 restent à valider.\nJournal : %s\n' "$WORK_DIR"
