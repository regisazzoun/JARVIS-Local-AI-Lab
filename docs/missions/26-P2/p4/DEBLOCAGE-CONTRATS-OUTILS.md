# P4 — déblocage du contrat d’outillage

Le checkpoint conservait une tâche version0 avec rapport obligatoire mais outils
limités à la lecture. Une autre étape déclarait host_exec#dell2, qui n’existe pas.
La relecture du rapport absent produisait FileNotFoundError, pas un test applicatif
échoué. Les sorties et compteurs historiques restent disponibles.

La coordination périodique a diagnostiqué/rendu disponible l’écriture77179–77184
et JARVIS a repris. Sa révision4 a ensuite obtenu coverage FAIL77233 : livrables
incomplètement couverts et chemins de rapports partagés. Ce FAIL n’est pas effacé.

Codex installe77253 un contrôle déterministe avant exécution : une tâche de type
report exige host_write_file et des noms d’outils réellement enregistrés. Pour un
contrat historique incorrect, l’interface demande à Qwen de réviser l’ID concerné
et conserve son report_path ; elle ne remplit aucun objectif ni commande à sa
place. Les contrats valides et tâches reçues restent immuables. Les autres lacunes
de couverture doivent ensuite être corrigées par le modèle.

Une erreur du préflight Codex a révélé une autre faiblesse : le transport des
schémas conditionnels rangeait les propriétés dans $defs comme un objet brut ;
un champ title était alors interprété comme mot-clé JSONSchema. Aucun appel
modèle/outil n’avait été transmis. Correction : encapsuler les propriétés dans
un schéma objet valide et conserver les références relocalisées. Régression
explicite pour title/type/required et les contraintes conditionnelles de chemin.

175tests ciblésPASS, couvrant les contrats de rapports, transport, acceptation
par preuves, couverture adaptative et non-régression26B. Préflight natif77260 :
24068/27648octets. Contrôle77295 limite host_write_file au chemin du rapport
courant ; les modifications applicatives passent par les exécutants distants.
Seuls les workers sont rechargés, les compteurs/versions et originaux conservés.

P4 est remise en file sur le même checkpoint. Les corrections d’infrastructure
sont Codex, les prochaines révisions de plan et opérations restent JARVIS/Qwen.
Aucun artefact canari ni déploiement actif n’est reçu à ce jalon. P3 conserve sa
réception ciblée avec réserves77116 ; P4 etphase2 restent NONVALIDÉES.
