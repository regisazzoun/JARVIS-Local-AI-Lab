# Distribution des commandes et des inférences

## A. Tâches techniques

Les deux workers persistants tournent sur le **Mac**, dans le même Mission Engine et la même base missions.sqlite. Dell1 etDell2 hébergent des espaces autorisés `/opt/jarvis-lab/...` exécutés parSSH ;ils ne font pas tourner ces deux processusworkers centraux.

Dans le parcoursdistributed_authority, Qwen80B choisit fichier, commande, executor=dell1/dell2 et contrôle. authority_work passe par le broker hôte sur socket Unix, les profilsSSH épinglés, les contrôles d'identité et les racines autorisées. authority_sync conserve le manifeste exact ;authority_accept impose une vérification sur l'autre hôte. Ansible est un outil distinct sur le Mac. Le modèle s'exécute surDell1, mais les commandes choisies peuvent aller surDell2.

Ce parcours est prouvé **historiquement**, pas rejoué :réception26-P1, missione26946bff84d4e06ad395b969ffcd72f, reçus39844/40117 et40292/40357, plansQwen versionnés. P2 reprend les compteurs persistants et états d'exécution distincts, réception52932 pour l'intégration ciblée. P3 conserve les archives, checkpoints et compteurs, complément77116. Ces événements existent encore dans la base actuelle (E05). La réception était ciblée et assistée ;aucune généralisation silencieuse à toutes les missions.

L'audit utilise réellement SSH surlesdeuxDell pour relever matériel et services. Ce sont des commandes **Codex**, pas des sous-tâches choisies parJARVIS. La missionP4 c32347de3edf4288a4751a3e65afa7eb reste interrupted/version0, MANUAL-HOLD présent, superviseur arrêté. Aucun nouveau calcul d'une mission suspendue n'est déclenché.22missionscompleted,19interrupted,6waiting_external,3reported et1incomplete à l'instantané ;aucunequeued/running. Les processusworkers actifs peuvent donc être légitimement inoccupés.

## B. Inférences IA

| Nœud | API et routage | Preuve / limite |
|---|---|---|
| Mac | Ollama11434 ;conversationQwen27 dansHybridRouter | Réponse directe et viaJL03 reçues ;cheminAPI non restreint503 |
| Dell1 principal | Ollama11434, GPU0 uniquement, contexte par défaut4096 | API/catalogue réels ;catalogue partagé avec11435, ordonnanceur indépendant |
| Dell1 missions | Ollama11435, GPU0+1, défautservice8192 mais requêtes80B32768 | Qwen Code80B neuf exécuté ;Mission Engine historique reçu |
| Dell2 | Pas d'Ollama actif/installation standard trouvée ;pas de port11434/11435 | Routeur :enabled=false,url=null,textehéritéoffline_pending_enrollment malgréSSHfonctionnel |

Le routeur connaît le nomDell2, mais **pas un nœud d'inférence disponible**. Son étiquette «offline» est obsolète pour l'administration SSH, pas la preuve d'une API IA. Aucun partage d'inférence entreDell1/Dell2 n'est démontré. Les deux cartesDell2 restent autour de1Mio occupé lors de l'audit. Les calculsCUDA14B et les testsPython26 prouvent des calculs/commandes, pas unLLM chargé.

Le repli28A versMac a été testé historiquement avec panneTCP injectée dans une copie de configuration ;il n'est pas une garantie générale en charge ni un repli reçu versDell2. L'audit ne coupe aucun serveur et ne refait pas ce test acquis.

## Interaction des ordonnanceurs

HybridRouter possède une filecompute_jobs canonique avec priorités et bail parnœud. Les appelsWebUI etQwen Code sont **directs versOllama**, sanspasser par cette file. Ils partagent éventuellement la file interneOllama mais pas les règles d'admission/priorité/checkpoint deJARVIS. DeuxOllama surDell1 peuvent aussi charger deux runners indépendants sur une VRAM commune. Ceci explique le risque de compétition et de rechargements ;aucune nouvelle saturation n'est provoquée pour le tester.

L'exécuteurDell2 est utile pour tests, compilation et vérification croisée. L'installation d'un autre80B ne découle pas de cet audit :3090+3080 n'offrent pas la même capacité mémoire que deux3090, et une copie supplémentaire ne résout pas l'intégration des files. La suite autorisée doit d'abord corriger routage/configuration et réutiliser les exécutants disponibles.
