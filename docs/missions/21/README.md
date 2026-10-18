> **Continuité mission22 (18 octobre2026).** Copie de la source initiale, conservée pour historique. La reprise réelle est suivie dans [réception22](../22/RECEPTION-MISSION21.md) et dans [ETAT sur la branche de travail21](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/blob/jarvis/mission-21-autonomie/docs/missions/21/ETAT.md). Les rapports courants seront réconciliés à la réception.

# Mission 21 — Autonomie opérationnelle JARVIS
**Statut initial : prévue, non exécutée.** Exécutant : **JARVIS seul**, via ses outils hôte/SSH/Ansible/GitHub. Matériel : Mac mini Debian et **Dell n°1**. Cette mission ne concerne ni le Dell n°2 (mission 14) ni le calcul distribué (mission 20).

## Démarrage
1. Lire réellement `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, `SUIVI.md`, `ROADMAP.md`, puis `docs/missions/11B/RACCORDEMENT-ADMIN-DELL.md` et le rapport de mission 00.
2. Lire `ETAT.md` pour retrouver le **premier lot non terminé** et les résultats précédents.
3. Lire uniquement la fiche `TACHES/0N-*.md` correspondante, exécuter ses opérations et les contrôles.
4. Enregistrer **les preuves réelles** dans `/var/lib/jarvis/projects/mission21/` et le rapport public expurgé dans ce dossier GitHub, sur cette branche.
5. Mettre à jour `ETAT.md` (état, preuve, prochaine tâche), puis poursuivre **automatiquement dans l'ordre 01 → 07**, sans validation humaine intermédiaire. En cas de blocage réel, noter la cause et continuer les tâches indépendantes.
6. Finir par `RAPPORT-FINAL.md`, actualiser `SUIVI.md` et `ROADMAP.md` dans cette branche, publier et vérifier les commits. Pas de fusion automatique dans main.

## Tâches
| Ordre | Fiche | Objectif |
|---|---|---|
| 01 | [Santé](TACHES/01-SANTE.md) | Inventaire Mac mini + Dell |
| 02 | [Journaux](TACHES/02-JOURNAUX.md) | Anomalies actuelles et corrections applicables |
| 03 | [Documentation](TACHES/03-DOCUMENTATION.md) | Rapports techniques persistants |
| 04 | [Concordance](TACHES/04-CONCORDANCE.md) | Changements depuis mission 00 |
| 05 | [Administration Dell](TACHES/05-ADMIN-DELL.md) | Modification réelle via SSH/Ansible |
| 06 | [Supervision](TACHES/06-SERVICE.md) | Installer et contrôler un service |
| 07 | [VNC](TACHES/07-VNC-TAILSCALE.md) | KDE via LAN et Tailscale |

## Règles de réception
- Un outil **exécuté et observé** prime sur une réponse textuelle. Distinguer `réussi`, `réussi avec réserves`, `bloqué`, `échoué`, `à faire`.
- Garder les accès SSH clés **et** mot de passe, Tailscale, les services Mac mini/JARVIS/Ollama, la mémoire canonique et le DHCP Bbox. Ne toucher ni au RAID ni aux disques ; ne pas installer le Dell n°2.
- Utiliser la politique hôte persistante réellement disponible ; un refus d'outil est un blocage technique à rapporter, **pas** une réussite. Ne pas inventer de nouvelles approbations humaines au sein de ce périmètre déjà lancé.
- Ne jamais publier de secrets, mots de passe, clés, UUID/séries, journaux privés ou jetons. La publication distante exige une vérification du commit et de la présence des rapports.
- La mission 21 contribue aux preuves de **14A**, sans valider automatiquement 14A ni modifier le périmètre de la mission **14**.

**Autorisation du propriétaire :** exécution complète des sept tâches sur Mac mini et Dell n°1, sans Codex comme exécutant et sans validation intermédiaire. Toute impossibilité réelle doit être expliquée et l'exécution des autres tâches poursuivie.
