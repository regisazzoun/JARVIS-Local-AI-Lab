# Lot 03 — Fiches historiques des missions 04G à 04J

## Fiche 04G : Vérification après branchement du Razer Core
**Titre/Fonction :** Vérification post-branchement  
**Objectif :** Confirmer la détection et l’allocation de la Quadro via le Razer Core.  
**Matériel :** Razer Core (annoncé), NVIDIA Quadro (10de:1eb0).  
**Actions/Résultats :** Branchement annoncé par l’utilisateur. Vue système inaccessible pour observer le Core ou la GPU après branchement. Conclusion D : test non concluant, informations insuffisantes.  
**Réserves :** Aucune preuve de détection système ou d’allocation BAR. Journal noyau restreint/incomplète.  
**Dépendances :** Accès système complet, redémarrage éventuel.  
**Exécutant :** À confirmer (vue système limitée).  
**Chemin :** /home/adminjarvis/JARVIS/rapports/mission04G.md

## Fiche 04H : Validation de la réallocation PCIe
**Titre/Fonction :** Validation réallocation PCIe  
**Objectif :** Vérifier l’attribution des BAR 1 et 3.  
**Matériel :** Razer Core (autorisé), NVIDIA Quadro (81:00.0).  
**Actions/Résultats :** Détection confirmée, bureau réactif maintenu. Conclusion C : réallocation inefficace, BAR 1/3 non attribués, fenêtres insuffisantes.  
**Réserves :** Allocation partielle uniquement. Aucune preuve de réussite fonctionnelle.  
**Dépendances :** Paramètres PCIe (realloc), configuration GRUB future.  
**Exécutant :** À confirmer (contrôles en lecture seule).  
**Chemin :** /home/adminjarvis/JARVIS/rapports/mission04H.md

## Fiche 04I : Entrée réserve PCIe 512M installée
**Titre/Fonction :** Installation entrée de réserve mémoire PCIe  
**Objectif :** Réserver 512Mo pour l’eGPU au démarrage via GRUB.  
**Matériel :** Aucun test physique ; configuration logicielle uniquement.  
**Actions/Résultats :** Entrée `/etc/grub.d/45_jarvis_t2_egpu_reserve_512m` installée et vérifiée syntaxiquement (2026-10-11T21:36). Statut : préparation terminée, utilité non démontrée.  
**Réserves :** Aucune preuve de test au redémarrage ou d’attribution effective. Réservation conditionnelle.  
**Dépendances :** Redémarrage futur, validation par lspci/sysfs après boot.  
**Exécutant :** JARVIS (installation contrôlée autorisée).  
**Chemin :** /home/adminjarvis/JARVIS/rapports/mission04I.md

## Fiche 04J : Vérification avant branchement
**Titre/Fonction :** Audit pré-branchement  
**Objectif :** Valider la faisabilité d’un nouveau branchement après installation de la réserve.  
**Matériel :** Razer Core (déconnecté), Quadro, système avec nouvelle entrée GRUB.  
**Actions/Résultats :** Analyse des fenêtres PCIe accessibles. Conclusion D : données hôte manquantes, réserve inefficace locale, goulets inchangés. Instruction explicite : NE PAS brancher le Razer Core.  
**Réserves :** Validation complète du nouveau démarrage empêchée par isolation. Fenêtres insuffisantes.  
**Dépendances :** Collecte de preuves post-redémarrage, décision utilisateur.  
**Exécutant :** JARVIS (contrôles lecture seule).  
**Chemin :** /home/adminjarvis/JARVIS/rapports/mission04J.md

---
*Note : Ces fiches synthétisent des rapports historiques datés du 11 octobre 2026. Aucun résultat n’est inventé ; les conclusions D et C reflètent les limites documentées à ces dates. L’installation de 04I ne constitue pas un test physique validé.*
