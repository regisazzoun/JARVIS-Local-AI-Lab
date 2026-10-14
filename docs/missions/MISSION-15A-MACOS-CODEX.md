# Mission Codex 15A — Application native JARVIS pour macOS
**Statut : CAHIER DE MISSION PRÊT — NON EXÉCUTÉ**  
**Date : 14 octobre 2026**  
**Branche de travail suggérée :** `codex/mission-15a-macos`

## Objectif
Construire une application native macOS (Mac mini et MacBook), permettant de dialoguer avec JARVIS sur le Mac mini Debian et, plus tard, d'autres nœuds. Mission indépendante du déploiement Dell (14) et menée en parallèle de 15B iOS.

## Règles communes obligatoires
- Avant toute écriture, inventorier en lecture seule les rapports 13F, les réserves, les ports et endpoints réels, les schémas d'authentification, et la disponibilité des sources Mac/Xcode. Ne jamais inventer une route API ni annoncer une fonction validée sans essai.
- Ne modifier ni l'installation Debian du Mac mini, ni Ollama, Open WebUI, SQLite/FTS5, SSH/Tailscale, ni le Dell sans approbation explicite. Éviter tout secret, token ou adresse privée dans GitHub et les logs.
- Prévoir une couche API JARVIS versionnée et un contrat commun documenté : modèles conversation, messages, STT/TTS si exposés, souvenirs, tâches, approbations, état/santé et gestion d'erreurs. Marquer chaque endpoint EXISTANT / À ADAPTER / À CRÉER, avec preuve.
- Développer un client Swift/SwiftUI avec transport HTTPS ou tunnel privé sécurisé, authentification protégée par trousseau, sélection d'hôte configurable et aucun identifiant en dur. Les actions à risque exigent une confirmation explicite côté serveur.
- Prévoir un mode de démonstration avec données fictives si backend indisponible, clairement identifié et ne jamais le présenter comme une connexion réelle.
- Privilégier composants réutilisables et package Swift partagé; ne pas modifier la branche de l'autre mission. Convenir du contrat API avant intégration; travailler sur une branche dédiée et soumettre une PR plutôt que pousser directement sur main.
- Effectuer les tests possibles automatiquement et distinguer : code livré, compilation attestée, tests simulés, tests physiques et acceptation utilisateur.
- Livrer sources, mode d'emploi reproductible, rapport final, limites/réserves, captures possibles sans données sensibles, et propositions de mises à jour README/ROADMAP. Ne pas bloquer pour des anomalies cosmétiques mineures.

## Travaux attendus
1. **15A.1 — Inventaire / architecture** : examiner les livrables 13F et relever les réserves qui impactent les clients ; vérifier les prérequis Mac/Xcode, arrêter le contrat commun API avec 15B et produire le schéma d'architecture et des maquettes simples.
2. **15A.2 — Connectivité** : client HTTP(S) asynchrone, profils serveur configurables, indicateur réellement connecté/hors ligne, authentification, timeout, reconnexion et erreurs explicites. Aucun serveur ouvert sur Internet pour faciliter les tests.
3. **15A.3 — Conversation / voix / mémoire** : conversation texte avec historique affiché, streaming si existant, Push-to-Talk et lecture audio uniquement si les API réelles le permettent, consultation de mémoire validée en lecture seule dans le premier jalon ; demander accord explicite avant écriture de mémoire.
4. **15A.4 — Pilotage des missions** : interface pour consulter état, journaux expurgés et demandes d'approbation ; aucune exécution distante arbitraire depuis le client et pas d'approbation locale contournant les contrôles serveur.
5. **15A.5 — Distribution et tests** : projet Xcode compilable sur Mac disponible, .app local pour test sans publication, validations réelles de texte/voix selon matériel, tests unitaires du réseau et scénarios hors ligne, documentation installation et désinstallation.

## Premier incrément à réaliser en priorité
Un prototype macOS exécutable : choix du serveur, vérification /health réellement existante ou alternative documentée, conversation texte réelle si endpoint connu, état et erreurs visibles, et tests. Les fonctions vocales/agentiques non exposées restent indiquées « non disponibles » plutôt que simulées silencieusement.

## Critères GO / réserves
- Compilation locale prouvée sur macOS et ouverture de la fenêtre ; contrat API documenté.
- Connexion et échange texte prouvés sur backend réel OU signalés explicitement BLOQUÉS avec preuves et prototype autonome ; pas de faux GO.
- Aucune modification destructrice du Mac mini; aucune donnée privée publiée.
- Rapport final avec commandes, résultats, captures anonymisées et décisions restantes.

## Prompt de lancement Codex
> Exécute la mission 15A définie dans ce fichier. Commence par l'inventaire non destructif des API et des réserves de 13F puis développe un premier prototype macOS SwiftUI testable. Respecte les règles communes, coordonne le contrat d'API avec 15B, crée une branche et une pull request. N'affirme jamais un test réel non effectué, n'altère pas les services JARVIS existants, et termine par un rapport GO / GO AVEC RÉSERVES / NO-GO argumenté.
