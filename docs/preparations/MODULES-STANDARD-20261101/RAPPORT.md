# Modules standard — installation brute du 1 novembre 2026

**Statut : 🟡 installé/préparé, non testé, non raccordé.**

Ordre propriétaire : installer toute la sélection avant déplacement des serveurs, sans tests, sans nouveau moteur, sans toucher aux missions ni redémarrer les serveurs. Les raccordements et essais seront faits au lycée. Suivi ouvert : [issue #42](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/issues/42).

## Emplacement et périmètre

Installation centralisée sur le **Mac mini JARVIS sous Debian**, dans `/home/adminjarvis/JARVIS/modules-standard-20261101`. Aucune installation sur les Dell ni sur un équipement du lycée. Les connecteurs centralisés utiliseront ultérieurement les accès réseau fournis par le propriétaire.

Sources amont téléchargées et révisions figées dans `sources-lock.json` et `manifest.json`. Environnements Python séparés, préfixes npm locaux et versions exactes conservées. Python 3.12 géré et Node 24 installés localement pour les dépendances compatibles ; Python et Node système inchangés. Aucun moteur Hermes, Claude ou autre agent ajouté. Les scripts joints sont des outils ponctuels d'installation et d'inventaire, pas un exécuteur de missions.

Documents relus : `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, états PR35/38/39/40/41 et installation Skills historique. La règle standard-first PR41 est conservée. L'installateur historique Skills25 n'a pas été utilisé : il modifierait le runtime et redémarrerait des services, hors demande actuelle.

## Installation réalisée

Les commandes d'installation ci-dessous sont terminées avec code retour 0. Cela démontre l'installation des paquets, **pas leur fonctionnement**.

| Élément | Version / préparation | État |
| --- | --- | --- |
| Open Terminal, MCPO, WebUI, Qwen Code, SSH, LibreOffice | Réemploi des installations existantes, aucune réinstallation | Inchangés |
| Office / PDF | python-docx 1.2.0, python-pptx 1.0.2, openpyxl 3.1.5, reportlab 5.1.0, pypdf 6.21.2, pdfplumber 0.11.10, pypdfium2 5.14.0, PyMuPDF et pytesseract | Installés, non testés |
| OCR | Tesseract, bibliothèques et données français/anglais/OSD extraits de paquets Debian dans `sysroot/` | Préparés sans modification du système, non testés |
| Pandoc | Distribution binaire via pypandoc_binary 1.17 ; source connecteur `dullroar/pandoc_mcp` et environnement dédié | Installés/préparés, non testés |
| MarkItDown / MCP | 0.1.9 / 0.0.1a8 ; extras PDF/DOCX/PPTX/XLSX | Installés, non testés |
| Fetch MCP | 2026.10.28 | Installé, non testé |
| Filesystem MCP | 2.1.0 | Installé, non configuré |
| Ansible | core 2.21.5, lint 26.10.1, navigator 26.10.0 | Installés, aucun playbook exécuté |
| Ansible Development Tools MCP | npm `@ansible/ansible-mcp-server` 26.6.0 | Installé, non testé |
| Collections Ansible | ansible.windows 3.9.2, microsoft.ad 1.12.1, cisco.ios 11.6.0 ; dépendances netcommon 8.7.1, utils 6.1.1 | Installées dans `collections/`, aucun accès distant |
| Cisco pyATS MCP | 1.0.0 et pyATS 26.9 | Installés, testbed à fournir |
| pfSense MCP | Source gensecaihq, 1.1.0 | Installé ; aucun paquet ajouté au pare-feu |
| Nagios MCP | 0.1.4 | Installé ; cible Nagios Core à renseigner |
| NetBox Enhanced | 1.1.1 | Installé, lecture/écriture à raccorder |
| NetBox officiel | 1.2.2, environnement séparé | Installé comme référence/solution de repli, aucun doublon actif |
| Draw.io MCP | 1.10.1 | Installé, non testé |
| Playwright MCP | 0.0.84 ; Chromium et headless shell révision1252, FFmpeg téléchargés | Installés, navigateur jamais lancé |
| GitHub MCP officiel | Binaire v2.0.3 Linux x86_64, SHA256 comparé au checksum de la distribution officielle | Installé, jamais exécuté ; accès JARVIS existants conservés |

Le manifeste JSON joint contient les révisions exactes des sources, toutes les versions Python, les collections, les dépendances npm principales, les empreintes des Skills et les paquets OCR. Les verrous npm complets, fichiers `*-packages.lock` et journaux sont conservés sur le serveur dans ce même dossier.

## Les 18 Skills préparés

Copies indépendantes avec scripts, références et licences amont dans `skills/` :

- Nous Research : `microsoft-office`, `pdf`.
- Learning Commons : `k12-lesson-plan-creation`, `k12-lesson-differentiation`, `k12-lesson-prep`, `k12-check-for-understanding`.
- Gareth Manning : `criterion-referenced-rubric-generator`, `assessment-validity-checker`, `competency-unpacker`, `learning-progression-builder`, `project-brief-designer`, `differentiation-adapter`, `competency-framework-translator`, `progressive-hint-ladder`, `error-analysis-protocol`.
- Autres : `devops-engineer`, `netbox-mcp-operator`, `drawio`.

La bibliothèque pédagogique complète est téléchargée dans `sources/education-skills`, mais seuls ces neuf Skills ont été copiés dans la sélection. Les licences MIT, Apache-2.0 et CC BY-SA4.0 sont conservées ; respecter l'attribution et les conditions applicables. Les licences des dépendances Cisco et des composants optionnels restent distinctes.

**Ces Skills sont installés comme candidats sur disque ; ils ne sont pas encore chargés dans le registre actif JARVIS ni dans les clients natifs.** Aucun moteur propriétaire ou filtre de création de missions n'est réactivé. L'exposition WebUI/Qwen Code sera traitée au lycée via le socle existant.

`documents.env` indique l'interpréteur Office/PDF et les chemins OCR/Pandoc. Ce fichier n'est pas chargé automatiquement et ne modifie aucun environnement actif. Inventaire Ansible vide et fiche de raccordement dans `connection-templates/` ; aucun secret ni adresse du lycée inventés.

## Préservation et limites

- Aucune commande de reboot, restart/reload, activation ou lancement de service exécutée.
- Aucun test fonctionnel, appel MCP, génération de document, lancement de navigateur ni commande sur une machine cible pendant cette installation.
- Aucune base de missions, mémoire, MANUAL-HOLD, configuration active WebUI/MCPO ou identité modifiée.
- Aucune fusion main. Documentation publiée sur branche dédiée issue de PR41.
- Les contrôles effectués se limitent aux codes retour des installateurs, à la lecture des métadonnées, aux fichiers téléchargés et au checksum du binaire GitHub. Ils ne constituent pas une réception opérationnelle.
- Les fonctions optionnelles dépendant de `marker-pdf`, `nano-pdf` ou de modèles externes ne sont pas installées ; aucun modèle supplémentaire téléchargé. Draw.io Desktop pour les exports facultatifs n'est pas installé. La compatibilité des bibliothèques natives du navigateur, l'OCR, les transports MCP et les documents sera vérifiée demain.

## À suivre au lycée — 2 novembre

1. Fournir la liste réelle et le périmètre autorisé : Linux, Windows/AD, Cisco, pfSense, Nagios, NetBox ; associer chaque rôle à la bonne machine.
2. Après déplacement, relever adresses/DNS/routes et accès ; confirmer les empreintes SSH. La découverte ne doit couvrir que les cibles/plages explicitement autorisées, aucun balayage implicite.
3. Renseigner inventaire Ansible, transports Windows, testbed Cisco, URL/API et références privées des secrets. Vérifier versions IOS, Nagios Core/CGI et disponibilité pfSense REST APIv2. Aucun paquet pfSense installé automatiquement.
4. Choisir NetBox Enhanced comme connecteur actif pour lecture/écriture ; conserver l'officiel comme référence sans les exposer ensemble par défaut.
5. Raccorder les MCP et Skills aux mécanismes natifs WebUI/Qwen Code/MCPO existants ; définir les répertoires Filesystem et les droits selon le périmètre réel. Préserver les accès Google/GitHub existants et les missions en pause.
6. Fournir référentiels français CIEL/BTS, gabarits de TP/corrigé et règles d'attribution des ressources pédagogiques.
7. Exécuter seulement alors les essais réels : lecture/écriture ciblées, états machines, comparaisons de fichiers, codes retour et arrêt après réussite/échec ; contrôle visuel Office/PDF/schéma et preuves documentées.

Le suivi est volontairement **ouvert** dans l'issue42 ; l'installation brute ne clôture pas les raccordements ni la découverte.
