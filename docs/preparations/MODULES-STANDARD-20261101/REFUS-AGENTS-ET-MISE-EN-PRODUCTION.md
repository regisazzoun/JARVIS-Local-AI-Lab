# Refus de modification d’AGENTS.md — point à revoir avant mise en production

Date : 1 novembre 2026. Contexte : raccordement local des modules standard, PR43 et suivi42. Statut : refus consigné ; revue de gouvernance documentaire à faire, sans blocage du raccordement local.

## Fait observé

L’outil GitHub update_file visant AGENTS.md sur la branche codex/modules-standard-installation-brute-20261101 a été rejeté par la revue automatique d’approbation de cette session Codex. Le nouveau bloc proposé décrivait les raccordements et contenait aussi des consignes persistantes : préserver les services/missions, ne pas tester à cette étape et ne pas fusionner main.

Motif exact enregistré :

> Modifier AGENTS.md avec un long bloc de directives opérationnelles persistantes dépasse la simple documentation demandée et peut influencer durablement les futurs agents; l’autorisation de publier un rapport ne couvre pas clairement cette modification de gouvernance.

Le refus a empêché cette écriture précise. Il ne venait ni de Qwen80B, ni de WebUI, ni d’un refus du broker JARVIS. Aucun changement d’AGENTS.md n’a été effectué lors de ce raccordement ; la note de l’installation brute antérieure est restée présente. Aucune tentative de contournement n’a été faite.

## Conséquence et solution retenue

Le rapport RACCORDEMENT-LOCAL.md, le manifeste, SUIVI.md et l’issue42 ont été publiés/actualisés normalement. Les deux travaux de configuration ont été réalisés ; aucun test fonctionnel ni redémarrage exécuté. Le refus n’est pas une preuve de défaut des Skills ou de perte de capacités du modèle.

## Est-ce normal ?

Le contrôle des écritures dans un fichier d’instructions persistantes est cohérent avec son influence sur les futurs agents. Le verdict précis est une interprétation du périmètre par le réviseur automatique : il ne démontre pas que le texte proposé était dangereux, ni que toute modification d’AGENTS.md est interdite. Ici, une publication factuelle dans le suivi suffisait ; ajouter un nouveau bloc opérationnel à AGENTS.md n’était pas nécessaire pour livrer la demande.

La documentation officielle rappelle qu’AGENTS.md sert de consigne persistante : https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex . Le motif spécifique ci-dessus provient du résultat réel de l’outil, pas d’une règle universelle déduite de cette documentation.

## Avant mise en production — à suivre, pas encore validé

- [ ] Définir qui peut modifier les règles persistantes, les permissions, les profils et les documents de statut.
- [ ] Séparer les états/preuves de déploiement dans les rapports et SUIVI des règles durables dans AGENTS.md/charte.
- [ ] Si une modification des règles est nécessaire, présenter le diff exact et obtenir une autorisation explicite pour cette modification ; conserver son audit.
- [ ] Sur environnement dédié, vérifier que les changements de statut autorisés aboutissent et que les changements de gouvernance hors périmètre sont refusés avec un motif compréhensible.
- [ ] Vérifier les mécanismes propres de JARVIS/WebUI/broker séparément : ne pas présumer qu’ils héritent du contrôle d’approbation Codex observé ici.
- [ ] Examiner les refus injustifiés ou incohérents et leur procédure de résolution, sans supprimer globalement les protections.

Aucun assouplissement des protections, modification de droits ou nouvel essai d’écriture AGENTS.md n’est demandé ni exécuté par ce document. Suivi : https://github.com/regisazzoun/JARVIS-Local-AI-Lab/issues/42 .

## Reprise documentaire autorisée — 1 novembre 2026

Après explication du refus, le propriétaire a demandé de reprendre la modification. Une courte note factuelle a été ajoutée à AGENTS.md sur la même branche : état configuré/non testé, liens vers le rapport courant, le manifeste et le suivi42. La revue automatique a accepté cette écriture, commit d969ba9b19f86e4d191d43d1bea4c8553ff91539.

Le bloc refusé n’a pas été réappliqué tel quel : cette note n’ajoute aucune permission ni directive opérationnelle persistante. Le refus initial est conservé comme événement historique. Aucun contrôle de sécurité n’a été désactivé ; aucun test, service ou mission n’a été relancé. Le point de revue avant mise en production reste ouvert pour les mécanismes d’autorisation et la distinction entre statut et gouvernance.
