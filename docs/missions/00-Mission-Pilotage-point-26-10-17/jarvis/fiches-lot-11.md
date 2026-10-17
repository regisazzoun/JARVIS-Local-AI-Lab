# Fiches Historiques — Lot 11 (Mission 00)

## Fiche 13A : Socle Vocal Isolé

- **Fonction** : Installation durable et isolée du socle vocal.
- **Objectif** : Déployer Whisper (small) et Piper (Tom) en mode offline, sans Ollama ni réseau.
- **Matériel/Composants** : Mac mini 2018, Debian 13 T2Linux. Moteurs dans `/opt/jarvis/voice`. Scripts `run-offline`, `voice_worker.py`.
- **Actions et Résultats** : Installation validée. Deux cycles de synthèse/transcription réussis avec quatre processus distincts. Tests sur disque permanent.
- **Réserves** : Validation limitée au périmètre des tests fichiers. Aucune activation systemd permanente.
- **Dépendances** : Python 3.13.5, Noyau `6.18.54-1-t2-trixie`.
- **Exécutant** : À confirmer (non attesté dans l'extrait).
- **Chemin** : `/home/adminjarvis/JARVIS/rapports/mission13a.md`.

## Fiche 13B : Passerelle et Mémoire

- **Fonction** : Test de la passerelle vocale et gestion de la mémoire.
- **Objectif** : Valider le flux audio et les contraintes de temps.
- **Matériel/Composants** : Non documenté spécifiquement. CUDA, Ollama, Open WebUI, Whisper, Piper mentionnés.
- **Actions et Résultats** : Synthèse Piper vers transcription Whisper validée sur phrase française fictive. Rejet d'audio vide/silence/durée excessive.
- **Réserves** : Rapport GO PARTIEL. Validation navigateur et Ollama réel non confirmés à cette étape.
- **Dépendances** : API backend testées sans transport HTTP.
- **Exécutant** : À confirmer.
- **Chemin** : `/home/adminjarvis/JARVIS-Documentation/missions/mission-13b/README.md`.

## Fiche 13C : Mémoire Structurée

- **Fonction** : Implémentation de la mémoire persistante structurée.
- **Objectif** : Tester SQLite et FTS5 pour le stockage des souvenirs.
- **Matériel/Composants** : Open WebUI, SQLite, FTS5. Base runtime initialement vide (hors schéma).
- **Actions et Résultats** : 9 tests unitaires/intégration passés. Migration idempotente vérifiée. Sauvegarde/restauration testée. Souvenir fictif retrouvé.
- **Réserves** : Rapport GO PARTIEL. Validation intégrée différée. Aucune donnée personnelle utilisée.
- **Dépendances** : API backend testées en direct.
- **Exécutant** : À confirmer.
- **Chemin** : `/home/adminjarvis/JARVIS-Documentation/missions/mission-13c/README.md`.

## Fiche 13D : Pilotage et Réception Historique

- **Fonction** : Suivi global des missions et réception historique.
- **Objectif** : Centraliser l'état des jalons (03 à 14) et documenter les réserves.
- **Matériel/Composants** : Non spécifié dans cet extrait de suivi. Références croisées vers Dell 13D-E / 14.
- **Actions et Résultats** : Tableau de pilotage permanent maintenu. Réception complète validée pour certaines étapes (ex: 17/10 à 15h09). Mise en garde contre l'interprétation des anciens rapports incomplets.
- **Réserves** : Certains états intermédiaires historiques non consolidés. Ne pas déduire un GO de la seule existence de fichiers.
- **Dépendances** : [Feuille de route](ROADMAP.md), Chronologie, Débrief 13F.
- **Exécutant** : À confirmer (document de suivi).
- **Chemin** : `/home/adminjarvis/JARVIS/mission00/SUIVI.md`.

---
*Note : Ces fiches synthétisent les données extraites des rapports historiques cités. Les résultats reflètent l'état à la date de production des documents source et ne constituent pas une validation du système actuel.*