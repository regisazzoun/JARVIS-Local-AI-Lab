# Vérifications avant publication

14 octobre 2026. Base GitHub main : `3650860eed5a7a0a148da6b2ea952ac942eb434b`, inchangée au dernier contrôle avant commit.

- Huit fichiers historiques : mêmes chemins et mêmes empreintes Git ; aucun remplacement ou déplacement.
- Première livraison : 744 ajouts, contenus locaux et blobs distants comparés un à un par empreinte Git. Les deux documents de clôture sont ajoutés ensuite.
- Empreintes SHA-256 des copies et de tous les membres des 71 paquets contrôlées ; aucun écart.
- Aucun fichier publié ne dépasse 100 Mio ; plus grand paquet : 1 645 271 octets.
- Contrôle des clés privées et formats de jetons sur les fichiers retenus ; contrôle prudent préalable du contenu textuel, des noms privés et traces d’authentification. Fichiers suspects exclus, sans prétendre certifier automatiquement toute donnée personnelle.
- Navigation documentaire générée : zéro lien non résolu. 205 liens historiques non résolus recensés dans LIENS.json ; les originaux restent inchangés.
- `git diff --cached --name-status` : uniquement des ajouts. `git diff --check` signale des espaces historiques ; ces contenus ne sont pas réécrits.
- Le `.gitignore` historique exclut archives et dossiers de preuves. Ajout explicite uniquement des fichiers contrôlés autorisés par la mission ; ce fichier reste inchangé. Aucun ajout de base, `.env` ou clé privée.
- Aucune commande de modification des services, réseau, Docker, pilotes ou modèles. Aucun script historique exécuté. Le dépôt déployé sous /opt/jarvis/conversation reste hors espace de travail ; ses changements locaux sont conservés et des travaux concurrents peuvent continuer pendant la collecte.
- Snapshot local indépendant créé via connecteur, faute d’authentification Git CLI. Son commit de base local est un snapshot, pas une réécriture du dépôt distant. Le commit distant a pour parent le vrai commit main cité ci-dessus.

Limites : cinq sources ont rencontré des refus de lecture, trois autres erreurs concernent des sockets hors documentation. Les détails sont dans ERREURS.json. Les modèles, bases runtime et historiques Codex/shell ne sont pas publiés. Les validations restent historiques ; aucun nouvel essai serveur n’a été lancé.
