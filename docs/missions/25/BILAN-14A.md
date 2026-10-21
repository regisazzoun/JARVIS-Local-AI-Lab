# Réévaluation14A — mission25

**Verdict : 🟡 en cours.** Les capacités outillées progressent réellement ; les critères d'autonomie globale ne sont pas tous reçus. Il ne s'agit ni de maintenir les anciens blocages de transport déjà levés, ni de déduire un GO d'une installation de catalogue.

## Critères de référence retrouvés

Le référentiel original accessible est la section14A de ROADMAP (inventaire, planification, outils autorisés, recherche, détection/correction, vérification, restitution de preuves), complétée par `docs/missions/13D-E/AGENT-14A.md`. Aucun rapport final autonome14A n'a été retrouvé. Le contrat ancien propose un banc VM ; il n'est pas une réception et ses restrictions historiques de droits sont dépassées par11/11B et les ordres récents. L'absence de nouveau PXE/RAID/installation de VM dans25 n'est pas transformée en blocage artificiel du progrès agentique ; le Dell2 demeure hors périmètre.

| Critère | État observé en25 | Preuve / portée exacte |
| --- | --- | --- |
|Inventorier ses capacités|Démontré avec erreurs de sélection et de synthèse| Catalogue réel, fichiers et GitHub ; premiers mauvais hôte/action/dépôt conservés, droits non révoqués. [État initial](INVENTAIRE-INITIAL.md). |
|Planifier une mission|Partiellement démontré| Codex a fourni le graphe de quatre lots correspondant au cahier propriétaire. JARVIS choisit outils, programme, manifests et itérations ; aucun `mission_plan` autonome pour un objectif global non décomposé n'est démontré ici. |
|Exécuter plusieurs outils sur le matériel|Démontré| Debian/processus/systemd, Ansible et SSH Dell1, GitHub, MCP stdio et skills actifs ; reçus `JARVIS-runtime`, aucune substitution de Codex opérateur. |
|Rechercher une solution technique|Démontré| Deux pages officielles Python (`json`, `pathlib`) effectivement lues par JARVIS pendant le développement. |
|Détecter, corriger et recommencer|Démontré avec assistance d'infrastructure| JARVIS corrige son chemin distant, les types/dépendances du manifeste, crée/modifie son programme et répare0/chaîne invalide. Les répétitions de templates nécessitent l'ajout `argv` par Codex ; la panne stdin Ansible est aussi corrigée par Codex. |
|Conserver le contexte et reprendre|Démontré sur services/checkpoints| Même exécution, versions/activations/runs et empreintes de tâches préservés après redémarrage ciblé ; reprise des tâches suivantes. Aucun reboot global revendiqué. |
|Vérifier indépendamment|Démontré sur les sorties concrètes ; généralisation limitée| SSH relit le fichier Ansible, JARVIS relit les JSON et compare les empreintes, GitHub relit les blobs. Contrôle Codex confirme les deux résultats. Le vérificateur interne du skill créé se limite toutefois à un code0 et au mot `status` : ce contrôle ne suffit pas à garantir seul la sémantique d'un résultat futur. |
|Rapporter fidèlement et publier les preuves|Partiellement démontré| Publications réelles et rapport de réutilisation cohérent ; inventaire et rapport de développement comportent encore des erreurs factuelles. [Erratum de réception](TESTS-REPRISES.md). |
|Réutiliser une compétence sans nouveau correctif|Démontré sur une seconde tâche| Même programme et skill révision6, second fichier, désactivation/refus/réactivation et résultat idempotent ; zéro nouvelle instruction de coordination pendant `d_reuse`. |

## Réserves historiques effectivement levées

Ne plus conserver comme blocages14A : absence générale d'accès Debian, lecture/écriture hôte, SSH/Ansible Dell1, publication GitHub, découverte des outils ou reprise du transport après redémarrage.11/11B/21/22/24 apportaient déjà ces acquis ;25 ajoute un registre de skills exécutables réellement créés, testés, versionnés et réutilisés, plus l'appel MCP effectif. Le profil Dell était déjà habilité : les mauvais sélecteurs de l'inventaire ne révoquent rien.

## Interventions Codex, distinctes des actions du modèle

Codex conçoit/déploie Skill Lab/MCP, fournit les trois compétences initiales et le graphe d'essai, crée les fichiers de test dédiés, corrige stdin Ansible, ajoute `argv` après échecs répétitifs, améliore les diagnostics, vérifie et consolide la publication. Le programme `config_repair.py`, ses modifications, ses six manifests, ses essais et ses appels réutilisés sont JARVIS. L'export de leurs octets dans le dépôt est une opération documentaire Codex, pas une écriture du programme à sa place.

## Travail précis restant pour clôturer14A

Un scénario inédit peut couvrir les réserves restantes : confier à JARVIS un objectif technique non prédécoupé, lui faire enregistrer son propre plan et créer/adopter une compétence avec les interfaces désormais installées, résoudre son échec sans nouvel ajustement d'infrastructure par Codex, vérifier le résultat par une observation séparée et produire un rapport exact sur le code, les reçus et les contributions. Renforcer les vérifications du skill créé au-delà d'une présence textuelle de `status` ; confronter notamment port et conservation des champs au résultat réellement écrit.

La seconde opération25 montre déjà une moindre dépendance pour la réutilisation. Elle ne prouve pas à elle seule une nouvelle création complète sans aide. La réserve de rapport reste actuelle : `JARVIS-DEVELOPPEMENT.md` annonce source-b à0 alors qu'elle contient une chaîne, décrit une correction «si !=8091» alors que le programme accepte les entiers positifs, et omet l'origine Codex de la nouvelle interface `argv`. Ces erreurs ne sont pas effacées ni attribuées à un transport qui fonctionne.

## Tâche à faire — épreuve finale 14A (décision propriétaire du 21 octobre 2026)

**Statut : 📋 planifiée, à reprendre ultérieurement. Aucun test, aucune exécution et aucune clôture 14A demandés pour l'instant.**

Objectif : évaluer de manière ciblée l'autonomie globale restante de JARVIS en capitalisant sur les acquis reçus des missions 11/11B, 21/22, 24 et 25, sans répéter les vérifications déjà acquises.

Critères de la future épreuve :
1. Confier à JARVIS un **objectif technique inédit non prédécoupé** ; JARVIS élabore et enregistre lui-même son plan, ses étapes et ses critères de succès.
2. JARVIS choisit ses outils, **crée ou adapte un skill**, le teste, le corrige après une erreur représentative puis l'utilise réellement **sans nouvel ajustement d'infrastructure ou plan imposé par Codex pendant l'épreuve**.
3. JARVIS contrôle indépendamment le résultat effectif, au-delà d'un code de retour 0 ou de la présence de `status` : état exact produit, conservation des éléments attendus, gestion des erreurs et idempotence selon le scénario retenu.
4. Il produit un rapport final fidèle aux preuves, distinguant **actions JARVIS, interventions Codex, résultats prouvés, hypothèses et erreurs**, avec correspondance aux reçus d'exécution et aux fichiers/commits.
5. La réception confronte ces résultats aux critères historiques de 14A. Attribuer **✅ GO** uniquement si les critères sont effectivement satisfaits ; sinon conserver **🟡 ouverte** avec écarts précis. Codex peut vérifier indépendamment après l'exécution sans se substituer à JARVIS.

**Important :** cette inscription est une tâche future, **pas le lancement de l'épreuve**, ni une autorisation de lancer un nouvel environnement, ni une remise en question des réceptions 25/24 et des anciens acquis.

