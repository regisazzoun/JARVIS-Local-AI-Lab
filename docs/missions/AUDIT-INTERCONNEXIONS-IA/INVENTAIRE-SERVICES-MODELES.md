# Inventaire réel — 29 octobre 2026

Audit sans installation, suppression de poids, modification de service ou reprise de mission suspendue. Les appels de test chargent des modèles déjà présents ; ce chargement n'est pas une nouvelle installation. Les adresses détaillées, identités SSH et discussions originales restent dans les preuves privées. E01–E12 désignent les fichiers JSON du présent dossier.

| Machine | Debian / CPU / RAM | GPU réellement observés | Rôle actuel |
|---|---|---|---|
| Mac mini | Debian13 T2Linux ; i7-8700B,12threads ;31,20GiB | RTX3090,24GiB | Services centraux, interfaces, mémoire, workers d'orchestration ; conversation27B ; Qwen Code expérimental local |
| Dell1 | Debian13 ; i9-10980XE,36threads ;251,42GiB | DeuxRTX3090,24GiB chacune | Deux instances Ollama ;80B de missions et exécuteur SSH |
| Dell2 | Debian13 ; i9-10980XE,36threads ;125,51GiB | RTX3090,24GiB + RTX3080,10GiB | Exécuteur SSH ; aucun service d'inférence observé |

Les cinq GPU existent, mais ce ne sont **pas cinq RTX3090**. Dell2 n'a pas le matériel visé initialement de deux3090. Tailscale fonctionne sur Mac et Dell1. Aucun binaire en PATH, unité tailscaled ou adresse tailnet n'est trouvé sur Dell2 lors des contrôles ciblés ; SSH LAN fonctionne. Sources : E01, réception14B du25octobre.

| Service / composant | Installé/configuré | Démarré / accessible | Requête fonctionnelle / usage |
|---|---|---|---|
| Open WebUI0.12.0 Docker existant | Image épinglée, volume conservé | Conteneur healthy, MacLAN3000 | Login HTTPS et formulaire modèle réels ; conversations historiques préservées |
| Apache2.4.69 | VHost unique loopback8088 | Actif, proxy vers3000 | HTTPS→proxy→API répond ;WebSocket/SSE reçus antérieurement |
| Tailscale1.104.2 Mac | Serve privé80/443 | Actif | Certificat valide et accès Dell1 reçus ;pas de Funnel |
| Ollama Mac0.40.3 | Loopback11434, catalogue3modèles | Actif |27B répond BONJOUR ;8B utilisé par test WebUI |
| Ollama Dell1 principal0.40.3 | LAN11434, un GPU visible | Actif, API accessible | Catalogue lu ;pas de nouvelle inférence ici durant l'audit |
| Ollama Dell1 missions0.40.3 | LAN11435, deuxGPU visibles | Actif |80B utilisé réellement par Qwen Code ;8B aussi par WebUI |
| Ollama Dell2 | Aucun binaire connu, unité, répertoire standard ou port trouvé | Absent des contrôles | Aucune inférence surDell2 démontrée |
| JARVIS conversation | `/opt/jarvis/conversation`,8765 | Actif ;sondeOK | API sans restriction d'outils :503 ;avec outils limités :200/Qwen27 |
| JL03 | `/var/lib/jarvis/projects/jl03`,8766 | Actif, page et API accessibles | Conversation réelle27B/Mac reçue pendant cet audit |
| Prototype vocal23D |8783 | Actif, page «Mission23D» | Distinct deJL03 ;aucun nouveau test physique vocal |
| Broker hôte | `/run/jarvis-host/bridge.sock` | Socket Unix écouté | SSH/Ansible historiques reçus ;SSH actuel contrôlé parCodex |
| Workers1/2 Mission Engine | Deux processus surMac | Actifs, aucune mission running/queued à l'instantané | Les Dell sont des exécuteurs distants, pas ces processus persistants |
| Qwen Code0.26.4 | Node22.23.4 isolé, wrappers locaux | CLI et relais8091/8092 accessibles | Nouveau défaut corrigé par80B, tests indépendants3PASS |
| Skill Lab/MCP |61outils exposés parAPI ;4skills actifs | API accessible | Acquis historiques conservés ;MCP Qwen Code non configuré |

La quantité d'outils exposée par le processus conversationnel n'est ni une mesure de qualité ni la somme des anciens rapports. Skills : config-repair6, debian-diagnostic1, dell-roundtrip1, github-publish1. Le moniteur de santé et le watchdog de ressources tournent surMac. Le superviseur M26-P4 reste désactivé par pause propriétaire. La sonde verte ne détecte pas le503 conversationnel sans restriction d'outils.

## Modèles, catalogues et consommateurs

Tailles décimales enGo des catalogues ;«actif» décrit l'instantané et les appels observés, pas une résidence permanente. Sources E02/E03/E08/E10 et testQwen E04.

| Modèle | Machine | Taille | Installé | Actif | Utilisé par | Justification |
|---|---|---:|---|---|---|---|
| llama3.1:8b | Mac |4,921|Oui|Chargé pendant essaiWebUI|Open WebUI profilQualité|Défaut global hérité et premier backend possible |
| qwen3.5:27b-q4_K_M | Mac |17,479|Oui|Chargé après test|JARVIS/JL03 ;WebUI possible|Conversation canonique et réponse réelle |
| ministral-3:14b-instruct-2512-q4_K_M | Mac |9,083|Oui|Non observé chargé|ProfilWebUI, configurationJARVIS|Présence et référence, pas nouvel usage prouvé |
| llama3.1:8b | Dell1 |4,921|Oui|Chargé pendant essaiWebUI|Open WebUI|Deuxième backend du même identifiant |
| qwen3.5:27b-q4_K_M | Dell1 |17,479|Oui|Non observé chargé|WebUI peut le sélectionner|Même identifiant disponible surdeuxbackends |
| ministral-3:14b-instruct-2512-q4_K_M | Dell1 |9,083|Oui|Non observé chargé|WebUI possible|Catalogue historique |
| qwen3:32b-q4_K_M | Dell1 |20,201|Oui|Non observé chargé|Comparatifs28A ;WebUI disponible|Pas de nouveau benchmark |
| llama3.3:70b-instruct-q4_K_M | Dell1 |42,520|Oui|Non observé chargé|Comparatifs28A ;WebUI disponible|Aussi référence inactive du futur nœudDell2 |
| qwen3-coder-next:q4_K_M | Dell1 |51,742|Oui|Chargé réellement32768|Mission Engine et Qwen Code ;profilWebUI|Test neuf80B et acquis26 |
| Aucun poids observé | Dell2 |—|Non trouvé|Non|Aucun|Pas d'API ni de service Ollama |

SurDell1,11434 et11435 partagent **le même** `/var/lib/ollama/models` et le compteollama :deux API ne signifient pas deux copies des poids. Le Mac a son catalogue indépendant `/home/adminjarvis/JARVIS/ollama/models`. Trois modèles sont donc présents surdeuxmachines, avec les mêmes empreintes de contenu, mais des stockages indépendants. La récente installation WebUI/Qwen Code a téléchargé des paquets logiciels, aucun poids de modèle :dates de modèles antérieures, sources de l'installation et catalogues l'attestent. Les catalogues sont revérifiés après l'audit.

Le réglage vocal `gpt-realtime-2.1-mini` est une valeur de fournisseur facultatif avec ENABLED=false, pas un modèle installé ou une connexioncloud utilisée. Les moteurs actifs sont Whisper/Piper viaJARVIS. Ne pas prendre une valeur par défaut d'interface pour un déploiement.
