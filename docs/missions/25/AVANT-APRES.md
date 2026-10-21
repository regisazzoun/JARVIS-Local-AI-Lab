# Comparaison avant/après25

| Dimension | Départ mesuré | Résultat réel |
| --- | --- | --- |
|Outils natifs exposés|41 ;28 entrées hôte dans le reçu initial|47 ;six interfaces nouvelles (`skill_list/define/test/activate/run`, `mcp_tools`). `host_exec` enrichi avec `argv`, sans nouvel outil privilégié. |
|Compétences exécutables|Pas de Skill Lab versionné raccordé au modèle|Quatre skills testés et actifs ; trois bootstrap Codex, un créé par JARVIS avec six révisions de manifeste et deux versions de programme conservées. |
|Interopérabilité MCP|Aucun chemin MCP natif démontré|SDK officiel, serveur local stdio à la demande, huit schémas dérivés du registre ; découverte et appel de service réels par JARVIS. |
|Erreur et correction|Mauvais sélecteurs et défaut stdin ; rapport trop général| Chemin distant corrigé par JARVIS ; stdin et interfaceargv corrigés par Codex ; adaptation/test/réutilisation du skill par JARVIS. |
|Réutilisation|Procédures textuelles et outils ponctuels existants| Même skill/code utilisés sur un second fichier sans nouveau correctif ni instruction de coordination pendant cette tâche. |
|Persistance|Acquis moteur/broker déjà reçus en22/24| Nouveau registre/activations/runs préservés après redémarrage ; tâches et artefacts conservés ; réutilisation ultérieure effective. |
|Réception14A|Ouverte, accès outillés démontrés avec assistance|Toujours ouverte ; réserves désormais précises sur plan autonome, aide d'infrastructure et fidélité/vérification sémantique. |

## Mesures observées, sans faux benchmark

[Mesures calculées](MESURES-AVANT-APRES.json) : avant le premier déploiement,11 retours hôte réussis sur17 ; après,49 sur52 à la clôture des quatre lots. Les commandes sous-jacentes des skills sont comptées, leurs enveloppes ne sont pas recomptées. Les six échecs initiaux comprennent mauvais hôte/action/dépôt/chemin et panne stdin ; les trois échecs hôte après comprennent chemin distant, lecture de `/tmp` hors politique et rejet JSON volontaire attendu.

Les scénarios diffèrent : ces fractions ne mesurent pas un gain contrôlé de vitesse ou de raisonnement. Les essais de manifests ont leurs propres échecs, exclus des fractions hôte :8 définitions dont2 refusées ;8 tests de skills dont4 réussis et4 échoués ;7 utilisations dont6 réussies et1 refus attendu après désactivation. Les quatre compétences possèdent chacune un test réel réussi de leur version active.

Les traces contiennent des lectures, corrections et révisions : ce ne sont pas autant de progrès utiles. La création de compétence a demandé plusieurs versions inutilisables avant l'ajoutargv ; cette répétition demeure un résultat négatif de l'essai, pas un succès masqué par le catalogue.
