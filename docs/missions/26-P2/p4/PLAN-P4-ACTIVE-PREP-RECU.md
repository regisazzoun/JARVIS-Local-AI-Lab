# Plan préparatoire P4-ACTIVE-PREP

Le plan moteur est en version3 ; sa couverture a reçu PASS dans event:66089. Ce PASS concerne la couverture du plan, pas le déploiement ni la réception globale P4.

Cette tâche prépare l’intégration. Aucun déploiement de l’attestation applicative n’est reçu dans ce rapport. Les étapes ci-dessous sont des propositions de travail, pas des opérations déjà exécutées.

### Étape 1 : Acquérir les métadonnées du candidat worker reçu65474  
- **Source** : paquet préparatoire 65528/65537 (précédemment consulté).  
- **Objectif** : identifier unités, chemins, configurations, versions.  
- **Preuve** : event:66368 (`host_service` slot2 actif, unité `jarvis-mission-worker@2.service`).  
- **Limites** : aucune lecture redondante (`active_task.objective`).

### Étape 2 : Analyser les preuves nécessaires du code chargé  
- **Critères** :  
  - Fraîcheur du rapport de démarrage (timestamp, signature, source).  
  - Code chargé réellement exécuté (pas seulement fichier présent ou PID actif).  
  - Observation du service par `host_service show/status/is-active` ; cela ne prouve pas le code Python chargé. Une attestation du processus reste nécessaire.  
- **Observation historique** : event:66368 (`host_service show` slot2 → active) ; aucune preuve du code chargé n’en est déduite.

### Étape 3 : Proposer une intégration progressive  
- **Canari** : slot2 actif (observé via `host_service`, non fichier/PID seul).  
- **Retour arrière** : chemin distinct par worker/slot, préservation des autres workers.  
- **Limites** : aucune exécution, seulement une proposition documentée.

### Étape 4 : Produire le rapport final  
- **Format** : compact, fondé sur les reçus, avec canari/rollback explicitement futurs.  
- **Chemin** : `/var/lib/jarvis/projects/mission26-phase2/plan-P4-ACTIVE-PREP.md`.  
- **Vérification** : `mission_verify active:0`, sans nouvelle exécution.

Des vérifications antérieures du rapport ont échoué : event:66872 (FAIL), event:67201 (FAIL) et event:67634 (FAIL). Leurs résultats et les brouillons originaux restent conservés ; ils ne deviennent pas des réussites du rapport courant.

La rectification event:66904 retire quatre reproches du contrôleur, sans annuler le FAIL historique de event:66872. L’erratum sur la date est conservé séparément dans le dossier de preuves ; aucun horodatage de rédaction exact n’est requis ici.

Codex a rectifié les références factuelles du rapport (event:67730). Le plan technique et la rédaction initiale restent attribués à JARVIS. Cette assistance ne démontre pas une autocorrection autonome de la rédaction par JARVIS.

La vérification finale doit relire ce fichier avec mission_verify active:0. La préparation et P4 restent non reçues avant leurs contrôles respectifs. Aucun rejeu des campagnes P2/P3/candidat n’est demandé.
