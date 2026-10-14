# Mission 13F — architecture et limites de droits

```text
Navigateur authentifié sur localhost / HTTPS privé préexistant
  microphone → AudioWorklet/RMS + pré-roll → WAV → Whisper Small CPU/int8
  texte / transcription → passerelle → identité v2 + souvenirs SQLite → Ollama
  réponse écrite → résumé oral nettoyé → Piper Tom CPU → lecteur navigateur
                               ↕
                    registre d'outils et boucle d'intervention
                               ↕
               diagnostics hôte bornés / sources HTTPS / laboratoire Bubblewrap
```

## Voix

VAD navigateur sans modèle supplémentaire : seuil RMS 0,012, début continu 140 ms, pré-roll 300 ms, fin après 850 ms de silence, au moins 250 ms de voix, limite 40 s. Whisper conserve son VAD local et la langue française. En synthèse/génération, l'écoute évite les captures concurrentes ; après lecture elle reprend. Barge-in optionnel à seuil 0,035 avec echoCancellation/noiseSuppression demandés au navigateur. Ce n'est pas une garantie anti-écho physique. Capture arrêtée au passage en arrière-plan et à la déconnexion.

Le texte écrit reste complet. Le champ spoken_answer est borné : 280/500/1100 caractères avant suffixe éventuel, commandes/tableaux/liens retirés. Résumé LLM si nécessaire, repli déterministe si son appel échoue. Le même contexte modèle évite un rechargement. Davantage de détails pour un seul tour ne change pas la préférence persistante. Bouton stop invalide les requêtes audio en attente et arrête le lecteur, sans tuer un worker Piper déjà lancé ; interruption vocale testée avec micro artificiel.

## Autorité mémoire unique

runtime/memory.sqlite est la base active commune à tous les modèles. Schéma v3 : preferences référence memories par clé étrangère ; preference_history conserve uniquement clés et valeurs du catalogue. Ce sont des tables de la base canonique, pas une mémoire concurrente. Souvenir, index et audit sont validés dans la même transaction. Détection déterministe de formulations explicites, pas approbation libre par le modèle. Les secrets, permissions et faits sensibles restent hors promotion automatique. FTS5 lexical, historique privé séparé des souvenirs actifs ; pas de synchronisation avec la base WebUI.

Le catalogue est limité et peut refuser des formulations ambiguës, négatives ou des exemples cités. Paramètres conservés même après changement de moteur ; les anciennes réponses ne sont pas réécrites quand un souvenir est supprimé. L'édition libre d'une préférence gérée est refusée : utiliser une consigne ou le réglage UI pour garder contenu et valeur cohérents.

## Registre et agent

system_status, disk_usage, jarvis_services, software_versions, hardware_inventory, service_logs, read_configuration, web_search, web_fetch, active_memories, propose_memory, lab_terminal, intervention_report. Arguments validés, aucune interpolation des arguments modèle dans les commandes hôte. Les commandes libres sont uniquement des scripts shell dans la sandbox dédiée, sans sudo. Les journaux de la passerelle sont bornés et rotatifs ; les autres journaux restent soumis aux droits Unix, absence de ligne != absence d'erreur.

La boucle offre jusqu'à 32 tours, jusqu'à quatre outils par tour. L'objectif et une synthèse des observations sont conservés lors de la réduction du contexte ; traces complètes privées. Un plan seul provoque une continuation en mode laboratoire. Pas de rapport à la fin de la limite : résultat explicitement incomplet. Le format textuel `fonction[ARGS]{JSON}` de Ministral est converti uniquement pour une fonction connue, puis passe les mêmes contrôles.

Recherche DuckDuckGo Lite, fallback incidents GitHub publics. Bing RSS a été écarté après résultats non pertinents. Lecture HTTPS limitée à des domaines documentaires/GitHub/forums publics configurés dans le code, redirections et URLs privées refusées, taille et délai bornés. HTML lu comme données ; scripts/style retirés. Deux documents réellement consultés sont requis avant un rapport pour un objectif demandant de la recherche ; ancres et versions du même document ne comptent qu'une fois.

## Périmètre laboratoire

Politique publique config/lab-policy.json : mission 13F, cible mac-mini/bubblewrap-lab. API agent_mode explicite et lab_enabled nécessaires. Un modèle ne peut ni modifier la politique ni étendre la cible. /usr lecture seule, /work dédié seul modifiable, /tmp jetable, PID/user/network namespaces, capabilities retirées, loopback isolée. Aucun montage des données personnelles, de runtime/auth ou de la racine hôte. Limites CPU 15 s, commande 25 s, mémoire virtuelle 512 Mio, fichiers individuels 2 Mio, workspace surveillé 128 Mio/4096 fichiers ; unité limitée à 2 Gio/128 tâches. La surveillance du volume n'est pas un quota noyau instantané : un léger dépassement transitoire est possible.

Les sources externes n'accordent aucune permission. Dell désactivé, aucune autorisation irréversible. Pas de terminal administrateur hôte. L'état d'une mission n'est pas encore un contrôleur durable reprenant automatiquement une installation longue après reboot : prérequis futur de 14.
