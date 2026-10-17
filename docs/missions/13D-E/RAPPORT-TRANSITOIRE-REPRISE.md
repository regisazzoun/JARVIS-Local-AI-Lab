# Rapport transitoire — clôture de tentative et mission complémentaire Dell

Date : 17 octobre 2026 (Europe/Paris). Tentative actuelle clôturée à la demande du propriétaire. Ne pas relancer d'installation dans cette session. Objectif de la mission complémentaire : terminer l'installation et rendre l'administration distante réellement opérationnelle.

## État acquis et limites

- Découverte physique et identité des deux NVMe conservées dans le manifeste privé ; PXE UEFI physique validé.
- Partitionnement et installation Debian réalisés ; événements `guard-ok-starting-partman` le 16/10 à 20:34, `late-start` à 20:39, `late-ok` à 23:21. La synchronisation RAID a été observée en console par le propriétaire, puis la finalisation a réussi. La santé courante devra être relue, sans nouvelle synchronisation imposée.
- GRUB observé, Debian démarre sur disque. Après redémarrage manuel, SSH Debian répond sur 192.168.1.75:22, adresse MAC conforme au Dell. Cette IP est à redécouvrir, pas à considérer fixe.
- L'écran noir provenait d'une bascule de sortie vers HDMI : le propriétaire a retrouvé une invite de connexion. Pas de panne graphique démontrée.
- Aucun rapport de premier boot reçu, aucune session SSH authentifiée ouverte par cette tentative, aucun accès permanent validé, aucune réception Ansible démontrée. La cause du défaut de rapport reste inconnue.
- Écart de compte : le preseed crée jarvis-bootstrap et la reprise prévoit jarvisadmin ; le propriétaire impose désormais adminjarvis. Ne pas recopier les anciens noms comme cible finale.
- Arrêt demandé des services temporaires du contrôleur ; consulter status.json et deployment.log privés pour la preuve de nettoyage. Ne pas supprimer les preuves ni les secrets nécessaires à une récupération du système existant.

## Directives utilisateur pour la mission complémentaire

1. Utilisateur permanent imposé : **adminjarvis**. Mot de passe expressément choisi par le propriétaire, conservé dans `deployment/13de/private/reprise-user-password.txt` (0600, ignoré par Git). Lire ce fichier localement pour l'appliquer ; ne pas générer de mot de passe complexe, ne pas imposer de changement ou de politique de complexité qui contredit ce choix. Ne jamais publier le mot de passe dans Git, les journaux ou les commandes affichées.
2. Alléger les mécanismes d'accès qui ont empêché l'aboutissement, dans le laboratoire autorisé. Prévoir dès le départ une voie SSH fonctionnelle et récupérable pour adminjarvis. Corriger les restrictions AllowUsers et la configuration effective ; ne pas se contenter d'installer openssh-server. Le rapport automatique ne doit pas être l'unique voie d'accès ou de récupération. Conserver les contrôles d'identité de la cible et une vérification praticable de la clé hôte.
3. **Maintenir SSH par mot de passe au moins jusqu'à une nouvelle connexion indépendante par clé et une validation de sudo.** Aucun verrouillage/expiration du compte, retrait du mot de passe ou désactivation de PasswordAuthentication avant cette preuve. La validation par clé n'impose pas à elle seule de supprimer ensuite le secours par mot de passe : suivre la décision du propriétaire.
4. **Clavier français AZERTY à toutes les étapes** : environnement de secours et installateur, consoles et système installé. Vérifier la disposition réellement active, y compris lors d'une reprise manuelle après échec. Locale seule insuffisante ; configurer explicitement le clavier et vérifier la saisie des commandes et du mot de passe.
5. **Réutiliser autant que possible le partitionnement, le RAID1 déjà synchronisé et Debian installé.** Commencer par découvrir et lire l'état réel, assembler/monter le miroir existant si nécessaire et réparer les comptes, SSH, le rapport et la configuration. Ne pas lancer automatiquement wipefs, recréation mdadm, formatage ou repartitionnement. Une nouvelle exécution partman destructrice n'est pas la voie par défaut. Une resynchronisation nécessaire à la santé du miroir doit être distinguée d'une recréation inutile. Si une réinstallation système est indispensable, conserver les métadonnées et partitions compatibles autant que possible et expliquer la nécessité technique des changements.
6. Réaliser l'amélioration consolidée du [rapport final](RAPPORT-FINAL.md) : progression globale et par tâche, coches seulement après validation réelle, états/durées/dernière activité/erreurs/journaux actualisés, affichage console et SSH temporaire permettant de surveiller **toutes** les tâches. Pas seulement le RAID. Indiquer clairement les progressions estimées et les résultats réellement mesurés.

## Déroulement attendu à la reprise

1. Relire AGENTS.md, la charte, ce rapport, le suivi, la roadmap, le rapport final et les preuves privées. Ces directives plus récentes remplacent les anciens comptes et mécanismes de verrouillage contradictoires.
2. Réutiliser le démarrage Debian existant si possible ; sinon préparer une image PXE de réparation avec clavier français et accès distant prévu. Vérifier UUID/DMI et identités exactes des deux NVMe avant toute action sur le stockage.
3. Diagnostiquer le service jarvis-install-report et corriger sa cause réelle. Établir un moyen de vérification de la clé hôte qui ne dépende pas exclusivement du service défaillant ; ne pas présenter un simple port 22 ouvert comme une authentification réussie.
4. Créer/réparer adminjarvis avec le mot de passe utilisateur privé, SSH effectif et sudo. Éprouver une connexion par mot de passe depuis JARVIS ; conserver cet accès pendant la mise en place des clés.
5. Installer la clé autorisée ; ouvrir une session indépendante par clé, vérifier identité et sudo, puis retester après toute modification des accès. Vérifier le maintien du secours convenu.
6. Contrôler RAID sain, montages, deux ESP, chargeurs et services ; ne pas refaire les qualifications VM déjà acquises. Distinguer ces preuves des essais physiques de boot sur chaque disque, non réalisés ici.
7. Appliquer le socle Ansible et vérifier une seconde passe sans changement/échec/inaccessible. Vérifier le redémarrage, le retour SSH et la réception du rapport avant de déclarer la mission complète.
8. Nettoyer les seuls services temporaires et produire un rapport final avec preuves et réserves. Aucun déploiement GPU/IA n'est réputé réussi sans vérification.

## Autorisations et frontières conservées

Mission de cette session : clôture et documentation seulement. La mission complémentaire sera lancée par le propriétaire. Une fois lancée, poursuivre les opérations dans le périmètre Dell déjà autorisé sans validations humaines intermédiaires inventées ; privilégier la conservation du stockage demandée ci-dessus. Préserver le Mac mini, ses accès/services/SQLite, le DHCP Bbox et les paramètres BIOS/VROC/VMD. Aucun benchmark NVMe ni fusion automatique. Identifiants matériels et secrets restent privés.

Directives consultées : AGENTS.md, docs/CHARTE_DIRECTIVES_JARVIS.md, SUIVI.md, ROADMAP.md, PROMPT-INSTALLATION-AUTONOME.md, RAPPORT-FINAL.md et consignes utilisateur du 17 octobre ; autorisations conservées et anciennes contraintes d'accès corrigées par les directives ci-dessus.
