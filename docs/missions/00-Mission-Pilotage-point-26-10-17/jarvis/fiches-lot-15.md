# Fiches Lot 15 — Mission00 (2026-10-17)

## 00 — Pilotage
Fonction: Audit et réception documentaire.
Objectif: Compléter audit GitHub et délégations réelles pour le bilan du 17/10.
État: 🟡 En cours de réception documentaire.
Réserves/Dépendances: Assistance Codex requise ; preuves JARVIS en cours. Non validation globale 14A.
Exécutant: Àconfirmer (assistance Codex/JARVIS).
Preuve: host_audit_read SUIVI.md, id 00.
Chemin lu: /home/adminjarvis/JARVIS/mission00/SUIVI.md

## 13D.1 — MacBook : Tailscale, SSH clé/mot de passe
Fonction: Connexion SSH double méthode sur MacBook via Tailscale.
Objectif: Valider accès par clé publique et mot de passe sans retirer existants.
État: ✅ Validée le 15/10.
Réserves/Dépendances: Clé publique ajoutée ; configuration serveur préservée.
Exécutant: Utilisateur (tests du 15/10).
Preuve: host_audit_read SUIVI.md, id 13D.1.
Chemin lu: /home/adminjarvis/JARVIS/mission00/SUIVI.md

## 13D.2 — MacBook : alias SSH, reconnexion, tmux
Fonction: Alias `ssh jarvis`, gestion sessions et tmux.
Objectif: Faciliter accès distant avec préservation sessions et reprise flexible.
État: ✅ Validée le 15/10.
Réserves/Dépendances: Alias fonctionnel ; sessions préservées ; test jarvis-test réussi.
Exécutant: Utilisateur (tests du 15/10).
Preuve: host_audit_read SUIVI.md, id 13D.2.
Chemin lu: /home/adminjarvis/JARVIS/mission00/SUIVI.md

## 13D.3 — Accès multi-postes macOS (Mac mini & MacBook)
Fonction: Validation accès SSH/Tailscale sur Mac mini et MacBook, secours.
Objectif: Confirmer fonctionnement multiposte sans modifier configuration serveur.
État: 🟡 Accès multi-postes validés, contrôles finaux à compléter.
Réserves/Dépendances: Mac mini confirmé 14/10 ; MacBook testé 15/10.
Exécutant: Utilisateur (tests 14-15/10).
Preuve: host_audit_read SUIVI.md, id 13D.3.
Chemin lu: /home/adminjarvis/JARVIS/mission00/SUIVI.md

## 15A.1 — MacOS : Inventaire & Architecture
Fonction: Examiner livrables 13F, vérifier prérequis Mac/Xcode, arrêt contrat API commun 15B.
Objectif: Produire schéma d'architecture et maquettes simples.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Réserves 13F à relever ; contrat 15A-15B à arrêter.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15A-MACOS-CODEX.md, outline item 1.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15A-MACOS-CODEX.md

## 15A.2 — MacOS : Connectivité HTTP(S) asynchrone
Fonction: Client asynchrone, profils serveur, indicateur connecté/hors ligne, auth, timeout/reconnexion.
Objectif: Robustesse réseau sans ouverture serveur Internet pour tests.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Profils configurables ; erreurs explicites à implémenter.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15A-MACOS-CODEX.md, outline item 2.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15A-MACOS-CODEX.md

## 15A.3 — MacOS : Conversation / voix / mémoire
Fonction: Texte avec historique, streaming si existant, PTT, lecture audio, consultation mémoire seule.
Objectif: Interaction sécurisée ; accord explicite avant écriture mémoire.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: APIs réelles à valider ; premier jalon lecture seule.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15A-MACOS-CODEX.md, outline item 3.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15A-MACOS-CODEX.md

## 15A.4 — MacOS : Pilotage des missions
Fonction: Interface consultation état, journaux expurgés, approbations ; pas d'exécution distante arbitraire.
Objectif: Contrôle strict serveur ; contournement local interdit.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Backend approvals à exposer ; validation journaux.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15A-MACOS-CODEX.md, outline item 4.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15A-MACOS-CODEX.md

## 15A.5 — MacOS : Distribution & Tests
Fonction: Projet Xcode compilable, .app local, validations texte/voix, tests unitaires réseau/hors ligne.
Objectif: Documentation installation/désinstallation ; tests réels selon matériel.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Matériel disponible ; scénarios hors ligne à valider.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15A-MACOS-CODEX.md, outline item 5.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15A-MACOS-CODEX.md

## 15B.1 — iOS : Architecture mobile SwiftUI
Fonction: Reprendre contrat commun 15A, projet Xcode iOS SwiftUI, navigation tactile, permissions minimales.
Objectif: Support tailles d'écran ; base cohérente avec MacOS.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Contrat 15A à finaliser ; entitlements Apple à vérifier.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15B-IOS-CODEX.md, outline item 1.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15B-IOS-CODEX.md

## 15B.2 — iOS : Connexion sécurisée & authentification trousseau
Fonction: Profils serveur, HTTPS/tunnel, auth Keychain, erreurs hors réseau ; respecter 13D.
Objectif: Sécurité renforcée sans modifier accès SSH/Tailscale existants.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Mission 13D reportée à respecter ; profils provisionning.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15B-IOS-CODEX.md, outline item 2.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15B-IOS-CODEX.md

## 15B.3 — iOS : Voix et conversation
Fonction: Texte prioritaire, micro avec permission explicite, PTT, TTS si endpoints attestés.
Objectif: Pas d'écoute arrière-plan ni réveil vocal/promesse bouton Action/Siri.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Endpoints API à valider ; permissions iOS strictes.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15B-IOS-CODEX.md, outline item 3.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15B-IOS-CODEX.md

## 15B.4 — iOS : Mémoire et validations
Fonction: Affichage souvenirs/décisions autorisés, approbations explicites sécurisées.
Objectif: Notifications locales facultatives ; push distant après vérification entitlements compte gratuit.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Backend approvals à exposer ; entitlements Apple gratuits limités.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15B-IOS-CODEX.md, outline item 4.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15B-IOS-CODEX.md

## 15B.5 — iOS : Installation gratuite & réception
Fonction: Doc Xcode, iPhone personnel, Developer Mode, Personal Team, signature auto, déploiement, provisioning 7j.
Objectif: PWA séparée en repli sans remplacer app native silencieusement.
État: 📋 PRÉVU (non exécuté).
Réserves/Dépendances: Renouvellement profils/app à prévoir ; erreurs provisioning fréquentes.
Exécutant: Àconfirmer (désignation développeur SwiftUI).
Preuve: host_audit_read MISSION-15B-IOS-CODEX.md, outline item 5.
Chemin lu: /home/adminjarvis/JARVIS/mission00/docs/missions/MISSION-15B-IOS-CODEX.md
