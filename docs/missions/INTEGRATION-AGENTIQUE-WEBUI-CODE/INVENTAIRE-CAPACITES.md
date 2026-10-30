# Inventaire des capacités réellement constatées

Inventaire du30octobre2026, captures originales privées, résumés et empreintes dans les preuves structurées. Les informations historiques ne remplacent pas ces observations.

| Élément | Installation/configuration | Charge active | Essai réel dans cette campagne |
|---|---|---|---|
| Open WebUI0.12.0 | Conteneur existant, données conservées | Oui | Conversations Chromium authentifiées, appels natifs et résultats |
| Apache2.4.69 | Reverse proxy existant loopback8088 | Oui | Parcours HTTPS et streaming via le nom Tailscale |
| Tailscale1.104.2 | Tailnet existant | Oui sur le Mac | Accès Chromium et requêtes HTTPS sans tunnel manuel |
| Ollama Mac0.40.3 | Instance et catalogue existants | Qwen27B réellement chargé | Conversations et outils du nouveau profil |
| Qwen Code0.26.4 / Node22.23.4 | Lanceur et paquet existants corrigés | À la demande | Lecture, édition, test, objectif et MCP ; cas longs réservés |
| JARVIS conversation/Mission Engine | Runtime canonique existant | Services conservés | Registre chargé, missions consultées, appels et reçus canoniques |
| Skill Lab | Base et quatre skills actifs conservés | Accessible par registre | `github-publish` découvert, exécuté et vérifié |
| MCP historique | Huit outils stdio conservés | Accessible | Tests ciblés historiques de découverte et erreurs de paramètres |
| MCP clients | Six outils de découverte/appel, dont commande distante directe | Chargé par les nouvelles sessions Code | Appels réels et essais de délégation |
| GitHub | Authentification existante dans le broker | Accessible aux outils | Recherche, publication réversible et relecture ; index de recherche incomplet |
| Google Workspace | Connecteur et OAuth officiel installés | Statut accessible | `AUTH_REQUIRED` observé dans WebUI ; aucune API distante reçue |
| Dell1 | Deux RTX3090, Debian existant | Ollama et exécution SSH | Qwen80B réellement chargé ; transferts et tests CPU distants |
| Dell2 | RTX3090 et RTX3080, Debian existant | Exécuteur SSH | Transferts et tests CPU ; aucune inférence déclarée |
| JL-03 | Déploiement indépendant existant | Actif | État et accès contrôlés, pas de nouvelle réception vocale |

## Modèles observés

Le Mac possède les tags Qwen27B, Ministral14B et Llama3.1:8B. Le processus chargé observé est Qwen27B. Dell1 expose sur l’instance de mission les tags Qwen80B, Qwen32B, Llama70B et les anciens27B/14B/8B ; le modèle chargé pendant les essais est Qwen80B. Aucun modèle n’a été téléchargé, déplacé ou supprimé par cette mission.

L’alias historique Llama8B reste un choix disponible ; il n’est pas le défaut livré. Le nouveau profil conversationnel conserve le27B et lui raccorde les outils. Le profil développement conserve le80B du Dell1.

L’inventaire matériel réel indique une RTX3090 également sur le Mac mini ; les cinq GPU présents sont donc une carte sur le Mac, deux3090 sur Dell1, et3090+3080 sur Dell2. Aucun calcul GPU sur Dell2 n’est déduit des tests Python CPU.

## Niveaux d’exposition

Le registre natif contient les outils hôte, missions, mémoire, skills, MCP et calcul existants, avec les extensions spécialiste et Google. Le connecteur client expose un sous-ensemble de ces outils, les schémas sont demandés à la volée. Les opérations de planification/clôture internes restent sous le moteur canonique ; leur présence dans le dépôt ne les transforme pas en outils WebUI publics.

Les tests d’installation/configuration ne sont pas comptés comme des missions autonomes. Les appels de connectivité lancés directement par Codex sont identifiés comme tels, même s’ils utilisent le transport nommé QwenCode/MCP.
