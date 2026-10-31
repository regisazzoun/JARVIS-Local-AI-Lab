# Concordance applicative prioritaire

| Application | Dell 1 | Dell 2 | Rôle/écart/recommandation |
|---|---|---|---|
| Ollama | 0.40.3 | absent des services/API/chemins examinés | Deux services Dell 1, même stockage ; pas un doublon de poids par service. |
| NVIDIA | 550.163.01 | 550.163.01 | Mac T2 différent ; ne pas imposer le même pilote sans validation. |
| CUDA toolkit | 12.4.131 | 12.4.131 | Pilote compatible ne prouve pas toolkit ; toolkit installé ne prouve pas charge actuelle. |
| Python | 3.13.5 | 3.13.5 | Socle commun. |
| Node.js | 20.19.2 | 20.19.2 | Binaire standalone sur Dell ; npm absent. |
| npm | absent du PATH et paquets | absent du PATH et paquets | À ajouter seulement si build npm requis. |
| Git | absent du PATH et paquets | absent du PATH et paquets | Transferts par manifeste utilisés ; manque pour workflow Git local sur workers. |
| Qwen Code | non trouvé | non trouvé | Client sur Mac, inférence Dell 1 ; pas installé sur les Dell. |
| Ansible | pas de contrôleur local | pas de contrôleur local | Différence voulue : contrôleur Mac, cibles Python/SSH. |
| OpenSSH | 10.0p2 | 10.0p2 | Profils épinglés existants ; clé non publiée. |
| Tailscale | Running | binaire absent dans PATH ; paquet non trouvé | Dell 2 administré en LAN via Mac ; accès direct tailnet non reçu. |
| Open WebUI | non trouvé | non trouvé | Une instance centrale, profils pas modèles supplémentaires. |
| Apache2 | non trouvé | non trouvé | HTTPS terminé par Tailscale Serve ; Apache en HTTP loopback8088. |
| Docker | non trouvé | non trouvé | Ne pas installer sur les cibles sans besoin. |
| Broker JARVIS | cible SSH + garde identité | cible SSH + garde identité | Un broker central, pas trois brokers concurrents. |
| Mission Engine | copies de travail/candidats | copies de travail/candidats | SQLite Dell = fichiers de candidats ; pas preuve de moteur actif. |
| Registre/MCP JARVIS | accessible via orchestration Mac | accessible via orchestration Mac | Ne pas copier la mémoire canonique sur les Dell. |
| Skill Lab | exécution distante selon skill | exécution distante selon skill | Présence de copies SQLite ne signifie pas catalogue canonique répliqué. |
| Qwen TTS expérimental | venv 107 distributions | non trouvé | Environnement spécialisé Dell 1 conservé ; pas un modèle conversationnel. |
| Whisper/Piper | non trouvé | non trouvé | Moteurs CPU canoniques Mac ; TTS expérimental distinct. |
| Bureau/VNC | Plasma/VNC actif | non trouvé | Différence de rôle ; pas nécessaire sur Dell 2 sans besoin. |
| Supervision | jarvis-supervision + gpu-normal | console de progression | La télémétrie existe ; le diagnostic agentique P7 complet n’est pas reçu. |
| JL-03 | pas de frontend | pas de frontend | Dépôt Launcher3 indépendant. |
| Google MCP | via MCP central | via MCP central | Éducation trois lectures reçues ; écritures et clients Éducation non reçus. |

Les écarts ne doivent pas être corrigés uniformément. Ollama/TTS/bureau sur Dell 1 sont des spécialisations historiques. Ansible central Mac et cibles SSH est une répartition cohérente ; pas besoin de troiscontrôleurs. Git/npm absents sur les Dell limitent en revanche les projets qui demandent checkout/build natif ; leur installation doit dépendre d’un profil de rôle reproductible. Le manque d’inférence Dell 2 est une capacité non déployée, pas une panne d’Ollama déjà installé. Les copies du moteur/SQLite dans/opt/jarvis-lab sont des candidats/tests, sans service canonique correspondant observé.
