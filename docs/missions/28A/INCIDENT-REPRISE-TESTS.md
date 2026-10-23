# Boucle après installation32B : diagnostic et corrections

État du23 octobre2026 : 🟡 essais32B exécutés, collecte et réception en cours. Le worker actif seul ne constitue pas une preuve d’avancement.

## Causes observées

Le contexte de base dépassait le budget calculé : environ34711caractères pour10576disponibles après les schémas de tous les outils. La compaction réinjectait ce socle trop volumineux. Le modèle Llama70B répétait des identifiants fictifs de tâche/preuve et d’anciennes lectures, sans exécuter le test demandé. Le moteur rejetait ces validations mais les reprises ne changeaient pas suffisamment les conditions de l’échec. Ces constatations expliquent ce cas ; elles ne démontrent pas une cause unique de tous les incidents historiques.

Codex a arrêté cette boucle au checkpoint, archivé le contexte et installé une sélection des outils déclarés par la tâche, avec maintien des outils de diagnostic/contrôle. Le contexte d’exécution réduit les doublons ; l’objectif original, versions et reçus restent intacts et consultables via mission_progress. L’interface présente le véritable identifiant B_models, le chemin du rapport et les paramètres des vérifications, sans remplir une preuve à la place du modèle. Les anciennes missions sans sélection restent compatibles.

Le plan4 de coordination Codex renforce B_models avec une preuve issue de six inférences32B et un résultat JSON local. Ce découpage est attribué à Codex, sans revendication de planification autonome. Après reprise,16outils sont proposés ; le socle mesuré est passé à24329caractères pour29227de budget. L’estimation en caractères ne remplace pas une mesure de tokens ; le point décisif est l’appel réel observé ensuite.

## Avancement effectivement observé

JARVIS a lancé project_exec pour quality_compare.py avec le seul candidat32B. Les six réponses et métriques existent : le téléchargement est donc suivi d’une véritable exécution, pas uniquement d’une lecture de catalogue. Les premiers contrôles affichent2/6, mais un verdict est faussé par un défaut du vérificateur Codex : str/float manquants dans son espace d’évaluation Python. Les réponses originales et verdicts ne sont pas effacés.

Un second défaut de préparation Codex empêchait la récupération : le nouveau dossier local mission28a était resté propriétaire root. Le mécanisme de transfert, exécuté par l’utilisateur technique, refusait d’y publier. Le propriétaire de ce seul dossier a été corrigé ; aucune ouverture générale des chemins ou permissions n’a été ajoutée.

Codex a installé le vérificateur corrigé et une réévaluation dans un nouveau fichier, qui conserve les verdicts précédents et l’empreinte de l’original sans relancer silencieusement les inférences. JARVIS doit retenter le transfert et utiliser cette correction ; les résultats effectifs de cette reprise restent à recevoir à ce stade du document.

## Contrôles et responsabilité

La suite logicielle passe221tests, dont deux nouveaux contrôles du contexte/identifiant/objectif durable et deux du vérificateur/relecture sans écrasement. Les tests ne prouvent pas l’autonomie générale. Les causes de préparation et de vérification ci-dessus sont Codex ; les appels et essais sont JARVIS. Les erreurs factuelles propres au32B restent conservées et empêchent toute conclusion anticipée de supériorité.

## Reprise effectivement réalisée après correction

Le pilote70B a ensuite tenté une référence de preuve littérale et rédigé un rapport de20caractères. Le moteur a refusé la validation. Codex a donc basculé temporairement le pilote Dell vers le27B déjà éprouvé, sans toucher au27B conversationnel du Mac et sans sélectionner définitivement un nouveau modèle puissant. Ce repli et son motif sont enregistrés comme provisional_model_fallback.

JARVIS, avec ce pilote de repli, a exécuté le nouveau --recheck. La lecture indépendante du fichier corrigé confirme3/6, contre2/6initialement : code, diagnostic et attribution passent ; calcul de moyenne, conversion mémoire et ordre vérification/rapport échouent toujours. La correction du faux FAIL de code ne transforme pas ces trois autres erreurs en réussites. Il ne s’agit pas de nouvelles inférences, mais de la réévaluation des mêmes réponses avec verdicts précédents conservés. Le32B fonctionne techniquement ; sa supériorité qualitative n’est pas démontrée.
