# Attribution et limites des preuves

| Élément | Auteur / opérateur réel | Preuve |
| --- | --- | --- |
| Extension Python du moteur, schémas, installation, tests logiciels | Codex | Sources `agentic/engine_v2`, installateur26,105 tests |
| Fixtures settings/original/consumer et objectif brut | Codex | OBJECTIF-BRUT, fixtures versionnées |
| Plans et révisions proposés | JARVIS | 3 versions reçues, propositions refusées conservées |
| Sélection des outils et écritures de démonstration | JARVIS, exécution hôte par broker | PREUVES-JARVIS et CORRELATION-BROKER |
| Diagnostic de la fausse réussite du skill | JARVIS | Port99999 conservé malgré skill passed, lecture et FAIL sémantique |
| Correctif de is_valid_port | JARVIS | host_edit_file réel : borne1..65535, reçu et SHA256 |
| API append, schémas et contrats structurés, statuts partiels | Codex | Événements de déploiement, jamais une autocorrection du modèle |
| Contrôles déterministes et rapport factuel | JARVIS-engine | Événements semantic_verification/report_facts_checked |
| Rapports libres et rapport de résolution | JARVIS | Artefacts bruts conservés, errata prioritaires |
| Vérification de fichiers, programmes, services, mémoire, GitHub et réception | Codex | JSON indépendants, sept cas du programme corrigé |

14 événements Codex explicites sont présents à cet export ; ils comprennent installation, interruptions/corrections d'interface et rappel du livrable omis. Ils ne sont pas des opérations autonomes JARVIS. Les essais de fausse réussite exécutés directement par Codex sont séparés et ne sont pas injectés dans les reçus modèle.

Le programme modifié reste `/var/lib/jarvis/projects/mission25/config_repair.py` ; JARVIS a amélioré ce fichier existant. La version historique reste inchangée dans `agentic/skill_lab25/jarvis-created/`, la nouvelle est exportée octet pour octet sous `agentic/mission_engine26/jarvis-created/`. Codex exporte ces octets, il n'a pas écrit le correctif. Le manifeste historique reste version6 ; ne pas inventer une nouvelle révision de skill. Son vérificateur interne textuel reste faible ; le moteur autonome ajoute la barrière sémantique indépendante.

Les critères de création d'un nouveau skill sans aucun ajustement infrastructure restent réservés à la future épreuve14A. Le nouvel outil mission_action est vérifié par tests logiciels de reprise/doublon ; son utilisation par le modèle dans cette démonstration n'est pas revendiquée.
