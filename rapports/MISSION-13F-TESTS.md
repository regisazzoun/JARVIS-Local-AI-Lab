# Mission 13F — campagne et preuves

**Résultat : GO AVEC RÉSERVES.** Toutes les preuves brutes restent locales dans `mission13f-preuves/` ; ne pas les publier, notamment l'inventaire réseau et les traces privées. Les résumés ci-dessous portent sur des données fictives ou des compteurs.

| Catégorie | Exécution et preuve | Résultat |
|---|---|---|
| Unitaires/backend | `python -m unittest discover -s tests -p 'test*.py'`, unit-tests.txt | 27 passent ; SQLite réel, rollback, dédoublonnage, refus de sources privées, permissions, quotas, boucle et adaptateur |
| Simulés | Transports LLM stubs dans tests unitaires ; échantillons audio nuls dans Chromium | Ne prouvent aucune décision d'un vrai modèle ni acoustique physique |
| Intégration API réelle | integration-tests.json, 8 contrôles | Auth, mémoire automatique, trois moteurs réels, remplacement/suppression, langue, écrit/voix, diagnostics, audio, backup/restart |
| Navigateur réel | browser-tests.json, 8 contrôles | Chromium, AudioWorklet, micro WAV artificiel, silence de fin, deux échanges automatiques, Piper, interruption vocale, logout ; 1 contrôle algorithmique simulé |
| Vérification finale réelle | final-checks.json, 6 contrôles | Consignes durables, trois rappels, détails oraux ponctuels, lecture des logs par Qwen |
| Autonomie modèle réelle | autonomy-attempt5.json, autonomy-retry-final.json, autonomy-sources-final.json | Qwen choisit les outils, applique les corrections, vérifie HTTP 200 et rapporte ; preuve documentaire complète seulement au dernier essai |
| Physique/humain | Microphone/hp réels, bruit/écho, Safari/iPhone/macOS | NON TESTÉS dans 13F ; confirmation humaine antérieure de 13E conservée comme point de départ |
| Boot/PXE/RAID/Dell | Hors mission | NON TESTÉS, NON EXÉCUTÉS |

## Protocole d'autonomie

Les fixtures sont créées avec un port invalide, parfois sans section INI ou avec fichier en lecture seule. Les sondes démarrent un vrai processus HTTP dans Bubblewrap, demandent `/health`, vérifient le contenu attendu, puis arrêtent le processus. Ce n'est ni une VM ni une émulation HTTP. Un script de test transmet un objectif à l'API déployée ; il n'appelle pas les outils, ne choisit pas les commandes et ne répare pas la configuration.

L'essai d'itération obtient d'abord `HEALTH_FAILED` (port non entier), puis une sauvegarde récursive échoue : `cp: cannot copy a directory, '.', into itself`. Qwen choisit ensuite une copie du seul fichier, ajuste ses droits, corrige le port et obtient `HEALTH_OK`. Durée 198.33 s. Son affirmation de consultation de pages était fausse : cet essai ne valide pas le critère documentaire.

L'essai final lit effectivement :
- https://docs.python.org/3/library/configparser.html
- https://docs.python.org/3/library/http.server.html

Deux documents distincts d'un même éditeur, pas deux publications indépendantes d'éditeurs différents. Le contrôle refuse deux ancres ou versions du même document. Durée 125.51 s, 17 appels. Qwen compare réécriture/édition interactive/modification ciblée, choisit `sed`, sauvegarde, vérifie le vrai service et enregistre le rapport. Le premier appel de sonde est lancé depuis un mauvais dossier ; la trace montre l'erreur et l'appel final utilise le bon répertoire. Ne pas présenter ce premier échec comme une preuve du port invalide : cette panne a été reproduite dans l'autre fixture.

Les empreintes des scripts service/check sont inchangées. verified-autonomy-summary.json conserve le bilan contrôlé par Codex ; runtime/tool-traces.jsonl conserve les arguments et sorties privés ; l'audit minimal est dans SQLite. Les descriptions finales du modèle sont relues, pas acceptées comme preuves à elles seules.

## Mémoire et non-régression

La transaction d'une préférence échoue volontairement en unitaire : aucune ligne ni annonce de réussite ne subsiste. Une préférence identique garde le même ID ; une correction remplace le souvenir et l'index dans la même transaction. Suppression réelle de FTS5, puis rappel réel des trois modèles en nouvelle conversation. Préférences et historique reviennent après restart/relogin. Les langues anglais puis français sont réellement appliquées. Demande de détails pour un tour : la préférence durable courte reste intacte.

Les lignes initiales sont comparées intégralement avec la sauvegarde privée : 2 conversations, 14 messages, 1 souvenir identiques. Les modèles/voix existants sont réutilisés ; seules les données fictives de validation explicitement identifiées sont nettoyées. FTS5 integrity-check et foreign_key_check réussissent. Sauvegarde par unité systemd et restauration vers base neuve réelles ; reboot complet non réalisé.

## Performances

STT 4.07 s ; génération 1.95 s ; Piper 2.16 s ; total 8.17 s, audio 3.36 s. Rapport écrit 4239 caractères, synthèse orale 259 caractères ; résumé LLM 2.95 s.

Changements de modèle lors du rappel : Qwen 1,46 s, Ministral 9,12 s, Llama 11,61 s ; chargement inclus, campagnes non équivalentes. Un résumé vocal utilise maintenant le même num_ctx que la génération pour éviter le rechargement inutile observé initialement. 90 relevés GPU/CPU conservés dans autonomy-resources.json ; mesures hôte partagées, aucun SLA revendiqué.

## Reproduire sur l'installation existante

Préparer le WAV fictif avec `tests/prepare_voice_13f.py` (refuse d'écraser un fichier existant), puis exécuter les tests API/navigateur. Le dossier d'export QA est par défaut runtime/qa13f ; JARVIS_TEST_OUTPUT permet un autre dossier privé. Les tests lisent les identifiants localement, sans les afficher.

Pour une nouvelle panne, archiver **uniquement la fixture fictive identifiée** sans l'effacer, puis recréer la même fixture :
```sh
cd /opt/jarvis/conversation
mv runtime/lab/incident13f_sources runtime/lab/incident13f_sources-archive-$(date -u +%Y%m%dT%H%M%SZ)
.venv/bin/python tests/lab_fixture_13f.py --name incident13f_sources
.venv/bin/python tests/autonomy_sources_13f.py
```

Ce scénario prépare un défaut, envoie un seul objectif à Qwen et conserve ses choix. Il ne lance aucune commande de correction à la place du modèle. Les sources actualisées restent à vérifier à chaque exécution ; les modèles peuvent prendre d'autres décisions. Ne pas déplacer un répertoire contenant autre chose que cette fixture connue.
