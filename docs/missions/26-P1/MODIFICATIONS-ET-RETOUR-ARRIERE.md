# Modifications et retour arrière

Les fichiers installés avant intervention sont sauvegardés sous `~/JARVIS/mission26-phase1-private/installed-before/`. La politique propriétaire originale reste dans un fichier privé mode0600 ; son contenu ne doit pas être publié.

- Ajout de `jarvis/distributed_authority.py`, outils génériques et compteurs dans MissionStore.
- Ajout de l’enregistrement opt-in dans `jarvis/tools.py`, diagnostics de schéma courts pour ces seuls outils.
- Ajout de la vue courte et de l’exposition d’outils dédiés dans `jarvis/durable_cycle.py`, suspension après trois refus comparables.
- Ajout des deux profils projet `mission26-phase1` à la politique SSH/broker existante et du chemin local de transfert. Aucun droit sur d’autres projets ajouté.
- Création de la fixture isolée sur les deux Dell. Aucune modification JL03, modèle, GPU, pilote ou service conversationnel.
- Redémarrage des deux workers uniquement, après vérification de l’absence de mission active. API conversation et JL03 conservées actives.

La branche documentaire précédente ne contenait pas encore certains fichiers déjà installés lors de la clôture JL03 : `jl03_assist.py`, strict_tools et compact_finalization sont repris à l’identique de leur état installé pour préserver ces acquis. Ils ne sont pas attribués à la nouvelle démonstration.

Pour revenir en arrière : interrompre uniquement la nouvelle mission, attendre la fin d’un éventuel reçu en cours, sauvegarder les nouveaux événements, restaurer tools.py et durable_cycle.py depuis installed-before, retirer uniquement distributed_authority.py, puis redémarrer les workers au repos. Retirer si nécessaire les seules entrées de politique mission26-phase1, sans restaurer aveuglément une ancienne politique qui effacerait d’autres changements. Garder les espaces et preuves sur les Dell ; aucune suppression de données n’est requise. Les tâches historiques, SQLite et services d’inférence restent intacts.

## Incident de démarrage conservé

Avant le correctif des refus d’interface, cinq appels de planification ont été refusés pour granularité/format incompatibles. La limite de trois n’a pas tenu pour ce premier type d’erreur. Codex a interrompu la mission, conservé les reçus, amélioré les diagnostics et précisé le contrat générique de lots réceptionnés. Il n’a fourni aucun correctif applicatif, fichier responsable ou commande de test à Qwen. La reprise est une stratégie d’interface différente, explicitement journalisée, et non une remise à zéro silencieuse des compteurs.

## Autres corrections d’infrastructure observées

Les événements codex_interface_escalation conservent notamment la correction du spec d’acceptation initialement mal typé, le rétablissement des résultats structurés et de l’historique assistant/outils pendant chaque quantum, la distinction plan initial/révision globale, les références numériques d’exécution et la preuve d’une modification réelle. Les compteurs applicatifs restent attachés aux exigences stables.

Le stockage a nécessité le retrait du seul doublon read_roots ajouté pour la nouvelle racine : le bind RO masquait son bind RW. La politique finale diffère de la sauvegarde uniquement par les deux profils isolés et la racine locale d’écriture. Le script public provision.py ne réinitialise jamais les sources et ne crée pas ce doublon.

Les trois rédactions finales du modèle sont conservées. Les deux réouvertures ont archivé l’ancien texte et vidé uniquement report_path pour permettre une nouvelle rédaction native ; aucune tâche technique ou preuve reçue n’a été retirée. Les erreurs encore présentes sont rectifiées dans ERRATA-RAPPORTS.md, pas par une quatrième relance du modèle.
