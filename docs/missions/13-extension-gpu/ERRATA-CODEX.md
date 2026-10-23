# Rectifications indépendantes prioritaires

Les sources brutes JARVIS restent dans `jarvis/attempt-*.md` et dans les événements canoniques. Le présent texte Codex prime sur leurs interprétations erronées ; aucune correction n’est attribuée à une autocorrection indépendante de JARVIS.

| Affirmation ou ambiguïté | Rectification fondée sur preuve |
| --- | --- |
| Gen1 = panne critique, performances gravement limitées | NVIDIA documente une baisse du lien hors charge. Aucune panne ni performance sous charge n’est démontrée par cette seule mesure. |
| Pilote seulement inféré, nvcc non testé |550.163.01 est directement observé ; nvcc annonce12.4/V12.4.131. |
| Même0,179s sur les deux cartes | Reçu CUDA :0,17954168899996148s sur0,0,017779354000026615s sur1. Pas des temps d’inférence. |
| Torch25430786048octets ≈23,6Go |25,430786048GB décimaux, environ23,68GiB. GPU1 :25428426752octets. Conserver de préférence les octets exacts. NVIDIA annonce24576MiB par carte ; ne pas mélanger ces lectures. |
| Différences «normales à froid» établies | Une seule petite exécution ne démontre pas la cause de ces différences ; initialisation est une interprétation plausible. |
| Parallélisme1 signifie pas de parallélisme multi-GPU | Ce paramètre limite les requêtes simultanées. La visibilité d’un seul UUID est ici le vrai obstacle à l’utilisation de deux GPU par ce service. |
| SYS prouve une liaison QPI/UPI physique entre CPU | Non : machine mono-socket ; SYS est un classement de topologie. Pas de mesure de débit ni de pontNVLink reçu. |
| Peer accessFalse prouve tout le câblageNVLink physique | Non : accès direct non disponible au runtime et aucun NV# dans topo. Aucun inventaire physique de pont n’a été effectué. |
| Identité OEM ne peut être confirmée que par UUID/série | Le contrôle PCI indépendant confirme le sous-système Dell1028:3880 sur les deux cartes. Leur DP/N exact reste à relever ; publier des UUID/séries n’est pas nécessaire. |
| Service indisponible parce que127.0.0.1 refuse | Le bind réel était différent. Codex a corrigé le lecteur et JARVIS a observé le catalogue ; pas de panne Ollama reçue. |
| Petit CUDA réussi = installation complète/charge électrique reçue | Seulement un calcul correct par appareil. Câblage, intensités, températures stabilisées et inférence double restent non reçus. |

Le premier inventaire Codex produisait trop de sortie et tronquait son JSON ; cela a été corrigé puis retesté réellement par JARVIS. Des inventaires intermédiaires complets restent longs pour la vue modèle ; ils ont ensuite été résumés. Les27lectures répétées ne sont pas des essais de stabilité. JARVIS a également appelé le petit calcul malgré une consigne de différer si deux cartes étaient présentes. Les barrières d’identité ont fonctionné ; cette consigne n’était pas un verrou technique de l’outil. Aucune charge prolongée ni changement de puissance n’a suivi.
