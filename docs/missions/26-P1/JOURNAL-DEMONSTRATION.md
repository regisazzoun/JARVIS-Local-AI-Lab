# Démonstration réelle et décisions — 26 octobre 2026

Mission canonique `e26946bff84d4e06ad395b969ffcd72f`, projet isolé `mission26-phase1`. Les références numériques ci-dessous sont les identifiants d’événements dans [PREUVES-JARVIS.json](PREUVES-JARVIS.json), avec décisions, paramètres, reçus et horodatages. Les commandes applicatives sont écrites par Qwen ; les enveloppes de confinement, transfert et observation sont Codex.

## A — Décider, localiser et planifier

L’objectif initial demandait de réparer un module conformément à son README et de distribuer exécution/validation. Codex fournit le programme défectueux et ses critères de comportement, sans fichier à réparer, correctif, commande de test ou découpage opérationnel. Qwen choisit les lectures Dell1 (39633/39638, 39645/39650), identifie les défauts de validation et de mutation, puis propose ses lots.

Les premiers appels de plan sont refusés pour format ; un candidat omet Q2 et le contrôle de couverture le refuse (39727). Le plan reçu comporte deux lots décidés par Qwen (39796/39797). Trois versions persistantes, auteurs `JARVIS/Qwen80B@Dell1`, restent dans l’export. Les motifs de certaines révisions décrivent encore un ancien état : ils ne remplacent pas les observations de fichiers.

## B — Modifier et tester sur Dell1

Qwen choisit `labtool/codec.py` et écrit sa validation stricte sur Dell1 (décision39839, exécution39844). Empreinte observée : `7c20488f5185762faf4567c6d65bfba0955af9cf1ef23f9d536fc634f9e336e6`.

Pour Q2, une commande d’assertion déclarée «correct» échoue sans changer aucun fichier (40257/40262). C’est une vérification exécutée, pas une correction effectuée ni une absence de test. Qwen diagnostique le `pop` mutateur (40271), puis choisit un `sed` qui corrige réellement `labtool/buckets.py` sur Dell1 (40287/40292). Le contrôle local40305 réussit. Empreinte finale : `b23c8d2a7114f082ffc6724c0f6b394a0431f9dbaf10a4a6fa455247ae728730`.

## C — Exécuter réellement sur Dell2

Qwen choisit Dell2 pour ses validations. Le premier contrôle39858 exécute vraiment Python et importe le module, mais porte sur l’ancienne version et imprime FAIL malgré un code0. Qwen identifie lui-même la copie obsolète (39866), choisit fichier/sens de transfert et demande la synchronisation SHA (39883/39897).

Après transfert, les contrôles Dell2 sont notamment40088 (processus1), 40117 (processus0, Q1) et40357 (processus0, Q2). Il ne s’agit ni de simples connexions SSH ni de lectures de répertoire. Le broker vérifie clé SSH épinglée et `identity_check` avant chaque opération.

## D — Valider la version exacte sur l’autre machine

| Critère | Correction observée Dell1 | Test réel Dell2 | Acceptation Qwen + observation fraîche | Version du manifeste |
|---|---|---|---|---|
| Q1 | 39844 | 40117 | 40163 /40167 | `dbd7be7c1ae23b75b0b8037e0fc3f7999ec7df60bfe617393f8d54d1c25f2e06` |
| Q2 | 40292 | 40357 | 40379 /40383 | `83917aa83be9f55b26a22f78a29241df4e64c15ef14e2a2181c1937ccc4760a8` |

Les fichiers du manifeste sont README et trois sources Python ; les commandes de test sont conservées séparément dans les reçus. Aucun commit Git distant n’est inventé : Git n’est pas présent dans ces exécutants. Les sources finales ont été relues sur les deux Dell, comparées entre elles et à l’oracle indépendant (40404, [preuve](VERIFICATION-INDEPENDANTE.json)).

La tentative40313 annonce «Dell2» dans ses paramètres d’acceptation, alors que sa référence40305 est un test Dell1. Le garde la refuse : la machine attestée par l’exécution prime sur la machine annoncée.

## E — Interpréter l’échec et choisir la suite

40088 est un test effectivement exécuté sur Dell2, avec traceback et code1 : l’exception attendue n’est pas capturée. Le compteur conserve un cycle infructueux Q1. Qwen choisit ensuite un test qui capture explicitement ValueError (40112), l’exécute réellement (40117) et obtient un code0. Codex n’a fourni ni cette commande corrigée ni le correctif applicatif.

Des acceptations erronées sont refusées : référence de décision utilisée comme exécution, test non réussi, source qui n’est pas une correction et validation sur le même hôte. Les améliorations d’ergonomie des références sont Codex, pas une autocorrection autonome de JARVIS.

## Contrôle indépendant Codex

Même oracle, exécuté réellement sur chaque Dell, sans modifier les sources :

| État | Dell1 | Dell2 | Interprétation |
|---|---|---|---|
| Initial | 4 PASS /8 FAIL | 4 PASS /8 FAIL | Défauts réellement présents |
| Après Q1 | 11 PASS /1 FAIL | 11 PASS /1 FAIL | Q2 reste incorrect |
| Final combiné | 12 PASS /0 FAIL | 12 PASS /0 FAIL | Q1 et Q2 conformes dans ce périmètre |

Les contrôles couvrent notamment les entiers, booléens, chaînes, champ absent, négatifs, propriétés supplémentaires, conservation des entrées, regroupement, ordre et labels. Cet oracle est Codex ; il ne doit pas être attribué à JARVIS.
