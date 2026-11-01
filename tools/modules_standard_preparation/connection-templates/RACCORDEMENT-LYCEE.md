# À compléter au lycée — aucune cible active

1. Régis fournit les machines et le périmètre de découverte autorisé. Renseigner infrastructure.csv, aucun scan avant cette définition.
2. Après déplacement : adresses, routes, DNS, comptes et empreintes/certificats. Garder les secrets dans des fichiers privés, jamais dans Git.
3. Ansible : inventory.yml est vide. Les group_vars en .example sont inactifs ; ne copier que le transport adapté après contrôle de l’OS et des droits. ansible.cfg pointe vers les collections isolées et conserve le contrôle des clés d’hôte.
4. Cisco : compléter le testbed à partir de l’exemple amont, remplacer ses exemples par les vrais équipements et définir la liste de devices autorisés.
5. NetBox : choisir Enhanced pour lecture/écriture, renseigner URL et droits. Nagios : Core/CGI et CA. pfSense : version réelle, REST API v2 et CA ; aucune installation automatique sur le pare-feu.
6. mcp-lycee.pending.json est un dossier de candidats, pas une configuration importée. Les secrets doivent remplacer les références seulement dans une copie privée.
7. mcpo-local.pending.json prépare un éventuel raccordement HTTP des six MCP locaux pour WebUI. Il n’est pas ajouté au MCPO actif ; aucun service démarré/rechargé et aucun endpoint fictif enregistré dans WebUI. Les Skills WebUI utilisent déjà la voie native Open Terminal.
8. Référentiels français CIEL/BTS et gabarits : à fournir. Les ressources pédagogiques CC BY-SA nécessitent attribution et respect de leur licence.
9. Tests réels et réception : différés. Prévoir des objets/fichiers dédiés et vérifier codes retour, contenu, arrêt après résultat et rendu visuel. Aucune mission historique à reprendre.
