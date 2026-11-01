# Missions distantes longues — réception et lancement JM-01

**1 novembre 2026 — ✅ qualification des unités distantes à checkpoints ; 🟡 JM-01 lancée sur Dell 2, unité 01 audit en cours au relevé.** Ceci remplace la réserve «contrôles distants fixes seulement» de la première réceptionPR #47. Aucune réception globale d’une mission arbitraire ni d’un client mobile livré n’est déduite du lancement.

## Directives et périmètre

Relus : AGENTS.md et chartePR #47, rapport initialPR #47, ROADMAP/SUIVI, issue #46-JM01 et référencesPR #39/41/29 du rapport initial. Ordre courant explicite : qualifier les longues missions distantes avec suspension/reprise, puis lancerJM01 surDell 2 si disponible, préserver le travailDell 1 et publier les preuves, sans validations intermédiaires. Cette extension remplace dans ce périmètre la limitation précédente aux lectures distantes. Les anciennes réceptions et leurs limites à leur date restent conservées. AGENTS et charte n’ont pas été modifiés. Aucune fusionmain ; M26-P4/MANUAL-HOLD et toutes les anciennes missions restent intacts.

## Exécution et arrêt distants

`remote_runner.py` supervise un processus à argv absolu, cwd limité à `~/JARVIS/idle-workspaces/`, contrat `checkpoint_safe=true`, sous une unité transitoire du gestionnaire systemd utilisateur. Le contrôleur ne lance pas un second moteur de missions. Le superviseur est une infrastructure de processus et de bail, sans boucle d’inférence ni collecte matérielle. La télémétrie existante dePR #47 reste utilisée.

- Manifest JSON persistant et immuable parID (argv, cwd, environnement explicite, délai/bail) ; changer le contrat sous le mêmeID est refusé. Cela ne garantit pas l’immutabilité de tout le code d’une application en développement.
- Verrou d’exécution et verrou de contrôle distincts ; `start` se rattache à l’unité déjà active, ou retourne le résultat déjà terminé. Pas de doublon après reprise du contrôleur.
- Cgroup systemd `KillMode=control-group`, SIGTERM, arrêt forcé après 6s, PIDprincipal nul et unité inactive vérifiés avant confirmation d’arrêt. La mort du superviseur principal tue également ses descendants.
- Bail renouvelable15s pendant les essais,45s pourJM01. Sans renouvellement, le superviseur termine l’arbre et conserve l’état paused ; après reconnexion, mêmeID et checkpoint applicatif. Pas de promesse de survivre au reboot matériel sans requalification.
- Erreurs persistantes plafonnées à 3, quatrième lancement refusé ; crash ambigu compté une fois, aucune remiseàzéro. Préemption/pause ne compte pas comme échec. État et checkpoints atomiques. L’application doit être idempotente entre checkpoints : aucun mécanisme générique de transaction/annulation de mutations externes.
- Budgets locaux du superviseur/enfants : Nice15, CPU 100%(un cœur), Tasks128, mémoire2GiB pourQwen Code. Le serveurOllama préexistant n’appartient pas à ce cgroup et n’est ni redémarré ni arrêté. L’arrêt du client ferme sa requête ; aucun kill global du serveur n’est utilisé.

L’environnement est un répertoire distinct, avec variables explicites et sans copie de cléSSH/GitHub ou réglages privés de production. `NoNewPrivileges=true` est actif ; ce n’est pas un confinement filesystem hermétique. Le processus garde les droits du compteadminjarvis. Les scripts tiers d’Open MobileUI ne sont pas installés/exécutés dans la tranche lancée.

## Admission et priorité

Le lancement exige les mesures fraîches et la disponibilité du nœud sélectionné. La file canonique reste lue seule par nœud ; Dell 1 occupé ne bloque pasDell 2. Pour un jobGPU déjà en cours, sa propre utilisationGPU et les poids de son modèle ne provoquent pas sa suspension. La résidence du seul modèle explicitement déclaré est admise à la reprise, sans éviction ; un autre modèle reste réservé. CPU libre requis au lancement≤25%, RAM disponible≥35%. Pendant sa propre inférence, gardeCPU≤95% afin de ne pas confondre le prétraitement du80B avec une charge externe ; la réserveRAM et la fraîcheur restent contrôlées.

La priorité aux autres requêtes d’inférence est complétée par la lecture de la table des connexionsTCP du port protégé11435 surDell 2 : Qwen Code local utilise l’adresse propre duDell 2 ; une connexion d’un autre hôte tenue plus de 6s préempte l’unité. Le seuil initial2s pouvait confondre les sondes existantes(timeout3s) et une lecture d’administration(timeout5s) avec un client interactif. Il a été corrigé et retesté avec une connexion persistante réelle, préemption observée à 6,3s. Ce contrôle n’analyse pas le contenuHTTP : il reste conservateur, et deux clients locaux au mêmeDell ne sont pas distingués par cette heuristique. Aucune promesse d’arbitrage parfait de toutes les sessions natives.

## Preuves de qualification

| Cas | Résultat démontré | Preuve |
|---|---|---|
| Contrôleur central → Dell 2, pause/reprise | Checkpoint8 stable à 8 pendant arrêt, puis12, unitécompleted | REMOTE-QUALIFICATION.json |
| Perte du renouvellement | Bail5s expiré, checkpoint 4 stable à 4, reprise à12 ; start ultérieur retournecompleted sans exécution | REMOTE-QUALIFICATION.json |
| Trois échecs et commande modifiée | Trois sortiesfalse comptées, quatrième refusée, changementmanifest sousmêmeID refusé | REMOTE-EXTRA-QUALIFICATION.json |
| Mort du superviseur principal | Descendant arrêté parsystemd, compteurheartbeat stable, résultatinterrupted et échec persisté | REMOTE-EXTRA-QUALIFICATION.json |
| Autre client d’inférence | Préemption réelle, unitéinactive/MainPID=0, échec0 | EXTERNAL-PRIORITY-GRACE.json |
| NativeQwen Code/JM01 | Session arrêtée, état persistant inchangé, reprise avec mêmes identifiants natifs | JM01-NATIVE-PAUSE-RESUME.json |
| Tests logiciels finaux | **16 tests PASS**, dont course complétion/systemd, erreur perdue comptée une fois et budgets de la propre inférence | REMOTE-TESTS.txt |

Incidents conservés : premier harnais interrogeait le checkpoint avant sa création et s’est arrêté(code du harnais, unité distante terminée normalement) ; il a été corrigé sans effacer cette première unité. La réception dédiée suivante a révélé une vraie course SIGTERM : arrêt demandé enregistréfailed si le fils mourait avant le contrôle du drapeauSTOP. Correction réelle puis reprise sur le mêmeID ; failure=1 historique toujours présent. Une autre course de lecture, entre écriturecompleted et observation systemd, a été reproduite en test avant correction ; relecture de l’état avant classementinterrupted, test finalPASS. Les préemptions de charge/sondes de la mise au point du80B restent dans le journal, pas présentées comme des essais réussis ni effacées.

Les fixtures de qualification sont courtes ; la réception du mécanisme est complétée par le lancement réel de la mission native, sa pause et la reprise de la même session. Aucun test de tenue de plusieurs heures ni garantie universelle sur tout logiciel distant.

## JM-01 effectivement lancée

Cadrage : issue #46, JARVISMobile réutilisant [Open MobileUI/RonasIT](https://github.com/RonasIT/open-webui-react-native). Source main épinglée au commit`84360a5cfd0c805edf70b121e35e13eeae6810a1`. Le fichierLICENSE amont estGPLv3 ; audit des conditions de distribution confié àQwen, aucune qualification juridique ou compatibilitéiOS reçue ici. La charte visuelle est référencée par le CSSLauncher2 existant, sans prétendre qu’une charte mobile complète a déjà été validée.

Dell 2 était disponible : admissioneligible, métriques fraîches enregistrées avant lancement. Jobstable`jm01-mobile-dell2-v1`, exécuté sous unité`jarvis-idle-adc8b0653adb3e956790.service`. Processus réels, session native persistante et appelsread_file/glob observés, pas seulement création d’une mission. Qwen Code0.26.4 officiel et son runtimeNode existant ont été copiés depuis le socle standard sans modification ; empreintes identiques contrôlées. Git absent a été installé surDell 2 (git/git-man/liberror-perl), sans miseàjour globale ni changementOllama. Node système20 reste inchangé, runtime fourni séparément.

Modèle80B existant`qwen3-coder-next:jarvis-dell2-32k`, contexte 32768 : relevé effectif chargé size53580812723, size_vram32765326128. Aucune sélection de modèleDell 1, aucun téléchargement, aucune modification des profils WebUI ou du routage global. ConfigurationQwenHome propre àJM01, clélocale facticeOllama, aucun réglageprivé copié/exporté.

Le wrapper`jm01_units.py` ne fait qu’appeler Qwen Code natif séquentiellement, préserver ses sessions, vérifier la présence des artefacts/tests et créer un commit Git par unité terminée avec contrôle structurel ; la réception factuelle indépendante reste nécessaire. Il ne fabrique pas les rapports du modèle et ne constitue pas une réception de leur exactitude générale.

Unités :01audit(code/licence/branche) →02inventairefonctions(API/auth/chat/outils/voix) →03prototype de connexion à serveurHTTP simulé et testsNode sans dépendances →04état/limites. iOSd’abord/Androidensuite restent l’objectif du chantier ; ni buildXcode, ni distributioniPhone, ni déploiementproduction ne sont autorisés par cette tranche. Les opérations et fichiers sont dans `~/JARVIS/idle-workspaces/jm01/`. Les sorties brutes et sessions natives restent privées surDell 2.

Au relevépublié : **unité 01 en cours, aucun livrable final ni checkpoint métier reçu**. Ne pas annoncerJM01 terminée, un prototype développé ou une autonomie générale. Le service reste actif et poursuit la tranche sans attendre une nouvellevalidation humaine ; préemption automatique si le nœud devient occupé.

## Préservation et publication

PID des deux servicesOllamaDell 1 identiques avant/après lancement ; active, travaux non interrompus. Configuration de calcul canonique strictement identique parSHA256. Conversation, broker, MCPO, OllamaMac, deux workers et ordonnanceur actifs ; WebUIHTTPS 200. Les contrôles établissent la santé observée et l’absence de redémarrageDell 1, pas un benchmark de latence ou une absence mathématique de toute dégradation.

Code et preuves relus publiés surPR #47. Le contrôle automatique a refusé une proposition de copie automatique des futurs livrables versGitHub : contenu/périmètre d’export encore inconnu. Cette automatisation n’a pas été installée ni contournée. Les checkpointsGit natifs restent surDell 2 ; leur publication nécessite la relecture du contenu réel. Le présent dossier de preuves connu et expurgé est publié dans le périmètre demandé. Une tentative inutile d’export des réglages privésQwen a aussi été refusée ; remplacée par une configuration dédiée construite sans lecture/export des secrets.

Retour arrière : créerPAUSE sur le contrôleur, vérifier unité distanteinactive ; désactiver seulement`jarvis-idle-scheduler` au besoin. Le bail termine une unité isolée du réseau si le contrôleur disparaît. Conserver historiques/checkpoints/sessions et tous les servicesQwen/WebUI. Aucun main fusionné.
