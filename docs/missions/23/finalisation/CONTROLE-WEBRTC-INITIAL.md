# Contrôle indépendant initial —20 octobre2026

Codex a généré un WAV français avec le Piper canonique, puis exécuté verify_livekit_voice.py contre le véritable serveur LiveKit. Le client a ouvert une salle WebRTC ; le serveur a dispatché un job à l'application. Le journal systemd de l'agent contient TypeError: Agent.__init__() missing 1 required keyword-only argument: instructions. Le vérificateur échoue avec No real agent participant joined.

Ce test confirme une panne fonctionnelle, pas une panne du SDK client ni du serveur. Aucun micro physique. Aucun fichier applicatif corrigé par Codex. Échantillon de test Piper :3,564s, PCM mono44100Hz, RMS3103 ; fichier privé conservé localement. Les logs détaillés restent locaux pour éviter d'exporter des identifiants réseau.

JARVIS doit corriger l'application et rejouer un essai réel avant réception. Le vérificateur indépendant est livré avec l'outillage, distinct de l'agent.
