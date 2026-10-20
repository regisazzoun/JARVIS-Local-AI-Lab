# Édition ciblée réutilisable

Défaut observé : JARVIS remplaçait tout agent.py pour corriger un appel et introduisait des imports/décorateurs inexistants. host_exec permettait déjà une édition Python, mais aucun outil structuré n'exprimait la précondition de remplacement. Codex ajoute host_edit_file, sans élargir les write_roots.

Contrat : path absolu autorisé ; old fragment exact non vide ; new remplacement, vide pour suppression ; count occurrences attendu, défaut1 ; expected_sha256 optionnel. Correspondance ambiguë/absente ou empreinte périmée : refus sans modification. Succès : remplacement atomique sous l'identité technique, permissions conservées, SHA avant/après et nombre de remplacements. Les chaînes shell restent littérales. Les autres fragments et fins de ligne sont conservés.

La mutation est suivie dans le checkpoint de débogage et exige une preuve ultérieure pour la réception. Questions conversationnelles ne peuvent pas appeler cette mutation pour créer une mission. Les lectures projet status/logs sont admises en batch ; restart et host_exec ne le sont pas.

Tests : cible unique, source CRLF intacte, texte contenant substitutions shell non exécuté, ambiguïté et hash périmé refusés sans changement, suppression vide acceptée jusque dans le registre. Première utilisation réelle JARVIS : événements6053/6056, sur la même mission originale. Ce mécanisme évite des changements collatéraux ; il ne prouve pas un raisonnement universellement correct.
