# Installation du candidat32B — incident et correction

État au23 octobre2026 : 🟡 retest JARVIS en cours. Ce document ne réceptionne pas la mission28A.

## Diagnostic observé

La présence du modèle dans le registre officiel et sa présence dans le catalogue local sont deux observations distinctes. Le tag exact est `qwen3:32b-q4_K_M` ([registre officiel](https://ollama.com/library/qwen3:32b-q4_K_M)). Le premier rapport libre JARVIS proposant le27B comme substitution était erroné ; le27B était déjà installé. Le téléchargement du70B a réellement abouti, sans démontrer son avantage qualitatif.

Les tentatives suivantes de JARVIS ont utilisé `host_remote` avec `action=pull` et `model=...`. Le contrat actif ne déclarait pas le champ `model` ; le registre a donc rejeté l’appel avant toute installation. D’autres cycles ont tenté des identifiants de tâche/preuve d’exemple et lu les mêmes preuves sans progrès. Le moteur a refusé de valider ces fausses complétions. Ces événements restent dans la mission canonique `59830a3414a243c198c53e5624a286a3`.

Une première révision de contrat par Codex n’avait pas été appliquée, car l’appel de plan n’indiquait pas la version attendue. Cette erreur de coordination a été reconnue, corrigée et journalisée ; les versions2 puis3 sont effectivement persistées. Elle ne doit pas être attribuée à JARVIS.

## Correction Codex déployée

Le broker existant accepte désormais `host_remote(host="dell-observe", action="model_pull", model="qwen3:32b-q4_K_M")`. L’alias `pull` reprend le même contrat. Le programme distant protégé utilise POST `/api/pull`, conserve des fichiers de progression privés, limite la durée de chaque appel et permet une reprise depuis le cache. La liste des candidats reste dans la politique propriétaire protégée ; aucun paramètre URL ou fragment shell n’est ajouté au modèle.

Une réussite exige la fin de téléchargement ET une relecture du tag exact dans `/api/tags`. Un HTTP200 contenant une erreur, un flux interrompu ou le seul27B présent ne valent pas réussite. Une nouvelle lecture `hybrid_catalogue` reste disponible pour la vérification indépendante.

Codex a installé l’interface, pas déclenché le téléchargement par ce nouvel outil. JARVIS doit exécuter l’appel et produire un reçu réel avant réception. Le worker a été arrêté au checkpoint pour le remplacement de code, son contexte ancien archivé et son plan révisé en version3 ; les preuves historiques restent conservées.

## Validation logicielle

Sept nouveaux tests couvrent POST et tag exact, absence de tag malgré status success, erreur dans HTTP200, progression tronquée, modèle déjà présent, refus d’un candidat hors politique et commande distante fixe. La suite complète dans le venv actif donne217 tests réussis. Une première tentative avec le Python système a échoué faute de `jsonschema` ; son journal est conservé et ne constitue pas une régression du venv installé.

Les tests de fixtures HTTP sont des preuves logicielles, pas des preuves d’exécution autonome. Le résultat opérationnel et le reçu seront ajoutés après observation.
