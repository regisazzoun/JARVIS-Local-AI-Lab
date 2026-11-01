# WebUI — quatre raccordements d’autonomie

Demande propriétaire : « corrige ces 4 points alors ». Extension ciblée de PR39 ; aucune fusion dans main. Les autorisations déjà accordées restent applicables. M26-P4 et MANUAL-HOLD sont préservés.

## Avant / après

| Point | Avant observé | Correction installée |
|---|---|---|
| Contexte opérationnel | Profil80B : quatre phrases génériques ; environnement Debian et droits non présentés automatiquement. | Filtre natif sur les deux profils existants, réservé au propriétaire administrateur : identité canonique, politique actuelle du broker, catalogue exposé et cibles. |
| Mémoire | WebUI passait par le garde d’inférence sans la récupération utilisée par Core ; aucun appel client `active_memories` observé. | Même fonction de récupération pour Core/WebUI/missions ; préférences et souvenirs approuvés pertinents, périmètres et expiration conservés. Pas de seconde mémoire. Contexte retenu après compaction. |
| Passage à l’action | La demande naturelle de scanner le réseau recevait des instructions à exécuter soi-même, sans appel d’outil. | Classificateur existant étendu aux formulations d’action naturelles ; création d’une mission canonique sans tâches prédéfinies, clé stable propriétaire/chat/message. Une question et une citation ne créent pas de mission. |
| Véracité et retour | Refus générique sans preuve ; pas de retour automatique durable vers le même message. | Présentation déterministe du véritable reçu, jamais un succès depuis queued/running. Blocages référencés. Boucle de publication existante et API native WebUI mettent à jour le contenu **et** le rendu ; aucun moteur supplémentaire. |

L’accès automatique à la mémoire et au dispatch est limité à l’identité propriétaire vérifiée et aux profils `jarvis-tools-conversation` et `jarvis-qwen-code-lab`. Les souvenirs et documents sont des données, jamais une source de nouveaux droits. Les permissions réelles restent celles du broker, rechargées à chaque demande. La requête initiale est conservée intégralement. Le tour d’interface qui présente le reçu ne déclenche pas en parallèle une seconde exécution par ses outils.

Le routage s’appuie sur le classificateur existant : les formulations usuelles testées sont prises en charge, pas une reconnaissance universelle de toutes les intentions possibles. Les modèles, routes, fenêtres et quotas sont conservés. Les outils de contrôle internes au moteur ne sont pas exposés aveuglément aux clients.

## Essai navigateur de la demande propriétaire

Phrase exacte soumise dans un nouveau chat80B : « Je veux que tu scannes le réseau et que tu me dise quelles sont les machines et quelles sont leurs utilités dessus, s’il te plaît. »

Création automatique unique : `30dde783a2ff4b6c80914c89f9f4302f`, événement95262. Aucun nom d’outil, CIDR, plan ou tâche fourni dans cette requête. Le paquet nmap, absent de la politique initiale, a été ajouté seul à la liste autorisée et installé par le broker existant ; reçu client420. Installation attribuée à Codex, pas au modèle.

Premier plan insuffisant refusé95318 ; JARVIS ajoute lui-même l’étape de scan, couverturePASS95344. Ce contrôle n’est pas une preuve de scan. Trois sorties host_exec incompatibles interrompent l’essai95390–95391 ; aucun outil exécuté pour ces sélections refusées. Les sorties et compteurs restent conservés.

Cause traitée : les paramètres étaient contraints dans le format transmis mais insuffisamment visibles au modèle, particulièrement après compaction. Le schéma exact est désormais présenté dans le contexte des nouvelles missions WebUI, y compris le checkpoint réduit. Aucune transformation conjecturale des arguments refusés. Sonde réelle Qwen95397 : sélection conforme `nmap --version`, sans exécution de commande pendant la sonde. Rebase natif puis reprise de la même mission avec nouvel epoch lié à cette preuve ; anciens trois refus conservés.

Le contrôle navigateur indépendant a également révélé que l’API native de modification du contenu laissait l’ancien champ `output` visible. Correction via mise à jour native du seul message dans l’historique fusionné et événement de complétion ; aucune modification du code tiers WebUI. État réellement interrompu reçu après rechargement du navigateur, puis reprise.

## Incidents supplémentaires reçus et traités

La première présentation du contrat dupliquait aussi le catalogue au tour de sélection : dépassement avant inférence, trois incidents de capacité conservés. Correction limitée au tour de paramètres de l’outil choisi. Rejeu du paquet réellement refusé :23246octets sur27648, sans suppression des exigences ni augmentation de fenêtre. Résolution native95438, compteurs historiques3/3résolus conservés.

La première observation host_exec réussie95472 révélait un verrou du cycle existant : contrat de rapport final exigé avant toute opération suivante, rapport pas encore écrit. Arrêt explicite de cette stratégie répétée. Correction **uniquement** pour nouvelles missionsWebUI marquées client_autonomy et tâches dont tous les critères sont la lecture du rapport déclaré : les processus réellement terminés avec code0 restent VALIDATION_INCONCLUSIVE jusqu’à la validation du rapport, mais ne bloquent plus une opération distincte nécessaire à sa production. Même opération = reçu original, aucun nouvel effet. Tout résultat inconnu ou processus encore actif reste bloquant ; les autres missions conservent le verrou initial. Un verdict de rapport commun n’est compté qu’une fois, pas une fois par opération. Tests dédiés et journal existant reçus ; aucun PASS fonctionnel déduit du seul code0.

Le compacteur omettait aussi stdout des reçus host_exec non imbriqués, tout en gardant leur code retour. Correction limitée aux missionsWebUI : sortie réelle, commande choisie, preuve broker, référence complète et indication d’extrait. Mesure du paquet réel corrigé :25769/27648octets ; pas de fenêtre augmentée. Les autres missions gardent leur projection existante.

Un refus d’installation du paquet facultatif arp-scan95680 était traité comme effet inconnu malgré le refus explicite de politique avant exécution. La classification de ce seul refus attesté est maintenant NOT_EXECUTED ; toutes les autres exceptions inconnues restent bloquantes. Aucun droit arp-scan ajouté, aucune installation de ce paquet. Clarification native de l’ancienne tentative et reçus historiques conservés. Le compteur d’interfacehost_exec:P2 atteint quatre entrées agrégées : les trois anciennes concernaient le verrou du rapport, la suivante l’installation refusée sur une tentative différente après changement technique. Cette agrégation et ses sorties originales ne sont ni effacées ni présentées comme trois tentatives. Nouvelle frontière liée à la preuve de correction réelle, pas un simple renommage.

Pour ces seules nouvelles tâchesWebUI à rapport absent, sans effet inconnu, la phase présente les outils opérationnels et l’écriture, puis repropose vérification/complétion dès création du fichier. Le modèle ne peut plus demander PASS sur un rapport inexistant ; un résultat inconnu conserve l’accès au vérificateur. Aucune tâche ni commande rédigée par le coordinateur, aucun critère reçu d’avance. Le contexte précise aussi la différence entre système de fichiers confiné host_exec et état des paquets via host_package status.

Un processus terminé en erreur avec code entier et preuve broker liée était aussi classé inconnu. Pour ces tâchesWebUI, il est désormais EXECUTION_FAILED, compteurs et sortie conservés ; les pertes de transport sans reçu restent inconnues et bloquantes. La tentative existante a été clarifiée avec le reçu original, sans remise à zéro.

Le paquet effectivement réduit contenait les anciennes consignes de préparation P4 : « Le présent paquet prépare uniquement : aucun déploiement applicatif » et « Ne clos jamais P4 ». Elles sont conservées pour les anciennes missions, mais remplacées pour les nouvelles missionsWebUI par l’exécution de leur propre objectif dans les droits courants du broker. Le filtre de phase est marqué pour retirer sa consigne précédente lorsque le rapport apparaît ; aucune restriction historique artificielle transportée vers la nouvelle mission.

Une erreur Codex d’import manquant dans le nettoyage de phase a provoqué deux NameError avant inférence et action. Import corrigé, nettoyage directement testé (remplacement, retrait après changement de phase, contraintes restantes conservées). Cycle réel96206 atteint après ce nettoyage ; résolution native96218. Deux incidents originaux conservés, résolus2/2, aucune commande attribuée à ces tours échoués.

Autre décalage observé dans le paquet réel : les consignes citaient active_task.contract, mais la projection réduite ne présentait que task_contract. Pour les nouvelles missionsWebUI, active_task est maintenant reconstruit depuis les champs canoniques, sans nouvelle valeur inventée. Les processus réellement terminés en code0 sont explicitement identifiés comme attendant le rapport, sans PASS fonctionnel ; les effets inconnus gardent leur statut. Régression de structure ajoutée et paquet réel remesuré avant reprise.

La sonde historique continuant les lectures, Codex utilise ponctuellement le réglage existant execution_tool_focus pour **step-01 seulement** : mission_report_facts, host_write_file, mission_note, mission_block. Les opérations de step-02 restent proposées normalement. C’est une assistance opérateur explicite, pas une décision autonome attribuée au modèle ; aucun texte de rapport ni tâche rédigé à sa place. JARVIS écrit son premier rapport6347octets, reçu96438 ; ce seul fichier ne reçoit pas l’objectif de scan. Une confusion d’hôte est relevée indépendamment (Dell d’inférence vs Mac mini exécutant), rapport non reçu en l’état ; le contexte commun est corrigé pour séparer hôte de commande, hôte d’inférence et identité de mission, sans déduire une identité depuis un nom de répertoire historique.

Clarification du contrat existant : les citations techniques doivent être dans chaque phrase/ligne contrôlée, les références d’une autre section n’étant pas automatiquement transportées par le contrôle atomique. Aucun algorithme de vérification modifié ni PASS forcé. Le rapport96631 reste FAIL ; les trois incidents d’interface de la tâche sont résolus nativement96714 après contexte corrigé et mesure24989/27648, totaux et états historiques conservés.

## Raccordement natif et restitution des résultats

Le navigateur a montré un autre écart réel : les noms du catalogue sont des opérations broker, pas des fonctions natives WebUI. Le catalogue, le schéma et le contexte présentent maintenant explicitement `jarvis_schema` puis `jarvis_call`. Aucun nouvel outil métier n’est développé. La fonction native `jarvis_call` reçoit désormais un objet structuré `arguments`, plutôt qu’un objet JSON doublement encodé dans une chaîne. L’ancienne forme objet encodé reste acceptée pour compatibilité ; une chaîne de commande seule est refusée avant dispatch. Les essais mal formés restent archivés : quarante appels/recherches dans le chat76f968eb…, interrompus par Codex, aucune commande exécutée pour ces refus. Ce cas n’est pas une réception autonome.

Les réponses modèle n’embarquent plus les diagnostics dupliqués ; les grandes sorties sont explicitement marquées comme extraits avec empreinte et référence du reçu intégral paginé. Le résultat exact demeure dans le journal canonique. L’interface reçoit le corps complet des rapports de tâches seulement si chemin et SHA correspondent au rapport validé, avant le wrapper final de mission. Test de lecture seule sur une ancienne mission terminée :11442caractères rendus, un corps de tâche reçu, aucun nouveau PASS ni changement de mission.

Une demande naturelle distincte a réellement exécuté la découverte réseau depuis WebUI : douze machines observées, reçus434/436/438/440/442/444/446 reliés aux arguments UI par leurs signatures. Les rôles déduits de noms/services restent des hypothèses ; un SSH brut sans clé a échoué, distinct des accès SSH structurés déjà reçus dans PR39. La table a été affichée sur une relance explicite « montre les résultats déjà obtenus » : réception assistée, réponse1724caractères SHAa390a78da92199548e5d122edb6f38d30dd1ae62068295a99eec1454e774d7c5. Aucune identité privée des machines n’est publiée.

Les essais en un seul tour ont révélé l’accumulation de contexte avant restitution. Le relais existant conserve désormais l’intégralité des messages et résultats et peut retirer uniquement les définitions d’outils pour une phase finale de restitution, si le paquet tient dans27648octets et qu’un vrai reçu canonique OpenWebUI est présent. Aucun objectif/résultat n’est tronqué ; formats structurés exclus ; original archivé privé avec SHA. La réponse est tamponnée : sans texte final ou avec nouvel appel d’outil, refus409 avant toute nouvelle opération. Même ComputeQueue, modèles, fenêtre32768 et sortie4096 ; aucun nouveau moteur ni base. Première sonde refusée correctement car le modèle voulait encore un outil. Consigne de fin de tour corrigée ; rejeu modèle seul du paquet exact :2682caractères, zéro appel d’outil,24891/27648octets. Ce contrôle ne remplace pas une réception navigateur complète.

La sonde durable30dde783… reste interrupted : dernière frontière de capacité97454, neuf incidents historiques dont six résolus, aucun quatrième cycle identique réémis. Rapport révisé5366octets écrit96835 après premier FAIL96631 ; aucun rapport de scan final reçu. Le dépassement77ko brut n’est pas contourné par une augmentation de fenêtre, une suppression de consigne ou un compteur remis à zéro. La campagne générale de qualité des rapports reste hors périmètre.

## Vérifications

176 tests logiciels ciblés PASS : autonomie, catalogue client, intentHTTP, budget/contexte, mémoire canonique, moteur durable, adaptateur asynchrone, transport structuré et reprise worker. Tests du cas exact, questions/citations, propriétaire distinct, scopes mémoire, attente/expiration, idempotence, résultat inconnu sans réémission, échec de livraison sans succès artificiel et conservation du schéma après compaction.

Question navigateur distincte : langue et environnement retrouvés automatiquement depuis préférences/contexte, sans création de mission. Préférences réelles observées : languefr, longueur vocale courte, sources citées, vérification demandée. Le contenu des souvenirs privés n’est pas publié ici.

## Déploiement et retour arrière

Sources installées dans `/opt/jarvis/conversation/jarvis`, adaptateur existant dans `/opt/jarvis/webui-tools`. Filtre natif créé par API puis attaché seulement aux deux profils ; aucune fonction globale activée. Aucun redémarrage de Docker, WebUI, Ollama ou des Dell. Le seul relais client `jarvis-qwen-guard` a également été rechargé pour le raccordement de restitution, sans recharger l’inférence. Rechargements ciblés des services conversation, deux workers et adaptateur, après vérification d’absence de mission active. Sauvegardes privées datées, versions antérieures des modèles et filtre, conservées dans `webui-autonomie-private`.

La synchronisation du module missions conserve également les protections de lease déjà actives sur le runtime avant cette intervention et absentes de la base Git ; ces protections ne sont pas un développement nouveau de cette mission.

Retour arrière : désactiver ce filtre et retirer son ID des deux profils en conservant leurs autres paramètres ; restaurer les seuls fichiers modifiés depuis les sauvegardes ; recharger les services concernés lorsqu’ils sont inactifs. La mémoire et les bases missions ne sont jamais restaurées en arrière ni effacées. Retirer nmap de la politique si cette capacité n’est plus souhaitée ; aucune désinstallation n’est nécessaire pour revenir au comportement de l’interface.

## Réception finale

Réception partielle : mémoire/contexte, création unique de mission et opérations réseau réelles reçus. La restitution navigateur en un seul tour est reçue techniquement, mais son analyse contient une mauvaise attribution matérielle ; la mission durable reste interrompue sur capacité. Aucune autonomie générale fiable déclarée. Les raccordements installés et les tests logiciels ne constituent pas une réception d’autonomie générale ni une preuve que tout objectif futur réussira.


## Dernière réception navigateur indépendante

Chat9e0f32d4-bcde-4c7a-8936-bc2e85b53620 : une seule question naturelle, sans nom d’outil/CIDR/relance. Quatorze reçus538à564 par pas de2, treize succès broker et une expiration de scan exhaustif conservée ; tous les arguments UI correspondent aux signatures canoniques, zéro erreur de fonction native. Le modèle passe après expiration à des ports ciblés ; aucune commande de scan rédigée par Codex dans ce chat.

Réponse2232caractères affichée automatiquement après191secondes, SHAcf2f6afd4826a6667717201ef63dc9d59bc4ab22c6e02a52f6f180bb07c2f7a2. Le relais a effectivement fermé les outils pour la restitution :28114octets entrants,24268 transmis, tous les messages conservés, HTTP200 et aucune opération supplémentaire dans cette phase. Le test modèle seul précédent reste distingué de cette réception UI.

**Réserve fonctionnelle bloquante pour la fiabilité de l’analyse** : le texte assimile à tort un Dell à un Mac mini. Les ports observés et la livraison sont reçus ; cette attribution matérielle et l’analyse globale ne le sont pas. Les résultats bruts privés et la réponse originale sont conservés sans correction silencieuse. Une découverte de ports/noms/fabricants ne prouve pas seule l’utilité ou le matériel d’une machine. Les raccordements corrigés ne permettent pas de déclarer toutes les conclusions Qwen fiables.

La sonde durable reste à son arrêt97454, neuf incidents de capacité dont six résolus. Une mesure supplémentaire sans inférence montre qu’une simple déduplication du contrat ne suffit pas ; cette hypothèse n’est pas déployée et aucun compteur ni état n’est modifié. Pas de nouvelle campagne générale de standardisation ni de quatrième cycle inchangé.
