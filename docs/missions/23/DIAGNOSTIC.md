# Diagnostic correctif de mission23 —19 octobre2026

**🟡 En cours.** Codex intervient sur le moteur et l’infrastructure ; JARVIS conserve le développement LiveKit. Exécution originale `7971ec0311124fb4be9e3125dcb291fd`, tâche `t05_dev_agent_python`, quatre réceptions conservées. Les instructions et le code réellement produits ont été lus ; les sauvegardes complètes restent privées. [État avant](ETAT-AVANT.json), [lancement](INSTRUCTIONS-LANCEMENT.md), [cycle23–31](../CYCLE-23-31.md), architecture et bilan22 consultés.

## Causes établies

| Domaine | Observation réelle | Conséquence |
| --- | --- | --- |
| Documentation | `web_fetch` refuse docs.livekit.io ; `host_github` refuse les dépôts officiels tiers | Le modèle cherche des exemples incomplets ou des URL404 plutôt que lire l’API officielle |
| Lecture des longues pages |9000 caractères renvoyés sans pagination | Même première portion relue alors que les classes recherchées sont plus loin |
| Python/SDK | LiveKit Agents1.8.8 installé ; imports/types/constructeurs supposés incompatibles | Nombreuses erreurs distinctes : AudioBuffer, SynthesisContext, ChatContext, rôles LLM et paramètres TTS |
| Dépendances | Venv Python3.13 présent ; pip et paquets installables dans le venv ; plugin manquant ensuite installé par JARVIS | Pas de panne générale Python ; le refus python3-pip a retardé l’exploration, puis contourné légitimement par venv |
| Processus | Le rapport04 montre un démarrage dans Bubblewrap, vérifié dans le même appel ; aucun serveur n’écoute ensuite sur7880/7882 au diagnostic | Le processus éphémère ne peut pas servir les tests ultérieurs entre appels ; installation/binaire/config conservés, disponibilité durable non établie |
| Configuration applicative | Agent.py importe encore des classes d’autres générations ; adaptateurs incohérents entre eux ; modèle par défaut absent de l’inventaire ; chemins voix supposés | Le développement doit être corrigé et testé par JARVIS, pas seulement compilé |
| Réseau/Ollama | API tags répond, un chat vers un modèle absent retourne404, un essai choisi avec timeout30s expire | Ni indisponibilité générale du Dell ni panne moteur démontrée par ces tests applicatifs |
| Contexte | Compression réelle : le dernier lot structuré était remplacé par un résumé cherchant stdout à la racine, absent dans un lot ; corps des classes perdu avant utilisation | Relectures identiques et corrections fondées sur les seules fins de fichiers ; [tailles observées](DEFAUT-COMPRESSION.json). Les preuves complètes n’étaient pas perdues dans SQLite |
| Erreurs remontées | Certaines commandes redirigent stderr vers stdout ; le résumé d’erreur reste alors vide malgré un traceback complet | Retour d’erreur peu exploitable dans les résumés, sans perte du reçu intégral |
| Faux succès applicatif | Le test LLM capture une panne de génération, affiche un avertissement puis retourne0 | Un succès shell ne valide pas une inférence ; contrat05 réparé pour exiger un flux réel et une intégration cohérente |
| Lots | JSON parfois mal formé, noms d’outils inexistants, host_exec envoyé dans un lot de lectures | Refus de paramètres réels ; aucune preuve d’exécution des entrées refusées |

La documentation actuelle décrit `AgentSession` comme orchestrateur et distingue les interfaces STT/TTS/LLM. La version installée est inspectée localement : elle fait autorité pour le prototype. Sources primaires : [sessions](https://docs.livekit.io/agents/logic/sessions/), [API TTS](https://docs.livekit.io/reference/python/livekit/agents/tts/index.html). Ces références n’affirment pas la compatibilité du code JARVIS actuel.

## Inférences : pas confondre événement et erreur

Les générations enregistrées dans le snapshot initial se terminent par `done_reason=stop`, sans panne de routage observée. Aucun `cycle_error` Ollama n’a été trouvé sur cette exécution au diagnostic. Les nombres et durées exacts sont publiés dans ETAT-AVANT.json. Les événements `inference_finished` contiennent des métriques, pas le champ de résultat d’un outil. L’adaptateur de suivi les expose avec `ok=null` ; son rendu actuel est neutre. Un affichage ancien différent n’est pas une preuve de panne du modèle. Aucun chantier Launcher n’est entrepris.

Le modèle répond et appelle effectivement ses outils, mais cela ne démontre pas la justesse de son code. Ni OOM, dépassement de contexte, génération tronquée ni indisponibilité globale Ollama n’est retenu comme cause prouvée. Le contexte configuré reste32768 ; les mesures du snapshot sont inférieures à cette valeur.

## Ce que les quatre validations signifient

Les quatre empreintes et états ne sont pas modifiés. Leur validation historique n’est pas étendue :04 prouve installation/configuration et démarrage ponctuel, pas un service permanent ni une conversation WebRTC. Les contrats créés par le modèle étaient vides : la présence d’un rapport et d’un reçu ne vérifie pas toutes ses affirmations. Les critères de05 ne sont pas abaissés ; son import, ses adaptateurs et ses tests doivent réellement progresser.


## Nouveau blocage exposé par le test indépendant

Le premier appel réel du vérificateur LLM échoue après45,884s : le SDK fait quatre tentatives de10s. Les journaux Ollama Mac montrent des annulations499 qui interrompent le chargement de Qwen avant disponibilité. La factory développée par JARVIS vise localhost, alors que le projet prévoit l’inférence Dell. Le modèle Qwen est réellement résident sur le Dell configuré et son API compatible répond. Codex a transmis ce diagnostic et assigné à JARVIS la correction de sa factory ; aucune modification applicative par Codex. [Preuves](TIMEOUT-CHARGEMENT.json). Ce délai applicatif ne doit pas être confondu avec une erreur d’inférence du worker, dont les appels Dell continuent normalement.

## Inventaire complet des échecs

Voir l’[inventaire détaillé](INVENTAIRE-ERREURS.md) et le [bilan correctif](RAPPORT-CORRECTIF.md).
