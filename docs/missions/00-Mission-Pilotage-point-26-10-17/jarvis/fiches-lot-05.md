> **Trace de production, avec limites de réception.** Ce fichier conserve une sortie ou un assemblage de la mission 00 ; il ne remplace pas le registre consolidé. Voir les corrections Codex et le bilan agentique dans le dossier parent de mission. Les textes historiques ou propositions du modèle ne créent aucune nouvelle autorisation ou obligation de validation.

# Fiches Historiques Lot 05 — JARVIS Mission00

## Fiche 04O : Vérification des fenêtres de ressources NP/PREF
**Identifiant :** 04O  
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission04O.md`  
**Fonction :** Audit PCIe en lecture seule.  
**Objectif :** Valider la disponibilité des fenêtres Non-Prefetchable (NP) et Prefetchable (PREF) pour un futur eGPU sans action matérielle.  
**Matériel :** Macmini8,1 (Apple), Noyau T2Linux 6.18.54-1-t2-trixie.  
**Actions & Résultats :** Nouveau boot distinct analysé. Confirmation que NP agrandie (66 Mio) et PREF conservée couvrent les besoins théoriques (NHI + GPU + USB). Aucun pilote NVIDIA, modification GRUB ou branchement effectué.  
**Réserves/Preuves :** A ne vaut pas preuve de fonctionnement GPU ni autorisation de branchement.  
**Dépendances :** Autorisation distincte requise pour essais matériels.  
**Exécutant :** À confirmer (non attesté dans l'extrait).

## Fiche 04P : Attribution PCIe Quadro RTX 5000
**Identifiant :** 04P  
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission04P.md`  
**Fonction :** Validation de l'allocation des ressources.  
**Objectif :** Attribuer les BARs à la Quadro RTX 5000 via Thunderbolt (Core).  
**Matériel :** GPU NVIDIA Quadro RTX 5000 (10de:1eb0), Razer Core.  
**Actions & Résultats :** Attribution PCIe réussie. Identification dynamique confirmée. Réserves hotplug internes partiellement refusées (demande 49 Mio NP > espace disponible). Commandes GPU à 0, aucun pilote graphique lié.  
**Réserves/Preuves :** Fonctionnement avec pilote et stabilité non testés. Statuts GPU à surveiller lors d'une mission distincte.  
**Dépendances :** Accord utilisateur avant nouvelles interventions.  
**Exécutant :** À confirmer.

## Fiche 04Q : Diagnostic écran GRUB et absence DRM
**Identifiant :** 04Q  
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission04Q.md`  
**Fonction :** Diagnostic graphique en lecture seule.  
**Objectif :** Comprendre pourquoi l'écran conserve le fond GRUB sans session GNOME.  
**Matériel :** Hôte JARVIS-MacMIini, SSH actif, Core connecté.  
**Actions & Résultats :** Debian démarrée mais chaîne graphique locale non initiée. GPU Intel 0000:00:02.0 absent de l'énumération PCI. i915 non chargé. Boot sur `fb0 = EFI VGA`. Comparaison automatisée des captures PCI-sysfs effectuée.  
**Réserves/Preuves :** Pas de validation pilote NVIDIA ni demande de correction. Origine du problème en amont de SDDM.  
**Dépendances :** Autorisation pour expériences contrôlées si nécessaire.  
**Exécutant :** À confirmer.

## Fiche 04R : Disparition GPU Intel au pont hôte
**Identifiant :** 04R  
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission04R.md`  
**Fonction :** Analyse de la configuration matérielle ACPI/PCIe.  
**Objectif :** Identifier la cause de l'absence du GPU Intel détectée en 04Q.  
**Matériel :** Macmini8,1, Noyau 6.18.54-1-t2-trixie.  
**Actions & Résultats :** Lecture registre matériel : `DEVEN = 0x0000000f`. Bit 4 (`D2EN`) à zéro, expliquant le masquage PCI. Tables ACPI statiques identiques aux boots antérieurs (04O/04P). Ressources NVIDIA inchangées. Pas de faute IOMMU ou AER.  
**Réserves/Preuves :** Masquage matériel Intel identifié ; origine firmware probable mais non prouvée.  
**Dépendances :** Autorisation distincte pour expériences contrôlées.  
**Exécutant :** À confirmer.

## Note sur les incréments 15A/B (Cahier de charges)
Cinq incréments explicitement prévus sont listés dans le cahier des charges pour les lots 15A et 15B. Ces éléments sont documentés comme prévisions futures ; ils n'ont pas été exécutés dans le périmètre des missions 04O-R analysées ici. Aucune preuve d'exécution ne figure dans ces rapports historiques.
