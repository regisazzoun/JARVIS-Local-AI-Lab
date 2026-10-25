# Escalade — progression et tests,25octobre2026

**Aucune correction vocaleD01/D02 reçue à ce point.** Après reprise, D01est encore arrêtée sur erreurs de simulationWebAudio ; D02a réellement produitAUDIT-WAV.json puis s'est remise à relire cet artefact jusqu'au seuil de garde. L'auditWAV n'est pas une transcription et ne doit pas être appelé testWhisper.

## Intervention ponctuelleCodex

D01 : conservation du fichierJARVIS avant intervention, correction du harnais de test seulement. Le constructeurAudioContext est raccordé après l'évaluation d'Object.assign ; le doubleMediaRecorder fournit isTypeSupported ; les cinq cas enregistrent un nettoyage de leurs ressources. Un premier test révèle l'absence supplémentaireAudioNode.connect dans le double ; cette méthode est ajoutée lors d'une deuxième correction justifiée. Les assertions originales sont conservées. Résultat réel : cinqPASS. Les cinq cas de base comprennent des attentes de zérotranscript et ne prouvent pas la prise en compte d'une émission : ils ne reçoivent donc pasD01. Aucun fichier du pipeline vocalproduction n'est corrigé par cette intervention.

D02 : ajout de la seule opération fixe`host_remote(local-ssh,jl03_d02_stt_probe)` au broker existant. Elle utilise le vrai servicecanonique`/api/stt`, avec l'authentification opérateur existante gardée hors du contexte modèle. Trois fichiers préqualifiés parSHA256, aucun chemin ou code fourni par le modèle, un appel par cas, pas de nouvelle installationWhisper ni changement de modèle/routage. Les réponses et empreintes sont conservées enJSONprivé et dans les reçus natifs lors de l'appelJARVIS.

PrévolCodex : accueil6,16s, transcription exacte après normalisation de ponctuation,WER0 ; silence rejetéHTTP400 ; fichier invalide rejetéHTTP400. Ce PASS porte uniquement sur ce corpus contrôlé, pas le microphone du propriétaire ni un problème intermittent dans la capture navigateur. L'interface de test peut rendreINSUFFICIENT si la passerelle est occupée ; aucun succès ne sera déduit de ce retour.

## Retour àJARVIS

Les deux mêmes missions reprennent avec les compteurs et historiques conservés. D01doit retester le harnais réparé, le transférer et l'exécuter sur les deuxDell, puis produire une vraie reproduction de la réception vocale. D02doit appeler le nouveau testSTT et confronter ses propres reçus au chemin de capture ; elle ne doit plus relire l'auditWAV pour prétendre vérifierWhisper. Un extrait déjà observé du contrôleur reste dans le checkpoint de travailD01 pour éviter une quatrième lecture inchangée.

Les critères précédents ne sont ni retirés ni reçus par un résumé. En absence de panne reproduite, JARVIS doit expliciter la preuve manquante plutôt qu'annoncer un correctif. Le contexte volumineux et les limites de supervision restent ouverts. D03/D04/D17 ne sont pas transmis.

Fichiers protégés installés : `/usr/local/lib/jarvis-host/jl03_stt_probe.py`, `/etc/jarvis/jl03-stt-probe.json`. La configuration ne contient que cas fixes/empreintes/texte attendu ; les secrets restent dans les mécanismes d'authentification existants. Aucun serviceJL01/JL02, moteur, routage ou répartition des calculs n'est modifié.
