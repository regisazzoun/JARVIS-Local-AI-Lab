> **Réception propriétaire complémentaire du 23 octobre 2026 :** ✅ alimentation et câbles acceptés comme *fonctionnels pour le montage effectivement testé* ; les deux calculs CUDA restent reçus. Les cases historiques « brochage inconnu » et « charge double non exécutée » décrivent les limites des mesures, sans retrait de cette décision. [Décision](DECISION-RECEPTION-ALIMENTATION.md).

# Réception ciblée —23 octobre2026

**🟡 Mission incomplète. Détection double et petits calculs reçus ; alimentation et inférence double non reçues.**

| Contrôle | Résultat attendu | Résultat observé | Réception |
| --- | --- | --- | --- |
| Identité Dell | Garde11B réussi avant SSH | Contrôles broker et vérification indépendante réussis | ✅ |
| Détection PCI/NVIDIA | Deux RTX3090 avec pilote actif | Deux GA102, sous-système Dell1028:3880,550.163.01,24576MiB chacune | ✅ |
| CUDA GPU0 | Somme120.0 |120.0, compute8.6 | ✅ calcul léger |
| CUDA GPU1 | Somme120.0 |120.0, compute8.6 | ✅ calcul léger |
| Accès pair | Observation, sans succès présupposé | Faux dans les deux sens ; topo SYS | ✅ observation, capacité P2P non obtenue |
| Journaux de boot ciblés | Rechercher Xid/AER/perte GPU | Chargement pilote ; aucun de ces défauts dans l’extrait consulté | ✅ périmètre limité |
| Services | Disponibles après observations | SSH/Ollama/nvidia-persistenced/Tailscale actifs ; backend/broker Mac disponibles | ✅ lecture, pas une nouvelle réception réseau complète |
| Câblage / PSU / lignes | DP/N, pinout et courant qualifiés | Non obtenus ; PSU950W déclaré seulement | 🟡 INSUFFICIENT |
| Charge double, températures stabilisées | Mesures réelles après qualification | Non exécutée | 🟡 différé |
| PCIe sous charge / bande passante | Génération/largeur et débit mesurés | Gen1 faible usage, x16/x8 observés ; pas de débit mesuré | 🟡 incomplet |
| Inférence split / modèles concurrents | Résidence et temps mesurés par carte | Service principal restreint à un UUID ; pas de nouvel essai | 🟡 différé |

Le calcul CUDA réel est le reçu **9d7d9f0fbc2a4639937c698ff3dfa832**, corrélé à une invocation JARVIS et au broker root. Le script Codex crée une matrice4×4 et la multiplie par l’identité ; ce n’est pas une charge prolongée. Les durées0,179541689s et0,017779354s incluent les effets d’initialisation de cet appel et ne sont pas un benchmark de débit GPU ni de LLM. Le modèle a exécuté ce calcul malgré la consigne de le différer si deux cartes étaient présentes ; cet écart d’orchestration reste consigné, sans lui attribuer une qualification électrique.

## Exécution agentique et corrections

La première étape JARVIS a exécuté31outils, dont27lectures répétées d’inventaire, un calcul CUDA et trois écritures de compte rendu. Elle a atteint sa limite de conversation sans rapport d’étape enregistré. Les répétitions ne sont pas27validations indépendantes ni une campagne utile de stabilité. Codex a corrigé le programme d’inventaire initial tronqué et son adresse Ollama ; il n’a pas installé le second GPU ni modifié les pilotes.

La continuation ciblée a réellement écrit un erratum distinct puis enregistré un rapport d’étape : deux outils supplémentaires. Total33appels natifs,32reçus broker root corrélés ; le rapport d’étape local n’est pas un appel au broker. Les versions et les erreurs sont conservées. L’erratum reste lui-même imparfait et est corrigé dans ERRATA-CODEX.md. Il ne s’agit pas d’une autonomie sans assistance ni d’une levée des réserves26B.

## Préparation logicielle vérifiée

Les trois utilitaires Python se compilent, l’interface `benchmark.py --help` fonctionne. Les deux commandes fixes installées dans la politique ont été utilisées par JARVIS ; aucun paquet/pilote n’a été installé. Le benchmark est préparé et non exécuté, aucune performance inventée. Les200tests logiciels historiques TTS restent leur instantané antérieur, pas200tests supplémentaires de cette extension.

## Reprise au checkpoint utile

Conserver l’inventaire et les calculs reçus. Compléter la qualification matérielle à partir des références réellement présentes et du montage décrit. Ensuite seulement : essai ciblé GPU par GPU, observation thermique/puissance/PCIe, instance Ollama d’essai avec affectation explicite, mesure mono/split/concurrence et comparaison de modèles. Le script refuse d’écraser un résultat précédent. Aucune réinstallation ni reprise26B/TTS/14A automatique.
