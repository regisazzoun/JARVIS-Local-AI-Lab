# État initial mesuré — mission25

Exécutant : JARVIS/Qwen, exécution persistante `4612213a05624836abec58385813439c`, tâche `a_inventory`. Le [rapport initial du modèle](JARVIS-INVENTAIRE.md) est conservé comme production brute ; il n'est pas approuvé intégralement. Les appels, erreurs, reçus et acteurs sont dans [PREUVES-JARVIS.json](PREUVES-JARVIS.json), le catalogue reçu avant extension dans [CATALOGUE-INITIAL.json](CATALOGUE-INITIAL.json).

Le registre installé initial expose41 outils natifs, dont28 outils hôte listés par `capability_status`. Les capacités persistantes sont32, demandes5 lors du premier reçu. Ces nombres sont des objets de catalogue, pas autant d'opérations démontrées. L'accès Debian, le shell confiné, les fichiers, services/journaux, SSH/Ansible Dell1 et GitHub existent déjà. Les acquis de24 ne sont pas requalifiés ici.

JARVIS a choisi ses appels à partir d'un objectif général d'inventaire, sans liste de commandes à recopier. Il a interrogé le catalogue, exécuté une commande de répertoire, créé/relu un témoin et consulté les branches puis le README de la branche de planification. Ses premières tentatives distantes ont utilisé `dell1` inexistant, puis l'action SSH `ping` non disponible ; il a utilisé aussi un dépôt fictif `adminjarvis/mission25` et un chemin `MISSION.md` absent à la racine. Ces erreurs indiquent une sélection incorrecte, pas une révocation des habilitations.

Un échec supplémentaire est effectivement infrastructurel : Ansible a refusé le stdin non bloquant hérité. Codex a corrigé uniquement cette cause dans `run()` du broker (`stdin=DEVNULL`), puis JARVIS a lui-même réussi `host_remote identity` et `host_ansible ping`. La politique propriétaire n'a pas changé. Le moteur a refusé une première réception de tâche sans preuve SSH réussie ; après les retests, la même tâche a été validée, sans réinitialiser ses observations. Le premier inventaire demeure antérieur à ces retests.

## Rectifications du rapport initial

- `capability_status` décrit outils, ressources et demandes persistantes, pas seulement « capacités Codex ». Son argument optionnel n'est pas établi par l'affirmation du modèle : le catalogue réel fait foi.
- Le profil `dell-observe` existe déjà et est administrable ; l'action `ping` appartient à Ansible, pas au catalogue SSH. Aucune extension de droits ni nouveau dépôt n'était nécessaire.
- Le refus Ansible est un défaut d'entrée standard concret, maintenant corrigé et retesté. Il n'autorise pas à conclure que la politique exclut Dell1.
- Les dates, tailles/empreintes et compteurs cités par le modèle doivent être confrontés aux reçus. Son schéma GitHub résumé omet plusieurs actions déjà existantes.
- La procédure historique du port8091 citée dans son rapport n'est pas une correction effectuée pendant cet inventaire. Elle ne compte pas comme preuve d'autonomie25.

## Écart initial avec14A

Exécution et reprise outillées sont acquises antérieurement avec guidage ; la sélection et la synthèse restent fragiles. Aucun Skill Lab exécutable versionné/testable n'était raccordé, ni chemin MCP natif utilisable depuis le modèle. L'inventaire démontre de nouvelles erreurs de sélection et une conclusion documentaire trop large ; il ne reçoit donc pas14A par lui-même. La comparaison finale devra porter sur les nouveaux scénarios réels, en séparant corrections Codex, actions du modèle et réceptions automatiques du moteur.
