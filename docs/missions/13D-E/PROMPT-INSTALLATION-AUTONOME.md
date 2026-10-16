# JARVIS — 13D-E : installation complète, une seule intervention PXE

## Objectif et autorisation explicite du propriétaire

Continuer dans regisazzoun/JARVIS-Local-AI-Lab, branche codex/mission-13de-preparation et PR brouillon n°5, sans fusion. Réutiliser la chaîne PXE UEFI déjà validée et la découverte physique déjà reçue. Ne pas recommencer leur conception.

La seule intervention humaine admise est : **le propriétaire lance le Dell par F12 → UEFI IPv4 quand les services sont prêts**. Aucune copie de résultats, saisie de secret, transfert de clé, validation intermédiaire ou configuration manuelle du Dell.

Le propriétaire autorise, pour ce déploiement du Dell identifié :

1. L'activation temporaire des seuls services réseau nécessaires.
2. La destruction de toutes les partitions des deux NVMe identifiés dans le rapport privé, puis l'installation complète de Debian 13 minimal en RAID1 logiciel avec une ESP indépendante sur chaque disque.
3. Le redémarrage automatique du Dell, la création du compte temporaire, la prise de contrôle administrative SSH, l'établissement de l'accès permanent par clé et l'application du socle Ansible.

Ces directives remplacent les anciens prompts et validations humaines intermédiaires de la mission. Ces autorisations sont acquises : ne pas les redemander. Elles couvrent exclusivement le Dell et les deux NVMe associés à son UUID, leurs séries/modèles/capacités étant dans deployment/13de/private/bootstrap-discovery-04/inventory.observed.json. Ne pas publier ces identifiants uniques ni les secrets.

## Résultat attendu

Un seul lancement PXE → vérification d'identité → partitionnement/RAID1 → installation Debian minimal → deux ESP et chargeurs de secours → compte jarvis-bootstrap temporaire et SSH → reboot disque → rapport automatique et clé hôte publique → connexion bootstrap depuis JARVIS → création/validation de jarvisadmin par clé → révocation bootstrap → configuration et deux passes Ansible → rapport automatique dans Codex.

Aucune validation humaine après le lancement PXE. Remplacer les anciens points de validation humaine par des contrôles automatiques réels, qui échouent en sécurité. Ne pas inventer une qualification ni transformer un résultat inconnu en succès.

## Contrôles automatiques obligatoires

- Vérifier UUID, DMI réellement observé Precision 5820 Tower X-Series, séries, modèles et tailles exactes des deux NVMe, mode UEFI et absence de disque cible ambigu.
- /dev/sda est apparu comme lecteur SD/MMC sans média, taille nulle. Le traiter uniquement comme périphérique exclu, jamais comme cible, avec une règle précise vérifiant l'absence de média ; si une capacité non nulle apparaît ou si un autre disque non approuvé est présent, arrêter automatiquement.
- Le DMI annonce BIOS 2.8.0 ; conserver le firmware en place. Ne pas imposer une mise à jour ni modifier BIOS/VMD/VROC.
- Qualifier automatiquement la recette RAID/double ESP au moyen de contrôles ciblés nécessaires, sans campagne complète de laboratoire ni benchmark NVMe. Ne pas effacer les NVMe réels pour simplement tester une recette inconnue.
- Après partitionnement autorisé, vérifier le miroir, les deux ESP, les chargeurs, l'initramfs et le chemin de démarrage de secours. Aucun reboot automatique si une vérification d'installation échoue.
- Compte bootstrap et secret uniques au déploiement, secret clair seulement dans le stockage privé JARVIS, pas d'authentification root par mot de passe, accès bootstrap limité à JARVIS. Pas de secret dans Git, URL, argv ou journal.
- Créer si nécessaire une identité de déploiement dédiée sous private, sans modifier les clés existantes du Mac. Ne demander aucun transfert manuel de clé.
- Épingler la clé hôte reçue par le mécanisme de déploiement borné et vérifier DMI/UUID avant administration ; ne pas désactiver StrictHostKeyChecking. Limiter les services/artefacts au Dell sur le LAN de cette session et retirer les secrets/artefacts servis après usage.
- Ouvrir une NOUVELLE connexion SSH indépendante à clé et vérifier sudo avant de verrouiller le compte temporaire. Retester après révocation ; permettre une reprise automatique après interruption.
- Appliquer Ansible uniquement après réception automatique du stockage et de l'accès permanent. Deuxième passe sans changement/échec/inaccessible. Conserver les preuves privées et un rapport public expurgé.

## Périmètre IA et protections

Déployer le système de base et l'accès administratif indépendamment des GPU. NVIDIA/CUDA/Ollama ne deviennent opérationnels que si réellement implémentés et vérifiés. Ne pas bloquer la réception du socle sur la seconde RTX 3090 non alimentée ; laisser ces étapes ultérieures sans réinstallation.

Ne pas modifier SSH/Tailscale, comptes/clés existants, services JARVIS, SQLite ou sessions du Mac mini. Conserver la Bbox comme seul DHCP d'allocation. Aucun benchmark NVMe, modification BIOS/VROC/VMD, changement d'alimentation GPU ou fusion main.

## Méthode

Effectuer les adaptations et contrôles nécessaires avant de demander l'unique lancement PXE. Quand la chaîne est prête, activer les services temporaires dans le périmètre déjà autorisé, vérifier leur disponibilité, puis demander uniquement « Lancez le Dell par F12 → UEFI IPv4 ». Surveiller et poursuivre automatiquement jusqu'au résultat, nettoyer les services temporaires et publier les preuves sur la branche/PR existantes.

Si un blocage technique rend l'automatisation impossible, arrêter les seules opérations concernées, préserver les accès et données, et expliquer ce blocage précisément. Ne pas présenter une simple préparation comme une installation réalisée. Une nouvelle demande d'approbation ne remplace pas la résolution du problème technique.

Directives consultées : AGENTS.md, docs/CHARTE_DIRECTIVES_JARVIS.md, SUIVI.md, ROADMAP.md, RAPPORT-FINAL.md ; autorisations préservées : réseau, effacement des deux NVMe identifiés, installation, reboot, bootstrap SSH et Ansible sans validation intermédiaire ; écarts corrigés : anciennes demandes de GO remplacées par la directive autonome récente.
