# Proposition de code dans un contexte isolé

## Motif et périmètre

Malgré les corrections d’interface, Qwen répétait ses lectures et ses notes sans
modifier le candidat. L’escalade64624 est conservée. Codex a donc développé une
stratégie différente : une unité de rédaction sans historique global, utilisant
le **même Qwen80B, le même transport, le même routeur et le même journal SQLite**.
Ce n’est ni un deuxième moteur de missions ni un modèle nouvellement déployé.

Sources34e5c41,37b0cf5,cbd0a70,6bf65e4. La mission et son plan3 restent inchangés.
Les décisions de fichier, objectif, code et Dell exécutant restent celles de
JARVIS. Codex n’écrit pas le raccordement du worker à travers cette interface.

## Deux opérations distinctes

`authority_draft_edit` exige une invocation canonique réellement démarrée pour
la tâche active. JARVIS choisit le Dell, un fichier Python existant, l’objectif
précis et les faits d’API utiles. Le fichier est lu sur le Dell, avec confinement
du chemin et refus des répertoires réservés. L’unité est limitée à6000octets ;
le payload complet respecte aussi le budget propriétaire. Son objectif de
contexte est écrit avant transmission.

Le modèle reçoit seulement cette unité, sans l’historique de mission. Il renvoie
un JSON avec le nouveau contenu et sa justification. La syntaxe Python est
contrôlée et les inférences sont attribuées seulement après observation de
nouvelles métriques confirmant Qwen80B surDell1. La proposition complète est
journalisée ; elle n’est ni appliquée ni testée. Trois tentatives de génération
maximum sur le même fichier inchangé, même après reprise ou reformulation.

`authority_apply_draft` reçoit la référence de cette proposition. Il refuse une
proposition d’une autre mission/tâche, puis appelle l’éditeur canonique avec les
arguments exacts enregistrés, via une invocation imbriquée traçable. L’ancre
ancienne doit toujours correspondre. CompteursP2, garde d’effet inconnu et
contrôles de l’éditeur restent applicables. Une application connue est renvoyée
depuis son reçu, sans seconde écriture. Un refus d’application ne devient pas
un succès outil. Aucun test n’est déduit de l’écriture.

## Paquet de travail et contexte durable

Un mode explicite `authority_code_focus` limite temporairement les outils au
paquet proposition/application. Les outils ordinaires reviennent seulement
après une correction réellement exécutée, rc0 et modification observée. Une
ancienne correction, un test seul, une erreur ou un faux changement ne suffit pas.
Ce mode actuel est une consigne de travail bornée, sans réinitialiser les problèmes.

La référence d’une proposition non appliquée reste dans le contexte réduit :
le modèle n’a pas à recopier le source ni à redécouvrir ses propres décisions.
Le dernier refus outil est conservé séparément des dernières notes/analyse.
`all_satisfied=false` est explicitement un état de réception, pas un test échoué.

## Vérifications et limites

158 tests ciblés locaux réussis, dont11 tests de rédaction/application et35 de
contexte surchaqueDell. Fixtures : source réelle modifiée une fois, ancre périmée
refusée, proposition non appliquée, mauvais acteur d’inférence refusé, portée des
tâches, maximum3générations après réouverture du journal, persistance du refus.
Ce sont des tests logiciels Codex, pas une réception d’autonomie.

Installation initiale64626, objectif de contexte64627, préflight64628 ; reprise
avec conservation du refus et propagation de l’échec64810. Voir les JSON voisins
pour sauvegardes et reçus. Les fichiers applicatifs worker.py/core.py ne sont pas
modifiés par ces installations d’infrastructure.

Première utilisation réelle : JARVIS a appelé le rédacteur, mais64683 a refusé
un source trop grand avant inférence. Ce n’est pas un test applicatif échoué.
ObservationCodex64811 : worker.py1900octets, core.py29731octets. Le modèle doit
choisir une unité admissible. La sélection de fragments de gros fichiers n’est
pas implémentée dans ce helper ; l’éditeur normal garde ses capacités antérieures.

Le raccordement effectif et ses tests restent à vérifier. Une proposition,
une application et une validation indépendante sont trois preuves différentes.
P4, l’autonomie complète et l’attestation du service actif ne sont pas reçues.

Retour arrière : mission interrompue, absence d’appels démarrés vérifiée, restaurer
les modules sauvegardés et recharger les workers. Désactiver seulement le mode
de contexte si nécessaire ; conserver propositions, reçus et compteurs. Ne pas
rejouer un effet incertain. Aucun changement de modèle, routage ou service vocal.
