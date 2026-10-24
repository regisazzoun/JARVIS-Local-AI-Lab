# Mission 28A — clôture en l’état du 24 octobre 2026

**🟡 Clôturée incomplète sur décision du propriétaire.** Le propriétaire demande : « Cloture a sa place. On bascule sur la 80B vu qu’elle semble plus performante et on refera des tests plus tard. » Codex réalise la clôture et la publication sans transformer les échecs en validations. Le cœur hybride est installé et exploitable ; la réception agentique finale reste non acquise. Branche `codex/mission-28a-routage-modeles`, [PR25](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/25), base préparatoire ac2b0cb préservant les travaux précédents.

**Choix opérationnel conservé :** `qwen3-coder-next:q4_K_M` pour les missions Dell1 ; `qwen3.5:27b-q4_K_M` pour la conversation sur Mac mini. Cette affectation était déjà effective : la décision propriétaire confirme son maintien. Les nouvelles campagnes sont différées, sans reprise automatique de 28A.

## Modèles et ressources

Qwen3.5:27b-q4_K_M est installé et réellement utilisé sur le Mac mini, qui dispose aussi d’une RTX3090 externe. Aucun remplacement par un modèle léger. Pendant deux missions durables actives, six réponses API simples ont pris0,828–0,961s. Cette série courte ne promet pas cette latence pour un dialogue complexe ou un chargement froid.

Le Dell utilise désormais Qwen3-Coder-Next:q4_K_M,80B MoE(~3B actifs). JARVIS a installé le candidat et lancé18inférences comparatives27/70/80B. Les scores bruts sont4/6,2/6,5/6 ; le32B installé et testé auparavant atteint3/6 après correction du juge Codex, sans nouvelles générations. Le cas coverage est ambigu ; les réponses et FAIL restent conservés. Le débit médian80B est87,5tokens/s contre29,7pour27B Dell sur le protocole, soit~2,95fois. Ce petit screening ne reçoit pas une autonomie générale.

Deux GPU sont réellement utilisés : environ23044et22968MiB occupés au contexte24576. Les journaux indiquent49/49couchesGPU et des buffers CPU_Mapped6511,19MiB : la RAM DDR4 participe au mappage, mais aucun offload de couchesCPU n’est démontré. Deux cartes24GiB ne deviennent pas une carte monolithique48GiB. Le comparatif détaille quantifications, chargements et compromis.

## Routage et disponibilité

La conversation va sur Mac ; les missions durables vont sur Dell. Le routage initial de demandes complexes est une règle explicite par expressions, complétée par compute_escalate que JARVIS peut appeler : ce n’est pas une estimation universelle de difficulté. L’admission observe catalogue, ressources, charge et disponibilité. Le Dell2 reste désactivé, sans URL ni capacité fictive ; son profil d’enrôlement futur est préparé.

Deux slots utilisent le même Mission Engine, SQLite, mémoire et file d’inférence. Deux missions sont réellement observées running avec appels du broker attribués JARVIS-runtime ; le GPU reste sérialisé entre leurs inférences. La priorité critique a été vérifiée sur requêtes réelles avant un deuxième traitement de fond en attente. Un calcul GPU engagé n’est pas préempté ; les checkpoints permettent la reprise. Une panne TCP injectée dans une copie de configuration a déclenché une vraie inférence de repli Mac sans arrêter le Dell.

Les contextes sont stabilisés16384Mac/24576Dell ; l’attente critique est bornée2s. Six réponses pendant mission80B :0,829–1,067s, demande critique repli3,895s. Les valeurs antérieures15,53s au premier appel et13,85s de repli avant correction restent conservées. Le contrôle apparié direct/routeur à8192tokens mesure un surcoût médian~0,265s sur son protocole ; aucune accélération historique avant/après à charge identique n’est inventée.

## Quotas et énergie

Mac : CPUQuota900%=9sur12threads, soit plafond75% pour le slice de fond ; réduction300% pendant interaction, retour900% observé. Les réservations MemoryLow parent/interactif et l’admission mémoire protègent la disponibilité. Cela ne constitue pas une partition25% physique de VRAM. Les deux workers partagent ce quota.

Dell : les missions peuvent utiliser les deux GPU et la RAM disponible, sous admission/concurrence contrôlées. Les profils interactif200W, équilibré250W, mission280W et pointe350W/carte sont installés. La campagne réelle JARVIS a atteint699,37W cumulés, maximum66°C, fenêtre~10,17s, sans erreur observée dans cette fenêtre. Retour automatique250W/carte relu indépendamment. Pas de mesure à la prise, pas de certification ni tenue700W prolongée. La réception fonctionnelle des câbles13 n’est pas rouverte.

## Réception agentique et exactitude

Les installations, comparaisons, observations et campagne GPU de JARVIS sont distinguées des développements, plans et contrôles Codex. Les références parent de vérification et le candidat de clôture évitent les boucles sur reçus enfants. Les contrats sémantiques restent obligatoires pour clôturer une tâche dirigée. Les outils enregistrés peuvent exposer leur schéma dans la phase d’exécution, sans extension de droits.

La première consolidation écrite avec des constantes a été rejetée comme preuve de programme. JARVIS a ensuite créé son propre Python ; le vérificateur protégé détecte FAIL4/4 malgré code retour0, sources inchangées et manifeste valide : chaque modèle reçoit à tort11/18. Le dernier contrôle observé à 02 h 01 le24 octobre échoue encore aux quatre variantes : les scores par modèle sont corrigés sur les originaux, mais model_count vaut3au lieu de4 et le programme ignore les chemins d’entrée fournis, en relisant des fichiers fixes. Le réemploi du skill et la réception E restent non acquis. La tâche JSON de l’audit est validée par le moteur, mais son rapport conserve une citation inventée et une affirmation incorrecte sur l’absence de résultats individuels. La validation du JSON ne reçoit donc pas sa prose. Aucun succès par décret. Les textes comportant erreurs de comptage, unité et attribution sont conservés avec errata.

54outils natifs et quatre skills actifs sont accessibles (config-repairv6, debian-diagnosticv1, dell-roundtripv1, github-publishv1).238tests logiciels passent dans le venv actif ; ils sont distincts des opérations agentiques. Les services conversation, broker, Ollama, workers, watchdog et LiveKit restent actifs ; les huit fichiers du moteur et le broker correspondent aux sources publiées. Les missions historiques et bases n’ont pas été remplacées.

## Écarts et suite

Le nouveau pilote améliore le screening mais exige encore assistance et contrôles de réception. La planification globale28A a été fournie/versionnée par Codex, donc ne lève pas la réserve26B sur une planification sans rappel. Les rapports libres restent à contrôler ; les FAIL historiques ne deviennent pas des succès. Dell2 est préparé uniquement.14A reste une épreuve distincte non lancée ;26B clôturée incomplète,24-Old etTTS-01 ne sont pas repris.

## État de clôture et travaux différés

Six étapes principales restent validées : inventaire, essai32B, installation80B, comparatif, routage et profils GPU. E_program, E_reception et F_concurrency sont interrompues, sans coche de réception. La tâche audit secondaire garde sa validation JSON historique ; ses erreurs de prose restent des réserves.

Les deux exécutions canoniques sont interrompues au checkpoint sur ordre du propriétaire. La publication automatique vers le dépôt incorrect `jarvis-labs/mission28a`, branche main, avait été refusée par le broker ; son élément de file est désormais superseded et ne sera plus retenté. Aucune publication de cet audit dans ce dépôt ni fusion main n’est déclarée. Codex publie les preuves et la clôture dans la branche autorisée de la PR25.

Le dernier correctif logiciel isole les observations et notes de la tâche active ;238tests passent. Les derniers essais agentiques montrent toutefois encore des erreurs de format, des répétitions et des tentatives de clôture sans preuve appropriée. Le correctif est installé, mais sa réussite logicielle ne lève pas les réserves opérationnelles.

Lors d’une campagne ultérieure explicitement lancée, reprendre les preuves et les versions de programme : respecter les arguments d’entrée, compter les quatre modèles, obtenir un contrôle varié conforme, vérifier le skill et corriger les rapports. Ne pas recommencer les installations ni les campagnes reçues. Aucune date ni relance automatique n’est créée.

Les preuves structurées, versions de plans, sorties originales et empreintes restent dans PREUVES-JARVIS.json et preuves/. Le rapport et les événements distinguent les développements/diagnostics Codex des opérations et du code JARVIS.14A reste ouverte et non lancée ;26B reste clôturée incomplète,24-Old/TTS-01/Dell2 ne sont pas repris. Aucune fusion automatique main.
