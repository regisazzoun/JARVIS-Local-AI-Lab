# Ordonnanceur de fond — intégration et activation PR47

**1 novembre 2026 — ✅🟡 GO avec réserves pour le service central et les unités courtes reçues.** `jarvis-idle-scheduler.service` installé sur Mac JARVIS, enabled, active/running. Deux unités terminées : smoke à checkpoints Mac, contrôle des deux services Ollama Dell2. Contrôleur ensuite idle, aucune mission utile JM-01 en cours. **🟡 Longues missions distantes avec modifications : non qualifiées, non activées.** Aucun service ordonnanceur installé sur les Dell.

## Directives et autorisations

Relus : AGENTS.md et charte de la branche PR47 ; versions runtime récentes dans webui-operationnel ; rapports WEBUI-OUTILS-OPERATIONNELS(PR39) et WEBUI-SOCLE-STANDARD(PR41), réception GPU ; descriptions PR29/39/41/47 ; SUIVI/ROADMAP récents ; rapport26-P2 et préparation P4 avec addenda. Conversation de reprise lue via read_thread.

Autorisé : intégration, tests bornés, installation/activation et publication sur PR47 sans validation intermédiaire. Interdit/conservé : aucune fusion main, aucune reprise M26-P4/MANUAL-HOLD, aucune modification Qwen/WebUI/routage, aucune répétition des anciennes campagnes ou installation de collecteur. Les restrictions historiques de préparation seule dans le prototype sont remplacées, dans ce périmètre, par l'ordre propriétaire courant. Les restrictions historiques Dell2 ne sont pas réintroduites. Nouvelle autorisation nécessaire : aucune pour le travail réalisé.

État26 : P2/P3 reçus avec réserves, P4 et phase2 non reçues ; les descriptions anciennes de P4 en cours ne valent pas instruction de lever la pause ultérieure. Aucun accès en écriture à la file des missions, aucun checkpoint historique ni compteur touché par l'ordonnanceur. Les seuls nouveaux reçus de registre sont des observations indépendantes de cette mission.

## Schéma effectif et accès

MCP existant : client `jarvis.client_mcp`, MCPO officiel sur écoute locale8094, montage `/jarvis`. `GET /jarvis/openapi.json`, puis `POST /jarvis/jarvis_schema` et `/jarvis/jarvis_call`, authentification Bearer existante lue localement sans copie dans Git. Le premier essai sur la racine MCPO a répondu404 ; montage identifié puis appels réussis. Aucun connecteur ajouté.

| Outil registre | Entrée | Réponse effective | Limites pour admission |
|---|---|---|---|
| system_status | `{}` | `system`, `release`, `load`(1/5/15min), `memory:{returncode,stdout,stderr}` via free-m | Mac uniquement ; charge n'est pas CPU%; pas GPU/VRAM ni timestamp dans le payload |
| host_resources | `{}` | `cpu`, `ram`, `gpu`, `tailscale`, résultats de commandes ; evidence_id/diagnostic | lscpu décrit le matériel ; free-m RAM textuelle ; GPU CSV name/memory.used/utilization.gpu, sans total VRAM ; pas un snapshot multi-hôte normalisé |
| compute_status | `{}` | `nodes`, `jobs`, `conversation_model` | disponibilité/modèles/file ; aucune mesure CPU/RAM/GPU. Description historique Dell2 offline obsolète ; résultat actuel trois nœuds enabled/ready |

Reçus MCP réels : system_status702, host_resources704, compute_status706. Origin QwenCode/MCP désigne le transport stdio existant, **pas une décision ou exécution autonome du modèle**. Le résultat compute_status excède la vue compacte ; le résultat complet est relu dans l'audit canonique, trois nœuds ready. Ne pas interpréter l'extrait comme un champ manquant.

Producteur actif `jarvis-hardware` : script existant `open-webui/branding-jarvis/collector.py`, module existant `launcher_telemetry.py`. Fichier atomique `metrics/latest.json` : `{sampled_at, machines:{mac-mini,dell-1,dell-2}}`. Par machine : `available`, `sampled_at`(epoch secondes), `cpu_percent`(0..100), `cpu_threads`, `load1`, `ram_total_mb`, `ram_used_mb`(total-MemAvailable), `gpu`, `ollama`, `active_models`. Les MB sont des MiB arrondis. Cadence8s plus durée de collecte ; refus à25s. Ce fichier provient d'un service de mesures existant, et non d'une API Launcher présumée canonique.

**Limite découverte : `gpu` ne présente que la première carte.** L'adaptateur réutilise donc la sonde d'admission complète existante `operations28a/resource_probe.py`, locale sur Mac et via `host_remote(action=hybrid_resources,host=dell-observe|dell2)` sur les Dell. Réponse JSON dans `result.stdout` : `captured_at`, `memory_total_bytes`, `memory_available_bytes`, `cpu_threads`, `load1`, `gpu:[{index,total_mib,free_mib,utilization_percent,temperature_c,power_w}]`. Retour0 et fraîcheur contrôlés ; timeout borné. Aucun de ces producteurs n'est recopié/réinstallé/modifié.

Adaptateur : ajout transitoire `gpu_all` et `gpu_captured_at` au snapshot en mémoire, sans réécrire le fichier du collecteur. CPU/RAM et toutes les cartes sont contrôlés ; seuils25%CPU,35%RAM disponible,20%utilisation de chaque GPU ; unités GPU sous50%VRAM utilisée et sans modèle résident. Une unité CPU ne décharge pas Qwen pour satisfaire un seuil VRAM.

Observations réelles : Mac12threads/~31GiB/1×3090 ; Dell1 36threads/~251GiB/2×3090 ; Dell2 36threads/~126GiB/3090+3080. Cinq GPU reçus, pas trois. Dell1 occupé a été refusé «GPU busy» pendant l'inférence ; Dell2 disponible utilisé pour le contrôle de services. Mesures datées dans TELEMETRY-PROOF.json ; aucune conclusion de performance générale.

## Intégration et réception

Réutilisation : SQLite compute_jobs lue en mode lecture seule, priorité par nœud aux calculs queued/running ; workers historiques non modifiés. Le scan saute un nœud occupé, donc Dell1 ne bloque pas Dell2. Les sessions natives WebUI ne passent pas toutes par compute_jobs ; GPU/résidence complètent les gardes, sans promesse de détection parfaite de toutes les sessions entre deux tours.

Verrou monoinstance, état atomique/fsync, tentatives persistantes plafonnées3, signaux/groupes, délais, pause/reprise et reprise après redémarrage. Le service est borné CPU/RAM, Nice15 et sans privilège nouveau. Le contrat checkpoint appartient à l'unité ; aucun rejeu de mission canonique par le contrôleur.

Preuves ACTIVATION-PROOF.json et FINAL-PROOF.json : activation sous PAUSE, lancement réel, interruption au checkpoint2 resté2 pendant pause, reprise à12, completion persistante ; redémarrage du seul ordonnanceur, même completion sans rejeu. Puis admission Dell2, SSH fixe `systemctl is-active jarvis-ollama.service jarvis-ollama-missions.service` : active/active, code0, unité completed. Aucune commande de travail envoyée sur Dell1. Le service reste enabled/active et idle après ces unités ; cela ne signifie pas qu'une mission productive est en exécution.

**11 tests ciblés PASS sur le Mac JARVIS**, couvrant données absentes/périmées/futures/NaN, RAM, seconde carte occupée, VRAM/résidence, monoinstance, trois erreurs, nœud occupé non bloquant et suspension automatique/reprise sur perte simulée de ressources. Le premier test après restriction des unités distantes a échoué car sa fixture déclarait Dell pour un argv local ; fixture corrigée vers Mac, garde conservée, suite finale PASS. Simulation de pression distincte d'une charge réelle imposée au matériel. Pause opérateur et reprise réelles reçues dans le service installé.

## Préservation, publication et limites

Contrôles finaux : conversation, broker, collector, MCPO, Ollama Mac et deux workers actifs ; deux services Ollama actifs sur chaque Dell ; WebUI HTTPS200. Aucun redémarrage de ces services pendant cette mission. Seul nouveau service installé/rechargé : ordonnanceur central ; daemon-reload systemd sans redémarrage des autres unités. Sources moteur, configurations Ollama, modèles, comptes et bases historiques préservés. Aucun collecteur créé, aucun modèle téléchargé, aucune fusion main.

Infrastructure et opérations de réception : Codex. Pas d'attribution à Qwen. Les scripts de capture lisant les réglages privés restent privés ; seules preuves expurgées publiées. Source/état locaux JARVIS préexistants non écrasés : worktree dédié PR47 ; les autres worktrees et changements non publiés sont conservés.

Réserves : les longues tâches distantes à mutations, leur arrêt distant garanti et leurs checkpoints distribués ne sont pas implémentés/reçus ici. Le contrôleur les rejette explicitement. JM-01 n'est ni définie ni exécutée par ce smoke test ; aucune activation globale des missions historiques n'est revendiquée. L'ordonnanceur effectif est activé pour le périmètre reçu ; la mission large de fond productive reste partielle.

Retour arrière : `sudo systemctl disable --now jarvis-idle-scheduler`, conserver répertoire privé/état/checkpoints, restaurer uniquement sa source Git si nécessaire. Aucune restauration de SQLite ni arrêt des services Qwen/WebUI. Procédures dans ops/IDLE_SCHEDULER.md.

Le contrôle automatique a refusé une proposition d’ajout de texte d’autorisation dans AGENTS.md et la charte : risque de modifier les instructions futures hors périmètre explicite. Ces fichiers restent inchangés ; ordre courant documenté uniquement ici, dans ROADMAP/SUIVI et la PR.
