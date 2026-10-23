# Décision propriétaire — réception fonctionnelle du raccordement GPU

**Date : 23 octobre 2026. Décision explicite du propriétaire.**

> « Réceptionne la mission en levant les réserves sur l'alimentation et les brochages. Si la deuxième carte fonctionne, c'est que les câbles et brochages sont bons. »

## Portée de la décision et preuves déjà reçues

**✅ Le propriétaire reçoit l'installation et le raccordement GPU comme fonctionnels dans la configuration matérielle réellement montée et éprouvée.** Aucun nouveau contrôle de brochage ou de référence de faisceau n'est demandé comme condition générale pour poursuivre les opérations du laboratoire.

Preuves disponibles à la réception initiale : deux RTX3090 Dell OEM distinctes visibles par PCI/NVIDIA avec pilote actif, 24576MiB chacune ; JARVIS a exécuté un petit calcul CUDA donnant la sortie attendue sur **chaque** carte. Aucune erreur Xid/AER n'a été observée dans l'extrait de journal consulté. Voir [TESTS-DEUX-GPU.md](TESTS-DEUX-GPU.md) et [RAPPORT-FINAL.md](RAPPORT-FINAL.md). La validité de ces petits calculs n'est pas remise en question.

**La réserve « absence de démonstration du bon raccordement fonctionnel du second GPU » est donc levée par décision du propriétaire et par les essais réels.** Les identifiants complets des faisceaux, la correspondance de chacune des broches, le courant admissible par ligne et la puissance disponible à pleine charge n'ont en revanche pas été mesurés ni démontrés ; ils demeurent des caractéristiques **non documentées**, sans annuler la réception fonctionnelle décidée par le propriétaire.

Les deux RTX3090 annoncent chacune350W ; l'étude historique cite une enveloppe graphique Dell5820 de600W et une alimentation déclarée950W. Cette observation de dimensionnement reste techniquement pertinente : **fonctionner sous une petite charge CUDA ne démontre pas une tenue électrique/thermique en charge prolongée**. Ne pas décrire les 700W comme déjà testés, ni publier un tableau de brochage inventé.

## Statut et suite opérationnelle

- **✅ GO — reconnaissance, initialisation et calcul CUDA sur chacun des deux GPU**, câblage et alimentation *fonctionnels pour la configuration testée* ; réserves de simple absence de certification de brochage levées comme condition bloquante, sur instruction du propriétaire.
- **✅🟡 Mission13 — GO avec réserves de périmètre**, puisque les essais d'inférence sur les deux GPU, la mesure sous charge et le choix définitif de modèle n'ont pas encore été effectués.
- **Travaux à poursuivre sans nouvelle approbation générale :** mesures ciblées de puissance/température en conditions d'usage, limites GPU adaptées si nécessaires, vérification des performances d'inférence, documentation des ressources disponibles pour la mission28. Conserver pilotes et services reçus et ne pas refaire les calculs légers validés sans raison technique.
- Une constatation d'anomalie électrique/thermique réelle doit être traitée comme problème technique observé, non comme une nouvelle campagne de validations humaines.

La réception ne constitue ni une certification électrique générale, ni la preuve d'un brochage universel réutilisable sur un autre Dell/câble, ni la réception des tests d'inférence encore absents.

