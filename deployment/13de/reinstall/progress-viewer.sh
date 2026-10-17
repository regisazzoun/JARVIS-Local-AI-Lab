#!/bin/sh
trap 'exit 0' INT TERM
while :;do
 printf '\033[2J\033[H'
 echo 'JARVIS — SUIVI DU DEPLOIEMENT'
 echo 'Actualisation automatique. Alt+F1 : connexion ; Alt+F8 : suivi.'
 echo
 if [ -r /run/jarvis/progress.txt ];then cat /run/jarvis/progress.txt;else echo 'Attente de la prochaine transmission du controleur...';fi
 if [ "${1-}" = --once ];then exit 0;fi
 sleep 2
done
