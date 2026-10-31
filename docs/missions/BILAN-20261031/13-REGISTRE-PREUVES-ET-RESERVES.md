# Registre des preuves et réserves

Les preuves JSON publiques sont des projections expurgées : machines, paquets, services, modèles, empreintes, contrats et résultats fermés. Les originaux avec adresses, DMI, sorties Google et configurations privées sont hors Git dans bilan-20261031-private (répertoire 700). manifest-prive.json fournit empreinte et taille, pas le contenu privé. Les scripts de collecte tournent en lecture seule sur les cibles ; leurs seuls fichiers produits sont les artefacts de cet audit sur Mac.

| Référence | Provenance | Ce qu’elle établit | Limite |
|---|---|---|---|
| preuves/mac.json, dell1.json, dell2.json | observation directe Codex | matériel, paquets, services, API de catalogue/chargement | instantané ; pas benchmark ni boot physique |
| logiciels.csv, services.csv | collecte gestionnaires/venvs | installé/chargé | présence ≠ usage effectif |
| preuves/local.json | imports, schémas, SQL lecture seule |87 outils,65visibles,4skills,compteurs,6 écarts SHA | disque ≠ code chargé en mémoire |
| preuves/webui.json | volumeSQLite et environnement conteneur | profils, modèle défaut et fournisseurs | pas parcours Safari/microphone |
| preuves/qwen-observation.json | exécution Qwen Code réelle | erreur contexte initiale puis appels190/192 | résumé faux ; ne pas recevoir sa prose |
| preuves/local.json#google_education | reçus 164/166/168 | lectures Drive/Calendar/Gmail Éducation réussies | pas écriture ni clients Éducation |
| SOURCES.json | fichiers Git et branche P7 distincte | contexte historique et provenance | recommandations anciennes ≠ déploiements |

Réserves : découverte bornée des binaires/venvs ; absence de snapshot atomique des trois hôtes ; compteurs évolutifs pendant la collecte ; absence de qualification physique des périphériques/ESP/énergie ; pas de test réel Apple/micro ; P4 suspendue ; P7 proposé non reçu ; restitution libre Qwen encore erronée ; droits/écritures Google Éducation non reçus. Les métadonnées de licence des paquets ne prouvent pas le droit de redistribuer toutes les images/modèles.

Les inventaires complets de tous les fichiers manuels, plugins de tous les processus et connexions de tous les utilisateurs ne peuvent être garantis par une recherche bornée. Le bilan est exhaustif dans les gestionnaires collectés et les composants JARVIS connus, avec ces frontières explicites. Aucune absence d’observation n’est transformée en échec.

Directives consultées : AGENTS, charte, suivi/roadmap, sources de SOURCES.json ; autorisations préservées : audit/publication autonome seulement ; aucun redémarrage, installation, suppression ou changement du routage. Écart documentaire expliqué : Google Éducation a été raccordé après le dernier commit37 ; ancien rapport conservé, état actuel ici. M26-P4/MANUAL-HOLD maintenu.


**Séparation Google :** les profils disposent de répertoires et jetons chiffrés distincts. L’interface actuelle reste toutefois un outil commun `google_mcp(profile=personal|education)`, pas deux conteneurs ou deux outils dotés de droits distincts. L’isolation complète demandée au niveau des interfaces reste à préparer ; elle n’est pas déclarée reçue par la séparation du stockage. Aucun changement d’architecture n’est fait pendant ce bilan.

Reproduction : `collecte-inventaire.py` est un collecteur ponctuel en lecture seule, à exécuter sur chaque hôte dans un contexte d’administration existant. Sa sortie brute contient des identifiants DMI/réseau : la conserver uniquement dans un répertoire privé, puis publier une projection expurgée. Le script ne crée aucun service de supervision. Les validations de ce dossier portent sur les références, compteurs, types, champs et absence de secrets détectables ; pas sur une nouvelle qualification des missions historiques.
