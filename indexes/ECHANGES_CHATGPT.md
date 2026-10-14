# JARVIS — Index central des échanges ChatGPT

> **Fil principal de travail :** le projet JARVIS dans ChatGPT, conversation centrale en cours. Ce document organise les sujets **sans créer de nouveaux fils de discussion**. Il ne prétend pas être une transcription mot à mot de toutes les conversations : les synthèses ci-dessous proviennent des échanges accessibles et des rapports archivés.

**Dernière mise à jour documentaire : 14 octobre 2026.**

## Comment l'utiliser

Dans **la même conversation ChatGPT**, nommer simplement le thème ou la mission à reprendre (« reprenons la 13F », « Dell RAID », « Ollama »). L'assistant s'appuie sur cet index, les rapports GitHub et le contexte conversationnel accessible. Chaque décision ou bilan important est ajouté au dépôt, sans déplacer les échanges.

| Bloc | Sujet | Synthèse et sources |
| --- | --- | --- |
| **01** | Pilotage, architecture, priorités | [Architecture](../docs/01-architecture/README.md), [ROADMAP](../ROADMAP.md), [décisions](DECISIONS.md) |
| **02** | Mac mini, Debian et démarrage T2 | [Mac mini](../platforms/mac-mini/README.md), [mission 03](../missions/mission-03/README.md), [chronologie](CHRONOLOGIE.md) |
| **03** | Razer Core, GPU, CUDA et pilotes | [Parcours GPU](../docs/02-plateformes-gpu/README.md), [05D](../missions/mission-05d/README.md), [09B](../missions/mission-09b/README.md) |
| **04** | Ollama, Llama, Qwen, Open WebUI et qualité | [Services IA](../docs/03-services-ia/README.md), [06](../missions/mission-06/README.md), [10](../missions/mission-10/README.md) |
| **05** | Voix, mémoire et identité JARVIS | [12](../missions/mission-12/README.md), [13A](../missions/mission-13a/README.md), [13E](../missions/mission-13e/README.md) |
| **06** | Autonomie, outils et mission 13F | [13F](../missions/mission-13f/README.md), [état technique](ETAT_TECHNIQUE.md) |
| **07** | SSH, Tailscale, HTTPS et sécurité | [13D](../missions/mission-13d/README.md), [ROADMAP](../ROADMAP.md) |
| **08** | Dell Precision 5820, RAID 1, PXE et double RTX 3090 | [Dell](../platforms/dell-precision-5820/README.md), [ROADMAP](../ROADMAP.md), [mission 14](../missions/mission-14/README.md) |
| **09** | Missions Codex, preuves, archives et GitHub | [Inventaire](INVENTAIRE.md), [rapport de consolidation](RAPPORT_FINAL.md), [archives](../archives/README.md) |
| **10** | Exploitation pédagogique / BTS SIO | [ROADMAP](../ROADMAP.md) ; documentation pédagogique spécifique à compléter |

## Décisions issues des échanges (état au 14 octobre 2026)

- **Un seul fil de travail ChatGPT**, organisé conceptuellement par thèmes, et un **dépôt GitHub unique** pour la documentation pérenne. Les historiques ChatGPT ne sont pas déplacés ni fusionnés automatiquement.
- **Priorité immédiate : finaliser JARVIS sur Mac mini** (voix naturelle, transcription fiable, mémoire persistante/contrôlée, agent supervisé, fiabilité), puis préparer le Dell.
- **Mission 13F** : en cours dans les derniers échanges ; archives partielles, **aucun bilan final confirmé** au moment de la consolidation. Ne pas perturber ses processus ni inventer sa clôture.
- **Mission 13D** (SSH/Tailscale et clients distants) : **mise en attente volontairement** ; ne pas en faire un préalable bloquant.
- **Dell Precision 5820** : deux RTX 3090 envisagées, deux SSD NVMe extractibles, objectif RAID 1 avec séparation système/données ; contrôleur et compatibilité Debian à vérifier. Préparation PXE et automatisation envisagées, sans exécution destructive sans validation du périmètre.
- **Mission 14** : projet de mise en place Dell, pas de réalisation prouvée ; **mission 15 reportée**.
- **Philosophie** : laboratoire expérimental, privilégier les progrès mesurables sans s'enliser dans les anomalies mineures, conserver les garde-fous sur les actions sensibles.
- **Publication GitHub** : préserver la branche `main`, garder les originaux, travailler par branches/PR ; pas de suppression d'archives ni d'écrasement silencieux.

## État documentaire et mises à jour

Le détail vérifiable des réussites, échecs et incertitudes est maintenu dans [ETAT_TECHNIQUE.md](ETAT_TECHNIQUE.md). Le [manifeste](MANIFESTE.json) répertorie les fichiers collectés ; il n'est pas une transcription des conversations ChatGPT.

Lorsqu'une mission Codex se termine :
1. Ajouter son rapport officiel et la preuve de validation.
2. Mettre à jour l'[inventaire](INVENTAIRE.md), la [chronologie](CHRONOLOGIE.md) et l'[état technique](ETAT_TECHNIQUE.md).
3. Reporter les nouvelles décisions structurantes dans [DECISIONS.md](DECISIONS.md) et [ROADMAP.md](../ROADMAP.md) après vérification.
4. Continuer la discussion **dans le même fil ChatGPT**.

## Limites

L'index permet de **retrouver et réconcilier** les échanges, mais ne restaure pas intégralement les conversations absentes de la fenêtre de contexte, et GitHub ne contient pas nécessairement la totalité de leurs messages. Toute précision non étayée doit rester signalée comme telle.
