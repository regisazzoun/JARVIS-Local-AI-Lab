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

## Vérifications

144 tests logiciels ciblés PASS : autonomie, catalogue client, intentHTTP, budget/contexte, mémoire canonique, moteur durable, adaptateur asynchrone, transport structuré et reprise worker. Tests du cas exact, questions/citations, propriétaire distinct, scopes mémoire, attente/expiration, idempotence, résultat inconnu sans réémission, échec de livraison sans succès artificiel et conservation du schéma après compaction.

Question navigateur distincte : langue et environnement retrouvés automatiquement depuis préférences/contexte, sans création de mission. Préférences réelles observées : languefr, longueur vocale courte, sources citées, vérification demandée. Le contenu des souvenirs privés n’est pas publié ici.

## Déploiement et retour arrière

Sources installées dans `/opt/jarvis/conversation/jarvis`, adaptateur existant dans `/opt/jarvis/webui-tools`. Filtre natif créé par API puis attaché seulement aux deux profils ; aucune fonction globale activée. Aucun redémarrage de Docker, WebUI, Ollama ou des Dell. Rechargements ciblés des services conversation, deux workers et adaptateur, après vérification d’absence de mission active. Sauvegardes privées datées, versions antérieures des modèles et filtre, conservées dans `webui-autonomie-private`.

La synchronisation du module missions conserve également les protections de lease déjà actives sur le runtime avant cette intervention et absentes de la base Git ; ces protections ne sont pas un développement nouveau de cette mission.

Retour arrière : désactiver ce filtre et retirer son ID des deux profils en conservant leurs autres paramètres ; restaurer les seuls fichiers modifiés depuis les sauvegardes ; recharger les services concernés lorsqu’ils sont inactifs. La mémoire et les bases missions ne sont jamais restaurées en arrière ni effacées. Retirer nmap de la politique si cette capacité n’est plus souhaitée ; aucune désinstallation n’est nécessaire pour revenir au comportement de l’interface.

## Réception finale

En cours : attendre les opérations réelles et leur réception indépendante. Les raccordements installés et les tests logiciels ne constituent pas une réception d’autonomie générale ni une preuve que tout objectif futur réussira.
