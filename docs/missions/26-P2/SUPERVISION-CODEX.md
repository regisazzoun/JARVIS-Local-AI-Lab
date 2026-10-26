## Réception ciblée terminée —26octobre2026

Les dix cas P2 sont reçus avec réserves, événement44885. Leur entrée quitte la liste active `tasks` du registre runtime pour `received_tasks`, avec les références de réception et sans effacement des compteurs. Le timer reste actif mais ne relance pas ces cas. La mission native reste en revue d’intégration ; P3/P4 ne sont pas envoyées. Les passages antérieurs ci-dessous restent l’historique. Le marqueur interactif MANUAL-HOLD est retiré après publication et contrôle de la liste vide.

# Supervision persistante des escalades P2

Le moteur arrêtait correctement certaines répétitions, mais aucun relais périodique ne traitait les escalades M26-P2 après le tour interactif Codex. Les workers restaient disponibles alors que la mission était interrupted. Le superviseur déjà installé pour JL03 accepte maintenant une configuration de périmètre ; son comportement et ses unités JL03 restent conservés.

## Périmètre

- Mission native unique `3aa717f3887e49daa7daf7e883ee52e4`, priorité P2 uniquement ; registre runtime `/var/lib/jarvis/projects/mission26-phase2/REGISTRE-CODEX.json`.
- Contrôle par `jarvis-m26-p2-supervision.timer`, toutes les120secondes après la fin du passage précédent. `jarvis-m26-p2-supervision.service` invoque le même `/usr/local/lib/jarvis-coordination/periodic_codex.py` avec configuration M26-P2.
- Si mission arrêtée, en attente de revue, ou sans modification/test depuis10minutes : passage Codex ciblé, puis main rendue à Qwen. Aucune décision technique courante ne passe systématiquement par Codex.
- Trois passages maximum pour une même cause stable. Le hash ignore noms de session et nouveaux contenus de résultat ; compteurs reconstruits depuis les événements canoniques si le cache privé disparaît. Aucun quatrième passage aveugle.
- Aucun P3/P4,14A,24Old,nouveau modèle, changement de routage ou autre mission. Pas de fusionmain. La réception P2 exige tous ses scénarios réels, pas les seuls tests logiciels candidats.

## Exécution et preuves

Les événements `coordinator_periodic_started/finished` sont dans la mission existante, avec acteur Codex-periodic. Les sorties CLI restent privées sous `/home/adminjarvis/JARVIS/mission26-phase2-private/supervision/`. Aucun deuxième moteur ni base opérationnelle n’est créé. L’unité sérialise les passages et le script maintient un verrou ; un dépassement de420secondes est enregistré comme échec, avec arrêt du groupe de processus. Trois essais infructueux restent un blocage explicite.

Le CLI a réellement répondu `M26_SUPERVISION_READY`. Le contrôle sans lancement a réellement détecté l’escalade42889. Trois tests logiciels ciblés vérifient cause stable, absence de quatrième passage même après perte du cache, et refus d’une mission hors périmètre ; ces fixtures ne sont pas des interventions agentiques réelles. L’activation et le premier contrôle du service sont à relire dans les événements et `systemctl list-timers`.

Référence technique : [mode non interactif Codex](https://learn.chatgpt.com/docs/non-interactive-mode). Authentification CLI persistante existante réutilisée, aucun secret publié.

## Intervention interactive et retour arrière

Avant modification manuelle, vérifier si le service superviseur exécute déjà un passage. Créer `MANUAL-HOLD` dans son répertoire privé pour différer les nouveaux passages, attendre la fin du passage actif, puis intervenir. Supprimer ce marqueur après restitution au moteur. Un passage périodique ne crée pas ce marqueur puisqu’il détient déjà son verrou.

Pour retirer seulement cette supervision : arrêter/désactiver `jarvis-m26-p2-supervision.timer` ; ne pas toucher aux anciens timers JL03. Configuration et prompt du périmètre sont privés. L’ancien script commun a été sauvegardé avant son extension ; les valeurs par défaut JL03 sont préservées. Un arrêt matériel, une limite du compte Codex ou trois corrections infructueuses restent des limites réelles, jamais une preuve d’activité continue.

## Lecture de preuves corrigée

Le refus42889 venait d’un nom de fichier UUID utilisé dans mission_evidence. L’option `authority_typed_evidence` masque cet ancien outil uniquement pour cette mission. `authority_read_execution` propose les références entières réellement enregistrées et restitue une fenêtre des sorties du reçu complet contrôlé par SHA. La lecture réelle de42878, lignes35à79, a réussi et montré la table erronée `events` dans le candidat. Les refus historiques et failed_cycles=4 sont conservés ; aucune nouvelle remise à zéro.

### Correction de classification du lecteur

Le premier usage réel sur un ancien test échoué a révélé que le Registry assimilait son code retour historique à un échec du lecteur. Le champ est désormais `observed_process_returncode`, vérifié par un test d’intégration exécutant le Registry avec SQLite temporaire. Les24tests du garde/lecteur passent. L’ancien événement42906 reste conservé avec son erratum. Les unités et les scripts d’installation sont publiés sous tools/mission26_phase2 ; aucun état simulé n’est présenté comme une exécution de Codex.
