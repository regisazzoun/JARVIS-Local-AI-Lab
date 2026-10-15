# Journal chronologique — 13 octobre 2026
1. Audit initial lecture seule : chemins 13A présents, imports moteurs réussis ; systemd/socket/netlink non accessibles, NVIDIA non visible. Aucune réparation entreprise.
2. Architecture backend bibliothèque standard, frontend sans dépendances. Répertoire home choisi pour respecter les droits d’écriture ; /opt conservé en lecture seule.
3. Création venv standard échoue faute d’ensurepip. Correctif autorisé : --without-pip ; aucun apt ni paquet installé.
4. Développement de la capture client, adaptateurs vocaux CPU isolés, orchestrateur Ollama et identité commune. Aucun nouveau service.
5. Développement SQLite/FTS5, approbations obligatoires, transactions et scripts privés de sauvegarde/restauration.
6. Six premiers tests réussis ; essai réel Piper/Whisper réussi en 5,14 s (premier passage). Bind HTTP essayé : socket interdite ; point bloqué, poursuite des tâches indépendantes.
7. Empreintes fichiers protégés relevées au checkpoint avant la campagne finale. Elles ne constituent pas un relevé antérieur au début de toute la mission ; les sorties initiales sont décrites dans le rapport global.
8. Correctifs : fermeture des connexions SQLite, contrôle booléen conservation, isolation temporaire, longs textes segmentés, protection Host/Origin/CSRF, arrêt par PID vérifié.
9. Neuf tests backend réussis ; campagne vocale réelle et persistance nouveau processus réussies. Node absent : validation syntaxique automatique JS non exécutée.
10. Classement 13B et 13C GO PARTIEL ; aucun test Ollama réel lancé dans l’environnement inaccessible, aucun tunnel créé, aucune exposition externe.
