# Architecture retenue — mission25

Le point d'autorité reste le broker Unix et sa politique propriétaire persistante. Le transport reçu en24 n'est pas remplacé. Le point de découverte des outils est `Registry.specs`, également utilisé par `Registry.schemas`, `capability_status` et le serveur MCP25. Les états de ressources et les résultats de tests ne sont pas déduits de l'exposition d'un schéma.

## Skill Lab exécuté

`jarvis/skill_lab.py` compose les outils existants, sans charger un module Python tiers dans le backend. Un manifeste JSON porte description, conditions, schéma des paramètres, prérequis, dépendances exactes, étapes, assertions de vérification, conduite sur erreur et journal de correction. Les scripts développés par JARVIS passent par `host_exec` et son confinement existant ; les actions SSH/Ansible/GitHub restent structurées par le broker.

Le registre procédural `runtime/skill-lab.sqlite` conserve versions immuables et empreintes, auteur de définition, version active, exécutions et checkpoints par étape. Il ne remplace pas la mémoire canonique SQLite/FTS5. Une définition identique est idempotente. Une nouvelle version reste candidate ; la version active antérieure est conservée. Activation impossible tant que le dernier test réel de la candidate n'est pas réussi. Désactivation sans effacement. L'activation est accordée dans la mission propriétaire, sans confirmation humaine supplémentaire.

Avant le premier effet, tous les paramètres et arguments d'étapes sont validés avec JSON Schema. La substitution `${param}` remplace seulement une valeur entière ; elle n'interpole pas un fragment shell. Les outils récursifs ne sont pas admis dans les étapes. Chaque étape passe par `Registry.execute`, conserve son reçu broker et est inscrite dans le journal durable/cockpit. Une assertion échouée donne un résultat échoué, même si la commande a un code0. La reprise explicite par `run_id` exige mêmes paramètres, version et mission ; les étapes d'action réussies sont conservées et les vérifications sont réexécutées.

Les prérequis déclaratifs décrivent les conditions ; les étapes doivent sonder les préconditions observables nécessaires. Les droits restent vérifiés à chaque sous-appel. Les tests ont des effets réels dans les seuls espaces autorisés : ils ne prétendent pas être une simulation ni un environnement séparé pour SSH.

## MCP installé

`jarvis/mcp_gateway.py` utilise le [SDK Python officiel](https://github.com/modelcontextprotocol/python-sdk), version installée1.30.0. Le [transport stdio](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) évite un nouveau service réseau. Le client JARVIS négocie la session, exécute `tools/list` ou `tools/call`, puis ferme le sous-processus. Protocole négocié lors du prévol Codex :2025-11-25.

Les [contrats d'outils MCP](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) sont dérivés du même registre. Huit outils utiles sont exposés : état de capacités, services, journaux, lecture fichier, SSH, Ansible, liste et exécution des skills. L'outil `mcp_tools` permet au modèle de découvrir puis appeler cet adaptateur ; l'ensemble des47 outils natifs reste disponible. Le catalogue MCP n'ajoute aucune habilitation et n'expose pas un serveur arbitraire fourni par le modèle.

Les sous-processus MCP lancés par le service gardent son cgroup et leurs appels broker sont identifiés `JARVIS-runtime`. Les reçus MCP sont aussi reliés aux événements de mission ; la connexion seule n'est pas une preuve d'exécution. `PREUVES-JARVIS.json` distingue les prévols Codex et les appels du modèle. Aucun raccordement voix23D/mémoire n'est déclaré ici.

## Limites de cette version

Exécution séquentielle et arrêt au premier échec ; la correction est conçue par JARVIS, pas par une boucle cachée du Skill Lab. Le checkpoint est écrit après chaque reçu ; après un arrêt entre effet externe et enregistrement, il faut observer l'état avant répétition. La version actuelle ne fournit pas de transaction distribuée exactement une fois. Les assertions sont déclarées par l'auteur du skill et exigent une réception indépendante pour éviter un test trop faible. MCP externe HTTP et chargement automatique de serveurs tiers ne sont pas implémentés.

## Amélioration observée de l'interface de commande

Les essais du modèle ont révélé plusieurs tentatives répétées d'interpolation d'un chemin dans une chaîne shell. Codex a donc étendu `host_exec` avec `argv`, tableau de chaînes exclusif avec `command` (contrat JSON Schema `oneOf`). Le client traduit le tableau avec `shlex.join` avant le même appel broker ; aucun nouveau droit ni outil hôte privilégié n'est introduit. Dans les skills, chaque paramètre peut occuper un élément entier d'`argv`. Le test de non-interprétation des espaces/métacaractères passe. JARVIS a effectivement adapté puis exécuté sa compétence avec cette interface : il ne s'agit pas d'un correctif de son programme réalisé par Codex.

Cette amélioration est une intervention d'infrastructure pendant le scénario de développement. Elle ne permet pas de revendiquer que toute sa résolution s'est déroulée sans assistance. Les manifestes et le programme avant/après restent attribués au modèle ; l'erreur d'interface et sa correction appartiennent au coordinateur.
