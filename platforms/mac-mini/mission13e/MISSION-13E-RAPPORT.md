# Mission 13E — intégration JARVIS, 14 octobre 2026

**État final : GO AVEC RÉSERVES.** Passerelle durable installée et active sur boucle locale. Chaîne audio → Whisper → véritable Ollama → Piper → lecture navigateur validée. Réserves : parole humaine et écoute physiques, Safari/iPhone/macOS réels, accès HTTPS distant (13D reste en attente).

## État initial et changements
Ollama 0.40.3 et Open WebUI actifs, API WebUI saine ; trois modèles installés : Qwen 3.5 27B Q4_K_M, Ministral 3 14B Q4_K_M et Llama 3.1 8B Q4_K_M. RTX 3090 disponible, pilote 595.91.07, CUDA annoncée 13.2 ; aucune modification de pilote. Passerelle 13B existante active, base vide. Sauvegarde privée avant reprise ; ancien dossier conservé. Code fonctionnel réutilisé, installé sous `/opt/jarvis/conversation` avec venv isolé.

Ajouts : authentification locale par mot de passe dérivé PBKDF2 et cookie HttpOnly/SameSite, identité versionnée, propositions via LLM sans approbation automatique, schéma SQLite v2, dédoublonnage, obsolescence, informations documentaires séparées, registre d’outils borné, lecteur audio natif mobile, envoi automatique après transcription désactivable. Service `jarvis-conversation.service` actif et activé ; sauvegarde quotidienne `jarvis-memory-backup.timer` activée et premier backup/restauration testés. Aucune modification des unités Ollama/Open WebUI, de leurs données, des modèles, de SSH/Tailscale, du pare-feu, du RAID ou du noyau.

## Résultats réels
15 tests automatisés passent. Trois moteurs réels retrouvent le même code fictif approuvé ; correction et suppression vérifiées séparément sur stockage et réponse LLM. Qwen appelle réellement le diagnostic des services et propose un souvenir laissé en attente. Redémarrage systemd de la passerelle : historique et souvenir retrouvés, reconnexion requise. Sauvegarde SQLite puis restauration vers une nouvelle base de test réussies.

8 essais Chromium réussis sur le service déployé : connexion, capture MediaRecorder WebM d’un WAV français fourni comme microphone artificiel, transcription, conversation réelle Qwen, lecture/arrêt audio, réponse longue segmentée, chaîne vocale automatique et disposition mobile, refus des APIs privées après déconnexion. Ce sont des tests de navigateur et audio réels avec source micro artificielle, pas des validations iPhone ou parole humaine. Capture ALSA physique de 2 s réussie mais quasi silencieuse (pic 6/32768), donc aucune validation de parole humaine.

## Performances mesurées
Premier flux complet : STT 2,84 s, Ollama 15,13 s (chargement 13,76 s), TTS 2,47 s, total 20,44 s. Sur service déployé, modèle chaud : STT 2,90 s, Ollama 1,52 s, TTS 2,59 s, total 7,01 s. Ces résultats concernent de courtes phrases, pas un SLA.

Changement de moteur avec rappel réel : Llama 9,17 s, Ministral 19,21 s, Qwen 17,92 s, principalement chargement. Essai Qwen parallèle aux workers CPU : génération 3,78 s, STT 3,44 s, TTS 2,52 s ; VRAM échantillonnée 17 503 MiB, GPU 82–87 % pendant génération. Campagne voix : CPU enfants cumulée 11,30 s sur 7,95 s murales, RSS maximal enfant 774 MiB ; mesures de campagnes distinctes, ne pas les additionner.

## Exploitation et limites
Interface locale : `http://localhost:8765`. Depuis macOS : tunnel SSH existant vers cette boucle locale, puis connexion utilisateur. Identifiants uniquement dans le fichier privé `/opt/jarvis/conversation/runtime/credentials.txt`, jamais dans les rapports ni GitHub. Guide iPhone : HTTPS privé préparé, non activé ; pas d’URL iPhone distante validée. Aucun port JARVIS ouvert sur LAN ou Internet.

Qwen conserve une identité commune et injecte les seuls souvenirs actifs/validés ; la recherche reste lexicale FTS5, pas sémantique. L’historique et les anciennes réponses ne sont pas effacés par suppression d’un souvenir : la suppression est testée comme retrait de la mémoire active dans une nouvelle conversation. Les sessions non conservées restent en RAM. Rétention automatique de l’historique au lancement : 30 jours configurables. Les sauvegardes quotidiennes ne sont pas purgées automatiquement ; contrôler leur espace disque.

Les preuves locales sont dans `mission13e-preuves/` : données fictives et mesures ; aucune preuve brute, base, credential ou sauvegarde privée publiée. Documentation expurgée proposée sur branche GitHub dédiée, sans fusion automatique. Prochaine étape : validation humaine des clients et reprise distincte de 13D ; aucun PXE/Dell exécuté.

Période observée entre audits initial/final : 616.9 secondes (10.3 minutes), hors finalisation documentaire. La session commence le 14 octobre vers 00 h 55, heure de Paris.
