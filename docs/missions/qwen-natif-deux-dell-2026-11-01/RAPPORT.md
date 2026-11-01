# Qwen natif — réception ciblée sur les deux Dell

Date : 1er novembre 2026, après alignement et raccordement de Dell 2. **✅ Réception ciblée des quatre parcours natifs.**

## Résultat

| Client | Dell 1 | Dell 2 |
| --- | --- | --- |
| Qwen Code → terminal natif → SSH → lecture réelle des services | ✅ Client terminé code 0, outil sans erreur, deux états actifs | ✅ Client terminé code 0, outil sans erreur, deux états actifs |
| Open WebUI → Open Terminal → SSH → lecture réelle des services | ✅ Code retour 0, deux états actifs | ✅ Code retour 0, deux états actifs |

Chaque session Qwen Code a émis un seul appel opérationnel et terminé avec un code client 0 après restitution du résultat. Les résultats natifs des outils indiquent is_error=false et les deux états actifs ; le code de commande est explicitement conservé dans les journaux Open Terminal pour les essais WebUI. Les deux premiers appels ont réellement traité **12 628 tokens d’entrée** ; les suivants **12 862**. Les demandes de sortie étaient bornées à 4 000 puis 4 096 tokens. Cela distingue cette réception de l’essai antérieur dont l’entrée était réduite autour de 4k.

Les deux tests WebUI ont été réalisés dans des chats navigateur isolés, puis leurs messages sauvegardés ont été relus. Un seul processus Open Terminal par Dell : état terminé, code retour 0, sortie réelle « active » puis « active ». Les journaux de commande ont été relus indépendamment ; leurs empreintes figurent dans les [preuves expurgées](PREUVES-EXPURGEES.json).

## Configuration reçue

- Profil modèle Dell 2 à **32 768 tokens**, avec sortie bornée à 4 096 ; poids déjà présents réutilisés, aucun téléchargement.
- Dell 2 ajouté comme choix distinct dans les fournisseurs natifs de Qwen Code et dans les modèles WebUI du Mac mini ; les outils restent ceux du socle existant.
- Dell 1 conserve le choix par défaut. Les deux profils WebUI préexistants ont été relus et sont inchangés ; un nouveau profil séparé a été ajouté pour Dell 2.
- Le lanceur Qwen Code ne force plus une seconde option de modèle : le choix explicite fonctionne tout en conservant le modèle par défaut des réglages.
- Les deux moteurs ont été observés chargés avec un contexte de 32 768 pendant la réception.

Le client et les outils peuvent rester sur le Mac mini, tandis que le modèle s’exécute sur le Dell choisi. Cette réception ne nécessite pas d’installer un deuxième agent sur chaque Dell.

## Diagnostic antérieur et portée des corrections

Avant alignement, le parcours natif standard visait Dell 1 seulement. Dell 2 ne possédait pas le profil de contexte équivalent ; une session native observée demandait une sortie de 32 000 avec un contexte serveur chargé à 8k, ne traitait qu’environ 4 098 tokens d’entrée et terminait sans outil. Le présent test natif sur Dell 2 traite plus de 12k tokens et exécute la commande attendue : la réserve de contexte/raccordement est levée pour ce scénario.

Un essai antérieur en langage naturel avait choisi un projet inexistant. Ce choix n’établit aucun lien causal avec les travaux de monitoring GPU du propriétaire. Les essais reçus ici sont ciblés et ne déclarent pas résolue la sélection autonome de tous les outils.

## Préservation

**Aucune configuration, fonction ou service de monitoring GPU n’a été modifié.** Aucun service redémarré. Aucun téléchargement de poids, aucune modification des accès, aucune création ou reprise de mission historique. Les sessions de test produisent leurs journaux habituels et chargent temporairement les modèles.

L’archivage de ce rapport est une opération documentaire uniquement : aucune commande sur les serveurs ni aucun nouveau test n’est déclenché par sa publication.

## Limites maintenues

- Commandes de lecture précisément demandées : pas de réception d’autonomie générale ni de clôture de 14/14A.
- Contexte configuré à 32k et entrée réellement supérieure à 12k : pas un test avec 32 768 tokens d’entrée.
- Les connecteurs et Skills métier, la charge concurrente, le repli et les scénarios longs restent des réceptions distinctes.
- Aucune réception après redémarrage : les réglages ont été enregistrés et relus par les interfaces natives, sans provoquer de reboot.
- Les preuves détaillées et sauvegardes restent privées. La version publique ne contient ni adresses, ni clés, ni jetons, ni comptes, ni chemins privés, ni URLs de chats, ni commandes d’accès.

## Historique et attribution

Ce complément succède à la [réception de présence et d’inférence Dell 2](../dell2-qwen80b-2026-11-01/RAPPORT.md) et à la PR #44. Les anciennes preuves restent datées et inchangées. Les notes ajoutées aux rapports concernés renvoient à cette réception sans leur attribuer rétroactivement les nouveaux tests.

Configuration et contrôle indépendant : Codex. Dans chaque essai, Qwen a sélectionné l’appel natif demandé, reçu les résultats réels et rédigé sa réponse finale. Les outils et transports ont exécuté les commandes ; un état affiché seul n’est pas la preuve retenue.

Directives consultées : AGENTS.md, charte JARVIS, suivi/roadmap, contrôle de publication et derniers rapports de réception/raccordement. Autorisations préservées : archivage et mise à jour des rapports expressément demandés, republication des rapports publics existants avec compléments datés autorisée ; exclusion des secrets et du monitoring GPU. Aucun changement des directives ni fusion automatique.
