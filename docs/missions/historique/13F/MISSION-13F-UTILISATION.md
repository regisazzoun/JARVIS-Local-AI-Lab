> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/MISSION-13F-UTILISATION.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 13F — utilisation disponible

Ouvrir http://localhost:8765 sur le serveur ou via le tunnel SSH déjà existant. Se connecter avec les identifiants privés actuels. Aucun accès SSH/Tailscale, pare-feu ou HTTPS distant n'a été modifié.

## Conversation vocale

Cliquer **Conversation automatique**, autoriser le micro et parler. JARVIS détecte la parole, attend le silence, affiche la transcription, puis envoie si « Envoyer après transcription » est coché. La réponse détaillée apparaît et une synthèse courte est lue. Après lecture, parler à nouveau sans nouveau clic. Arrêter l'écoute avec le même bouton ; garder la page au premier plan.

« Arrêter l'audio » coupe immédiatement la lecture. L'option **Interruption par la voix (expérimental)** permet le barge-in ; avec de vrais haut-parleurs, vérifier d'abord qu'il ne se déclenche pas sur la propre voix de JARVIS. Si nécessaire utiliser un casque ou désactiver cette option. Push-to-Talk et démarrer/arrêter le microphone restent les secours. Safari/iPhone physiques non validés ; le lecteur natif ▶ reste disponible si autoplay bloqué.

Régler **Longueur orale** ou dire : « Je préfère des réponses vocales courtes. » La préférence est enregistrée sans clic supplémentaire, uniquement après transaction SQLite. « Donne plus de détails » augmente un tour oral sans changer le réglage durable. « Oublie ma préférence de longueur vocale » supprime ce souvenir.

## Mémoire

Exemples acceptés : « Désormais réponds en français », « Je préfère les réponses en paragraphes », « Je préfère le tutoiement », « Désormais cite toujours tes sources », « Désormais vérifie toujours tes résultats avant de conclure », « Désormais utilise le système métrique ».

Consulter les souvenirs dans Mémoire, changer de modèle ou ouvrir une nouvelle conversation : mêmes préférences actives. Pour corriger une préférence gérée, donner la nouvelle consigne ; pour supprimer, utiliser le bouton correspondant. Autres souvenirs et consignes sensibles restent des propositions à approuver/refuser explicitement. Les phrases ambiguës peuvent ne pas être détectées ; vérifier la liste au lieu de se fier uniquement aux paroles du modèle. L'option « Conserver cet échange » concerne l'historique ; une demande explicite de préférence durable peut persister indépendamment.

## Mode laboratoire

Cocher **Mode laboratoire isolé · commandes autorisées**, choisir Qwen recommandé, puis donner un objectif concret pour `/work`. Exemple : « Examine le service du laboratoire, reproduis la panne, évalue le risque, consulte deux documents, compare les corrections réversibles, réalise la correction, vérifie HTTP et conserve le rapport. »

Le modèle choisit les outils. Il ne dispose d'aucun terminal administrateur Mac mini, accès aux données personnelles ou commande Dell. Les fixtures de test réparées ne constituent pas de nouvelles pannes ; créer une fixture neuve avec tests/lab_fixture_13f.py avant une nouvelle recette. À défaut d'objectif réussi, lire le résultat incomplet et les traces privées. Ne pas confondre un rapport rédigé et un contrôle réel.

Rapport : runtime/lab/intervention.md. Audit minimal : SQLite ; détails privés : runtime/tool-traces.jsonl ; journaux propres : runtime/service.log (rotation). Les diagnostics hôte sont en lecture seule. Ne jamais exporter publiquement ces fichiers sans revue, ni publier runtime/auth, credentials, bases ou sauvegardes.
