# Utiliser le banc JARVIS 23D

## Depuis le Mac

Ouvrir `JARVIS-23D.command` (copie fournie dans le workspace et `mission23d/`). Le lanceur réutilise l'accès SSH `jarvis`, démarre si nécessaire la passerelle temporaire et ouvre la page via un tunnel local. Garder la fenêtre du tunnel ouverte pendant la conversation.

Adresse : **http://127.0.0.1:8783/**, une fois le lanceur ouvert.

1. Choisir **Microphone** pour parler, ou **WAV** pour les essais sans micro. Démarrer obtient automatiquement un jeton de dix minutes et une salle dédiée.
2. En mode WAV, **Envoyer le scénario musée** démarre la session et publie le WAV prédéfini. **Interrompre : dimanche10h20€** injecte la correction sur la même piste. **Question de continuité** interroge le jour, l'heure et le budget.
3. Le menu de scénario et **Lancer le test WAV automatique** exécutent un essai mesuré dans une salle distincte. Le résultat indique PASS, FAIL ou interruption du test ; le WAV reçu est téléchargeable.
4. **Arrêter** coupe les lecteurs locaux, désactive le micro, ferme la session et supprime sa salle. Il demande aussi l'arrêt du test automatique éventuellement lancé par cette page.
5. **Exporter JSON** conserve événements UTC, temps relatifs, niveaux PCM, transcriptions et résultats. **Exporter audio conversation** devient utilisable après l'arrêt, une fois le WebM/MP4 finalisé. Les exports ne contiennent pas de jeton.

Les paramètres de connexion sont dans le panneau avancé. La page est temporaire et utilise les modèles déjà installés. Les preuves reçues sont numériques : le microphone et les haut-parleurs physiques restent à tester séparément.

## Côté laboratoire

Le prototype réutilise les services `jarvis-mission23-livekit-server` et `jarvis-mission23-livekit-agent`. La passerelle HTTP écoute uniquement sur127.0.0.1:8783. Le fichier privé de configuration LiveKit reste dans le workspace existant, hors Git.

Pour démarrer la passerelle au premier plan :

```sh
/var/lib/jarvis/projects/mission23/livekit-agent/venv/bin/python \
  /var/lib/jarvis/projects/mission23/mission23d/server.py
```

L'arrêter avec Ctrl+C dans cette fenêtre. Fermer une fenêtre de tunnel arrête l'accès du Mac, sans arrêter les services conversationnels ni le broker. La passerelle de réception est conservée en arrière-plan pour permettre l'utilisation du lanceur.

## Reproduire les mesures

Le pilote durable est le serveur de test, dont les processus survivent aux appels confinés de JARVIS :

```sh
curl -fsS -X POST http://127.0.0.1:8783/suite
curl -fsS http://127.0.0.1:8783/suite
```

La campagne comporte six exécutions : nominal, deux interruptions précoces, une tardive, silence et bruit au repos. Les entrées et seuils sont ceux du protocole. Le pilote produit un répertoire distinct par exécution et conserve un résumé daté par identifiant. Un résultat FAIL est une exécution effective en échec, jamais un PASS implicite.

Les trois essais correctifs sont dans `reports/retest-summary.json`. Le coordinateur de retest reprend son job actif et conserve les trois résultats ; il ne les rejoue pas lorsqu'on le relance après achèvement.

Pour vérifier les preuves d'une campagne achevée :

```sh
/var/lib/jarvis/projects/mission23/livekit-agent/venv/bin/python \
  /var/lib/jarvis/projects/mission23/mission23d/codex_suite.py --verify
/var/lib/jarvis/projects/mission23/livekit-agent/venv/bin/python \
  /var/lib/jarvis/projects/mission23/mission23d/codex_retest.py --verify
```

Ces vérificateurs confirment l'existence des résultats, y compris ceux en échec. Le verdict vocal est porté séparément dans le JSON. Les fichiers `routes-private.json`, les secrets, bases privées et journaux techniques bruts ne sont pas publiés.

## Retour arrière

Les correctifs applicatifs23D concernent `agent.py`, `factories.py` et `tts_adapter.py`. Les copies antérieures sont conservées dans `mission23d/historique/` avec leur empreinte ; le commit de base24 reste `ed3536393acddcd757ce23d55586a881a1d2d8f5`. Pour revenir en arrière, restaurer explicitement ces trois sources depuis les copies voulues, puis redémarrer uniquement le service agent LiveKit et refaire le test ciblé. Cela réintroduit potentiellement les défauts mesurés. Aucun reset SQLite, changement de politique du broker, suppression d'accès ou fusion dans main n'est nécessaire.
