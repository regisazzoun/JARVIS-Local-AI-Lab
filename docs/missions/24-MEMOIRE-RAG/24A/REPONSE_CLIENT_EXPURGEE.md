# Réponse du client observée — sortie non validée

**Audit 24A, copie privée, 13 novembre 2026. Ce texte conserve les défauts de la réponse ; ce n’est pas l’état de référence du lycée.**
Les valeurs et règles d’authentification, adresses, MAC et extensions ont été expurgées. Voir la revue critique dans TESTS_CLIENT_ET_ACL.md.

Je vais rechercher les informations sur le déploiement de la téléphonie IP dans la salle 407 en consultant le Drive Éducation du lycée.
J'ai trouvé plusieurs documents pertinents sur la téléphonie de la salle 407. Je vais maintenant lire les documents clés pour obtenir l'état d'avancement détaillé.
Voici l’état d’avancement du déploiement téléphonie IP de la salle 407, distinguant les aspects réseau, IPBX, téléphones, SIP, appels et reste à faire. Les informations proviennent des documents consultés dans le Drive Éducation (lycée Christophe Colomb) : *Salle 407 — Architecture réseau et six bancs élèves*, *FusionPBX — Installation, configuration et exploitation — SEP CIEL — 13-11-2026* et *Salle-407-Documentation-deploiement.md*.

---

### 1. Réseau (infrastructure physique et logique)
**État : Partiellement déployé et validé sur les bancs 1 et 2.**
- **Architecture centrale :** Le cœur Cisco Catalyst 3850 (*S407-Router*) assure le routage inter-VLAN avec la passerelle du VLAN 407 en `[ADRESSE EXPURGÉE]`. La route par défaut pointe vers pfSense (`[ADRESSE EXPURGÉE]`).
- **Distribution :** Un switch Catalyst 3560G (*S407-Router1*) dessert les bancs 1 et 2 via des liens trunk (Po128/Po48).
- **Banc 1 (référence opérationnelle) :**
    - Tête : Cisco 3850 (`[ADRESSE EXPURGÉE]`) reliée au routeur pédagogique (Cisco 3560G, `[ADRESSE EXPURGÉE]`) par un agrégat LACP Po1 (VLAN 99 et 407).
    - Ports clients : Gi0/1–12 en access VLAN 407. Dix MAC de téléphones apprises, IP observées entre `[ADRESSE EXPURGÉE]` et `.65`.
- **Banc 2 :** Réseau et administration validés (SSH authentifié, Po1 actif). Un test DHCP temporaire a réussi (`[ADRESSE EXPURGÉE]`).
- **Bancs 3 à 6 :** À inventorier et déployer. Les adresses de gestion sont réservées (`[ADRESSE EXPURGÉE]` à `.76` pour les têtes, `.83` à `.86` pour les routeurs pédagogiques).
- **DHCP :** Serveur `[ADRESSE EXPURGÉE]`, étendue `[ADRESSE EXPURGÉE]`, passerelle `.254`, DNS AD `.201`.

**Source :** *Salle 407 — Architecture réseau et six bancs élèves* (modifié le 12/11/2026).

---

### 2. IPBX (Serveur FusionPBX)
**État : Installé, configuré et opérationnel.**
- **Matériel :** Raspberry Pi 4 Model B Rev 1.4 sous Debian 13 ARM64.
- **Adressage :** IP fixe `[ADRESSE EXPURGÉE]` (réseau serveur), passerelle `.254`. Branchement déclaré sur le port 28 du Catalyst 3560 central.
- **Services :** FreeSWITCH (v1.11.3), Nginx, PostgreSQL actifs. Quatre profils SIP chargés.
- **Domaine :** `[ADRESSE EXPURGÉE]`.
- **Langue/Voix :** Français canadien (`fr`, dialecte `ca`, voix `june`) installé et configuré pour la messagerie.
- **Accès :** SSH local (`admin@[ADRESSE EXPURGÉE]`) et distant via JARVIS → Dell1 validés. Interface web HTTPS accessible.

**Source :** *FusionPBX — Installation, configuration et exploitation — SEP CIEL — 13-11-2026*.

---

### 3. Téléphones (Postes physiques)
**État : 11 postes configurés et enregistrés sur le serveur ; 1 poste déployé physiquement.**
- **Inventaire des extensions actives ([EXTENSION EXPURGÉE]–[EXTENSION EXPURGÉE]) :**
    - [EXTENSION EXPURGÉE] à [EXTENSION EXPURGÉE] : Cisco SPA504G.
    - [EXTENSION EXPURGÉE] : Polycom VVX 450.
    - [EXTENSION EXPURGÉE] : Aastra 480i.
    - [EXTENSION EXPURGÉE] : Grandstream GXP1620.
    - [EXTENSION EXPURGÉE] : Cisco SPA525G2.
    - [EXTENSION EXPURGÉE] : Polycom SoundStation IP 7000.
- **Enregistrements :** Les 11 extensions sont actives dans FusionPBX et enregistrées par des téléphones physiques (état *Reachable*).
- **Déploiement physique confirmé :** Le poste [EXTENSION EXPURGÉE] (Cisco SPA504G) est déployé sur le banc 1, IP `[ADRESSE EXPURGÉE]`, MAC `[MAC EXPURGÉE]`.
- **Provisioning :** Fichiers de configuration générés et accessibles via HTTP (Nginx). Dictionnaires français téléchargés pour Cisco et Polycom.

**Source :** *FusionPBX — Installation...* et *Salle-407-Documentation-deploiement.md*.

---

[PASSAGE D’AUTHENTIFICATION EXPURGÉ — valeur et règle non publiées]

**Source :** *Salle-407-Documentation-deploiement.md*.

---

### 5. Appels (Validation fonctionnelle)
**État : Partiellement validé.**
- **Appels audio :** Validés par l'utilisateur uniquement entre les postes [EXTENSION EXPURGÉE] et [EXTENSION EXPURGÉE].
- **Appels vidéo :** Non validés de manière bidirectionnelle complète (tests antérieurs sur softphones inconclus).
- **Messagerie vocale :** Configurée en français, mais l'écoute complète des annonces reste à vérifier.
- **Annuaire :** Service XML configuré vers un annuaire central de 11 contacts, mais l'accès depuis l'écran physique et les appels via l'annuaire restent à tester.

**Source :** *Salle-407-Documentation-deploiement.md* et *FusionPBX — Installation...*.

---

### 6. Reste à faire
- **Déploiement physique complet :** Déployer physiquement les postes [EXTENSION EXPURGÉE] à [EXTENSION EXPURGÉE] sur les bancs (actuellement seuls l'enregistrement SIP et le provisioning sont confirmés pour la plupart).
- **Recette complète des appels :** Tester les appels bidirectionnels audio et vidéo pour chaque modèle de téléphone.
- **Validation annuaire :** Tester l'accès à l'annuaire depuis les écrans des téléphones et effectuer des appels via celui-ci.
- **Bancs 3 à 6 :** Inventorier, câbler et déployer les équipements réseau et téléphoniques pour ces bancs.
- **Routes statiques :** Examiner la route générale du VLAN 407 vers le PBX pour supprimer les routes statiques temporaires (`/32`) ajoutées sur le serveur.
- **Sauvegarde :** Mettre en place une procédure de sauvegarde automatisée (base PostgreSQL, configurations) et tester sa restauration.
- **Sécurité :** Audit complet des règles iptables du PBX et des règles inter-VLAN.

**Source :** Synthèse des sections "Reste à faire" et "Recette" des documents consultés.
