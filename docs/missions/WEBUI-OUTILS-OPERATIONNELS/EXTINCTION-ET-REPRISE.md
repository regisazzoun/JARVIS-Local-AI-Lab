# Extinction du Mac mini pendant la réception WebUI

## Faits observés

Le propriétaire a confirmé que le Mac mini s’était éteint et l’a démarré manuellement. Au retour d’accès, les services conversation, adaptateur WebUI, broker et les deux workers étaient actifs ; la mission de réception conservait son identifiant, sa tâche et l’état interrupted. Aucun reboot supplémentaire n’a été demandé pour ce diagnostic.

Le journal du démarrage précédent s’arrête à **2026-10-31 21:49:40 Europe/Paris**. Les quatre rechargements de services effectués par Codex sont enregistrés à **21:49:29**, avec arrêts/démarrages réussis. Cette proximité de onze secondes est conservée ; elle ne démontre pas une causalité.

Recherche ciblée dans la fin du journal système à partir de 21:40 et dans le journal noyau du démarrage précédent : aucune occurrence des motifs d’arrêt ordonné, OOM/Out of memory/Killed process, Kernel panic/Oops/Hardware Error/thermal shutdown examinés. Les répertoires pstore étaient vides. Les quatre unités contrôlées ont FailureAction=none, StartLimitAction=none et OOMPolicy=stop ; elles ne prescrivent pas une extinction de la machine dans ces paramètres.

Les traces affichent aussi des tentatives répétées de lancement de la socket KDE DrKonqi refusées pour condition utilisateur non remplie. Ce message n’est pas, à lui seul, un crash applicatif reçu ni la cause démontrée de l’extinction.

Le début apparent du nouveau journal (21:48:57) n’est pas utilisé pour dater précisément le redémarrage physique : le contrôle à 22:11:58 indiquait moins d’une minute d’uptime, et l’horloge de démarrage a été corrigée. Ne pas déduire une durée d’indisponibilité de la soustraction de ces deux horodatages.

## Conclusion bornée

**Arrêt brutal ou perte de fin de journal compatible avec les observations ; cause non déterminée.** Les traces disponibles ne permettent ni d’attribuer l’extinction au rechargement, ni d’exclure un lien. Aucun OOM, panic ou arrêt logiciel explicite n’est démontré. Une disparition électrique ou une panne matérielle ne sont pas affirmées faute de preuve.

Les journaux complets sont archivés dans le dossier privé de réception, avec les identifiants d’accès conservés hors Git. Aucun stress test, benchmark, réinstallation, modification d’alimentation ou nouveau redémarrage automatique n’a été réalisé. Les opérations suivantes utilisent les services revenus après le démarrage propriétaire.

## Continuité de mission

L’autorisation explicite de mesurer, résoudre l’incident de capacité et reprendre a été conservée. Une nouvelle mesure du contrat compact sur copies SQLite isolées donne 25333 octets pour un budget conservateur de 27648 ; aucune inférence n’est effectuée par cette mesure. Résolution native enregistrée à l’événement 94844, puis reprise du même identifiant `3f64e6c1adc640e9847c9311d3350d8b`.

Le total historique d’incidents reste à 3 ; infra_resolved_through passe de 0 à 3 par le mécanisme existant. Le nombre de défaillances fonctionnelles de ce problème reste à 0. La résolution de capacité ne reçoit pas à elle seule le résultat de la tâche ; les verdicts de rapport et la clôture native sont vérifiés séparément.
