# Installation et utilisation du périmètre Phase1

L’installation réellement constatée est décrite dans [INSTALLATION-PREUVES.json](INSTALLATION-PREUVES.json). Les empreintes des fichiers installés correspondent aux sources de cette branche. Le moteur, ses workers, le broker et SQLite restent les composants existants.

## Provisionner sans écraser

`tools/mission26_phase1/provision.py` utilise les profils SSH existants et épinglés. Sans option, il inspecte les scopes ; avec `sudo python3 ... --apply`, il ajoute les deux seuls projets autorisés et la racine locale des rapports. Il ne copie ni ne réinitialise les sources. Une nouvelle exécution réelle a confirmé une politique inchangée et la conservation des fichiers.

Le projet de cette réception est `mission26-phase1`, racine distante `/opt/jarvis-lab/mission26-phase1` sur chaque Dell, racine locale `/var/lib/jarvis/projects/mission26-phase1`. Ne pas ajouter cette même racine aux read_roots : elle est déjà lisible par son droit d’écriture et un bind RO ultérieur masquerait le RW.

Sauvegarder les sources installées avant de copier tools.py, durable_cycle.py et distributed_authority.py depuis `agentic/engine_v2/jarvis/` vers `/opt/jarvis/conversation/jarvis/`. Conserver le module historique jl03_assist.py. Compiler ces fichiers, vérifier les tests ciblés puis recharger les workers au repos. La conversation et JL03 n’ont pas nécessité de redémarrage. [Retour arrière](MODIFICATIONS-ET-RETOUR-ARRIERE.md).

## Lancer par le moteur existant

Le point d’entrée existant `POST /api/missions` accepte `goal`, `model`, `project` et `spec`, sous l’authentification habituelle. Pour **ce contrat expérimental précis**, utiliser `project=mission26-phase1` et :

```json
{
  "distributed_authority": true,
  "authority_requirements": ["Q1", "Q2"],
  "autonomous": false,
  "assurance": false,
  "authority_interface_epoch": "phase-separated-dialogue-v4"
}
```

Ces deux derniers booléens de mode désactivent le contrat automatique de plan/rapport26B pour cette exécution particulière ; ils ne signifient pas que Codex décide des réparations. Le plan est produit par Qwen et ses prérequis d’exécution/version sont ceux de l’adaptateur. **La réception ne qualifie pas l’intégration de ce chemin aux contrôles complets autonomous/assurance26B.** Ne pas présenter cette exception comme un remplacement général du mode canonique.

Le champ model doit appartenir aux modèles acceptés par l’API ; le rôle mission est routé par la configuration existante. L’outil exige ensuite une observation effective de `qwen3-coder-next:q4_K_M` sur Dell1 pour attribuer la décision. Le modèle demandé ne suffit pas à attester cette identité.

La réception a été initialisée dans le même MissionStore par Codex ; elle est consultable sous l’identifiant `e26946bff84d4e06ad395b969ffcd72f`, avec les mécanismes existants de missions et événements. L’API de consultation et la présentation JL03 ne sont pas remplacées.

## Limites d’intégration

Activation explicite, projet et critèresQ1/Q2 configurés pour cette démonstration. Les autres missions gardent leur interface et leurs gardes historiques. La généralisation des profils et le raccordement par défaut de toutes les missions JL03 ne sont pas livrés. Ne pas relancer le scénario reçu en écrasant les correctifs ou ses checkpoints.

L’oracle reproductible `tools/mission26_phase1/independent_oracle.py` s’exécute dans la copie réelle du projet sur un Dell, sans modifier les sources. Son exécution sur Mac n’est pas une preuve distante. L’export `export_evidence.py MISSION --output CHEMIN` lit le journal canonique ; les conversations, secrets, politiques et clés SSH ne sont pas exportés.
