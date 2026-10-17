> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/MISSION-13F-INCIDENTS.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 13F — incidents, corrections et réserves

| Incident observé | Correction effectuée | Vérification |
|---|---|---|
| Aucun checkout Git/ROADMAP local | Lecture GitHub via connecteur, workflow PR ; rapports locaux lus | SHA/ref de main contrôlés, historique conservé |
| Assertion de test limitée au schéma v2 | Attente v3, fermeture explicite des connexions SQLite des tests anciens | Suite finale sans ResourceWarning, 27 passent |
| Bubblewrap CLI OK mais sous unité échoue NETLINK_ROUTE | Ajouter AF_NETLINK à RestrictAddressFamilies ; garder capabilities vides | Commandes réelles du modèle sous service fonctionnelles |
| Qwen s'arrête au plan | Mode laboratoire explicite et continuation jusqu'au rapport | Diagnostics puis modifications réelles |
| Fenêtre 8192 saturée, sortie tronquée | Réduire le contexte en gardant objectif et observations ; traces intégrales séparées | Dernier objectif complet, HTTP réel et rapport |
| Résumé avec num_ctx différent recharge le modèle | Réutiliser num_ctx 8192 | Résumé mesuré à environ 2,95 s au lieu d'un rechargement supplémentaire |
| Ministral émet active_memories[ARGS]{} comme texte | Adaptateur strict de message entier vers appel connu | Trois modèles retrouvent réellement la préférence ; pas de contournement lab |
| Ancienne identité interdit encore le shell et toute mémoire automatique | Identité v2 avec périmètre laboratoire et catalogue non sensible précis | Contrôles finaux de préférences et opérations réelles |
| Bing RSS retourne des résultats sans rapport avec les mots techniques | DuckDuckGo Lite, fallback GitHub incidents | Recherche réelle avec URLs pertinentes puis fetch |
| Qwen affirme lire des sources mais n'a appelé que web_search | Refuser intervention_report sans deux documents réellement fetchés pour un objectif documentaire | Unitaire refuse faux rapport ; essai final lit configparser et http.server |
| Port INI incorrect / lecture seule dans fixtures | Qwen sauvegarde, corrige la valeur et selon l'essai les permissions | HTTP 200, HEALTH_OK ; scripts de validation inchangés |
| Sauvegarde récursive dans elle-même | Qwen observe l'échec et copie ensuite le seul fichier de configuration | Nouvelle sauvegarde et correction réussies |
| Sonde lancée depuis le mauvais dossier | Qwen relance depuis le dossier de service | Première erreur conservée, dernière sonde réelle réussie |
| Curl immédiatement après restart parfois trop précoce | Attente de readiness dans les tests de reprise | Restart/relogin/historique et mémoire réels |
| WebUI inaccessible sur localhost:3000 | Pas de changement réseau : conserver l'adresse active existante | Outil jarvis_services obtient HTTP 200 sur la configuration actuelle |

Les essais échoués restent locaux. Le modèle a parfois mal nommé l'exception (NoOptionError/NoSectionError au lieu de ValueError/MissingSectionHeaderError) et enjolivé les sources. Les rapports automatiques ne sont pas publiés comme faits vérifiés : la réception utilise les outils, hashes, requêtes HTTP et SQLite. Le contrôle documentaire ne garantit pas la justesse de toute interprétation ni de toute citation dans une phrase libre.

Réserves restantes : heuristique VAD en acoustique réelle, Safari/mobile physique, temps de chargement lors des changements de modèles, taxonomie automatique limitée, FTS5 lexical, journaux autres que ceux de la passerelle parfois inaccessibles, pas de VM UEFI/PXE ni boot complet testé, pas de permissions Dell, pas de contrôleur de mission longue après reboot. L'autonomie est démontrée sur des incidents HTTP simples, pas sur un déploiement système.
