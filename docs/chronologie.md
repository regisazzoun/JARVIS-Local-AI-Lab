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

## Consolidation17 octobre 2026 — mission 00

Le rapport 08 a été retrouvé : installationMinistraltestée,qualitéavec réserves.09a constatéOllama CPU malgré CUDA ;09B corrige le verrou GPU ;10installe Qwen ;11 historique auditeJarvisVoice.13E/13F ont leurs rapports publiés.13D-E reçoitDell n°1 le17/10 ;11-Agentic/11B apportentdes opérationshôte / distant ;JL-02 estlivréeavec réserves.14A reste ouverte ;14 réservéeDell n°2JARVIS,15A/Bcahiers préparés. Voir [registre00](missions/00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md),sources et chronologie par mission.

La phraseancienne sur l’absence de compte rendu08 est un constat historique remplacé, corrigé en mission 00.
