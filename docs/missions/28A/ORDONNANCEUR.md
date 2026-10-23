# Ordonnancement installé

Les appels du modèle passent par `jarvis/compute.py`. La file `compute_jobs` est dans le SQLite canonique des missions : un appel actif par nœud, priorité0 pour conversation/demande critique et10 pour mission, ordre d’arrivée à priorité égale. Les baux sont renouvelés pendant l’inférence ; la reprise d’un bail d’inférence perdu ne relance jamais une mutation d’outil.

Une conversation utilise le27B du Mac. Une mission utilise un nœud Dell éligible, selon disponibilité, catalogue, enveloppe mémoire et charge de sa file. Le Dell2 désactivé ne provoque aucune requête réseau. Une demande critique vise le Dell puis se replie sur le même27B local après impossibilité d’admission ou attente bornée ; une mission indisponible conserve son checkpoint.

La priorité s’applique entre appels finis. Aucun calcul GPU en cours n’est migré ni préempté. La configuration durable autorise4096tokens par segment ; la réception de priorité utilise des segments128tokens, clairement identifiés comme profil d’essai. Un test effectif a vérifié que la requête critique commence sur Dell avant le second appel de fond déjà en attente. Les réponses locales et le repli ont également été observés ; aucune réponse de modèle simulée n’est utilisée dans ces contrôles.

Le screening de modèles utilise l’outil `compute_benchmark`, qui réserve la même file pendant son programme distant. Il conserve les reçus du `host_remote/project_exec` existant. Cela évite le changement concurrent de modèle pendant les mesures. Les appels critiques peuvent toujours revenir au Mac ; leurs résultats sont attribués au modèle effectivement utilisé.

Le worker conserve le moteur Missions/DurableCycle, ses missions et ses checkpoints. Il s’exécute dans un processus distinct de la conversation et partage sa mémoire canonique. Le garde-fou `defer_waiting_tasks` place la mission en attente lorsque tous les travaux restants dépendent d’une attente réelle : il n’appelle plus le modèle pour inventer une tâche prête. Une reprise explicite ou une résolution de dépendance permet de retrouver le checkpoint utile.

Limite à conserver : la réception de file porte sur plusieurs requêtes d’inférence réelles, pas sur plusieurs missions agentiques longues entièrement réceptionnées en parallèle. Le worker durable installé reste unique ; son dispatch des missions est séquentiel. Cette distinction doit rester visible dans le rapport final.
