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

## Rectification du transport après essai réel

Le garde contains du schéma n’était pas appliqué par la grammaire du backend :
les essais sans dispatch de la coordination confirment l’omission du writer77335.
Les refus précédents restent archivés, aucun succès n’est déduit de ces essais.
L’ajout de host_write_file est donc effectué par l’adaptateur de rapport et
explicitement attribué à Codex ; il ne choisit aucune opération applicative.
Le champ tools reste validé contre les vrais nomsAPI, la portée d’écriture
centrale reste bornée au report_path. Le plan et les opérations sont ceux de Qwen.

Les erreurs de sélection structurée indiquent désormais les champs fautifs au
lieu d’un objet complet tronqué ; le moteur archive la sortie originale refusée.
177tests ciblésPASS. Essai Qwen réel77347 : action conforme au nouveau contrat,
23919/27648octets, sans dispatch ni mutation du plan. Résolution77349 ; même
checkpoint remis enfile. P4 reste NONVALIDÉE : ce contrôle de transport ne prouve
ni artefact canari ni déploiement. Les quatre anciens refus sont conservés.

Les interventions manuelles et périodiques doivent utiliser le même verrou
coordinator.lock. Créer MANUAL-HOLD avant de l’acquérir, laisser finir un passage
engagé, puis conserver le verrou pendant les mutations. Retirer le hold et rendre
le verrou après vérification de la reprise. Ce protocole utilise le verrou déjà
présent et évite deux corrections concurrentes dans le même dépôt.
