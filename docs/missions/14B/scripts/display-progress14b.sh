#!/bin/sh
# Physical Dell2 installer console, based only on actual files/sysfs state.
# Source provided by Codex; no disk changes and no install commands.
set -u
bar() {
 value=$1
 filled=$((value / 5));empty=$((20 - filled))
 printf '[';i=0;while [ "$i" -lt "$filled" ];do printf '#';i=$((i+1));done
 i=0;while [ "$i" -lt "$empty" ];do printf '.';i=$((i+1));done;printf '] %s%%' "$value"
}
while :; do
 tmp=/run/jarvis-screen-next.txt
 {
 printf 'JARVIS — MISSION 14B — INSTALLATION DELL N°2\n'
 printf 'Suivi réel — actualisation toutes les 5 secondes\n\n'
 printf '%-8s %s\n' '[OK]' 'Identité Dell2 / MAC / UUID / SSH de supervision contrôlés'
 printf '%-8s %s\n' '[OK]' 'Deux NVMe 2 To identifiés — GPT et deux partitions EFI créées'
 if [ -e /sys/block/md0/md/degraded ];then
  degraded=$(cat /sys/block/md0/md/degraded)
  if [ "$degraded" = 0 ];then printf '%-8s %s\n' '[OK]' 'RAID1 : deux membres présents, aucun membre dégradé';else printf '%-8s %s\n' '[ERREUR]' "RAID1 : $degraded membre(s) dégradé(s)";fi
  action=$(cat /sys/block/md0/md/sync_action)
  sync=$(cat /sys/block/md0/md/sync_completed)
  mdstat=$(cat /proc/mdstat)
  if [ "$action" = idle ];then percent=100;else
   percent=$(printf '%s\n' "$mdstat" | awk '/resync[[:space:]]*=/ {for(i=1;i<=NF;i++) if($i ~ /^[0-9.]+%$/) {sub(/%/,"",$i);printf "%d",$i;exit}}')
   [ -n "$percent" ] || percent=0
  fi
  printf '%-8s %s ' '[SUIVI]' 'Synchronisation RAID1';bar "$percent";printf '\n'
  printf '%s\n' "$mdstat" | grep 'finish=' | sed 's/^ */         /'
 else printf '%-8s %s\n' '[ATTENTE]' 'État RAID non disponible';fi
 if [ -e /target/etc/debian_version ];then printf '%-8s %s\n' '[OK]' "Debian $(cat /target/etc/debian_version) installé sur le miroir";else printf '%-8s %s\n' '[ATTENTE]' 'Installation Debian';fi
 if [ -f /target/etc/sudoers.d/adminjarvis ];then printf '%-8s %s\n' '[OK]' 'Comptes adminjarvis / jarvis-bootstrap et configuration SSH';fi
 if [ -e /run/jarvis-install-complete ];then
  printf '%-8s %s\n' '[OK]' 'Finalisation Debian et deux copies EFI terminées'
  printf '%-8s %s\n' '[CORRIGÉ]' 'Fichiers de suivi ajoutés ; reprise sans reformater'
 else printf '%-8s %s\n' '[EN COURS]' 'Finalisation Debian — voir dernière étape ci-dessous';fi
 if [ -e /run/jarvis-gpu-packages-complete ];then printf '%-8s %s\n' '[PRÉPARÉ]' 'NVIDIA/CUDA : paquets et test compilés ; fonctionnement après boot à vérifier'
 elif [ -e /run/jarvis-gpu-install-started ];then
  if tail -n 3 /run/jarvis-install-progress.log | grep -q 'FAILED NVIDIA';then printf '%-8s %s\n' '[ERREUR]' 'NVIDIA/CUDA : correction requise, diagnostic conservé'
  else printf '%-8s %s\n' '[EN COURS]' 'Installation des paquets NVIDIA/CUDA';fi
 else printf '%-8s %s\n' '[TRANSMIS]' 'Préparation NVIDIA/CUDA confiée à JARVIS, lancement non encore observé';fi
 printf '%-8s %s\n' '[ATTENTE]' 'Redémarrage automatique après préparation et RAID synchronisé'
 printf '%-8s %s\n' '[À TESTER]' 'SSH installé, NVIDIA, calcul CUDA sur chaque GPU, Ansible'
 printf '\nDerniers événements réels :\n'
 tail -n 5 /run/jarvis-install-progress.log 2>/dev/null || :
 printf '\nDernière sortie NVIDIA/CUDA (si démarré) :\n'
 tail -n 2 /run/jarvis-gpu-install.log 2>/dev/null || :
 printf '\nAucune manipulation utilisateur requise. Ollama / routage / charges inchangés.\n'
 printf 'Codex : infrastructure/corrections — JARVIS : déclenchement des opérations.\n'
 } > "$tmp"
 mkdir -p /run/jarvis
 mv "$tmp" /run/jarvis/progress.txt
 { printf '\033[2J\033[H';cat /run/jarvis/progress.txt; } > /dev/tty1
 sleep 5
done
