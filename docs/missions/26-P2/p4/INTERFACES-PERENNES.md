# Interfaces corrigées pendant la reprise P4

Codex a corrigé trois obstacles d’interface dans le moteur existant. La mission
`d8fe752876db480cbe5f22cd5525e2dd` et le plan JARVIS version 3 sont conservés.
Ces corrections ne constituent pas la réception globale de P4.

## Identités des opérations

Le moteur attribue les identifiants depuis les appels SQLite effectivement
démarrés. JARVIS conserve le choix du code, des commandes et des exécutants.
La réception 62931 constate l’exécution 62737 puis sa réutilisation 62774,
sans double commande. Voir `IDENTIFIANTS-DURABLES.md`.

## Lecture utilisable malgré la réduction du contexte

La réduction conservait seulement le début des sources : JARVIS ne voyait pas
le corps de `worker.run` et répétait ses lectures. Le commit 5656225 conserve
une page utile issue d’une lecture réussie à la version courante. Les anciens
conseils de sélection manuelle des identifiants quittent la projection active,
mais restent archivés. Les contraintes, contrats et compteurs restent présents.

Préflight 62997 : 25 131 octets pour un budget conservateur de 27 648,
corps de `run` conservé. Ce contrôle de format n’est pas une inférence.
Après installation 62998, JARVIS a réellement lu la source à 63068 puis reconnu
la fonction complète à 63085. Les appels restent limités à la fenêtre de
32 768 tokens, sans augmentation de budget.

## Édition par chemin absolu interne

JARVIS a ensuite tenté une modification réelle à 63157. Le programme d’édition
l’a refusée avant écriture parce que le chemin était absolu, bien qu’intérieur
au projet. Ce résultat est un refus d’exécution, pas un test fonctionnel échoué.

Le commit 8ed99a8 normalise les chemins absolus internes contre la racine réelle
du worker. Les chemins extérieurs, traversées, répertoires réservés et liens
symboliques sortants restent refusés. Le programme historique reste inchangé
en mode legacy. La vérification de l’identité canonique utilise le même programme
normalisé ; aucun assouplissement du contrôle des appels n’est ajouté.

Installation 63326 : trois modules d’infrastructure sur Mac mini et les deux
Dell, sauvegarde privée et redémarrage des seuls workers. Les fichiers applicatifs
du worker candidat n’ont pas été écrits par Codex pendant cette intervention.
136 tests ciblés locaux réussis ; 10 tests d’édition et 14 d’identité réussis
sur chaque Dell. Ces tests logiciels sont attribués à Codex.

Instruction courte 63327 puis reprise native : JARVIS doit encore produire
l’instrumentation du worker, la tester et faire contrôler la même version sur
l’autre Dell. L’installation du candidat dans les services actifs appartient au
paquet suivant, après réception du candidat. Aucun compteur historique n’est remis
à zéro. Aucune réception P4, 14A ou autonomie complète n’est déduite de ces correctifs.

## Retour arrière

Interrompre la mission, vérifier l’absence d’appels démarrés, restaurer les modules
depuis la sauvegarde privée indiquée par `CHEMINS-DEPLOIEMENT.json`, puis recharger
les workers. Conserver les événements, reçus et compteurs ; ne pas rejouer une
opération d’effet inconnu. La sauvegarde antérieure à la lecture est distincte.
Les reçus de déploiement et de tests sont dans les JSON voisins.
