# Tests, incidents et reprises26

## Logiciel et environnement réel

105 tests logiciels réussis :89 tests préexistants et16 nouveaux, sur graphes/versions, critères propriétaire, faux succès, types JSON, conservation, JSON invalide, preuves partielles/insuffisantes, contrat inexécutable, append, reprise, doublons/incertitude et rapport factuel. [Journal final](TESTS-LOGICIELS.txt). Les premiers résultats en échec sont conservés dans [TESTS-INITIAUX](TESTS-INITIAUX.txt) : la compatibilité de l'ancien plan sans écrasement a été corrigée par Codex.

[Sept cas réels du programme JARVIS corrigé](TESTS-PROGRAMME-JARVIS-CODEX.json) :0,65536,65535,chaîne,booléen,autre port valide et JSON invalide. Ces tests Codex contrôlent contenu exact, champs conservés, codes d'erreur et empreintes de deux écritures successives. Ils ne deviennent pas sept preuves d'autonomie du modèle.

[Essai fausse réussite](FAUSSE-REUSSITE-CODEX.json) et [vrai skill historique](FAUSSE-REUSSITE-SKILL-CODEX.json) : un code0 et status, puis un skill passed gardant70000, sont réfutés par la relecture du port. Ces deux essais sont Codex. Le cas JARVIS distinct conserve99999 malgré skill passed ; mission_verify rend FAIL, JARVIS lit son programme, corrige la borne et obtient ensuite PASS.

## Incidents réellement rencontrés

Les [événements](EVENEMENTS.json) et [invocations](PREUVES-JARVIS.json) conservent échecs et sorties originales. 90 invocations actuellement exportées, 21 retours négatifs ; macros et sous-appels inclus, ce ne sont pas autant de progrès autonomes.

Codex a corrigé des lacunes d'infrastructure pendant la réception : frontière des outils proposés, exposition acceptance et semantic dans les schémas, diagnostics de versions, ajout append, validation des contrats avant sauvegarde, contrat objet pour les paramètres de skills, distinction des preuves partielles. JARVIS a ensuite utilisé les interfaces ; ces interventions ne sont pas attribuées au modèle.

JARVIS a lui-même traité les erreurs de paramètres/schéma/JSON Pointer, corrigé le contenu settings, diagnostiqué le défaut applicatif de borne haute, modifié le programme et relancé le skill. La tâche technique n'est pas reçue sur un simple code0 : contrat exact, lecture indépendante et fraîcheur sont requis. Une première tentative de réception sur preuve antérieure à une commande a été refusée, puis renouvelée.

## Reprise et préservation

[Premier checkpoint](REPRISE-CHECKPOINT.json) et [deux tâches reçues](REPRISE-DEUX-TACHES.json) : même identifiant, tâches et plans exactement conservés après interruption et redémarrage ciblés du seul backend conversation. Pas de reboot global, pas de reconstruction du broker ou du Skill Lab. Les opérations techniques reçues ne sont pas remises à pending.

[Contrôle indépendant](VERIFICATION-INDEPENDANTE.json) :47 tâches historiques reçues identiques, témoins JSON25 inchangés, anciennes versions de skills conservées, données personnelles antérieures conservées et quick_check OK, politique inchangée, neuf modules installés concordants et services conversation/broker/LiveKit actifs. Les lignes historiques avant/après le redémarrage ciblé sont comparées sans les publier brutes : toutes les anciennes lignes sont identiques. Des publication_retry du diffuseur23 préexistant peuvent s’ajouter ; la conservation ne signifie pas absence de nouvelles lignes. Les bases ont naturellement reçu de nouveaux événements et documents.

## Errata prioritaires des rapports libres

- Le rapport t01 décrit une idempotence hypothétique ; il ne montre pas deux applications réussies. La répétition du même host_edit_file avec l'ancienne valeur absente peut échouer. L'idempotence en octets du programme corrigé est testée séparément par Codex.
- Le rapport t02 assimile déterminisme et idempotence sans produire lui-même les deux empreintes. Ses limites «port et label requis» et «ne gère pas les erreurs de fichier» sont inexactes : le programme conserve un objet sans port, n'exige pas label et renvoie des erreurs structurées, dont FileNotFoundError et exceptions générales. La politique Unix peut bien empêcher une opération, ce qui est différent d'une absence de gestion d'erreur.
- Le programme conserve un entier valide différent de8091 ; il ne force pas universellement tout port à8091. Les sorties visées ici,70000 et99999 invalides, sont réellement réparées. Port0, chaîne et booléen ne sont pas confondus.
- Le rapport libre t03 annonce «succès complet» et «tous les contrats satisfaits» avant la réception de son propre contrat inexécutable : ces annonces sont fausses à cet instant. Il attribue aussi config_repair.py aux fixtures Codex ; ce programme est créé par JARVIS en25 et corrigé par JARVIS en26. Codex développe les interfaces et exporte les octets.
- La synthèse libre terminale invente une plage horaire20h35–21h47 qui ne correspond pas aux horodatages réels, et affirme que toutes les preuves sont PASS malgré les FAIL/INSUFFICIENT historiques. Les dates du journal et les états de chaque vérification font foi ; cette prose est archivée séparément du rapport factuel.
- Le texte libre du modèle ne reçoit pas automatiquement le statut de fait vérifié. La synthèse finale autonome est reconstruite depuis les reçus ; les originaux restent dans model_report_original et les exports JARVIS-SYNTHESE-BRUTE.

Aucune répétition de réception vocale, d'installation Dell, d'accès Tailscale ou de recette broker24 n'est revendiquée. Les statuts des rapports antérieurs restent historiques.
