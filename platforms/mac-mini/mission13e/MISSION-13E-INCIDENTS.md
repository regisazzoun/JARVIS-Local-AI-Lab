# Mission 13E — incidents et corrections

1. Rapports 13B/13C limités par sandbox : audit réel 13E confirme accès hôte, API et GPU. Aucun correctif réseau/pilote nécessaire.
2. Port 8765 déjà occupé par 13B : développement parallèle sur 8767 et base fictive ; sauvegarde puis arrêt ciblé de 13B, bascule sur service dédié.
3. Venv sans ensurepip : environnement sans pip conservé ; outils QA installés dans le seul venv neuf via pip existant, aucun paquet système.
4. Test Chromium wait_for_function incompatible avec CSP unsafe-eval interdite : polling via protocole de test, sans ajouter unsafe-eval à l’application. Essais relancés, réussis.
5. Débordement horizontal du sélecteur historique mobile : largeur bornée, essai 390×844 relancé, réussi.
6. Open WebUI active/exited mal interprété initialement par Qwen : outil enrichi avec sémantique oneshot Docker et véritable health HTTP. Nouvelle réponse Qwen correcte ; aucun service WebUI modifié.
7. Script de recette important le package depuis tests/ : chemin du projet ajouté ; fixtures exactes du test nettoyées après l’erreur. Nouvelle recette complète réussie, y compris restart et données persistantes.
8. Proposition réutilisée au deuxième essai déjà approuvée : rejet d’une seconde approbation attendu ; nettoyage des seules fixtures puis recette relancée. Aucun consentement utilisateur inventé.
9. Connexions de sauvegarde/restauration SQLite non fermées explicitement : context managers closing ajoutés ; 15 tests repassés.
10. Risque autoplay mobile : lecteur natif conservé, action humaine ▶ disponible ; autoplay effectif et interruption testés dans Chromium. Safari reste à valider physiquement.

Les échecs des tests initiaux sont conservés localement. Les rapports GitHub sont expurgés ; aucune base ni preuve brute publiée. Il n’y a eu ni reboot serveur, ni manipulation de pilotes, d’accès distants ou de données WebUI.
