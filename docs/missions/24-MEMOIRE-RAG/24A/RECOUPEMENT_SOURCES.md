# Recoupement des sources — correctif sur copie privée

**14 novembre 2026 — ✅ GO ciblé sur la question salle 407, en mode extractif vérifié. Aucune réception globale du RAG ni activation de production. 24B non lancée.**

La question de référence a été rejouée dans le frontend natif. Le dernier essai lit trois sources distinctes, couvre les six rubriques avec neuf passages vérifiés et affiche trois cartes de sources et trois liens ouvrables. La réponse sauvegardée est exactement celle rendue après contrôle des passages. [Mesures](preuves/RECOUPEMENT_CLIENT_S407.json) · [Réponse réellement affichée, expurgée](REPONSE_CLIENT_RECOUPEMENT.md).

## Ce qui corrige le défaut
La seule disponibilité des trois textes ne suffisait pas : un essai intermédiaire les avait effectivement lus, puis inventait un emplacement commun et une exclusivité de déploiement. Le correctif final sépare donc trois opérations :

1. **Recherche et lectures imposées avant réponse.** Deux recherches bornées dans le connecteur Éducation déjà autorisé découvrent les candidats. Le numéro de salle vient de la question ; les identifiants des documents ne sont pas codés en dur. Trois rôles sont recherchés : état réseau, installation/exploitation IPBX et état du déploiement. Les candidats compatibles avec docs.getText sont classés par rôle puis fraîcheur. Un état de déploiement est préféré à un guide de provisioning. Un fichier Excel ne peut plus tenir la place d’un texte lisible par cet outil.
2. **Choix de passages, pas rédaction de faits fusionnés.** Qwen reçoit les trois textes découpés selon leurs retours de ligne naturels et choisit des identifiants de passages pour chaque rubrique. Le client résout ces identifiants dans le texte original. Il ne demande plus au modèle de recopier des citations, ni de rédiger librement la réponse finale.
3. **Contrôle puis rendu.** Le client vérifie l’existence des passages, leur correspondance exacte après normalisation des espaces et la présence des familles de sources requises par rubrique. SIP confronte réseau et IPBX ; téléphones et reste à faire exigent deux sources pertinentes. Le passage IPBX de la rubrique SIP doit traiter d’enregistrements physiques, afin qu’un historique de timeout ne remplace pas l’état recherché. Un identifiant inventé, une source refusée ou un passage manquant entraîne une réponse « recoupement non validé », pas une synthèse déclarée complète. Les passages validés sont rendus avec date de modification distincte, attribution et lien.

**Ce mode est extractif.** Le GO porte sur ce parcours pilote et sa restitution sourcée, pas sur la capacité de la synthèse libre initiale à devenir fiable. Il est plus rigide : la sélection reste sémantiquement à revoir, même quand l’identité des passages est prouvée. Le candidat est volontairement limité aux questions de téléphonie de salle dans le Drive Éducation, avec une option de modèle activée seulement dans la copie. Il ne remplace pas tous les parcours JARVIS.

Aucun fait de la réponse attendue — nombre de postes, état SIP, emplacement ou état des appels — n’est injecté dans le code. Les contrôles de recette ci-dessous comparent la sortie aux textes effectivement lus. La règle de couverture et le vocabulaire de téléphonie du pilote sont explicites, sans prétendre à une recherche multi-domaines universelle.

## Résultat relu sur les sources réelles

| Critère | Vérification du dernier essai |
|---|---|
| Réseau | Constat du 12 novembre : Po1 actif sur les bancs 1–2 ; bancs 3–6 à inventorier/déployer, attribué au document réseau. |
| IPBX | Constat du 13 novembre : FreeSWITCH/Nginx/PostgreSQL actifs, quatre profils SIP chargés, attribué au document FusionPBX. |
| Téléphones et SIP | Le passage récent atteste onze extensions actives enregistrées par des téléphones physiques. Le constat réseau plus ancien rapporte dix MAC et une recette SIP encore à réaliser. Les critères et sources restent distincts ; aucun emplacement global ni déploiement « d’un seul téléphone » n’est déduit. |
| Appels | La validation utilisateur limitée à une paire est citée depuis le Markdown ; les tests restant à faire restent distincts de l’enregistrement SIP. Les numéros sont expurgés dans la publication. |
| Reste à faire | Les tâches réseau et les vérifications du poste documenté sont présentées avec leur source et leur portée ; aucun inventaire de ports n’est reconstruit à partir d’un nombre SIP. |
| Provenance | Trois lectures réussies, neuf passages normalisés exacts, six rubriques, trois cartes et trois liens dans le frontend ; date de consultation du 14 novembre. |

La vérification est **documentaire**. Aucune relecture SSH du PBX ou des switches n’a été exécutée par ce correctif. Les liens institutionnels et la classification Drive conservent les limites de la matrice initiale ; la présence d’un fichier sous le profil Éducation n’atteste pas, seule, tout son rattachement institutionnel.

Le paquet public supprime un passage d’authentification de la réponse et masque adresses, MAC, noms de profils dérivés de MAC et extensions. Le rendu privé reste intact. Le propriétaire a rejeté le filtrage de ses informations autorisées : **aucun filtre de sources ou de contenu n’a été ajouté au modèle**.

## Tests et historique des corrections
- **18/18 tests unitaires** sur données fictives : lectures bornées et dédoublonnées, priorité des documents lisibles, lacunes, erreurs fournisseur, autorisation/connexion, isolation entre requêtes, gros texte non tronqué silencieusement, fausse citation, famille manquante, passage inventé, historique SIP inadapté et rendu des passages originaux. [Preuve](preuves/RECOUPEMENT_TESTS_UNITAIRES.json) · [Tests rejouables](recoupement/test_crosscheck.py).
- **Refus natif d’accès du compte standard B au modèle propriétaire**, même avec des champs de réponse/activation forgés : HTTP 400. Aucun droit réel changé. [Preuve](preuves/RECOUPEMENT_REFUS_UTILISATEUR.json).
- **Deux mutations refusées avant transmission** par le garde de copie : écriture Docs et suppression Drive, HTTP 403. [Preuve](preuves/RECOUPEMENT_GARDE.json).
- **Un parcours complet final dans le vrai frontend copié**, avec lecture Google réelle et sélection Qwen réelle. Ne pas confondre les appels du contrôleur avec des fonctions spontanément choisies par le modèle : le plan réalise deux recherches et trois lectures ; Qwen réalise ensuite la sélection structurée.

| Étape observée | Résultat conservé et correction motivée |
|---|---|
| A — sélection initiale | Un inventaire XLSX est choisi pour le déploiement ; sa lecture échoue, le contrôleur signale incomplet. Correction de compatibilité MIME et du classement par rôle. |
| B — trois lectures, synthèse libre | Fusion non étayée du nombre de téléphones avec leur emplacement ; exclusivité de déploiement injustifiée. La présence des textes ne résout donc pas le défaut. |
| C — citations recopiées par le modèle | Trois passages reformulés ne correspondent pas au texte ; réponse d’abstention, pas de GO. Nouvelle hypothèse démontrée : sélectionner des identifiants et résoudre le texte côté client. |
| D — identifiants, blocs trop grossiers | Des blocs de 1 200 caractères coupent les paragraphes et un état SIP historique est sélectionné. Correspondance textuelle correcte, pertinence insuffisante ; aucun GO de qualité. |
| E — dernier état testé | Découpage naturel, un passage par famille requise et contrôle du constat SIP physique : neuf passages, trois sources, six rubriques ; revue documentaire conforme. |

Les étapes ont changé sur des causes nouvelles observées ; elles ne constituent pas une répétition indéfinie du même ajustement de prompt. Les essais non concluants et les refus restent dans [RECOUPEMENT_CLIENT_S407.json](preuves/RECOUPEMENT_CLIENT_S407.json). Les sorties intégrales antérieures restent privées, avec leurs informations sensibles ; leurs statuts ne sont pas effacés.

## Mesures et limites
Le dernier parcours prend environ **35 secondes entre création et dernière mise à jour du chat**. La sélection Qwen rapporte 15 183 tokens d’entrée, 305 de sortie et environ 21,2 secondes d’inférence. Paramètres de cette sélection : même moteur qwen3.5:27b-q4_K_M, contexte 32 768, température 0, raisonnement désactivé, plafond 6 000 tokens. Ce sont des paramètres propres à la sélection structurée, différents de la synthèse libre initiale ; **aucun gain de performance comparatif n’est revendiqué**. Le rendu final de 5 000 caractères ne consomme pas une deuxième génération libre.

Les deux recherches portent sur leurs résultats bornés, pas sur un inventaire exhaustif du Drive. Quinze candidats distincts ont été vus ; le fichier Excel et les autres documents ne sont pas déclarés lus. Trois rôles documentaires et six sujets sont des critères du pilote, pas une preuve automatique de vérité complète. Les textes de plus de 40 000 caractères sont signalés comme lacunes, sans troncature silencieuse. Aucun comportement sur un corpus général ou des sources beaucoup plus longues n’est réceptionné.

Les ACL du fournisseur, la propagation de leurs révocations dans un index, l’autorité entre mémoires et les sauvegardes atomiques multi-stores restent hors de ce correctif. Les contrôles précédents entre utilisateurs restent historiques ; cette reprise ne prétend pas les avoir tous rejoués.

## Livrables et clôture
[Contrôleur](recoupement/crosscheck24a.py) · [patch middleware](recoupement/middleware-recoupement.patch) · [patch de réponse native](recoupement/client-response.patch) · [configuration de copie](recoupement/apply-copy-config.py) · [passages expurgés et correspondances](preuves/RECOUPEMENT_PASSAGES.json).

Le patch middleware s’applique après les correctifs précédents ; le patch de réponse native s’applique au main.py de l’image initiale. Aucun fichier du service de production n’a été remplacé. Rejeu hors ligne depuis le dossier `recoupement` : `python3 test_crosscheck.py`. Les secrets de connexion et les snapshots ne sont pas fournis dans le paquet.

Même image que le client natif actif ; réseau de copie none, racine et arbre de code montés en lecture seule, relais limité à la lecture et à l’inférence. L’empreinte du contrôleur réellement essayé correspond au fichier publié. Les empreintes main.py/middleware.py de production correspondent aux sources initiales ; image et démarrage de production inchangés. [Environnement](preuves/RECOUPEMENT_ENVIRONNEMENT.json).

La copie et le relais ont été arrêtés. Les cinq fichiers temporaires d’authentification distants et les moyens temporaires locaux de connexion ont été retirés. Les preuves brutes restent dans les répertoires privés de recette. [Clôture](preuves/RECOUPEMENT_CLOTURE.json).

**✅ Correctif de recoupement extractif reçu sur S407 en copie privée. Réception générale du RAG non acquise. Aucune activation de production, aucune fusion, aucune 24B.**
