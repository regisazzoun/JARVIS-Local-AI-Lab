# Tests ciblés, incidents et reprises

## Logiciel

[Exécution enregistrée](TESTS-LOGICIELS.json) : **35 tests réussis**, aucun échec ni erreur. Seize nouveaux tests de provenance, compteurs, refus des faux reçus et continuité du dialogue ; dix-neuf tests existants ciblent journal, dépendances, checkpoints, isolation conversation et contexte. Les fixtures d’inférence simulée servent uniquement à tester le logiciel ; elles ne prouvent aucune autonomie.

Le garde refuse notamment un test non réussi, une autre version, une correction déclarée sans changement observé et une réexécution à issue inconnue. Une analyse peut porter sur une opération réellement exécutée, même si son étiquette déclarative était incorrecte.

## Réel

Deux lots natifs sont validated. L’oracle Codex passe de4/12 à11/12 puis12/12 sur **chacun** des deux Dell. Les fichiers finaux relus sont identiques, leurs empreintes correspondent aux contrôles. [Journal A–E](JOURNAL-DEMONSTRATION.md), [preuve indépendante](VERIFICATION-INDEPENDANTE.json), [sources](demo/final/).

## Incidents conservés

1. Cinq refus de plan avant installation du garde des erreurs de format : limite de trois non tenue dans ce premier essai. Codex interrompt, clarifie le contrat et conserve les reçus.
2. Résultats structurés masqués par une vue texte, puis dialogue réinitialisé trop souvent : Codex rétablit les données typées et la continuité native pendant chaque quantum. Ce n’est pas une réparation applicative JARVIS.
3. Notes textuelles d’acceptation placées par Codex dans un champ réservé aux contrats exacts : métadonnées de lancement corrigées, aucun plan ou critère reçu supprimé.
4. Candidats de plan incomplets, identifiants d’exigence inventés et versions périmées : refus conservés ; interfaces clarifiées. Le contrôle détecte l’omission de Q2.
5. Confusion entre décision, exécution et SHA : références d’exécution typées et diagnostics indiquant les candidats réellement observés. L’audit complet conserve les autres identifiants.
6. Validation d’une ancienne copie ou du même hôte : refus ; Qwen demande lui-même copie et nouveau test.
7. Test40088 avec exception attendue non capturée : processus1 réellement observé, un cycle infructueux Q1 ; Qwen corrige sa commande puis40117 passe.
8. Assertion40262 déclarée correct : processus1, aucun fichier changé. Qwen identifie le pop mutateur et applique40292. L’étiquette n’est pas une preuve de modification.
9. Rapports ERR30 : nouvelle racine présente en RW puis remontée RO par doublon. Codex retire uniquement le doublon ; son écriture/lecture indépendante réussit, puis JARVIS écrit et fait recevoir ses propres rapports.
10. Rapports libres incorrects : originaux archivés, deux révisions finales par Qwen ; arrêt après trois textes. [Errata](ERRATA-RAPPORTS.md), sans effacement des anciens résultats.

## Trois cycles et persistance

Les compteurs applicatifs finaux sont Q1=1 cycle infructueux, Q2=0 ; ils survivent aux reprises et redémarrages des workers. Les noms de tâches ou operation_id ne remettent pas ces compteurs à zéro. Le seuil de trois est testé logiciellement ; une série réelle de refus comparables d’interface conduit également à l’état interrupted et à l’escalade.

Des reprises Codex suivent des changements techniques documentés (schéma, restitution, continuité, séparation des phases). Les compteurs et refus antérieurs restent dans le journal, y compris un compteur de refus dépassant trois après une reprise coordonnée. Il ne faut pas présenter cette campagne comme exempte de dépassement initial ni comme une démonstration de trois corrections applicatives échouées en production.

Après les premières mises au point, les réparations du programme et le choix des tests restent Qwen. Codex n’a pas fourni de patch applicatif à exécuter sous attribution JARVIS.

## Contexte

106 inférences observées sur Dell1 ; fenêtre24576, maximum18161 tokens de prompt et18551 prompt+génération, quatre compactions moteur, aucun cycle_error. La revue du journal d’inférence complète ces métriques : [preuve](CONTEXTE-PREUVES.json). La première recherche lexicale de logs, trop large, est conservée séparément ; truncated=0 et making room ne sont pas des erreurs. Ce constat est borné à la campagne, sans réception générale de la Phase2.

La revue sémantique du journal observe106 `truncated=0`, zéro troncature positive et zéro erreur mémoire/contexte. Les154 correspondances du premier filtre Codex comprenaient106 fins normales,47 évictions du cache et une note de capacité configurée : elles ne représentaient pas154 erreurs. [Rectification du contrôle Codex](CONTEXTE-RECTIFICATION.json).
