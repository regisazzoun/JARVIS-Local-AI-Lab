# M26-P2 — Contrat de coordination

Ordre propriétaire du26octobre2026. Codex conserve le contrat global et ne transmet que P2, puis P3, puis P4 après réception de la priorité précédente. Qwen80B reste décisionnaire, Dell1/Dell2 exécutent, Mac coordonne et conserve le journal existant. Aucune validation humaine intermédiaire ajoutée.

P2 : machine d’états observable des tentatives, séparation non-exécution/exécution/test, trois corrections échouées maximum par problème stable, incidents d’infrastructure séparés et bornés, observation des résultats inconnus avant réexécution, compteurs persistants et escalade. Dix scénarios réels à contrôler.

P3, non transmise avant réception P2 : budget réel du modèle, contexte actif borné, mémoire opérationnelle et archives persistantes, checkpoint structuré et reprise sans perte ni doublon.

P4, non transmise avant réception P3 : provenance source/candidat/intégration/déploiement/version active, tests de divergence, déploiement partiel, retour arrière et validation sur l’application effectivement exécutée.

États de réception : VALIDÉ / VALIDÉ AVEC RÉSERVES / BLOQUÉ / NON VALIDÉ. Aucun résultat essentiel manquant ne doit être caché par un GO global. Préserver Phase1 et les services, pas de nouvelle architecture concurrente ou de modèle.14A et24-Old restent distinctes.
