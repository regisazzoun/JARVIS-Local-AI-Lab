# Plan proposé, sans mise en œuvre

| Action | Priorité existante | Problème démontré | Machines/composant | Solution réutilisée | Développement évitable | Effort estimé | Dépendances | Risque | Réception |
|---|---|---|---|---|---|---|---|---|---|
| R01 | P3 | Budget Qwen Code divergent | mac/dell1 / Qwen Code + guard | unifier réglages et mesure de requête sur version épinglée | gestion parallèle de budgets | 0,5–1,5j | lecture version/config effective | moyen | session longue sans échec de compaction ; pas de troncature silencieuse |
| R02 | P4 | Six modules runtime divergent du Git de base | mac / déploiement | manifestes SHA + profils Ansible existants | copies/patches manuels non reproductibles | 1–2j | conserver patches historiques | moyen | reconstruction candidate identique ; aucun patch perdu |
| R03 | P5 | Résumé Qwen invente données malgré outils corrects | mac/dell1 / rapports | facts structurés + contrôles déterministes déjà installés | reformulations répétées | 0,5–1j | préserver erreurs 190/192 | faible | relevé exact des sorties et unités ; erreur factuelle refusée |
| R04 | P1 | Dell 2 sans Git/npm et sans rôle d’inférence | dell1/dell2 / profils logiciels | rôles Ansible selon besoins de build | installations uniformes inutiles | 0,5–1j | définir projets exécutables | moyen | matrice de rôle + build représentatif sur même version |
| R05 | P6 | Profils UI confondent chat et mémoire canonique | mac / Open WebUI/JL03 | configuration des profils et API existantes | second historique présenté comme mémoire unique | 0,5j | pas de migration des données | faible | conversation/missions suivent le parcours annoncé |
| R06 | P7 | Diagnostic GPU complet non reçu | trois hôtes / supervision | nvidia_gpu_exporter ou collecte nvidia-smi existante + incident canonique | nouveau collecteur général maison | 1–3j | P2/P3/P4/P5 selon registre P7 | moyen | repos sans faux incident ; panne attendue détectée et reprise vérifiée |
| R07 | P1 | Dell 2 sans accès Tailscale direct observé | dell2 / réseau | client Tailscale existant amont si besoin de rôle | tunnels ad hoc | 0,5j | identité propre ; droits domaine | moyen | accès autorisé prouvé sans copie identité Mac |
| R08 | P5 | Éducation lectures reçues, clients/écritures non reçus | mac / Google MCP | réutiliser connecteur existant ; réception ciblée | remplacement inutile du connecteur | 0,5j | OAuth Éducation obtenu | faible | Docs/Sheets readback et parcours WebUI/Code Éducation |
| R09 | à rattacher au registre existant | Deux chemins Google et plusieurs sondes | mac / connecteurs/collecte | dépréciation guidée par consommateurs ; catalogue généré | interfaces redondantes | 1–2j | inventaire usage avant suppression | moyen | aucun consommateur orphelin ; un contrat par fonction |
| R10 | P9 | Coût et supervision des décisions encore assistés | mac/dell1/dell2 / missions | tâches courtes + Qwen Code + preuves existantes | nouvel agent/framework complet | 1–3j | P3/P4/P5 reçus dans leur portée | moyen | tâche inédite conclue sans correction Codex ; échecs conservés |

Estimations d’ingénierie, pas délais garantis ni travaux lancés. Corrections rapides : R03/R05/R08 ; standardisation intermédiaire : R01/R02/R04/R07/R09 ; évolution ciblée : R06/R10. Ne pas sommer mécaniquement : dépendances et travaux communs se recouvrent. Aucune nouvelle mission numérotée créée.

Référentiel de priorités retrouvé sur la branche docs/architecture-priorites-p0-p3-20261025 : P0.1–P3.2 sont des axes historiques distincts du registre opérationnel P0–P9. Les notes P7 précisent P2 boucles, P3 contexte, P4 code réel, P5 réception, P6 visibilité, P7 GPU, P9 autonomie. Le libellé courant de P8 n’a pas été retrouvé dans un registre opérationnel complet ; aucun libellé n’est inventé. Les rattachements ci-dessus sont proposés et n’altèrent pas le registre.

P4 reste en pause propriétaire, MANUAL-HOLD conservé. Ce plan ne la relance pas et ne clôture ni14A ni24-Old. Le socle installé et les réceptions historiques restent acquis dans leur portée.


[Comparatif des standards et contrats](COMPARATIF-STANDARDS.md).

R09 inclut la séparation des façades Google personnel/professionnel demandée par le propriétaire : réutiliser le même connecteur amont, mais exposer des identités d’outils et des droits propres aux profils. Critère : un client du profil Éducation ne peut pas sélectionner le jeton personnel par simple paramètre. Le stockage distinct actuel ne suffit pas à démontrer ce contrat.
