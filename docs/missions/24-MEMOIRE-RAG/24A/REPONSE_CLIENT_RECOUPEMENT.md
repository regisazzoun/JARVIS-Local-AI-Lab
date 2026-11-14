# Réponse effectivement affichée — recoupement sur copie

**14 novembre 2026. Mode extractif : passages choisis par Qwen, résolus dans les textes originaux et contrôlés par le client. Ce n’est pas une observation live PBX/Cisco ni une validation du RAG général. Expurgation de publication seulement.**

## État documentaire de la téléphonie

Documents lus le **2026-11-14**. Recoupement par extraits vérifiés : les constats de chaque source restent distincts, avec leurs dates et leur portée. Aucune vérification live du PBX ou des switches n’est revendiquée.

### Réseau

**Source [1] — Salle 407 — Architecture réseau et six bancs élèves** (modification : 2026-11-12T13:08:50.063Z)

> État vérifié le 12 novembre 2026 après récupération du 3560G du banc 2. Les deux centraux, les deux têtes et les deux 3560G ont été relus en SSH authentifié. Po1 est actif en trunk sur les bancs 1 et 2. Les bancs 3 à 6 restent à inventorier et déployer. [1]

### IPBX

**Source [2] — FusionPBX — Installation, configuration et exploitation — SEP CIEL — 13-11-2026** (modification : 2026-11-13T20:41:26.009Z)

> Au contrôle du 13 novembre, FreeSWITCH, Nginx et PostgreSQL sont actifs. Les quatre profils SIP sont chargés. Les onze extensions [EXTENSION EXPURGÉE] à [EXTENSION EXPURGÉE] sont actives et enregistrées par des téléphones physiques. Un enregistrement SIP confirme l’authentification et la présence du poste à cet instant. La validation de tous les appels, de chaque caméra et de la persistance après une coupure électrique reste une étape distincte. [2]

### Téléphones

**Source [3] — Salle-407-Documentation-deploiement.md** (modification : 2026-11-13T20:39:38.159Z)

[PASSAGE D’AUTHENTIFICATION EXPURGÉ — contenu conservé uniquement en copie privée]

**Source [2] — FusionPBX — Installation, configuration et exploitation — SEP CIEL — 13-11-2026** (modification : 2026-11-13T20:41:26.009Z)

> [EXTENSION EXPURGÉE] — Cisco SPA504G — Salle 407 - poste 01 [2]

### SIP : évolution entre les constats

**Source [2] — FusionPBX — Installation, configuration et exploitation — SEP CIEL — 13-11-2026** (modification : 2026-11-13T20:41:26.009Z)

> Au contrôle du 13 novembre, FreeSWITCH, Nginx et PostgreSQL sont actifs. Les quatre profils SIP sont chargés. Les onze extensions [EXTENSION EXPURGÉE] à [EXTENSION EXPURGÉE] sont actives et enregistrées par des téléphones physiques. Un enregistrement SIP confirme l’authentification et la présence du poste à cet instant. La validation de tous les appels, de chaque caméra et de la persistance après une coupure électrique reste une étape distincte. [2]

**Source [1] — Salle 407 — Architecture réseau et six bancs élèves** (modification : 2026-11-12T13:08:50.063Z)

> Les ports Gi0/1–12 du 3560G sont en access VLAN407. Dix MAC de téléphones sont apprises et leurs IP sont recoupées avec les entrées ARP du cœur et, pour plusieurs téléphones, les annonces CDP. Gi0/8 porte [MAC EXPURGÉE] et 192.4.7.65. Les autres IP observées vont de [ADRESSE EXPURGÉE] à .64. La recette SIP et les appels restent à réaliser. [1]

### Appels

**Source [3] — Salle-407-Documentation-deploiement.md** (modification : 2026-11-13T20:39:38.159Z)

> Appels avec audio validés par l’utilisateur uniquement entre [EXTENSION EXPURGÉE] et [EXTENSION EXPURGÉE]. Tester les appels du [EXTENSION EXPURGÉE] dans les deux sens. [3]

### Reste à faire relaté dans les sources

**Source [3] — Salle-407-Documentation-deploiement.md** (modification : 2026-11-13T20:39:38.159Z)

> Profil [PROFIL EXPURGÉ].xml reçu avec HTTP 200, dictionnaire français reçu avec HTTP 200. Configuration active : [EXTENSION EXPURGÉE], serveur [ADRESSE EXPURGÉE]:5060 UDP, nom Banc 1, français, fr.pool.ntp.org, Paris avec heure d’été automatique, format 24 h. L’heure affichée est cohérente. Le service XML « Salle 407 » est configuré vers l’annuaire central existant de onze contacts et l’accès HTTP est autorisé pour ce poste. L’ouverture du répertoire sur l’écran physique et un appel avec audio restent à tester. [3]

**Source [1] — Salle 407 — Architecture réseau et six bancs élèves** (modification : 2026-11-12T13:08:50.063Z)

> État vérifié le 12 novembre 2026 après récupération du 3560G du banc 2. Les deux centraux, les deux têtes et les deux 3560G ont été relus en SSH authentifié. Po1 est actif en trunk sur les bancs 1 et 2. Les bancs 3 à 6 restent à inventorier et déployer. [1]

### Lecture des écarts

Un inventaire de téléphones repérés, un enregistrement SIP, un détail de provisioning et un appel validé décrivent des critères différents. Ils ne sont pas fusionnés en un nombre, un emplacement ou une recette globale. Les points ouverts ci-dessus sont ceux relatés à leurs dates ; une absence documentaire ne prouve pas une absence de déploiement.

### Sources effectivement lues

- [1] [Salle 407 — Architecture réseau et six bancs élèves](https://docs.google.com/document/d/1acU_Eldah1TP1ogSj2zdLsPuQmQCDAVamp6h80i5wyk/edit)

- [2] [FusionPBX — Installation, configuration et exploitation — SEP CIEL — 13-11-2026](https://docs.google.com/document/d/176Ui1LYH2doDGX7mpaQmX75EprSesGQrSkT_E0l9oQw/edit)

- [3] [Salle-407-Documentation-deploiement.md](https://drive.google.com/file/d/1Brl27YGD0KcP7_mTFLPj1-ZBsBge3KKj/view)
