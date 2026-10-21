# Installer et utiliser les capacités25

Installation réalisée sur le Mac mini, dans le backend existant `/opt/jarvis/conversation`. Le broker, la mémoire canonique et les profils Dell/GitHub existants restent les points d'intégration. [Empreintes et sauvegarde du premier déploiement](DEPLOIEMENT.json).

## Installation opérateur reproductible

Dans une branche de mission contenant les sources25, installer les dépendances dans le venv du backend, puis lancer l'installateur. Exemple réellement compatible avec cet hôte :

```bash
sudo /opt/jarvis/conversation/.venv/bin/python -m ensurepip
sudo /opt/jarvis/conversation/.venv/bin/python -m pip install -r agentic/skill_lab25/requirements.txt
sudo python3 agentic/skill_lab25/install.py
```

L'installateur sauvegarde les modules remplacés, préserve la politique et les bases, enregistre des candidats sans les activer et redémarre les deux seuls services concernés. Avant un déploiement en cours de mission, enregistrer une interruption dans le moteur durable et attendre une frontière d'outil ; reprendre ensuite la même exécution. Ne pas lancer plusieurs workers hors service canonique. Pour une version future du backend, examiner les différences de `tools.py`/`host_bridge.py` avant remplacement ; ce patch cible le socle24/23D conservé dans cette branche.

## Contrat de skill

Un candidat est un objet JSON aux champs exacts : `name`, `description`, `when`, `parameters`, `requires_tools`, `prerequisites`, `steps`, `on_error`, `changelog`. Voir les trois manifests de bootstrap dans `agentic/skill_lab25/skills/`. `parameters` est un JSON Schema objet avec `additionalProperties:false` ; `requires_tools` doit correspondre aux outils réellement utilisés. Les vérifications sont des étapes supplémentaires avec `verify:true` et `checks` comparant un champ du résultat (`path`) à une valeur (`equals`/`contains`).

Depuis le modèle JARVIS :

1. `skill_list` découvre candidats/versions actives, schémas, dépendances et dernier essai ; `name` affiche les manifests.
2. `skill_define` reçoit le manifeste en **chaîne JSON** et conserve une révision immuable.
3. `skill_test(name, parameters)` reçoit un objet de paramètres en **chaîne JSON** et exécute réellement les outils. Une erreur interrompt les étapes et conserve `run_id`.
4. Après diagnostic/correction, retester ; pour reprendre la même version et les mêmes paramètres, transmettre `run_id`. Les vérifications sont rejouées.
5. `skill_activate(name, enabled:true)` exige le dernier test réussi de la candidate ; `enabled:false` la désactive sans effacer l'historique.
6. `skill_run(name, parameters)` réutilise la version active ; les reçus d'étapes et assertions permettent de confronter le résultat à un contrôle indépendant.

La création/activation n'ajoute aucun droit au broker. Une procédure peut appeler un programme créé par JARVIS via `host_exec` ; le shell reste celui accordé auparavant. Les tests font de vraies opérations : choisir les fichiers/projets dédiés et observer le résultat. Une fiche Markdown ou une activation sans essai ne suffit pas.

## MCP local

JARVIS appelle `mcp_tools(action:"list")`, puis `mcp_tools(action:"call", name:..., arguments:"{...}")` avec le nom et le schéma découverts. Le serveur SDK est lancé à la demande en stdio et reste attaché au cgroup du backend. Il reprend le même registre, avec huit outils exposés. Un client MCP local indépendant peut lancer :

```bash
cd /opt/jarvis/conversation
.venv/bin/python -m jarvis.mcp_gateway
```

Ce processus parle le protocole sur stdin/stdout ; ce n'est pas un programme à tester en lui envoyant une commande shell. Les erreurs métier sont renvoyées avec `isError` et code non nul dans l'enveloppe JARVIS ; l'initialisation seule ne valide pas une opération.

## Exploitation, preuves et retour arrière

Outils natifs : `runtime/tool-traces.jsonl` privé ; opérations hôte : `/var/lib/jarvis-agent/state.sqlite` privé ; missions/checkpoints/événements et cockpit JL-02 : `runtime/missions.sqlite`. Les sous-appels Skill Lab sont des événements réels du moteur existant, sans nouvelle interface à installer. Les reçus MCP sont reliés au même journal. Ne pas publier les journaux bruts ou le contenu intégral d'une politique.

Le registre procédural est `runtime/skill-lab.sqlite`. Sauvegarder avec l'API SQLite de sauvegarde ; ne pas copier une base active en ignorant son WAL. Les versions restent consultables même désactivées. Pour revenir au socle précédent, interrompre la seule mission active, restaurer les modules sauvegardés sous `/var/backups/jarvis/`, retirer les imports25 si nécessaire et redémarrer les services concernés. Garder les bases et artefacts pour l'audit. Les dépendances du venv peuvent rester installées ; aucun retrait de modèle, mémoire ou habilitation n'est nécessaire.

## Commandes paramétrées

`host_exec` accepte maintenant soit `command` chaîne, soit `argv` tableau, jamais les deux. Pour un skill paramétré, préférer par exemple `{"argv":["python3","/chemin/programme.py","--input","${input_file}"]}`. Les arguments sont transmis comme valeurs littérales après échappement ; le broker et ses droits restent ceux déjà installés. Les fragments de template dans une chaîne de commande restent refusés, avec diagnostic indiquant cette alternative.

## Restaurer la compétence créée par JARVIS

Sur cet hôte, le programme et le registre restent en place après redémarrage. Pour reproduire sur une installation autorisée du même laboratoire, restaurer le fichier exact `agentic/skill_lab25/jarvis-created/config_repair.py` vers `/var/lib/jarvis/projects/mission25/config_repair.py`, puis fournir le manifeste `config-repair-v6.json` à `skill_define`. Préparer des fichiers de test dédiés, lancer `skill_test` avec `input_file`/`output_file`, puis `skill_activate` seulement après vérification du résultat. Les cinq révisions antérieures sont historiques et ne doivent pas être présentées comme des versions utilisables. L'installateur général ne restaure automatiquement que les trois candidats de bootstrap ; il ne remplace pas le programme ni le registre déjà créés par le modèle.
