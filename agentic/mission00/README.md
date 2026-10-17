# Client d’audit documentaire — mission 00

Ce client réutilise les classes installées `jarvis.core.Core`, `Memory` et `Registry`, le transport Ollama réel et le broker propriétaire. Il ne réimplémente ni boucle d’outils, ni serveur, ni base de mémoire. Il ne recharge aucun service.

L’interface conversationnelle générale a montré des arrêts après lectures, des réponses vides et des digressions sur les préférences vocales. Le client utilise un contexte documentaire propre à la mission et expose au modèle les outils hôte de lecture/écriture et les sélecteurs documentaires, selon la phase du plan. La politique root et les contrôles de chaque outil restent effectifs. Les préférences et l’identité globales ne sont pas modifiées ; les conversations et audits rejoignent la base canonique existante.

Exécution opérateur, sur l’installation JARVIS existante :

```bash
/opt/jarvis/conversation/.venv/bin/python agentic/mission00/run-task.py \
  --task JARVIS-00-02 \
  --instruction-file /chemin/prive/instruction.txt \
  --output /chemin/prive/resultat.json
```

L’instruction contient l’objectif, pas une invocation d’outil imposée ou un résultat simulé. Qwen choisit et appelle les outils, observe leurs retours puis produit les fichiers. Le résultat brut contient des traces privées : la mission publie des preuves expurgées et des livrables revus, avec attribution séparée de Codex et JARVIS.

Le client attend au démarrage qu’aucune requête canonique ne soit déjà active. Il ne constitue pas un verrou distribué ni un nouveau superviseur système. Les limites du modèle, le contrôle indépendant des fichiers et les essais infructueux restent documentés dans le bilan agentique.

## Lectures structurées et plan guidé

Les sélecteurs de `audit_tools.py` renvoient des extraits et cellules réellement lus via le broker existant, sans attribuer de verdict ni écrire l’analyse. Leur code est une contribution Codex. Les paramètres du modèle et les identifiants de preuves des appels restent journalisés.

Le mode guidé reçoit une liste de fichiers d’entrée et un livrable. Il expose d’abord les seuls lecteurs, puis l’écriture après réception des lectures, sur une génération suivante. Ainsi, une écriture prédite avant d’avoir reçu les données n’est pas acceptée comme analyse de celles-ci. Le modèle choisit les appels et rédige le contenu. Par défaut le contrôleur s’arrête après l’écriture réelle, sans fabriquer de réponse du modèle ; Codex effectue la relecture et la réception sémantique séparément. `--finish readback` demande une relecture par le modèle et `--finish report` sa clôture propre, deux comportements qui restent moins fiables dans les essais.

Les rapports locaux ne déclenchent pas artificiellement l’exigence de deux pages web du moteur conversationnel général. Cette configuration appartient au seul client d’audit ; les contrôles de la politique root restent actifs, les secrets ne sont pas exposés et les comptes/services sont conservés. Ce guidage ne prouve pas une planification autonome générale ni la réception14A.

Les seules lectures documentaires nécessaires ont été ajoutées temporairement à la politique par l’opérateur, dans le périmètre autorisé. Les 517 ajouts ont été retirés à la réception, sans changer les dix racines initiales, les droits permanents 11B ou les droits d’écriture. Une réutilisation doit disposer de lectures bornées aux sources de son propre périmètre ; le modèle ne modifie pas lui-même la politique.

## Concordance du catalogue de missions

`python3 agentic/mission00/sync-mission-index.py` vérifie les identifiants du registre, leur présence unique dans le tableau courant de SUIVI, puis l’égalité des intitulés et états du catalogue README. `--write` actualise ce catalogue après révision du suivi. Les deux lignes de regroupement historique/activité transversale sont explicitement exclues ; les dix incréments natifs restent prévus, non exécutés. Ce contrôle est documentaire et ne sollicite ni le modèle ni les machines distantes.
