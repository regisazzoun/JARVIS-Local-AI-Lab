# Reprise du25octobre2026 — arrêt sur redémarrage

🟡 En cours. À09h42Europe/Paris, lecture réelle des journaux : Debian13 et EFI finalisés, NVIDIA550.163.01 et toolkitCUDA installés, test CUDA compilé. Le calcul surGPU n'a pas encore été exécuté sur le système installé.

Le RAID a terminé sa synchronisation cette nuit. La garde de stockage a retourné `STORAGE CLEAN`, les volumes `/target` et les deuxESP ont été démontés, puis `mdadm` a confirmé l'arrêt de`md0`. La machine est pourtant restée dans l'installateurRAM. L'observateur a atteint son échéance6h : ce fonctionnement autonome n'est pas une réussite complète et n'est pas présenté comme tel.

## Diagnostic et correctionCodex

LePID1est`/bin/busybox init`. Ses signaux`ShdPnd=0x14000` et`SigBlk=0x20014a07` montrent notamment unSIGTERM en attente et bloqué pendant le démarrage de l'installateur retenu par`early_command`. Les appels de reboot normaux retournent sans redémarrer. C'est un défaut du mécanisme de sortie fourni parCodex, pas un besoin d'autorisation propriétaire ni une erreur de partitionnement.

Après vérification indépendante de l'absence de volumes`/target`, de miroir actif et de swap, Codex déclenche une fois le chemin noyau direct du BusyBox natif. C'est une exception contrôlée après arrêt propre : la mauvaise pratique historique de reboot forcé pendant un RAID actif n'est pas reprise. L'appelSSH perd sa connexion et les deux ports deviennent indisponibles ; cela démontre la sortie du contexte précédent, pas encore le bon démarrage installé.

Le script réutilisable est corrigé pour cette condition d'arrêt propre. L'observateur de reprise est borné30min et reconnaît un installateur encore accessible3min après `reboot READY`, afin d'arrêter cette stratégie avec diagnostic plutôt que patienter silencieusement6h.

## Reste à recevoir

- Boot réel de Debian installé, identité et SSHclé/sudo indépendants.
- GPU réellement reconnus, modèles/VRAM mesurés ; ne pas annoncer deux3090 à partir du souhait initial.
- Exécution du test numérique CUDA sur chaque carte.
- Ansible réel et restitutionJARVIS confrontée aux reçus.
- Tableau physique aprèsboot et réception documentée.

L'état vivant reste dans`assist/CONTINUATION-STATUS.json` du projet privé14B. AucunOllama, routage ou mécanisme de répartition existant n'est modifié. Les états de la veille et l'échec nocturne restent conservés.
