# Chronologie technique — état provisoire

Chronologie issue des rapports Codex transmis ; les répertoires de preuves ne doivent pas être interprétés comme des validations à eux seuls.

| Mission | Fait documenté | Réserve |
| --- | --- | --- |
| 03 — 11 octobre 2026 | Debian 13.7, diagnostics hôte, SSH et démarrage | États intermédiaires |
| 04 — 11–12 octobre | GRUB, Thunderbolt, eGPU, essais de démarrage | Plusieurs tests non concluants |
| 04W — 12 octobre | Analyse d'un démarrage interrompu | Entrée dans le noyau non prouvée par ces traces |
| 05A — 12 octobre | Choix du pilote NVIDIA 595.91.07 | Préparation, non validation |
| 05B — 12 octobre | Installation contrôlée NVIDIA | Vérifier réserves DKMS dans les rapports |
| 05C — 12 octobre | Premier test de Quadro RTX 5000 en eGPU | Tests matériels et CUDA léger |
| 05D — 12 octobre | Calcul CUDA réel et Ollama 0.40.3, Llama 3.1 8B sur GPU | Une mesure citée : 70,38 tokens/s, non généralisable |
| 06 — 12 octobre | Open WebUI v0.12.0, authentification et inférenceGPU | HTTP local non chiffré |
| 07 — 12 octobre | Réglages d'inférence et recherche documentaire (RAG) | Résultats limités à la batterie de tests |

La présence de `mission08-preuves` ne prouve pas le résultat de la mission 08 en l'absence d'un compte rendu vérifiable.

## Consolidation du 17 octobre 2026 — mission 00

Le rapport 08 a été retrouvé : Ministral installé et testé, qualité avec réserves. 09 a constaté Ollama sur CPU malgré CUDA ; 09B corrige le verrou GPU ; 10 installe Qwen ; 11 historique audite JarvisVoice. 13E/13F ont leurs rapports. 13D-E réceptionne le Dell n°1 le 17 octobre ; 11-Agentic/11B ajoutent des opérations hôte et distantes ; JL-02 est livrée avec réserves. 14A reste ouverte ; 14 est réservée au Dell n°2 par JARVIS. Les cahiers natifs 15A/B restent préparés.

La phrase historique ci-dessus sur l’absence de compte rendu 08 est remplacée par le rapport retrouvé. La mission 00 consolide **68 missions/sous-missions et 28 anomalies**, dont la référence 04S sans rapport autonome. **129 documents/preuves** sont récupérés sur JARVIS, avec provenance et expurgation. Les cinq tâches documentaires JARVIS ont des traces réelles ; leur guidage et les corrections Codex restent explicites. Aucun déploiement, benchmark ou changement RAID n’est déclenché.

[Registre courant](missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) · [Rapport final](missions/00-Mission-Pilotage-point-26-10-17/RAPPORT-FINAL.md) · [Index des rapports récupérés](missions/README.md).
