# Réception documentaire T03 — Codex,24 octobre2026

Le nouveau choix est réellement rédigé et écrit par JARVIS dans la conversation authentifiée liée à la mission : Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice, voix intégrée Uncle_Fu. Les lectures de README sont celles de JARVIS via le worker. Codex a recentré l’étape puis interrompu le chat après l’écriture utile, car des tentatives intervention_report hors sous-ensemble étaient refusées ; le HTTP503 de cette interruption n’est pas une panne TTS.

La documentation primaire Qwen confirme le français et la voix masculine au timbre grave ; celle de Chatterbox confirme la prise en charge du français. Le choix de Qwen permet l’usage d’une voix prédéfinie sans référence externe. Sources : https://github.com/QwenLM/Qwen3-TTS ; https://github.com/resemble-ai/chatterbox.

Rectifications : «version éprouvée pour le français» n’est pas une réception locale. Aucun WAV n’est encore généré à cette étape. Le contrôle instruct de prosodie ne doit pas être promis pour0.6B ; la voix prédéfinie est le seul réglage vocal retenu pour le premier essai. Ces limites ne changent pas le choix et seront rappelées au générateur.

Verdict documentaire : choix accepté avec réserves par Codex après confrontation aux sources, pas PASS automatique du réviseur. Le contrôle de l’ancien rapport était INSUFFICIENT pour dépassement du budget des preuves citées ; ce résultat reste conservé et n’est pas transformé en PASS. Le critère technique de T03 est une comparaison/selection, pas le fonctionnement TTS, reçu séparément sur les futurs WAV. Cette réception opérateur débloque T04, sans valider l’autonomie générale ni la synthèse.

## Rectification de réception — versions successives

Le chat a écrit plusieurs brouillons. Le premier choisissait0.6B, le dernier fichier stable choisit **1.7B CustomVoice avec Uncle_Fu**. La première lecture/annonce Codex et son reçu mentionnaient encore0.6B : cette attribution est rectifiée ici et dans le journal, sans effacer les étapes précédentes. La variante1.7B dispose du contrôle instruct; les réserves0.6B visaient les brouillons intermédiaires.

Le dernier brouillon invente une voix Dylan «parisienne» : la fiche Qwen l’indique chinoise de Pékin, pas française. L’affirmation catégorique sur l’absence de voix utilisable Chatterbox sans référence n’est pas démontrée : le README propose aussi une génération par défaut; sa masculinité/qualité ne sont pas reçues ici. Le seul clonage explicitement exclu par le propriétaire est celui de Philippe Faure depuis les extraits de film; aucune nouvelle interdiction générale de voix autorisées n’est introduite. Le choix de la voix intégrée Qwen demeure valable, tandis que ces phrases du brouillon restent des erreurs conservées.
