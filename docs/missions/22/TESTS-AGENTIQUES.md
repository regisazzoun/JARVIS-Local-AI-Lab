# Réception et tests — mission22

**18 octobre2026 : moteur exploitable avec réserves ; mission21 en attente externe,6/7 tâches reçues.** Les tests unitaires ne remplacent pas les opérations du modèle.

| Vérification | Résultat |
| --- | --- |
| Tests V2 |36 réussis : journal durable, dépendances, reprise, sessions, contrats/provenance, publications/révisions, contexte, protocole et événements paginés |
| Non-régression13E/13F |18 tests historiques réussis sur les nouveaux modules lors de la réception initiale22 ; non relancés inutilement |
| Frontières broker |12 contrôles initiaux réussis ; contrôles ciblés supplémentaires des chemins GitHub et de la préservation documentaire dans la suite V2 |
| JavaScript |Deux suites existantes réussies ; syntaxe de la dernière version app.js validée |
| Navigateur connecté |22 assertions Chromium réelles : attente externe, sept rapports accessibles, six coches, acteurs JARVIS/Codex, événement de blocage, trois formats et ascenseurs internes : [preuve](RECEPTION-NAVIGATEUR-FINALE.json) |
| Journal intégral |14 pages API authentifiées,1865 événements, acteurs JARVIS/JARVIS-engine/Codex et aucun échec de pagination : [preuve](RECEPTION-EVENEMENTS-COMPLETS.json) |
| Attente après redémarrage |Nouveau processus, même cookie authentifié, état/checkpoints/empreintes inchangés et aucune reprise intempestive de la dépendance externe : [preuve](ATTENTE-EXTERNE-REDEMARRAGE.json) |

## Essais exécutés par le vrai modèle et le vrai broker

La [réception ciblée de production](PREUVES-RECEPTION-PRODUCTION.json) a terminé trois tâches en sept cycles,30 appels dont27 retours réussis,478,66s. Calcul volontairement incorrect, échec réel, correction, fichiers relus, administration SSH/Ansible Dell, copie idempotente et rapports réellement publiés. Les [rapports du modèle](reception/RAPPORT-AGENT-FINAL.md) sont récupérés avec leurs [manifestes](MANIFESTE-RAPPORTS-AGENT.json). Les corrections d’infrastructure Codex sont identifiées ; cette réception n’est pas présentée comme entièrement sans assistance.

Le [SIGKILL réel](INTERRUPTION-REPRISE.json) a conservé la tâche21.01 et son empreinte, puis repris automatiquement en122,92s. L’amélioration de récupération immédiate sous verrou exclusif est postérieure à cet essai et ne reçoit pas artificiellement cette mesure.

La [mission21 longue](PREUVES-MISSION21.json) termine cette réception en `waiting_external` :48 cycles engagés,639 intentions d’outils,638 retours enregistrés, six tâches validées,07 bloquée. Une intention restée sans retour lors d’une interruption n’est pas une réussite supposée. Les chiffres incluent lectures répétées, outils de suivi, lots et refus ; ils ne représentent pas639 opérations utiles distinctes. Les26 preuves opérationnelles sélectionnées correspondent toutes à des reçus broker `JARVIS-runtime`.

JARVIS a réellement installé/configuré VNC/KDE, authentifié RFB, reçu une image et vérifié le clavier français sur le LAN. Il a installé Tailscale et activé le service ; son propre contrôle retourne `NeedsLogin`. Il a corrigé ses documents après les refus du broker, publié le bilan partiel et appelé lui-même `mission_block`. Les24 intentions de publication se répartissent en22 versions vérifiées et deux versions rejetées puis remplacées ; aucune livraison non résolue. Les rapports01–07, ETAT et la synthèse partielle sont [récupérés depuis GitHub](MANIFESTE-RAPPORTS-MISSION21.json). Les [documents globaux sont conservés](PRESERVATION-PILOTAGE-MISSION21.json).

## Services, mémoire et voix

[Services après déploiement](NON-REGRESSION-SERVICES.json) : services centraux Mac actifs, SSH/Ollama Dell actifs, Tailscale Dell actif mais non enrôlé. Le statut systemd d’Open WebUI n’est pas un nouveau test conversationnel complet de cette interface.

[Whisper](NON-REGRESSION-VOIX.json) transcrit réellement le WAV synthétique existant en3,64s. [Piper/conversation simultanés](CONCURRENCE-VOIX-CONVERSATION.json) ont été exécutés pendant le worker Dell. Aucun microphone physique testé. [Toutes les lignes personnelles d’origine](PRESERVATION-MEMOIRE-FINALE.json) sont conservées, sans seconde mémoire.

La [promotion d’un chat ordinaire](PROMOTION-CONVERSATION.json) a créé une mission avant toute écriture puis publié un rapport, avec quatre tâches planifiées par le modèle et six cycles. **Échec précis conservé :** le marqueur a perdu son saut de ligne final demandé (`marker_exact=false`). Le contrat ne contrôlait pas cet octet ; aucune correction Codex cachée.

## Interprétation des performances et réserves

Avant :55/78 retours réussis dans deux échanges historiques, sans rapport final durable. Après : une réception ciblée27/30 avec trois tâches terminées, et une mission longue six tâches reçues sur sept. Les scénarios diffèrent : aucune amélioration contrôlée de qualité ou vitesse n’est déduite de ces ratios. Les relectures excessives, les corrections d’infrastructure pendant l’exécution et les erreurs de procédure empêchent une réception d’autonomie avancée sans réserve.

Les rapports modèle gardent des défauts sémantiques : date/attribution dans01, formulations de réception prématurées, confusion entre étapes07 et tâches de mission, commande utilisant un alias broker comme nom SSH. La [procédure vérifiée](ACCES-BUREAU-DELL.md) et les reçus d’outils font autorité. Le contexte a été adapté à32768 et les vues volumineuses sont explicitement abrégées, avec preuves intégrales conservées ; cela n’efface pas les échecs antérieurs.

Le test VNC direct par Tailscale et la clôture complète21 restent **non reçus**, faute d’identité d’enrôlement disponible. Aucun client physique MacBook ni déploiement Dell2 revendiqué.
