# Réception de la préparation P4-ACTIVE-PREP

**VALIDÉ AVEC RÉSERVES**, réception indépendante71632. Mission native
`e98fd4bbe37c492b922db9b5a1d782aa` completed ; trois tâches validated,
revue finale PASS71627 et bilan enregistré71630. Les trois fichiers ont été
relus par Codex, leurs empreintes comparées aux tâches et le rapport enregistré
comparé à son reçu SHA256. Il ne s’agit pas de la réception globale P4.

## Réserves et rectification indépendante

Codex a fourni les interfaces et un retrait éditorial limité sur un rapport de
tâche. La clôture finale et la rédaction sont réellement JARVIS ; l’autonomie
éditoriale générale reste non reçue. Les anciens brouillons, FAIL et
INSUFFICIENT sont conservés. Le bilan final brut reste publié sans réécriture.

Dans la première ligne des sources, la parenthèse `770102e22b...` est erronée :
elle reprend une autre invocation et ne désigne pas le reçu broker du premier
appel. La référence principale complète est correcte. La table suivante fait
foi pour la corrélation ; cet erratum ne modifie pas l’original ni son ancien PASS.

| Invocation originale | Opération | Reçu broker exact |
|---|---|---|
| 4b50149f1ed64aa49bc33f934b7d33e7 | is-active du worker principal | ff29a21714654638b0e0408ac4b7015b |
| 770102e22b5547c199f0865705b917c7 | is-active du worker slot2 | dbd0a2f77f164a3dad687c5d94410a40 |
| 0fb4bdcfb1854f8ba96408a887be056a | show du worker slot2 | 32de1a1fb304465f82e34b332718f53d |

Les états systemd sont des observations historiques. Ils ne prouvent ni le
code chargé actuel ni un déploiement de l’attestation. Le plan canari/rollback
reste une proposition ; sa mise en œuvre doit être vérifiée séparément.

[Bilan JARVIS original](JARVIS-BILAN-PREPARATION-ORIGINAL.md) ·
[Preuves de réception](RECEPTION-PREPARATION-ACTIVE.json) ·
[Suite réellement transmise](LANCEMENT-CANARI-STAGING.json).

## Continuité

Sous-unité séquentielle `c32347de3edf4288a4751a3e65afa7eb`, P4-CANARY-STAGE,
transmise dans le même moteur et sous le même parent. Qwen choisit son plan et
la répartition entre Dell1 et Dell2. Objet : adapter le raccordement reçu à la
base canonique actuelle, préparer un artefact/version et une vérification
indépendante avant activation. Aucun ancien worker complet ne doit écraser les
correctifs récents. Aucun service actif modifié dans cette seule unité de
staging ; la réception des huit situations P4 reste ultérieure. Pas de rejeu
P2/P3 ni campagne précédente du candidat inchangé, aucun14A/24-Old/mainmerge.
