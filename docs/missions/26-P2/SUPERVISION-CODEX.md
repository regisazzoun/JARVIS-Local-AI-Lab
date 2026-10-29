## Actualisation après réceptionP3 —27octobre2026

P3 reçue avec réserves55310 et enregistrée dans received_tasks. Même timer réutilisé pour P4-AUDIT seule, missiond1b0d69639724c60b5bd1b2143b1a5fa, même registre/même moteur. Voir supervision-p4.example.json et M26_P2_P4_CODE_REEL.md. Le one-shot de checkpoint a réellement fini après54915 ; il n'assure pas la surveillance des escalades. Aucun ancien essaiP2/P3 relancé. Les états ci-dessous restent historiques.

## Actualisation P3 —27octobre2026

P2 et son intégration sont reçus avec réserves. Le même timer est désormais configuré pour la seule continuationP3 `9e4a61d6faea4b73ad31251e72dcf7c1`, entrée activeP3 du registre existant ; les cas P2 restent reçus et ne sont pas rejoués. Le CLI de coordination a répondu M26_P3_SUPERVISION_READY. Voir [le déblocage, les limites et le mécanisme de checkpoint distinct](p3/DEBLOCAGE-54073.md). P3 n'est pas reçue, P4 non transmise. Les périmètres P2 ci-dessous décrivent les passages historiques.

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


## Sérialisation des interventions manuelles

Utiliser le verrou existant `coordinator.lock` aussi pour le coordinateur principal :
créer `MANUAL-HOLD`, acquérir ce verrou en attendant la fin d’un passage engagé,
puis corriger/vérifier/reprendre. Ne pas écrire simultanément avec un passage
périodique. Retirer le hold et libérer le verrou après reprise ; ne pas remettre
STATE.json à zéro. La directive permanente du29octobre exige la prise en charge
des blocages sans nouvelle relance humaine, avec changement technique vérifié,
compteurs persistants et retour à JARVIS.


## Surveillance santé ajoutée le29octobre

`jarvis-mission-health.timer`, activé au démarrage, lance un contrôle toutes les
60secondes via `service_watch.py`, sans attendre la fin d’un passage Codex long.
Le contrôle observe huit unités existantes : deux workers, broker, conversation,
JL03, timer et service du coordinateur, et son propre timer. Un service oneshot
inactif après succès est normal ; un code d’échec ou une unité absente reste
signalé. Une observation indisponible est UNKNOWN, pas un plantage confirmé.
Les redémarrages natifs et leurs incréments sont enregistrés dans HEALTH.json.

Les workers possèdent déjà Restart=on-failure (3/5secondes). Le moniteur ne tue
ni ne redémarre un worker actif, ne réinitialise aucun checkpoint et ne rejoue
aucune commande. Les effets inconnus restent à observer avant toute reprise.
Après60secondes de récupération automatique prolongée ou en cas de service
arrêté/failed, le moniteur demande le service de coordination existant. Il écrit
son constat avant de le démarrer, respecte MANUAL-HOLD/le coordinateur actif et
un intervalle de120secondes entre demandes. Trois demandes pour une panne
continue maximum ; ensuite `mission_health_escalation` persistant, sans quatrième
relance aveugle. Les tentatives historiques restent archivées après récupération.

Le coordinateur conserve ses propres trois passages par condition. Il distingue
les dernières escalades natives P2 des anciennes erreurs d’interface, et reconnaît
les résolutions groupées par IDs. La stagnation utile reste contrôlée à600secondes ;
les heartbeat, CPU/GPU à0 et connexions seules ne prouvent ni progrès ni panne.
Un relevé santé vieux de180secondes déclenche SERVICE_HEALTH_STALE : le moniteur
n’est pas implicitement considéré sain lorsqu’il cesse de publier.

`HEALTH.json`, `STATE.json` et les journaux privés restent sous le dossier de
supervision ; les événements apparaissent dans le MissionStore canonique.
Pas de nouveau moteur, pas de nouvelle mémoire. Les exemples de configuration
conservent les paramètres pour les missions suivantes, avec leur registre et
périmètre propres. Un arrêt électrique de l’hôte empêche ses moniteurs locaux
de tourner ; les timers reprennent après son démarrage.

Validation :12tests du moniteur et9tests de coordination PASS. Service réel
isolé volontairement sorti42, NRestarts=1 et secondPID observés ; journal systemd
confirme échec puis redémarrage. Le premier relevé était déjàOK : ne pas prétendre
avoir observé directement la phase d’échec dans ce poll. Service de test arrêté
et unité transitoire déchargée ; le reset-failed ultérieur était sans objet.
Les services JARVIS n’ont pas été perturbés. Ce test valide le redémarrage d’un
processus témoin, pas une réception supplémentaire d’autonomie agentique.
Voir SURVEILLANCE-SANTE-PREUVES.json. P4 etphase2 restent NONVALIDÉES.
