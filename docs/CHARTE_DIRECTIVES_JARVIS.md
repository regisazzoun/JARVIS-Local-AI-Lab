# JARVIS — Directives fondamentales du propriétaire

**Statut : décisions de référence pour ChatGPT, Codex et les agents JARVIS.**
**Date : 16 octobre 2026.**
**Périmètre : laboratoire JARVIS — Local AI Lab, réseau local privé.**

## 1. Autorité et méthode

- Les instructions explicites du propriétaire priment sur les recommandations de l'assistant, sous réserve des contraintes techniques réelles et des règles de sécurité applicables. Ne jamais réécrire une autorisation accordée en interdiction tacite.
- L'assistant peut signaler un risque et proposer une précaution, mais ne doit pas transformer cette recommandation en prérequis bloquant sans raison concrète. Si une opération est matériellement impossible ou présente un risque grave immédiat, l'expliquer précisément ; ne pas inventer une contrainte générique.
- Différencier strictement **décision utilisateur**, **recommandation**, **fait démontré**, **hypothèse** et **blocage effectivement observé**.
- Lorsqu'une directive récente remplace une consigne historique, la nouvelle décision prévaut dans son périmètre. Les textes historiques restent des traces, pas des ordres concurrents.
- Ne pas relancer une mission, campagne VM ou suite de diagnostics déjà validée pour satisfaire une préférence de prudence de l'assistant.

## 2. Contexte de risque assumé

- Le projet s'exécute dans un **laboratoire expérimental sur un réseau local privé et considéré isolé par le propriétaire**, avec du matériel dédié aux essais. L'utilisateur accepte explicitement que les machines cibles et leurs partitions puissent être réinstallées ou effacées dans le cadre du déploiement convenu ; pas d'exigence de continuité de production.
- Il ne s'agit pas d'un SI de production d'entreprise. Chercher à avancer et vérifier la faisabilité plutôt qu'à éliminer chaque défaut secondaire avant de tester.
- Le contexte local réduit l'exposition mais n'en prouve pas l'impossibilité absolue ; le mentionner **une fois si pertinent**, sans imposer par défaut une nouvelle revue de menace, une architecture complexe de secrets ou un refus de progression.
- Ne jamais appliquer cette tolérance aux autres machines, disques ou données qui ne font pas partie du profil de déploiement autorisé.

## 3. Autorisation effective — installation Dell 13D-E

- Le propriétaire a **déjà autorisé l'installation complète autonome** du Dell reconnu, sur les **deux NVMe explicitement identifiés et associés au manifeste privé**, y compris **la suppression des partitions existantes, le RAID1 logiciel mdadm, Debian 13 minimal, reboot, bootstrap SSH, installation d'accès permanent et socle Ansible**.
- **Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire.** L'agent poursuit automatiquement le périmètre déjà autorisé (PXE, effacement des NVMe identifiés, installation, reboot, SSH et Ansible), sans poser de GO à chaque phase. L'unique intervention physique normalement attendue est **F12 → UEFI IPv4** lorsque Codex l'indique. Ne pas créer de nouveaux obstacles administratifs avant le démarrage non plus.
- Cette autorisation n'est **pas** une autorisation générique de sélectionner des disques par ordre /dev/nvme* ou capacité : vérifier DMI/UUID et identité exacte du matériel et des deux SSD ; arrêter **uniquement en cas d'écart ou d'ambiguïté effective**.
- Le **PXE physique UEFI IPv4 a déjà fonctionné** : snponly.efi → iPXE → noyau → initrd → installateur Debian. Ne pas requalifier inutilement cette partie ; un nouveau boot peut être demandé quand la chaîne d'installation est prête.
- Les vérifications automatiques d'identité et de fonctionnement restent opérationnelles mais **ne doivent jamais se transformer en validations humaines**. Lorsqu'un mécanisme historique exige plusieurs GO, le mettre en cohérence avec l'autorisation globale déjà documentée, sans contourner silencieusement un contrôle technique. En cas d'écart matériel vérifié ou de défaillance concrète, signaler le blocage factuel et arrêter l'opération concernée.
- Le RAID1 logiciel **mdadm** et les **deux ESP indépendantes** sont décidés. Les tests ciblés nécessaires à la validité de la recette sont permis ; **aucun benchmark NVMe**, aucune campagne complète de VM imposée.
- **Compte SSH temporaire** avec mot de passe unique gardé localement sur JARVIS ; création et validation du compte permanent par clé ; **désactiver le bootstrap uniquement après connexion indépendante par clé et vérification des droits**. Aucun transfert manuel de clé.
- Une seule RTX 3090 dispose actuellement d'une alimentation auxiliaire complète : ne pas demander l'utilisation de la seconde avant vérification des câbles et de l'alimentation. Le déploiement de base n'est pas bloqué par cette situation.

## 4. Frontières à conserver

- Les opérations destructrices convenues ne concernent que les disques exacts du Dell, jamais le Mac mini, un autre périphérique ou le lecteur SD/MMC sans média.
- Ne pas altérer le DHCP de la Bbox ni les comptes, clés SSH, accès Tailscale, services en production locale ou mémoire SQLite du Mac mini.
- Ne pas publier mots de passe, secrets, séries, UUID ou inventaires identifiants dans GitHub. Les garder sous le répertoire `private/` ignoré par Git.
- Ne pas fusionner automatiquement la PR ou la branche de mission dans `main`.
- Les ajustements BIOS, alimentation physique et câblage nécessitent une intervention volontaire du propriétaire.
- Distinguer **réception de la préparation** et **résultat réellement démontré sur le Dell** ; ne pas déclarer une installation réussie sans preuve.

## 5. Barrière obligatoire avant tout prompt / mission

Avant de générer ou de lancer une directive Codex ou JARVIS relative au projet :

1. Lire `AGENTS.md`, ce document et les directives spécifiques de la mission en cours.
2. Lire l'état de référence le plus récent dans `SUIVI.md`, `ROADMAP.md`, le rapport de mission et, s'il existe, le prompt d'exécution autorisé. L'historique ne doit pas révoquer une autorisation plus récente.
3. Construire mentalement ou dans le rapport de travail un tableau : **AUTORISÉ / INTERDIT / DÉJÀ VALIDÉ / RESTE À FAIRE / NOUVELLE AUTORISATION VRAIMENT NÉCESSAIRE**.
4. Vérifier chaque « ne pas », « attendre GO », « uniquement en lecture seule » et chaque demande de test supplémentaire du nouveau prompt contre les décisions utilisateur. **Supprimer les restrictions incompatibles** au lieu de les recopier.
5. Si les documents sont inaccessibles ou contradictoires, le signaler avant d'affirmer que le prompt reprend fidèlement les instructions.
6. Démarrer l'exécution à partir du dernier jalon matériel **réellement prouvé**, sans refaire ce qui est acquis.
7. Mettre à jour ce référentiel lorsqu'une **nouvelle décision explicite** change la politique, puis propager le changement aux instructions d'agents.

**Interprétation à éviter :** « absence de validations répétitives » ne signifie pas « quelques validations restent souhaitables ». Pour la mission, appliquer la règle : **Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire.**, et **zéro barrière de confirmation inventée avant celui-ci**.

**Contrôle de conformité de chaque prompt :** inclure une courte ligne « Directives consultées : ... ; autorisations préservées : ... ; écarts : aucun / détaillés ». Ce contrôle est documentaire et ne remplace pas les contrôles matériels et applicatifs.

## 6. Sources spécifiques Dell

- `docs/missions/13D-E/PROMPT-INSTALLATION-AUTONOME.md` : formulation explicite des autorisations du propriétaire.
- `docs/missions/13D-E/DEPLOIEMENT-PHYSIQUE.md` : procédure historique, à interpréter avec la politique autonome plus récente.
- `docs/missions/13D-E/RAPPORT-FINAL.md` et `TESTS.md` : état et preuves datés.


## Directive de reprise — 17 octobre 2026

Tentative clôturée à la demande du propriétaire ; prochaine mission : finir l’installation en privilégiant la réparation de Debian et la conservation du RAID/partitionnement existants. Compte final imposé : **adminjarvis** ; mot de passe utilisateur conservé uniquement dans `deployment/13de/private/reprise-user-password.txt`, sans complexité supplémentaire imposée. Maintenir SSH par mot de passe jusqu’à validation indépendante par clé et sudo ; aucune suppression automatique du secours ensuite. Clavier français AZERTY à toutes les étapes. Suivi de toutes les tâches avec barres et coches de validation réelle. Ces directives remplacent les anciens noms de comptes et restrictions contradictoires. Lire `docs/missions/13D-E/RAPPORT-TRANSITOIRE-REPRISE.md` avant reprise. Ne pas relancer la mission pendant la clôture.


## Mission complète 13D-E / 14 relancée — 17 octobre 2026

Directive utilisateur actuelle : nouvelle installation Debian automatisée, conservation prioritaire GPT/RAID1/métadonnées/deux ESP, formatage rapide de la seule racine si compatible. Comptes jarvis-bootstrap et adminjarvis avec le même mot de passe imposé dans le fichier privé reprise-user-password.txt. Garder SSH par mot de passe pour adminjarvis même après validation indépendante par clé et sudo ; ne pas désactiver prématurément le bootstrap. Clavier français dans installateur/secours/consoles/système. Mission continue incluant Ansible, NVIDIA/CUDA, Ollama, Qwen/Ministral/Llama documentés, intégration conversation/voix/mémoire/outils et réception après reboot. Une RTX 3090 alimentée seulement. Aucune validation humaine intermédiaire ; email au propriétaire quand le PXE est réellement prêt. Les anciennes clôtures, reports IA, révocations automatiques et préférences de simple réparation sont remplacés dans ce périmètre. Aucun secret dans Git. Préserver services/accès/mémoire Mac mini et DHCP Bbox ; aucune fusion main.
