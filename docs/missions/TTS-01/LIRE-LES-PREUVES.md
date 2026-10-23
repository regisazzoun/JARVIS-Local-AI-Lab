# Lire les preuves TTS-01

La campagne reste en cours. Aucun moteur TTS ni échantillon vocal réel n’est encore reçu dans cet instantané ; les WAV silencieux des essais d’outillage ne sont pas les livrables de synthèse.

- `PLANS-ET-CHECKPOINTS.json` décrit les versions, auteurs et états conservés. Les anciens plans complets restent dans SQLite ; leur empreinte globale est publiée.
- `PREUVES-JARVIS.json` exporte les appels réels du worker. Les corps répétés de catalogues/plans sont remplacés par leurs empreintes ; les originaux restent dans le journal canonique.
- `REPRISE-ARCHIVE-JARVIS.json` contient les trois appels réels effectués par JARVIS dans la conversation JL-02 existante sur coordination Codex. Leur lien avec le checkpoint est explicite ; ils ne sont pas déguisés en appels du worker.
- `VERIFICATION-INVENTAIRE.json` distingue le PASS du petit contrôle technique T01 des réserves de sa prose.
- `JARVIS-ARCHIVE-BLOCAGE-INITIAL.md` et `JARVIS-ARCHIVE-ANALYSE-INITIALE.md` sont des originaux erronés, pas des références factuelles : le premier invente un refus de politique ; le second conserve cette cause et donne des calculs faux sans mesurer le signal.
- `REFERENCES-SIGNAL-INDEPENDANT.json` fournit les mesures CodeX indépendantes sur les fichiers originaux. Ce travail n’est pas attribué à JARVIS. La tâche complémentaire T09 doit lui faire utiliser la sonde enrichie et produire son analyse rectifiée.
- `TEST-TRANSPORT-INITIAL.json` conserve le premier test Codex qui masquait une absence de commande par le succès final du shell. `TEST-TRANSPORT-GPU.json` conserve le retest corrigé, avec vrai contrôle GPU et transfert byte-identique.
- `TEST-AUDIO-API.json` et `TEST-LECTURE-NAVIGATEUR.json` reçoivent l’infrastructure audio privée avec une fixture silencieuse. Ils ne reçoivent ni voix TTS ni écoute physique.

Les exports `jarvis/` conservent la prose du modèle et ses erreurs. Un état `validated` reçoit les prédicats précis de la tâche à cet instant ; il n’annule pas une réserve indépendante concernant la justesse du rapport. Les corrections et errata ont priorité lorsqu’ils sont explicitement liés à ces originaux.

Aucun extrait de film, archive audio privée, mot de passe ou clé n’est publié. Les rapports historiques26 et la clôture incomplète26B restent inchangés.
