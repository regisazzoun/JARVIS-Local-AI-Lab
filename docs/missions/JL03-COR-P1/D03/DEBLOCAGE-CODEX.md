# D03 — diagnostic et déblocage ciblé Codex

Le moteur a interrompu D03 après trois réécritures non contrôlées du test, dont les appels restent dans le journal canonique. Le dernier test JARVIS avait cinq succès et un échec. L’arrêt conservateur a limité la répétition, mais son motif « sans contrôle » est inexact : un test réellement exécuté et échoué figure entre les écritures. Le garde ne reconnaît actuellement que host_exec avec ok=true comme point de contrôle des réécritures ; il confond donc test échoué et absence de test. Ce défaut distinct est confirmé dans backend/loop_guard.py et reste à corriger ; aucun affaiblissement ni reset des compteurs d’échec n’a été appliqué.

La cause applicative est reproduite : une réponse vide ajoutait un message système dans `else`, puis levait une exception ; `catch` ajoutait une deuxième erreur. Le programme produisait donc trois entrées au lieu de deux (demande et une erreur). Autre défaut : une saisie effacée au départ n’était pas restaurée en cas d’erreur. Les modifications répétées du test ne corrigeaient pas ce chemin de production.

Le test JARVIS recopiait sendPrompt ; une réussite de cette copie aurait pu diverger de l’application. Codex a conservé son original et créé un harnais qui lit la fonction réelle du candidat app.js et l’exécute avec API/DOM de test. Les fixtures sont explicitement déclarées ; ce banc ne démontre aucune inférence ni réception navigateur.

Avant intervention sur la source, ce nouveau banc reproduit deux échecs, quatre succès. Codex corrige le candidat isolé : affichage d’erreur exclusivement dans catch ; restauration de la demande seulement si aucune nouvelle saisie n’est présente. Après : six succès, zéro échec ; huit tests existants de capture restent réussis. Commit candidat `5b459b0` sur `jarvis/jl03-cor-p1-d03`. Aucun déploiement en production ni intégration dans la branche applicative principale de correction.

Les six cas portent sur réponse normale, réponse vide, erreur réseau/authentification, sérialisation de deux demandes, file pleine, transmission du champ vocal et de la sélection de mission. Ils ne couvrent pas encore toute D03. Restent notamment la création de conversation lors de deux premières demandes simultanées, la visibilité immédiate de la file, les vrais appels workers et la vérification du parcours navigateur/API. Ne pas considérer six tests comme la réception de tous ces critères.

Le plan canonique passe en version2, l’historique original reste intact. Une nouvelle stratégie Codex est enregistrée avec ses preuves. Le contexte de travail est repris depuis un paquet court ; le défaut général de contexte volumineux n’est pas déclaré résolu. Aucun compteur de blocage n’est remis à zéro.

La première action demandée à JARVIS est une exécution native du test contrôlé, puis le transfert du ZIP actualisé et les tests sur les deux Dell. Les corrections et affectations suivantes restent à JARVIS. Son rapport doit distinguer son candidat initial et cette intervention Codex.

La reprise est préparée une seule fois sur ce plan et cette stratégie. Le coordinateur existant vérifie les références du plan et de l’événement Codex avant de remettre la même mission en file quand une place se libère ; aucun redémarrage aveugle après un nouvel échec. D04 et D17 occupent actuellement les deux contextes et continuent. L’attente est une limite de concurrence, pas une autorisation utilisateur. Aucune autre architecture, mémoire, modèle, routage ou service JL01/JL02 modifié.

Preuves conservées dans D03/deblocage/ : sorties avant/après, test original, harnais source réelle et patch candidat. Le chemin relatif du harnais publié est documentaire ; sa version exécutable est dans le worktree D03/source/tests et sera transférée par JARVIS aux workers.

## Responsabilités du contrôle

La réutilisation observée est une copie manuelle de sendPrompt dans le test, pas une preuve de cache ni de défaut mémoire. La boucle diagnostic/correction JARVIS a ensuite modifié le test alors que la trace montrait un double ajout applicatif. Le contrat de réception pouvait compter des tests réussis sans imposer leur lien avec le fichier réellement utilisé ; le nouveau harnais élimine cette copie. Enfin le garde Codex a mal qualifié la séquence : écriture, véritable test (5PASS/1FAIL), deux éditions, arrêt au troisième enregistrement d’écriture. Il ne s’agit pas de trois échecs de test successifs sur cette séquence. L’explication précédente présentant simplement trois réécritures « sans contrôle » est rectifiée ici, sans effacer le reçu original.
