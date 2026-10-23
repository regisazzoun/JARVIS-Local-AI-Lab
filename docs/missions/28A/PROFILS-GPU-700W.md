# Profils et pointe GPU mesurée

| Profil | Limite par carte |
|---|---:|
| interactive-priority |200W|
| balanced |250W|
| mission-intensive |280W|
| dual-gpu-burst |350W|

Le programme protégé vérifie les plages nominales exposées par NVIDIA et relit les limites appliquées. Le profil burst utilise une fenêtre courte, un retour en finally et un ExecStopPost indépendant. Un seuil de température85°C et la recherche de nouvelles erreurs Xid/PCIe interrompent la fenêtre et provoquent le retour au profil normal.

JARVIS a exécuté la campagne graduelle réelle. Le contrôle indépendant de son artefact donne : pointe cumulée699,37W, maximum GPU66°C, fenêtre de profil10,17s,34échantillons, aucune erreur détectée dans cette fenêtre. Les maxima séparés des cartes ne sont pas additionnés pour fabriquer une pointe simultanée. La cible nominale exacte700W n’a pas été franchie par l’échantillonnage.

Une seconde lecture confirme250W/carte après retour normal. Le contrôle de reprise a relu les mêmes limites, le service normal actif et la restauration ExecStopPost. La campagne n’a pas été répétée pour remplir la documentation. L’empreinte de la campagne originale est `c9de58efdec6133fda0b0f891f9680e37a22f9bd51e77eaca1b8ad9492adc141`.

La réception fonctionnelle des câbles reste acquise par décision propriétaire. Cette courte campagne ne certifie ni leur brochage détaillé, ni une tenue prolongée700W, ni la consommation totale de la machine. Aucun wattmètre système n’était disponible. Les températures48–51°C du premier rapport libre étaient mesurées après la charge ; le maximum réel sous campagne est66°C.
