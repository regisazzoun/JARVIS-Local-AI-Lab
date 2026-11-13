# Clôture des tests manquants — 24A

**13 novembre 2026. Audit terminé ; réception fonctionnelle RAG : NO-GO. 24B non lancée.**

## Dispositif et fidélité au système existant
Même image Docker que le client natif actif, même code Python réellement copié, même frontend, même modèle JARVIS conversation/outils, paramètres conservés (contexte 32 768, limite 4 096, température 0,1). Le hash de l'arbre Python est inchangé à la fin. Voir [ENVIRONNEMENT_TEST_CLIENT.json](preuves/ENVIRONNEMENT_TEST_CLIENT.json).

L'instance de recette a un réseau Docker « none », un système racine en lecture seule et des volumes privés d'audit. Un relais par socket Unix permet seulement les appels d'inférence existants et les lectures Éducation nécessaires. Les schémas des opérations exposées sont issus du connecteur réel. Terminal, exécution libre et autres connecteurs ne sont pas disponibles. Les credentials Éducation utilisés sont une copie privée : leurs rafraîchissements/verrous/journaux restent dans cette copie.

Les identités de copie A/B/C sont fictives. A a le rôle administrateur du propriétaire source ; B et C sont standards. Aucune identité ou permission réelle n'a été créée/modifiée. Les contenus des copies natives restent privés. Les canaris d'ACL sont synthétiques, indexés seulement dans la copie de recette : ce ne sont pas une ingestion de sources réelles ni le lancement de 24B.

Le modèle et les handlers clients ne sont pas corrigés dans cet audit. Le confinement réduit l'offre d'outils : cette baseline n'est pas un benchmark strict de l'instance live complète. Le parcours web, l'authentification, le streaming, les outils, les sources réelles et la réponse affichée ont néanmoins été exécutés. Aucun test micro/VAD ou iPhone physique n'est revendiqué.

## Réponse complète dans l'interface
Question de référence saisie sans ajout dans un nouveau chat, modèle « JARVIS — Conversation et outils ». La réponse finale a été vue dans le navigateur puis relue dans le chat stocké de la copie avec done=true.

| Mesure | Résultat |
|---|---|
| Appels d'outils | 6 tentatives : 2 recherches Drive (1 réussie), 3 lectures de documents réussies, 1 demande de métadonnées Sheets en échec |
| Documents effectivement lus | 3 distincts, returncode=0 et remote_access_verified=true |
| Sources | Architecture S407 du 12 novembre ; FusionPBX du 13 novembre ; documentation de déploiement Markdown |
| Réponse | 6 rubriques, 6 143 caractères avant expurgation |
| Citations dans la réponse | 3 titres de documents ; 0 URL, 0 carte source native |
| Délai approximatif | 104,3 s de la soumission à la dernière mise à jour du chat, précision de stockage à la seconde |
| Borne d'observation UI | réponse terminée observée avant 148,9 s ; ce délai inclut le délai de notre contrôle |
| Dernier appel modèle | 55,0 s selon le runtime ; ne pas le confondre avec le délai total |
| Production | aucune conversation de test, ingestion ou modification |

Voir [CLIENT_COMPLET_S407.json](preuves/CLIENT_COMPLET_S407.json) et la [réponse expurgée](REPONSE_CLIENT_EXPURGEE.md). Une seule exécution finale est retenue : pas de moyenne, percentile ni comparaison avant/après inventés. Les compteurs de tokens cumulés du runtime et ceux du dernier appel sont distingués dans le JSON.

Deux essais préparatoires sont conservés en privé : un compte standard sans accès aux outils Drive, puis un propriétaire dont deux lectures ont été refusées par une liste de sources de test trop étroite. Le garde a été élargi aux sources pertinentes découvertes, en excluant les fichiers de credentials. **Ces refus du dispositif ne sont pas attribués au connecteur de production.** La lecture finale du fichier Markdown réussit réellement ; l'hypothèse provisoire d'un format non lisible n'est pas retenue.

## Revue de la réponse : résultat NO-GO
- **Défaut bloquant :** une information d'authentification SIP, présente dans une source, est reproduite dans la réponse bien que la question ne demande aucun credential. La valeur et la règle d'attribution sont retirées de toutes les preuves publiques. Ce défaut concerne la sélection/protection du contexte et la sortie ; le coffre d'accès exclu n'a pas été ouvert par le client de test.
- **Citations :** le client cite des titres, sans lien ni identifiant résoluble dans la réponse. Les lectures sont prouvées par la trace, mais le lecteur final ne dispose pas de citations directement ouvrables.
- **Fraîcheur :** le document FusionPBX du 13 novembre rapporte onze extensions actives et enregistrées sur des téléphones physiques. Il est plus récent que le document réseau du 12 novembre, qui indiquait encore la recette SIP à réaliser. L'absence de SIP validé ne doit donc plus être érigée en état global actuel.
- **Synthèse temporelle imparfaite :** la réponse affirme simultanément onze postes physiques enregistrés et un seul poste physiquement déployé, puis prescrit le déploiement des autres. Le seul emplacement précisément décrit dans un document ne démontre pas l'absence de déploiement des autres. Cette ambiguïté doit être signalée au lieu d'être transformée en conclusion opérationnelle.
- **Surinterprétations :** des adresses proposées sont présentées comme réservées ; l'accessibilité web est annoncée plus largement que le trajet effectivement documenté. Ces points ne sont pas des observations live de 24A.
- **Statuts d’outils trompeurs :** une recherche Drive mal formée et la demande de métadonnées Sheets renvoient returncode=1, mais leurs appels sont marqués completed par le client. Quatre opérations réussissent réellement, dont les trois lectures. Ne pas prendre l’affichage « Exploré » comme preuve de succès.
- **Acquis :** les six catégories demandées sont présentes, FusionPBX est relié à FreeSWITCH, et la recette complète des appels n'est pas confondue avec un enregistrement SIP. Aucune confusion FreePBX/Asterisk n'a été observée dans la réponse finale.

## Droits entre utilisateurs : tests réels de la copie
Les appels HTTP utilisent les handlers natifs et des jetons obtenus par authentification des comptes fictifs. Les contrôles ne se limitent pas à des filtres SQL simulés.

| Surface | Contrôles exécutés |
|---|---|
| Notes B/C | propriétaire lisible ; lecture par ID, recherche, liste, modification et délégation étrangères refusées |
| Partage de note | accès en lecture accordé, écriture refusée ; révocation puis refus avec le même jeton |
| Mémoires B/C | listes/ID/chemins isolés ; recherches vectorielles ne restituant pas le canari de l'autre utilisateur |
| Fichiers et knowledge | métadonnées, téléchargement et requêtes de collection privées refusés ; accès positif après partage ; écriture refusée ; révocation appliquée aussi aux vecteurs et au contenu du fichier |
| Sessions | révocation réelle du jeton B sur copie : ancien jeton refusé ; session C toujours valide |
| Outils Éducation | catalogue disponible pour A ; demande forcée d'attachement du serveur par B n'expose aucun outil externe dans la requête d'inférence |
| Anonyme | refus d'accès aux notes et collections de vecteurs |

**46 contrôles consolidés : 45 conformes, 1 échec fonctionnel.** Le détail des statuts attendus/observés et des canaris non divulgués figure dans [ACL_CLIENT_MULTIUTILISATEUR.json](preuves/ACL_CLIENT_MULTIUTILISATEUR.json).

L'échec fonctionnel est distinct d'une fuite : le modèle utilisateur annoncé dans le catalogue B renvoie « Model not found » à l'appel direct. Un accès temporaire au modèle de base, accordé exclusivement dans la copie, fait réussir le contrôle positif ; cet accès est ensuite retiré. Le périmètre du modèle de base doit être réconcilié avec celui du modèle proposé à l'utilisateur. Aucun droit réel n'est élargi par cet audit.

Un refus de modification de knowledge renvoie HTTP 400 au lieu de 401/403. Le contenu original a été relu après l'essai et est inchangé : le refus est effectif, mais le code HTTP est peu explicite. Nous ne l'avons pas assimilé à une écriture réussie.

Ces résultats couvrent l'application native et son contrôle d'accès aux outils. Ils ne simulent pas une seconde identité Google inexistante et ne prétendent pas avoir révoqué un partage Drive réel. L'index historique ne porte pas d'ACL documentaire et la propagation automatique des révocations Drive n'est pas démontrée : c'est un écart d'architecture à traiter avant un corpus multiutilisateur.

## Restauration des vecteurs et garde de lecture
La copie réunit cette fois SQLite natif et Chroma existant. La même requête sous la même identité logique retrouve les mêmes quatre identifiants de résultats hachés en live et dans la copie. La restauration fonctionnelle est donc vérifiée pour ce scénario. Une photographie atomique multi-stores pendant des écritures concurrentes n'est pas revendiquée. Voir [RESTAURATION_NATIVE_FONCTIONNELLE.json](preuves/RESTAURATION_NATIVE_FONCTIONNELLE.json).

Quatre contrôles du garde renvoient 403 : écriture Docs, mutation Workspace générique, lecture du coffre exclu et installation d'un modèle. Aucune de ces opérations n'est transmise à la production. Voir [GARDE_LECTURE_SEULE.json](preuves/GARDE_LECTURE_SEULE.json).

## Clôture
**24A est terminée comme audit/diagnostic vérifié. La réception fonctionnelle du RAG est NO-GO**, avec backlog explicite : filtrage des secrets dans les sources/contexte/sortie, citations ouvrables, gestion des versions contradictoires, droits des modèles utilisateurs, autorité logique entre mémoire historique et native, propagation des ACL et sauvegarde multi-stores.

Les accès applicatifs entre utilisateurs testés n'ont pas divulgué les canaris étrangers. Cela n'annule ni le défaut de restitution d'authentification à l'utilisateur propriétaire ni les limites du périmètre testé.

**24B non lancée ; aucune fusion ou activation de production.**
