# Mission26 — Phase1 : réception Codex

**✅🟡 GO AVEC RÉSERVES — chaîne de décision et délégation démontrée dans un projet isolé.**

Le moteur installé a fait utiliser à Qwen80B des exécutants réels sur les deux Dell. Qwen a identifié les fichiers, choisi et appliqué deux réparations sur Dell1, choisi ses tests, demandé les copies vers Dell2, corrigé une commande de test après échec puis demandé les acceptations. Codex a développé et réparé l’infrastructure, fourni le programme défectueux et un oracle indépendant ; il n’a pas écrit les deux correctifs applicatifs sous attribution JARVIS.

Cette réception ne signifie pas que toutes les missions ordinaires JL03 ont basculé automatiquement sur ce contrat. L’activation est ciblée, et la fiabilité générale des rapports libres n’est pas reçue.

## Résultats établis

Mission native `e26946bff84d4e06ad395b969ffcd72f`, deux lots validated, état completed. Trois versions de plan conservent leur auteur Qwen80B/Dell1. Les106 inférences observées utilisent effectivement `qwen3-coder-next:q4_K_M` sur Dell1 ; l’identité ne repose pas sur le seul champ model demandé.

Dix-sept commandes authority_work instrumentées :13 sur Dell1,4 sur Dell2, auxquelles s’ajoutent les opérations de transport, ressources et observation. Deux changements applicatifs réels : validation stricte de count et absence de mutation du regroupement. Une commande déclarée correct exécute une assertion échouée sans modifier de fichier ; elle n’est pas comptée comme une réparation.

Les validations indépendantes JARVIS sont Dell2 :40117 pour le code Dell139844,40357 pour le code Dell140292. Le manifeste exact et la machine réellement observée conditionnent la réception. Des acceptations annoncées avec une mauvaise référence ou une fausse machine de validation sont refusées.

L’oracle **Codex** est exécuté réellement sur chaque Dell : initial4PASS/8FAIL ; après Q1 11PASS/1FAIL, échec Q2 ; final12PASS/0FAIL. Les sources finales relues sur les deux machines sont identiques et correspondent aux empreintes de cet oracle. [Preuve indépendante](VERIFICATION-INDEPENDANTE.json) · [Démonstration A–E](JOURNAL-DEMONSTRATION.md).

## Contrat de réception

| Critère | Résultat et preuve |
|---|---|
| Chemin réel des décisions identifié | ✅ [Audit](AUDIT-INITIAL.md), sources et états installés |
| Décisions Qwen80B traçables | ✅ Événements authority_model_decision liés aux inférences effectives Dell1 |
| Mac principalement orchestrateur | ✅ Pour ce projet : transport/journal/rapports ; aucune commande applicative host_exec locale |
| Dell1 modifie et teste | ✅ 39844,40292,40305 ; empreintes avant/après |
| Dell2 exécute une vraie tâche | ✅ Imports, assertions, exceptions et résultats40117/40357, pas seulement SSH/ls |
| JARVIS choisit les exécutants | ✅ Paramètres executor et demandes de synchronisation produits par Qwen |
| Résultats transmis au modèle | ✅ Reçus conservés et décisions suivantes ; dialogue outil/modèle rétabli |
| Décision après un test échoué | ✅ 40088 →40112/40117 ; également diagnostic40271 puis correctif40292 |
| Validation indépendante sur le code exact | ✅ 40167/40383, source et validateur distincts, SHA complets |
| Reçus identifiant les machines | ✅ Profils SSH épinglés +identity_check ; faux appel40313 refusé |
| Trois cycles et reprise durable | ✅🟡 Compteurs1/0 persistants, seuil logiciel et arrêts réels d’interface ; dépassement initial documenté |
| Services existants préservés | ✅ [Installation](INSTALLATION-PREUVES.json), cinq services actifs et trois anciennes missions JL03 toujours completed |
| Preuves conservées/publiées | ✅ [Export structuré](PREUVES-JARVIS.json), sources, rapports originaux et rectifications |

## Logiciel, contexte et continuité

35 tests logiciels ciblés passent :16 nouveaux,19 réutilisés. Ils vérifient contrats, provenance, compteurs, idempotence de commande, continuité du dialogue et conservation du journal. Ils ne constituent pas une preuve d’autonomie.

Fenêtre observée24576 tokens ; maximum18161 tokens de prompt,18551 prompt+génération, quatre compactions, aucun cycle_error. Le journal Ollama contient106 fins d’exécution explicitement truncated=0 et aucune troncature positive ou erreur de mémoire/contexte dans l’intervalle observé. Les47 évictions du cache de prompts ne sont pas des OOM. [Revue du contexte](CONTEXTE-PREUVES.json). Cela ne reçoit pas la refonte générale prévue en Phase2.

## Réserves importantes

1. **Assistance d’infrastructure importante.** Les schémas, références, vues de résultats, continuité du contexte et stockage ont nécessité des corrections Codex.106 inférences pour deux petits défauts montrent un coût opérationnel encore élevé. Ce n’est pas une preuve d’autonomie générale fluide.
2. **Intégration ciblée.** Le contrat opt-in couvre les profils du projet de démonstration. La généralisation des espaces et l’activation par défaut pour toutes les missions JL03 restent à faire. Ce chemin n’est pas qualifié avec les contrôles complets autonomous/assurance26B ; les autres missions conservent leur mode historique. [Utilisation et limites](INSTALLATION-UTILISATION.md).
3. **Tests du modèle partiels.** Le test Q1 reçu de JARVIS couvre count5 et l’exception pour champ absent ; le contrôle Q2 vérifie la non-mutation. La couverture élargie des comportements vient de l’oracle Codex. L’adaptateur garantit la provenance/version et l’exécution, pas à lui seul la suffisance sémantique d’un test arbitraire du modèle.
4. **Règle anti-boucle imparfaite au démarrage.** Cinq refus de plan surviennent avant correction du garde des erreurs d’interface. Les arrêts, reprises et compteurs antérieurs sont conservés, sans prétendre que la campagne entière a respecté le seuil dès sa première tentative.
5. **Restitution libre encore fragile.** Trois textes finaux sont conservés. Le dernier rétablit les principaux résultats, mais conserve un alias de projet erroné et des formulations imprécises. Aucun quatrième essai de cette rédaction : [errata Codex](ERRATA-RAPPORTS.md), originaux intacts. Un verdict du modèle n’est pas une réception indépendante.
6. **Essai limité.** Petit module Python, commandes légères, limitations par processus. Ni une longue mission applicative JL03, ni une qualification générale de l’ordonnanceur ou de la charge maximale.

## Livraison et suites

Sources installées et identiques aux fichiers de branche, procédure de retour arrière disponible. Aucun modèle, pilote, matériel, routage, service JL03 ou mémoire canonique remplacé. Les anciens protocoles JL03 déjà installés sont préservés, sans être présentés comme des choix autonomes de Qwen dans cette démonstration.

Branche `codex/mission-26-phase1-autorite-distribuee`, [PR28](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/28), empilée sur la branche précédente JL03/PR27. Aucune fusion automatique. La prochaine étape est de traiter les réserves d’intégration/contexte et de restitution, pas de relancer les correctifs reçus. **14A reste distincte et non clôturée** ; aucune mission24-Old, TTS ou installation matérielle n’est lancée.
