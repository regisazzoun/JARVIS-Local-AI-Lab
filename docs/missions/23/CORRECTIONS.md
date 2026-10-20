# Corrections infrastructure — mission23

Directives consultées : AGENTS/charte sur la branche de travail et main distant, cycle23–31 sur la branche de planification, objectif persistant original, états et code23, architecture/bilan22, politiques réellement installées. Autorisations préservées : installations/configurations du prototype, outils hôte, SSH/Ansible et ressources déjà accordés, aucune validation humaine intermédiaire. Écarts : ancien statut «planifié» remplacé par le lancement propriétaire ;04 conserve sa réception historique sans transformer son processus éphémère en service permanent.

| Correction Codex | Fichiers | Portée |
| --- | --- | --- |
| Documentation LiveKit/Ollama autorisée | `jarvis/agent.py`, `jarvis/tools.py` | HTTPS sur domaines précis ; refus des redirections et cibles arbitraires conservé |
| Pagination documentaire | mêmes fichiers | `web_fetch(offset=...)` expose prochaine portion, taille disponible et troncature de source ; reçu non inventé, limite de lecture existante explicitée |
| Dépôts officiels lisibles | `broker/host_bridge.py`, politique root | Lecture/inspection/téléchargement/branches des dépôts LiveKit ; aucun droit de publication sur ces dépôts tiers |
| Services de prototype persistants | `broker/project_service.py`, `host_bridge.py`, `jarvis/host_client.py` | Projet mission23 seulement, unités préfixées, identité technique et montage Bubblewrap identiques au terminal ; install/start/status/logs/stop/restart/enable/disable. Ni root applicatif, ni secret ajouté au modèle |
| Voix canonique accessible | politique root | Modèles, venv, scripts et fichier public de configuration voix existants montés en lecture ; aucune seconde instance imposée ni modèle retéléchargé par Codex |
| Dépendances déjà autorisées raccordées | politique root | python3-pip et espeak-ng peuvent être installés par JARVIS ; le venv existant est conservé, aucune réinstallation Python effectuée |
| Compression réparée | `jarvis/durable_cycle.py` | Le dernier résultat structuré réel reste dans le checkpoint, y compris les lots ; réduction explicite des anciens éléments et extraits adaptés à la place disponible, sans modifier le reçu canonique. Événements context_compacted avec tailles et référence de preuve |
| Checkpoint de débogage | `jarvis/durable_cycle.py` | Dernier résultat réel par commande, derniers échecs et dernières écritures/empreintes épinglés entre cycles ; une réécriture ne vaut pas retest réussi |
| Traceback redirigé exploitable | `jarvis/tools.py` | Si stderr est vide, le résumé d’erreur reprend stdout au lieu d’une chaîne vide ; reçu intégral et identité de preuve conservés |
| Validation fonctionnelle | `durable_tools.py`, `mission_store.py`, contrat05 | Un code0 avec avertissement de coroutine ou génération indisponible ne satisfait pas le contrat. JARVIS doit tester un flux LLM réel non vide et une construction cohérente agent/adaptateurs ; les marqueurs de test seuls sans assertions ne sont pas une réception |
| Continuité | même moteur/base | Contexte de travail archivé avant reconstruction ; aucun nouveau plan, ID, compteur remis à zéro ni tâche reçue modifiée |

Les fichiers applicatifs sous `livekit-agent/` ne sont pas corrigés par Codex. Un fichier de checkpoint explicitement attribué à Codex est ajouté à la racine de la mission pour informer JARVIS des capacités réparées. Le modèle reste responsable des adaptateurs, de l’agent, des choix de bibliothèques et des tests fonctionnels.

Aucun plafond CPU/RAM/GPU, nombre de cycles ou nombre d’appels n’est ajouté. Les erreurs API ne sont pas contournées par une validation artificielle. Le service de sonde infrastructure Codex est arrêté puis retiré après son test ; il n’est pas un serveur LiveKit développé par Codex.


## Essai de raisonnement

Le mode de raisonnement Qwen des missions durables était désactivé par défaut. Codex a activé un essai `durable_think=true`, en conservant contexte32768 et génération sans plafond d’économie. C’est une hypothèse d’amélioration face aux erreurs d’API, pas une cause démontrée ni un gain revendiqué. Les résultats après correction et les guidages Codex doivent être pris en compte avant de qualifier l’autonomie.

La demande de capacité existante a été rapprochée des droits réels et marquée ACCORDÉ, sans prétendre réceptionner l’application ni installer de nouveau le venv. Les secrets et politiques complets restent privés.


Le checkpoint ajouté initialement augmentait aussi la taille du préambule (54879 caractères observés). Le défaut de compression existait déjà avant intervention : le snapshot initial conservait88542 caractères, dont un checkpoint résumé. La correction du dernier lot évite que ce préambule plus riche provoque une nouvelle perte immédiate de la source. Aucun agrandissement arbitraire du contexte ni budget de mission ajouté.


Après réparation de la compression, des relectures subsistaient. Codex a recentré l’objectif de la même tâche05 sur un changement de stratégie : examiner puis réutiliser l’adaptateur Ollama officiel déjà installé (`openai.LLM.with_ollama`, disponibilité/signature vérifiées localement). Ce guidage est une intervention Codex, pas une découverte autonome de JARVIS ; aucun code applicatif n’est écrit à sa place.


## Vérificateur indépendant de05

Le test que JARVIS venait d’écrire affichait encore `LLM_STREAM_VERIFIED` sur une connexion échouée et `AGENT_ADAPTERS_VERIFIED` malgré les imports échoués. Codex ne reçoit pas ces marqueurs comme une preuve. Un petit vérificateur de recette, distinct de l’application et protégé en écriture, est installé sous `/usr/local/lib/jarvis-host/verify_livekit_agent.py`. JARVIS doit fournir un manifeste `verification.json` avec ses factories applicatives (module local:fonction et paramètres). Le vérificateur appelle réellement le provider, exige un LLMStream du SDK et un fragment de réponse non vide ; il importe ensuite l’entrée agent et construit une véritable AgentSession avec STT/TTS/LLM compatibles.

Le contrat accepte uniquement les deux commandes exactes du vérificateur, pas les marqueurs d’un script permissif du modèle. Cette contribution est un test de réception Codex, pas le développement de l’agent. Elle ne constitue ni un test de microphone ni une réception complète WebRTC. Le premier essai indépendant refuse bien un manifeste manquant avec code1 ; une recette positive reste à obtenir par JARVIS.
