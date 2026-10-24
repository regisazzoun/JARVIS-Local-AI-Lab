# Mission 26 — Complément anti-boucle et diagnostic de fond

**Décision du propriétaire : 24 octobre 2026.**  
**Statut : 📋 documentation préparatoire, non exécutée.**  
**Portée : toutes les missions JARVIS, y compris celles coordonnées par Codex et JL-03.**

## Décision
Le seuil de **trois tentatives infructueuses comparables** est un garde-fou permanent : arrêter la répétition à l'identique, inspecter les messages d'erreur, journaux, fichiers et résultats d'outils, ouvrir automatiquement une **sous-mission corrective**, corriger et vérifier, puis reprendre la mission initiale au checkpoint. Si la cause est claire dès le premier échec, la corriger immédiatement sans attendre trois essais. Ni sous-missions correctives récursives à l'infini, ni déclaration de succès sans preuve. Garder les autres étapes indépendantes actives.

## Diagnostic de fond indispensable
Le propriétaire ne souhaite pas un simple pansement : comprendre **pourquoi** JARVIS boucle régulièrement. Étudier transversalement les incidents documentés, notamment missions 25, 26 (préparatoire), TTS-01, JL-03 et missions agentiques pertinentes. Distinguer, preuves à l'appui :
- raisonnement du modèle et adaptation de stratégie après erreurs ;
- visibilité et précision des retours d'outils, erreurs et journaux ;
- orchestration, checkpoints, état des tentatives et détection des doublons ;
- mémoire de travail/contexte et réutilisation d'un diagnostic antérieur ;
- vérifications superficielles qui acceptent une réponse déclarative sans résultat réel ;
- interventions réelles de Codex qui débloquent JARVIS.

Aucune cause unique n'est présumée. Les trois essais sont un **plafond pour une stratégie inchangée**, pas un minimum de tentatives.

## Comportement du Mission Engine
1. Journaliser l'identité de l'opération, cible, signature normalisée de l'échec, paramètres, sorties, preuves et évolution de stratégie.
2. Détecter trois échecs équivalents et bloquer une quatrième répétition identique.
3. Créer dans **le moteur existant** une sous-mission corrective liée avec analyse, hypothèses, action distincte, tests et critère de reprise.
4. Exécuter et vérifier indépendamment l'effet réel de la correction ; réouvrir ensuite l'étape initiale au dernier checkpoint valide.
5. En cas d'échec non récupérable, exposer « bloqué » avec cause et preuves, sans masquer l'historique et sans boucler.
6. Produire un bilan chiffré des échecs corrigés **par JARVIS seul** et des corrections ayant nécessité Codex, et mesurer les répétitions évitées. Ne pas utiliser le nombre brut de tests comme substitut d'autonomie.

## Conservation et limites
Préserver la mission 25 reçue avec réserves, le broker, les skills actifs, la mémoire et les services actuels. Ne pas relancer maintenant la mission 26 ni JL-03 ; aucune modification immédiate d'un processus tournant. Pas de nouvelle validation humaine intermédiaire pendant les opérations déjà autorisées. Aucun nouveau moteur parallèle, aucune réinstallation ou fusion automatique dans main.

**Référentiel lu :** `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, `docs/missions/26/MISSION.md`, rapport de réception 25 et compte rendu 23D/TTS-01 vus dans le projet. **Autorisations préservées :** exécution autonome après lancement et conservation des acquis. **Écarts :** aucun signalé.

**Références :** [PR 18 — mission 25](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/18) ; [Mission 26 préparée](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/blob/plan/mission-26-moteur-agentique/docs/missions/26/MISSION.md).
