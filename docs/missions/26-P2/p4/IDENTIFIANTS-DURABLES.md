# Identifiants d’opération attribués par le moteur

## Problème constaté

JARVIS réutilisait un nom d’opération avec une autre commande ou description. Le refus était légitime, mais la création manuelle des noms et leur répétition bloquaient la mission d8fe752876db480cbe5f22cd5525e2dd. Trois passages de coordination étaient épuisés ; aucune relance inchangée n’était justifiée. Le propriétaire demande une correction pérenne, dans cette même mission.

## Contrat corrigé par Codex

Le mode authority_engine_operation_ids retire operation_id des schémas authority_work et authority_edit. Les nouvelles missions distribuées soumises par Missions.submit utilisent ce mode par défaut ; un choix legacy explicite est conservé. La missionP4 existante est migrée explicitement, sans nouvelle mission, nouvelle base ou remplacement de plan.

Avant chaque outil, DurableCycle et le chemin de chat lié à une mission ouvrent un contexte d’invocation issu du tool_calls canonique. Authority vérifie que cet appel existe, est started, appartient à la mission/tâche courante et porte réellement la commande ou les éditions demandées. L’identité call:<invocationUUID> est ensuite attribuée par le moteur. Le modèle ne peut ni choisir la clé ni substituer une commande sous un autre appel. Une invocation étrangère, terminée ou absente échoue avant délégation ; aucun identifiant aléatoire de secours.

Les décisions techniques restent attribuées àQwen : outil, code, commande et exécutant. L’événement authority_operation_identity attribue séparément la métadonnée au moteur, avec lien vers la décision et l’appel canonique. Les anciens alias et leurs reçus restent intacts ; le modelegacy continue de refuser leurs collisions.

## Idempotence et preuves

Le registre AttemptLedger existant conserve le contrôle des intentions : commande, classe d’opération, exécutant et manifeste de source observé. Le nouveau mode y ajoute la tâche afin de ne pas réutiliser une exécution d’une tâche précédente comme preuve d’une tâche nouvelle. Un changement de description n’est pas une nouvelle commande. Une répétition identique au même état retrouve le reçu, marqué cached=true et original_reference ; elle n’est pas annoncée comme une nouvelle exécution.

Un résultat réutilisé reste une observation historique, pas une preuve fraîche d’un service dont l’état externe a pu changer. Les observations sémantiques de l’état réel utilisent le vérificateur existant, qui relit effectivement sa source. Cette correction ne revendique pas un exactement-une-fois universel pour tous les effets possibles d’une commande.

Une opération dont l’effet est inconnu demeure bloquée, même sous une nouvelle invocation ou une autre commande de correction. Les compteurs et l’identité des problèmes sont partagés, non remis à zéro. Une troisième erreur continue d’arrêter les essais. Les diagnostics liés à des références sorties du périmètre actif sont masqués dans la vue de travail, avec leurs auteurs/compteurs toujours conservés dans le journal.

## Migration contrôlée

Les compteurs de problèmes et de refus, ainsi que les anciens alias, ont été comparés avant/après activation : identiques avant remise en file. Un ancien candidat JARVIS59858 avait un effet connu (enfant terminé, source modifiée, résultatinconclusif, unknown_outcome=0). Ce candidat a été remplacé par la correctionCodex61369, retestée nativement61801/61857. Sa tentative784193e8d7cf4da28095f77ef58cd79e a été placée BLOCKED avec motif de supersession et preuve62708 : aucun succès attribué, aucun faux échec de test ajouté. Cette quarantaine explicite du candidat obsolète permet la prochaine correction ; elle ne s’applique jamais aux effets inconnus.

SDK copié surMac et deuxDell ; workers et conversation rechargés après validation, sans changementOllama/modèle/routage. Une première suite distante a révélé un chemin d’identité Mac figé dans la fixture de test ; la fixture pointe désormais vers l’identité du vrai export. Cet échec de fixture est conservé, distinct d’un échecJARVIS. Les fichiersoriginaux et le spec précédent sont sauvegardés en privé.

Retour arrière : interrompre la mission, restaurer SDK/spec sauvegardés, retirer le nouveau module si absent avant installation et recharger les mêmes services ; réaligner les exportsDell au même source approuvé. Ne pas restaurer une ancienneSQLite ni effacer les événements/compteurs ; la tentative supersédée reste non reçue et aucun effet inconnu n’est rejoué.

## Validation

130tests locaux ciblésPASS après les dernières modifications, dont14nouveaux tests d’intégration du protocole. Ces14tests passent surchaqueDell : commandes distinctes sans clé modèle ; déduplication après nouvelle description/redémarrage de registre ; nouvelles tâches et sources distinctes ; résultat inconnu bloqué ; troisième échec maintenu ; appels étrangers/terminés refusés ; substitution de commande refusée ; aucun fallback ; modelegacy ; éditionlittérale ; vrai cheminDurableCycle ; choixpar défaut de l’API ; conservation des anciennes analyses horsvueactive. Ce sont des fixtures logicielles, pas des preuves d’autonomie.

Les usages réels deJARVIS sont à documenter séparément. P4 globale, instrumentation duworker actif et scénarios déploiement/rollback restent distincts de cette correction de transport.

[Déploiement et tests](IDENTIFIANTS-DEPLOIEMENT.json). Codeinitialdf59962, affinagefbe1790, fixtureportable62376a3 ; branchePhase2 etPR29, aucune fusionmain.


## Utilisation réelle reçue

Preuve indépendante62931 : trois appelsnatifs Qwen sansoperation_id, chacun lié au bon appelSQLite et à une identitéattribuée parlemoteur. Les deux premières décisions avaient la même commande/exécutant et des descriptionsdifférentes. Exécutionréelle62737, puis résultat réutilisé62774 avec cached=true/original_reference=62737 ; pas de secondecommande. Les anciens alias sont encore strictementidentiques. Une troisième inspection distincte a bien été exécutée62798 et échoué sur une classeWorker inexistante : c’est un défaut distinct d’interprétationdes sources, pas une collision d’identifiants. Les fixtures14cas ont aussi réussi surlesdeuxDell ; aucun nouveau processusmoteur ni missionprimaire créé.

[Appels et reçus JARVIS](IDENTIFIANTS-PREUVES-JARVIS.json). Cette réception porte surleprotocole d’identité/déduplication, pas sur touteP4.
