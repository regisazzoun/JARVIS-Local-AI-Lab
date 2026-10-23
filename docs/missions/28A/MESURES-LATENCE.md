# Latences mesurées et portée

| Mesure réelle | Échantillon | Résultat |
|---|---|---|
|Ollama local froid initial27B|Une requête limitée96tokens|Chargement~13,25s ; premier contenu~13,48s ; débit~37,4tokens/s|
|API JARVIS, réponse simple pendant worker Dell|6requêtes|Environ1,074–1,864s|
|API JARVIS, même réponse avec charge CPU de fond et Dell|6requêtes|Environ1,070–1,183s|
|Première réponse locale du contrôle de reprise|Une requête|14,70s, puis réchauffement|
|Routeur bibliothèque, réponse locale pendant requêtes distantes, essai v2|3requêtes|Environ0,378–0,680s|
|Contrôle alterné direct Ollama chaud|6requêtes identiques|Médiane0,285s ; p95 empirique par rang0,308s|
|Même contrôle via bibliothèque routeur|6requêtes identiques|Médiane0,550s ; p95 empirique par rang0,596s|

Le contrôle alterné utilise le même27B local, le même prompt, le même contexte8192, think=false et8tokens maximum. Il mesure le chemin actuel direct contre routé, sans prétendre reconstituer un état historique avant installation. Le surcoût d’admission/file/sonde est visible. La mémoire, l’interface et les outils de l’API expliquent un autre périmètre de latence ; ne pas comparer ces colonnes comme une accélération deJL-02.

Les percentiles sur six mesures sont descriptifs, pas une garantie de service. Le benchmark froid et le benchmark API chaud ne constituent pas un comparatif avant/après équivalent. Les longues réponses, recherche/outils et chargements de modèles ont des latences différentes ; le choix qualité/vitesse du Dell est traité dans le comparatif des modèles.

La réception de priorité a fait exécuter trois véritables requêtes Dell et des réponses locales simultanées. Une demande critique a commencé sur le Dell avant une demande de fond déjà en attente. Une autre épreuve a injecté une connexion impossible dans une copie de configuration et observé la réponse du même27B local ; aucun service Dell n’a été arrêté pour cette injection. Le premier essai de priorité était insuffisamment strict et reste conservé, distinct de l’essai v2 accepté.

## Configuration stabilisée et missions réellement concurrentes

Les tailles16384(Mac) et24576(Dell) sont désormais stables entre appels internes et utilisateur. Avant cette correction, le premier appel API pendant benchmark a pris15,53s et une demande critique13,85s avec une attente de file12s. Ces valeurs restent conservées. Après stabilisation et borne de file2s : six réponses API simples pendant mission80B prennent0,978/1,067/0,894/0,831/0,834/0,829s ; une analyse critique avec repli local prend3,895s.

Pendant deux missions durables réellement running, six réponses locales prennent0,961/0,870/0,828/0,921/0,927/0,892s. Ce sont des requêtes OK courtes sans outils, pas une garantie sur toutes les conversations. Le p95 empirique au rang supérieur vaut0,961s sur ces six points ; un tel échantillon ne caractérise pas une distribution de production. Les journaux conservent modèles, nœuds, baux et quotas avant/après.

Le contrôle direct/routeur apparié antérieur utilisait8192tokens pour les deux chemins, avant le profil stabilisé16384 : médianes0,285s direct et0,550s routeur, p95 au rang supérieur0,308/0,596s sur six appels chacun. Il mesure un coût de routage sur ce protocole précis ; il ne doit pas être présenté comme un avant/après historique à charge égale du système complet.
