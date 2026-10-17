# Concordance missions, composants et machines

| Fonction | Missions et chronologie | Machine / exécution | État démontré | Limite / suite |
| --- | --- | --- | --- | --- |
| Socle AppleT2 / démarrage | 01–03 ; famille 04 selon les identifiants attestés | Mac mini Debian ; Codex + propriétaire boot | Diagnostics, préparations, essais et contournements successifs | 04S citée dans 04T/04U, rapport manquant ; aucun trou comblé arbitrairement |
| GPU et CUDA initial | 05A,05B-P,05B,05B-A,05C,05D | Mac mini / Quadro puis RTX3090 | Installation et calcul GPU courts documentés | Réserves DKMS/boot historiques conservées |
| GPU RTX3090 / inférence | 09 →09B ;10 | Mac mini | 09 échec Ollama CPU ;09B corrige ;10 Qwen GPU | Ne pas réattribuer ces résultats au Dell |
| Interfaces de modèles | 06,07,08,10 | Mac mini / Open WebUI | WebUI, catalogue, contexte/évaluations | Qualité des réponses limitée ; pas autorité d’administration du modèle |
| Voix | 11 étude →12 essais →13A installation →13B →13E →13F →JL-02 | WhisperSmall/Piper Tom Mac mini, inférence Dell possible | Chaîne backend et navigateur réelle, audio synthétique | Acoustique physique, Safari/iPhone clients à réceptionner |
| Mémoire commune | 12 →13C →13E/13F →13D-E/JL-02 | SQLite/FTS5 canonique Mac mini ; requêtes modèle Dell via passerelle | Mémoire centralisée réutilisée avec plusieurs moteurs | Pas de base parallèle ni réplication active-active attestée ; WebUI peut conserver son historique propre |
| Administration distante | 13D.1/.2/.3 →13D-E →11-Agentic/11B | Clients Mac →Mac mini →Dell n°1 | SSH clés/mots de passe, sudo, Ansible, droits persistants | Succès du transport ne clôture pas toute la mission 11B |
| Autonomie agentique | 13F →11-Agentic →11B →JL-02 →00 ; jalon 14A | Laboratoire, hôte et Dell n°1 selon scénarios | Outils réels et tâches produites par Qwen ; Codex vérifie | Planification variable, intervention Codex explicite ;14A globale reste ouverte |
| Déploiement serveur | 13D-E, titre historique 13D-E/14 | Dell n°1, Codex opérateur | Réception complète17/10 | sync; reboot -f à corriger avant réemploi ; lien causal RAID non certain |
| Second serveur | 14, précédée du jalon 14A | Dell n°2, JARVIS sera exécutant | Prévu ; pas de déploiement déclenché en00 | Identification cible et correction contrôleur, pas de nouvelle installation en audit |
| Routage / orchestration | 11B,13D-E,JL-02 | Mac mini passerelle, Dell n°1 inférence, Dell n°2 futur | Appels Ollama distants et mesures multi-machines | Repli automatique, placement dynamique, équilibrage et orchestration multi-nœuds non globalement réceptionnés |
| ClientsWeb / raccourcis | JL-01 →JL-02 | Macs clients, passerelle privée | V1 préservée ;V2publiée, espace connecté confirmé utilisateur | Page publique sans données privées ; tunnel8765 déjà actif peut être réutilisé |
| Applications natives | 15 ancien regroupement →15A.1..5 et15B.1..5 | macOS /iOS | Cahiers préparés | Pas d’application SwiftUI livrée par JL-02 ;14 non bloquante |

## Alias et regroupements conservés

| Référence historique | Interprétation conservée | Comptage |
| --- | --- | --- |
|05|FamilleGPU, aucun rapport autonome suffisant|Sous-missions05A..D seules comptées|
|13|Famille voix/mémoire/accès/agent|Sous-missions attestées comptées|
|13BC|Rapport commun13B/13C|Pas une troisième mission autonome|
|15|Ancien intitulé provisoire applications|Remplacé pour la planification par15A/B et leurs cinq incréments chacun|
|13D-E /14 et RECEPTION-MISSION14|Titre historique du premier Dell|13D-E compte pourDell n°1 ;14Dell n°2 distincte|
|11 historique /11-Agentic|Collision de numéro constatée|Deux périmètres conservés sans renumérotation arbitraire|

Les étapes PXE, stockage, comptes, SSH, NVIDIA, CUDA, modèles et réception restent des tâches de 13D-E, pas des missions nouvelles. Aucune mission04A/D/F/S n'est inventée à partir des seules lettres absentes des inventaires.
