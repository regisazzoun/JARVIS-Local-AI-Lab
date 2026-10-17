# Fiches historiques — Lot 04

## Fiche 04K : Limitations PCIe Mac mini 2018
**Fonction :** Étude des contraintes d’allocation mémoire PCIe.  
**Objectif :** Diagnostiquer l’incompatibilité entre BAR GPU et fenêtres disponibles.  
**Matériel :** Mac mini 2018, ponts PCIe amont, Razer Core (non branché).  
**Actions/ Résultats :** Analyse statique des registres PCI et apertures ACPI. Détection de fenêtre NP insuffisante (2 Mio) pour BAR0 (16 Mio). Reconstruction PREF confirmée (512 Mio cible), mais routage GPU non établi. **Résultat partiel B**.  
**Réserves/ Preuves manquantes :** `/proc/iomem` masqué ; absence de collecte privilégiée en cours de test. Aucun essai exécuté.  
**Dépendances :** Autorisation utilisateur, accès racine complet.  
**Exécutant :** JARVIS (analyse documentaire).  
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission04K.md`

## Fiche 04L : Préparation réallocation PCIe ciblée
**Fonction :** Installation de script GRUB pour réallocation mémoire.  
**Objectif :** Préparer une entrée de boot avec paramètres `pci=resource_alignment=` et réserves.  
**Matériel :** Système Debian 6.12.111, Mac mini 2018.  
**Actions/ Résultats :** Script `/etc/grub.d/46_jarvis_t2_egpu_reallocation_ciblee` installé (root:root 0755). GRUB régénéré avec entrée `jarvis-t2-egpu-reallocation-ciblee`. Validation syntaxique OK. **Aucun redémarrage ni test matériel effectué.**  
**Réserves/ Preuves manquantes :** Installation seule ne prouve pas le comportement au boot. Empreintes système conservées dans `installation-20261011-221528/`.  
**Dépendances :** Autorisation de redémarrage, configuration GRUB valide.  
**Exécutant :** JARVIS (installation script).  
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission04L.md`

## Fiche 04M : Validation réallocation ciblée
**Fonction :** Test de la configuration installée en 04L.  
**Objectif :** Vérifier l’efficacité de la réallocation au démarrage.  
**Matériel :** Mac mini 2018, Razer Core (déconnecté).  
**Actions/ Résultats :** Boot avec entrée 04L. Reconstruction PREF réelle (1024 Mio amont, 512 Mio cible). **Fenêtre NP cible = 2 Mio**, insuffisante pour BAR0. Diagnostic **incomplet : NON CONCLUANT**. Réseau et affichage fonctionnels, mais routage GPU non prouvé.  
**Réserves/ Preuves manquantes :** `/proc/iomem` indisponible en namespace restreint. SMART NVMe inaccessible (`No such device`). Absence de logs noyau complets sur erreurs PCIe.  
**Dépendances :** Collecte privilégiée post-boot, accès aux registres physiques.  
**Exécutant :** JARVIS (analyse post-boot).  
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission04M.md`

## Fiche 04N : Installation autorisée NP 32M + PREF 512M
**Fonction :** Ajustement paramètres GRUB pour augmenter fenêtre NP.  
**Objectif :** Corriger la demande NP avec `pci=hpmmiosize=32M`.  
**Matériel :** Mac mini 2018, Debian 6.12.111.  
**Actions/ Résultats :** Script `/etc/grub.d/47_jarvis_t2_egpu_np32_pref512` installé. Entrée `jarvis-t2-egpu-np32-pref512` disponible. GRUB généré avec paramètre unique modifié. **Aucun redémarrage exécuté.** Registres finaux des 4 ponts documentés (COMMAND, NP/PREF base/limite).  
**Réserves/ Preuves manquantes :** Candidat non testé physiquement. Impact réel sur fenêtre NP inconnu sans boot.  
**Dépendances :** Autorisation de redémarrage manuel, validation post-boot.  
**Exécutant :** JARVIS (configuration GRUB).  
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission04N.md`

---
**Note générale :** Les fiches reflètent l'état documenté à la date de production des rapports (octobre 2026). Aucun essai physique complet n'est attesté dans ce lot. Les configurations installées restent en attente d'exécution utilisateur.