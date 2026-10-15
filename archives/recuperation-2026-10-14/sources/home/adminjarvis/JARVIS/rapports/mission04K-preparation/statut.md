# Suite autorisée de Mission 04K

Accord utilisateur reçu : « oui procede ». Validation préalable tentée depuis l'environnement disponible ; aucun test de démarrage exécuté.

Boot toujours a5d47772-9fed-4f51-8d99-ffe75be725b1, cmdline inchangée. sudo -n id échoue : NoNewPrivs=1, CapEff/CapBnd nuls, sudo.conf vu uid 65534. systemctl : Operation not permitted ; journalctl -b -k : aucune entrée visible avec avertissement de restriction ; iomem masqué. Ces résultats ne permettent pas la validation hôte obligatoire.

Collecteur `collecte-hote.py` préparé pour le terminal local de JARVIS hors isolation. Syntaxe vérifiée sans exécution. Lecture seule du système ; écrit uniquement les preuves utilisateur. Aucun paramètre, GRUB, EFI, module ou matériel modifié. La collecte ne vaut pas autorisation de poursuivre malgré ses éventuels échecs : examiner toutes les preuves avant le candidat resource_alignment.

Exécution depuis le terminal hôte :

```bash
sudo python3 /home/adminjarvis/JARVIS/rapports/mission04K-preparation/collecte-hote.py
```

Le programme affiche le dossier produit. L'analyse peut reprendre dès que ces preuves sont disponibles dans le workspace. Core toujours à laisser déconnecté.

## Nouvel essai hôte réussi — 21:56 CEST

Collecteur exécuté avec sudo -n python3, code 0, uid=0. Dossier : hote-a5d47772-9fed-4f51-8d99-ffe75be725b1-20261011-215637. Boot identique avant/après. Empreintes SHA256SUMS et intégrité des fichiers vérifiées. Journal noyau désormais accessible, iomem et 21 tables ACPI collectés. SSH actif et authentification distante visible ; Ethernet enp4s0 UP avec 192.168.1.99 ; Bolt confirme Razer Core disconnected, aucun périphérique NVIDIA dans sysfs PCI. smartctl a retourné le code 4 : son résultat doit être analysé avant de conclure sur la santé NVMe. Lecture speed de lo et wlp3s0 : EINVAL, non pertinente pour l'Ethernet actif.

Les restrictions d'accès précédentes sont levées pour cette collecte. Cela ne constitue pas encore la validation technique du candidat resource_alignment. Aucun changement système ni test de démarrage exécuté.
