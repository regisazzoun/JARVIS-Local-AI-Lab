# Modèle conversationnel du Mac mini

Le modèle choisi par le propriétaire, `qwen3.5:27b-q4_K_M`, est réellement installé et exploité localement. Le Mac dispose d’un Corei7-8700B,12threads logiques,32Gio de RAM physique et d’une RTX3090 externe24Gio. Cette découverte explique la faisabilité locale ; aucune substitution par un petit modèle n’a eu lieu.

Le chargement froid initial a pris environ13,25s ; première sortie à13,48s et génération autour37,4tokens/s, pour une sortie limitée à96tokens. Cette mesure de débit ne prouve pas la qualité d’une réponse tronquée. Le routeur maintient le modèle local résident avec keep_alive=-1 après usage.

Six réponses simples «OK» par l’API JARVIS pendant le travail du worker Dell ont pris environ1,074–1,864s. Avec une charge CPU de fond supplémentaire, six autres ont pris environ1,070–1,183s. Ces petits échantillons ne suffisent pas à caractériser tout dialogue ni toutes les demandes d’outils. Les mesures de bibliothèque du routeur, plus courtes, ne doivent pas être confondues avec les latences API de bout en bout.

Une première requête du contrôle de reprise a observé14,70s, puis des réponses chaudes plus rapides. La latence de premier chargement reste une limite réelle. Le test direct froid initial et l’API chaude après installation ne sont pas un comparatif avant/après contrôlé ; aucun gain de vitesse n’en est déduit.
