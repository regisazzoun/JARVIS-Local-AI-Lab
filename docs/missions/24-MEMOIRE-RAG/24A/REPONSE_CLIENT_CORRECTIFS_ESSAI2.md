# Essai 2 après correctifs — sortie observée

**14 novembre 2026, copie privée. Cette réponse reste soumise à la revue critique. Expurgation de publication seulement ; aucun filtre ajouté au modèle.**

Je vais rechercher les documents relatifs au déploiement de la téléphonie IP dans la salle 407 sur le Drive Éducation du lycée.
Voici l’état d’avancement du déploiement téléphonie IP de la salle 407, tel que documenté dans les sources consultées le 13 novembre 2026 :

### 1. Réseau (VLAN 407 et infrastructure)
*   **État :** Partiellement déployé et opérationnel sur les bancs 1 et 2.
*   **Détails :**
    *   Le VLAN 407 (réseau [ADRESSE EXPURGÉE], passerelle [ADRESSE EXPURGÉE]) est actif. Le serveur DHCP ([ADRESSE EXPURGÉE]) fonctionne et distribue les options DNS du domaine [2].
    *   Les bancs 1 et 2 sont câblés et configurés : les switches centraux (3850) et pédagogiques (3560G) sont connectés via des agrégats LACP (Po1) en trunk VLAN 99/407 [2].
    *   Dix téléphones ont été identifiés physiquement sur le banc 1 (ports Gi0/1–12 du 3560G), avec des IP dans la plage [ADRESSE EXPURGÉE] à .65 [2].
    *   **Reste à faire :** Les bancs 3 à 6 restent à inventorier et déployer [2]. La liaison physique vers les serveurs (port Gi1/0/12 du central) doit être confirmée [2].

### 2. IPBX (FusionPBX / FreeSWITCH)
*   **État :** Déployé, configuré et opérationnel.
*   **Détails :**
    *   Serveur : Raspberry Pi 4 (Debian 13), adresse fixe [ADRESSE EXPURGÉE] [3].
    *   Services : FreeSWITCH (v1.11.3), Nginx et PostgreSQL sont actifs [3].
    *   Domaine SIP : `[ADRESSE EXPURGÉE]` [3].
    *   Codecs : Audio (G722, PCMU, PCMA) et Vidéo (H.264, VP8) configurés et chargés [3].
    *   Messagerie vocale : Configurée en français (dialecte canadien, voix "june") [3].

### 3. Téléphones et Provisioning
*   **État :** 11 extensions créées et provisionnées ; 10 à 11 téléphones physiques identifiés comme enregistrés.
*   **Détails :**
    *   **Extensions actives :** [EXTENSION EXPURGÉE] à [EXTENSION EXPURGÉE] (format SSSPP) [3].
    *   **Modèles déployés :** Cisco SPA504G (6 unités), Polycom VVX 450, Aastra 480i, Grandstream GXP1620, Cisco SPA525G2, Polycom SoundStation IP 7000 [3].
    *   **Provisioning :** Les profils XML/CFG sont générés et accessibles via HTTP (code 200) depuis les téléphones. Le provisioning inclut la langue française, le NTP (`fr.pool.ntp.org`) et le fuseau Paris [1].
    *   **Spécifique [EXTENSION EXPURGÉE] :** Le poste "Banc 1" (Cisco SPA504G) a été déployé le 13 novembre après identification de sa MAC et IP ([ADRESSE EXPURGÉE]) [1].

[PASSAGE D’AUTHENTIFICATION EXPURGÉ — valeur et règle non publiées]

### 5. Appels et Audio/Vidéo
*   **État :** Partiellement validé.
*   **Détails :**
    *   **Audio :** Des appels bidirectionnels avec audio ont été validés entre les extensions [EXTENSION EXPURGÉE] et [EXTENSION EXPURGÉE] [1]. La validation complète sur tous les modèles reste à faire [1].
    *   **Vidéo :** Les codecs vidéo sont configurés, mais aucun test complet démontrant une image bidirectionnelle fonctionnelle n'est documenté comme réussi [3].
    *   **Annuaire :** L'accès HTTP au service d'annuaire est autorisé sur les postes, mais l'ouverture du répertoire sur l'écran physique reste à tester [1].

### 6. Reste à faire (Points en attente)
*   **Déploiement physique :** Inventorier et déployer les bancs 3 à 6 [2].
*   **Recette complète :** Tester les appels bidirectionnels sur chaque modèle de téléphone, notamment le Grandstream [EXTENSION EXPURGÉE] et les Polycom [1].
*   **Vérifications physiques :** Confirmer l'affichage français et la synchronisation heure sur tous les écrans physiques [1].
*   **Sécurité/Architecture :** Définir les droits d'administration élèves sur les switches pédagogiques avant leur ouverture complète [2].
*   **Sauvegarde :** Mettre en place une procédure de sauvegarde automatisée et tester la restauration [3].
*   **Vidéo :** Valider un flux vidéo bidirectionnel entre deux clients capables [3].

**Sources :**
*   [1] `Salle-407-Documentation-deploiement.md` (modifié le 13/11/2026) — Détails du provisioning, état des téléphones et tests.
*   [2] `Salle 407 — Architecture réseau et six bancs élèves` (modifié le 12/11/2026) — État du réseau, switches et câblage.
*   [3] `FusionPBX — Installation, configuration et exploitation — SEP CIEL — 13-11-2026` (modifié le 13/11/2026) — Configuration serveur, extensions et services.
