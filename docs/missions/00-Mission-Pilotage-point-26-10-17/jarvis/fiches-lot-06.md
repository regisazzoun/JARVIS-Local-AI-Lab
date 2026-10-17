> **Trace de production, avec limites de réception.** Ce fichier conserve une sortie ou un assemblage de la mission 00 ; il ne remplace pas le registre consolidé. Voir les corrections Codex et le bilan agentique dans le dossier parent de mission. Les textes historiques ou propositions du modèle ne créent aucune nouvelle autorisation ou obligation de validation.

# Fiches Historiques Lot 06 — Mission 00

## Fiche 04T : Préparation du diagnostic pré-Linux de DEVEN

**Fonction :** Diagnostic et analyse du registre PCI DEVEN (Intel) avant le démarrage Linux.
**Objectif :** Déterminer la méthode de lecture à l'invite GRUB pour identifier l'état du masque Intel (0x3f vs 0x0f).
**Matériel/Composants :** Mac mini 2018 (Macmini8,1), Debian 13 T2Linux, noyau 6.18.54-1-t2-trixie, GRUB 2.12.
**Actions et résultats :** Préparation documentaire uniquement. Proposition de la méthode `setpci -s 00:00.0 54.L` en invite GRUB pour lecture sans modification. Aucun redémarrage ni expérimentation exécutée. Attente d'autorisation explicite avant toute action.
**Réserves/Preuves manquantes :** Aucune expérience réalisée ; résultats 04S fournis par l'utilisateur mais non vérifiés localement dans ce rapport. Identification exacte des valeurs attendues à confirmer lors du test.
**Dépendances :** Autorisation de redémarrage et d'exécution de commandes GRUB en RAM.
**Exécutant :** À confirmer (rapport préparatoire, aucune exécution matérielle attestée).
**Chemin :** /home/adminjarvis/JARVIS/rapports/mission04T.md

## Fiche 04U : Localisation du masquage Intel entre GRUB et Linux

**Fonction :** Analyse comparative des états DEVEN avant et après le chargement du noyau.
**Objectif :** Identifier l'auteur de la transition `DEVEN 0x3f → 0x0f` (firmware, ACPI, ou noyau).
**Matériel/Composants :** Mac mini 2018, Debian 13 T2Linux, captures dmesg complètes (1 538 lignes).
**Actions et résultats :** Analyse des logs d'amorçage. Transition confirmée entre mesures GRUB et Linux. Intel absent dès le scan initial du bus racine en Linux. Auteur de l'écriture non identifié avec certitude.
**Réserves/Preuves manquantes :** Attribution exacte de l'écriture (firmware vs noyau) non démontrée. Nécessite des mesures supplémentaires et une instrumentation autorisée.
**Dépendances :** Autorisation pour expérimentation de boot et instrumentation.
**Exécutant :** À confirmer (analyse documentaire sur données communiquées, pas d'exécution locale).
**Chemin :** /home/adminjarvis/JARVIS/rapports/mission04U.md

## Fiche 04V : Préparation de la mesure DEVEN en fin de GRUB

**Fonction :** Définition de la méthode expérimentale pour lectures G0 et G1.
**Objectif :** Préparer une procédure distincte mesurant DEVEN avant (`G0`) et après (`G1`) le chargement linux/initrd, avant `boot`.
**Matériel/Composants :** Environnement Mac mini 2018, Debian 13 T2Linux.
**Actions et résultats :** Préparation uniquement. Méthode recommandée : console interactive GRUB avec commande manuelle de `linux`/`initrd`, puis lecture PCI avant `boot`. Aucun redémarrage ni modification effectué.
**Réserves/Preuves manquantes :** Aucune expérience exécutée. Validité de la distinction G0/G1 et impact de la procédure à confirmer lors d'un essai autorisé.
**Dépendances :** Autorisation couvrant redémarrage, commandes GRUB, lectures PCI et collecte Linux.
**Exécutant :** À confirmer (rapport préparatoire).
**Chemin :** /home/adminjarvis/JARVIS/rapports/mission04V.md

## Fiche 04W : Analyse du démarrage interrompu

**Fonction :** Investigation post-mortem d'un essai de démarrage avorté.
**Objectif :** Déterminer si Linux a commencé à exécuter l'essai prévu (04V) et identifier la cause de l'interruption.
**Matériel/Composants :** Mac mini 2018, logs journald conservés.
**Actions et résultats :** Classe F : traces insuffisantes. Aucun boot ID attribuable à l'essai 04V dans les journaux conservés. Dernière étape attestée : G1 dans GRUB avec DEVEN=0x3F. Cause de l'arrêt non élucidée (blocage noyau, initramfs, ou perte journaux).
**Réserves/Preuves manquantes :** Impossibilité de confirmer si le noyau a démarré avant la coupure. Paramètres `pci=hpmmioprefsize` et `pci=hpmmiosize` suspectés mais causalité non prouvée.
**Dépendances :** Nouvelle autorisation explicite, procédure revue, opérateur local, captures horodatées externes.
**Exécutant :** À confirmer (analyse d'incident sans récupération complète de données).
**Chemin :** /home/adminjarvis/JARVIS/rapports/mission04W.md

## Note sur 15A/B (Cahier des charges)

**Fonction :** Suivi des incréments prévus.
**Statut :** Mentionné dans le périmètre d'analyse historique. Les 5 incréments explicitement prévus par le cahier sont notés mais **non exécutés**. Aucun résultat opérationnel pour ces incréments n'est présent dans les rapports du lot 04T-W. À intégrer lors de la prochaine phase d'exécution autorisée.

---
*Rapport généré à partir des données historiques du lot 06. Aucune action matérielle ni service modifié.*
