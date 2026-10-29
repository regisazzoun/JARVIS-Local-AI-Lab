# Ordre d’exécution déléguée — 29 octobre 2026

Le propriétaire demande l’exécution de l’enchaînement proposé : JARVIS décide et
répartit les calculs sur les deux Dell ; Codex contrôle indépendamment puis
transmet une épreuve de validation distincte à JARVIS. Une priorité principale
active, sous-tâches indépendantes possibles. Aucun accord humain intermédiaire.

Ordre conservé : correctifs P3 ciblés, intégration/réception P4, correction JL03
encore ouverte choisie sur registre, contrôles Codex, test de validation JARVIS,
réceptionM26. L’épreuve14A reste distincte et conditionnée à ces acquis ; mémoire
24-Old/AutoDream vient ensuite. Ni14A ni mémoire ne sont lancées maintenant.
[Registre](ORDRE-EXECUTION-ET-VALIDATION.json). Pas de nouvelle architecture,
modèle, routage ou installation matérielle ; historique et réserves conservés.

## Capacité d’appel typé apportée par Codex

Après trois refus réels71846 (tableau transmis comme chaîne), mode opt-in
`structured_action_calls` : le modèle choisit un outil et ses paramètres dans
un format JSON contraint aux schémas réellement proposés. Aucun choix de
commande, fichier, correction ou plan n’est fourni par le mécanisme. Le registre,
les permissions, la concurrence et les vérifications restent contrôlés après
sélection. Les arguments incorrects ne sont pas convertis silencieusement.
Trois sorties de format invalides arrêtent avant tout dispatch.

Le transport évite le parseur XML des appels natifs. Son marqueur interne est
retiré avant émission réseau. Le contexte d’une action peut être réduit en
conservant son schéma, l’objectif et les compteurs ; cette permission ne se
propage jamais aux revues structurées, dont les preuves ne sont pas tronquées.

Essai réelQwen80B/Dell1 :71856, JSON valide et outil choisi, **non exécuté** par
cette sonde. Préflight71870 :16677/27648octets, source et compteurs inchangés.
Usage réel71883/71894/71905 : tableaux correctement typés, mais version3 devinée
alors que le plan courant est2. La version est désormais exposée comme jeton
courant exact dans le schéma ; le contrôle natif de concurrence reste présent.
Préflight71918 :15415/27648octets.199tests ciblésPASS, pas preuve d’autonomie.

Ces correctifs sont Codex. Le code fonctionnel du complémentP3 sera confié à
JARVIS sur copies isolées des deux Dell, puis contrôlé par Codex avant installation.
Les dix casP2, la réceptionP3 et le candidatP4 déjà reçus ne sont pas rejoués.

## Complément P3 réellement transmis

Mission native `bfd9a813c1804ffcaad77c9f01d54045` : JARVIS doit implémenter
le contrôle de couverture résilient aux revues trop volumineuses, avec tests
sur les deux Dell. Le paquet contient l’objectif et les contraintes, pas un
algorithme rédigé par Codex. Les exports comprennent105fichiers Python sources/tests,
une identité de test et un manifeste (107fichiers suivis). L’archive d’entrée est
vérifiée par empreinte sur chaque Dell ; [transferts](p3/ENTREES-CONTROLE-BORNE.json)
et [objectif transmis](p3/LANCEMENT-CONTROLES-BORNES.json).

Les trois inspections demandées ont rencontré un refus **avant exécution** :
le contrôle préalable sérialisait le manifeste complet dans stdout, plafonné
à16000octets. Codex a étendu le transport existant des reçus complets avec SHA
aux observations de manifeste préalables, aux contrôles de fraîcheur et aux
synchronisations. Aucun fichier n’est écarté du contrôle pour réduire la sortie.
Une observation instable, incomplète ou tronquée est refusée.

Installation71979 ; contrôles réels71998 :107fichiers identiques sur les deux Dell,
reçus complets26567octets. [Preuves](p3/TRANSPORT-MANIFESTES.json).
163tests logiciels ciblés passent (105contrats/transport/contexte et58interfaces/
intégration historique), dont un véritable processus local produisant un manifeste
supérieur à16Ko. Ils contrôlent l’infrastructure, pas l’autonomie de JARVIS.
Résolution71999, même mission remise en file ; compteurs et incidents conservés.
Retour arrière : restaurer les deux modules sauvegardés dans le stockage privé,
puis redémarrer les seuls workers en l’absence d’action active. Conversation et
interface n’ont pas été remplacées.

L’implémentation P3, sa réception indépendante, l’intégration P4 et l’épreuve
finale distincte restent à exécuter. Le test `M26-P2-VF01` demeure **NON TRANSMIS**
jusqu’aux contrôles Codex. Aucun statut global n’est promu par cette réparation.

## Contrat explicite des actions exécutables

Après reprise, JARVIS a exécuté ses inspections72029/72063 sur Dell1.
Deux lectures suivantes72111/72168 ont réellement échoué sur des chemins
inexistants ; ces résultats sont conservés et distincts des tests fonctionnels.
Codex a précisé la localisation observée de la fonction `audit_plan` et rappelé
le contrat des lots de réception, sans écrire son algorithme ni réviser son plan.

Trois propositions sans `executor`/`command` ont été refusées avant dispatch72198.
Les obligations conditionnelles du schéma étaient contrôlées par le backend,
mais non respectées dans les sorties observées du générateur. Codex a compilé
le sous-ensemble connu des discriminants finis en variantes explicites, avec
les mêmes champs obligatoires et les mêmes types. Les définitions sont partagées
pour limiter la taille ; les formes conditionnelles inconnues sont conservées,
aucune obligation supprimée.72tests ciblésPASS, dont comparaison d’acceptation
entre schéma original et variantes pour les modes et paramètres incomplets.

Sonde réelleQwen72204 : action conforme **non exécutée** ; les références et
identifiants inventés dans son texte ne sont pas des preuves. Préflight de la
requête suivante72211 :26713/27648octets. Résolution72212 puis remise en file de
la même mission, historique et compteurs intacts. [Reçus](p3/CONTRAT-EXECUTION-EXPLICITE.json).
L’implémentation P3 demandée à JARVIS demeure non reçue à ce stade.
