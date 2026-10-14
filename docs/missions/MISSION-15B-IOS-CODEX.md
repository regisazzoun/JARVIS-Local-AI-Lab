# Mission Codex 15B — Application native JARVIS pour iOS
**Statut : CAHIER DE MISSION PRÊT — NON EXÉCUTÉ**  
**Date : 14 octobre 2026**  
**Branche de travail suggérée :** `codex/mission-15b-ios`

## Objectif
Construire une application SwiftUI pour iPhone, extensible à iPad, pouvant accéder à JARVIS sur le Mac mini sans attendre le Dell. **Contrainte validée : installation GRATUITE pour l'instant** depuis Xcode avec compte Apple personnel (Personal Team). Ni abonnement Developer, ni TestFlight payant, ni publication App Store requis pour le prototype.

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
1. **15B.1 — Architecture mobile** : reprendre le contrat commun défini avec 15A, créer un projet Xcode iOS SwiftUI, navigation adaptée au tactile, support des tailles d'écran, permissions minimales.
2. **15B.2 — Connexion sécurisée** : profils serveur, HTTPS/tunnel privé, authentification trousseau, erreurs d'accès hors réseau ; respecter la mission 13D SSH/Tailscale reportée (ne pas modifier les accès existants).
3. **15B.3 — Voix et conversation** : texte fonctionnel prioritaire ; microphone avec permission explicite, Push-to-Talk et lecture TTS si endpoints attestés. Ne pas promettre écoute permanente en arrière-plan, réveil vocal ou accès illimité au bouton Action/Siri.
4. **15B.4 — Mémoire et validations** : afficher les souvenirs et décisions autorisés, permettre les approbations explicites sécurisées quand le backend les expose ; notifications locales facultatives, push distant uniquement après vérification des entitlements disponibles dans le compte gratuit.
5. **15B.5 — Installation gratuite et réception** : documenter précisément Xcode, connexion d'un iPhone personnel, Developer Mode si requis, choix Personal Team, signature automatique, déploiement, résolution des erreurs de provisioning et renouvellement des profils/app après environ 7 jours. Prévoir une PWA séparée comme solution de repli, sans remplacer silencieusement l'application native.

## Premier incrément à réaliser en priorité
Un prototype iPhone installable gratuitement : écran configuration serveur, état réel de connexion, chat texte si API existante, indication hors-ligne, authentification. En l'absence d'un iPhone/Xcode accessible, livrer un projet reproductible et un rapport « installation physique non testée » ; ne pas inventer une installation réussie.

## Critères GO / réserves
- Projet SwiftUI iOS livré, reproductible et compilé si environnement Xcode disponible.
- Installation physique sur iPhone testée si l'appareil est accessible ; sinon réserve explicite.
- Aucun coût obligatoire, aucune obligation d'App Store, aucun certificat partagé dans le dépôt.
- Voix et mémoire testées seulement si API/permissions réelles disponibles ; alternatives et limitations documentées.

## Prompt de lancement Codex
> Exécute la mission 15B définie dans ce fichier. Commence par relever les API/réserves 13F et vérifier le contrat partagé avec 15A. Construis d'abord un prototype natif iPhone SwiftUI, installable gratuitement via Xcode et Personal Team, sans achat ni abonnement. Travaille sur branche et propose une PR. Ne touche pas à la configuration serveur ni aux accès réseau sans validation. Rapporte exactement quels tests ont été réalisés sur simulateur, Mac ou iPhone physique, puis conclus GO / GO AVEC RÉSERVES / NO-GO.
