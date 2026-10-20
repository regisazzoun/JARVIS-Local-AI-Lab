# Registre des capacités — candidat23C

Le registre existant reste unique : Registry.specs décrit les outils ; capabilities/requests/events restent dans SQLite broker. capability_status ajoute effective_scope, policy_identity, recent_failures et, côté client, tools dérivé des spécifications réellement enregistrées. Aucun deuxième inventaire manuel de noms ou paramètres.

Chaque outil décrit son nom, fonction, schéma de paramètres, champs requis, mode, référence au périmètre effectif, documentation et méthode de test. Les machines exposées sont les noms de profils, sans clé, adresse ou commande privée. Les dix erreurs significatives les plus récentes parmi les cent derniers événements portent une référence de preuve et le diagnostic expurgé ; les anciennes erreurs restent explicitement legacy_unclassified.

L'état par défaut est **unverified** : un outil annoncé et une permission présente ne prouvent pas sa disponibilité. L'ancien état VALIDÉ demeure une preuve historique, susceptible d'être périmée après modification de politique.

| Situation | Interprétation et action |
| --- | --- |
| Permission applicable + opération réussie avec reçu courant | Capacité disponible pour cette opération précise |
| Outil existant mais transport/service échoué | Capacité existante mais indisponible ; diagnostiquer le reçu |
| Opération inconnue | Non implémentée ; development nécessaire |
| Ressource/action refusée par broker | Hors périmètre de la politique appliquée ; comparer à l'autorisation propriétaire |
| Présence seule dans tools ou ancien VALIDÉ | Non vérifiée actuellement ; exécuter une sonde |

Limites restantes : le candidat ne calcule pas encore automatiquement une disponibilité par tuple outil/action/ressource et empreinte ; les paramètres omis des diagnostics (corps, commande, contenu) restent uniquement dans les journaux privés préexistants. Ces limites empêchent la réception complète du registre demandé. Ne jamais transmettre ces journaux bruts au modèle ou à GitHub.
