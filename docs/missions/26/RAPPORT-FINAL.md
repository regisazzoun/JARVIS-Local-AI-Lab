# Réception mission26 — moteur résilient

**✅🟡 GO avec réserves.** Moteur installé sur le backend existant et réellement utilisé par JARVIS. Exécution `28c3fdf877ba47718dfc55e46f386656` : 3/3 tâches reçues, état durable `completed`, 3 versions de plan. Aucune fusion main.

## Résultats effectivement établis

- JARVIS reçoit un [objectif brut](OBJECTIF-BRUT.json), sans tâches soumises, et produit son [plan versionné](PLAN-JARVIS.md). Le premier plan est incomplet ; un rappel de résultat attendu et des améliorations d'interface Codex sont nécessaires. Les tâches et dépendances sont bien proposées par le modèle, pas écrites silencieusement par Codex.
- Les [neuf modules installés](VERIFICATION-INDEPENDANTE.json) étendent les missions/checkpoints/broker/skills existants.50 outils natifs observés, trois ajouts26 : mission_verify,mission_report_facts,mission_action. Quatre skills actifs conservés ; aucune cinquième compétence fictive comptée.
- Le skill historique annonce passed tout en conservant99999. JARVIS observe le [FAIL sémantique](PREUVES-JARVIS.json), examine son programme, corrige lui-même la borne haute puis réexécute le skill et obtient8091 avec champs conservés. Le correctif du programme est JARVIS ; les extensions moteur/API et leur déploiement sont Codex.
- Le moteur exige des preuves exactes et récentes. Code0/status seuls sont insuffisants ; PASS/FAIL/PARTIAL/INSUFFICIENT restent distincts. Les contrôles sont réutilisables par les futurs skills, avec contrats objets paramétrables. La forme historique du manifeste6 reste textuelle ; les nouvelles missions autonomes ajoutent la vérification sémantique, et tout nouveau candidat autonome doit en comporter une.
- La [reprise de deux tâches reçues](REPRISE-DEUX-TACHES.json) conserve identifiant, états, empreintes et plans. La préservation des47 tâches historiques, des checkpoints antérieurs, des témoins25, de la mémoire et des services est contrôlée indépendamment. Politique inchangée ; aucun broker reconstruit.
- 105 tests logiciels réussis et [sept cas réels du programme corrigé](TESTS-PROGRAMME-JARVIS-CODEX.json) passent, avec idempotence des octets et erreurs. Ces vérifications Codex ne remplacent pas les preuves agentiques du modèle.

## Rapport, erreurs et attribution

[Attribution complète](ATTRIBUTION-CODEX-JARVIS.md), [tests/reprises et errata](TESTS-ET-REPRISES.md), [faits du journal](FAITS-JOURNAL.json), [corrélation indépendante broker](CORRELATION-BROKER.json), [artefacts et empreintes](ARTEFACTS.json), [architecture](ARCHITECTURE.md), [installation/utilisation](INSTALLATION-UTILISATION.md).

Les sorties originales erronées sont conservées. La clôture autonome archive le texte libre et produit une synthèse factuelle déterministe depuis les reçus. Les erreurs de prose restantes sont rectifiées séparément, notamment hypothèse d'idempotence, comportement sans champ port/label et gestion des erreurs de fichier. Il ne s'agit pas d'une démonstration de rédaction autonome universellement exacte.

## Critères de réception

| Critère | Verdict et portée | Preuves |
| --- | --- | --- |
| 1 — Plan global proposé par JARVIS sans tâches soumises | ✅🟡 GO avec réserves | [OBJECTIF-BRUT.json](OBJECTIF-BRUT.json), [PLANS-JARVIS.json](PLANS-JARVIS.json) |
| 2 — Plan exploitable et durable, versions et auteurs | ✅ GO | [PLANS-JARVIS.json](PLANS-JARVIS.json), [REPRISE-DEUX-TACHES.json](REPRISE-DEUX-TACHES.json) |
| 3 — Opérations réellement exécutées par JARVIS | ✅ GO | [PREUVES-JARVIS.json](PREUVES-JARVIS.json), [CORRELATION-BROKER.json](CORRELATION-BROKER.json) |
| 4 — Détection de résultat incorrect malgré skill passed | ✅ GO | [EVENEMENTS.json](EVENEMENTS.json), [SKILLS-JARVIS.json](SKILLS-JARVIS.json) |
| 5 — Diagnostic, correction et reprise | ✅🟡 GO avec réserves | [PREUVES-JARVIS.json](PREUVES-JARVIS.json), [REPRISE-DEUX-TACHES.json](REPRISE-DEUX-TACHES.json) |
| 6 — Vérification par état effectivement relu | ✅ GO | [VERIFICATION-INDEPENDANTE.json](VERIFICATION-INDEPENDANTE.json), [TESTS-PROGRAMME-JARVIS-CODEX.json](TESTS-PROGRAMME-JARVIS-CODEX.json) |
| 7 — Rapport final fidèle aux événements et acteurs | ✅🟡 GO avec réserves | [JARVIS-RAPPORT-FACTUEL.md](JARVIS-RAPPORT-FACTUEL.md), [FAITS-JOURNAL.json](FAITS-JOURNAL.json), [TESTS-ET-REPRISES.md](TESTS-ET-REPRISES.md) |
| 8 — Capacités antérieures conservées | ✅ GO | [VERIFICATION-INDEPENDANTE.json](VERIFICATION-INDEPENDANTE.json) |

## Réserves de réception

L'autonomie progresse par la planification enregistrée, le diagnostic et correctif applicatif réellement JARVIS, la reprise et les contrôles exacts. Elle reste assistée : premier plan incomplet, nombreuses erreurs de contrat/version, onze déploiements d'infrastructure en cours de réception et rappel du livrable réutilisable, clarification de patch et rafraîchissement du contexte. Ces interventions empêchent un GO sans réserves sur l'autonomie longue. Le nouvel outil de clés d'opérations est testé logiciellement ; son usage par JARVIS n'est pas revendiqué ici. Les manifests de skills ne figent pas à eux seuls les octets d'un programme externe : le correctif est exporté avec son SHA256 et l'ancien programme reste versionné.

**14A reste 🟡 ouverte, épreuve finale 📋 différée**, sans lancement automatique. [Bilan14A](BILAN-14A.md).24-Old non lancée ; Dell2, OS/RAID, SSH/Tailscale, JL-02 et LiveKit préservés ; aucun test vocal physique supplémentaire revendiqué.

Publication sur `codex/mission-26-mission-engine`, base `plan/mission-26-moteur-agentique` conservant les PR antérieures. Le fichier PUBLICATION.json contient la PR et les relectures distantes après publication. **ROADMAP ↔ SUIVI synchronisés, format SUIVI conservé.**
