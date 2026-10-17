> **Trace de production, avec limites de réception.** Ce fichier conserve une sortie ou un assemblage de la mission 00 ; il ne remplace pas le registre consolidé. Voir les corrections Codex et le bilan agentique dans le dossier parent de mission. Les textes historiques ou propositions du modèle ne créent aucune nouvelle autorisation ou obligation de validation.

# Lot 07 — Fiches de missions NVIDIA (Mission 05)

## Fiche 05A : Sélection du pilote NVIDIA
**Fonction :** Analyse documentaire et sélection.
**Objectif :** Identifier la version de pilote optimale pour Debian 13 et Macmini8,1 sans installation.
**Matériel/Composants :** Macmini8,1, noyau `6.18.54-1-t2-trixie`, dépôt NVIDIA, paquets `.deb` inspectés.
**Actions/Résultats :** Téléchargement des métadonnées et inspection de 4 paquets (SHA-256 concordants). Recommandation du candidat **NVIDIA 595.91.07-1** avec modules ouverts (`nvidia-kernel-open-dkms`). Aucun paquet installé, aucun changement système.
**Réserves :** Validation cryptographique de l’index non réalisée. Compatibilité attendue, non compilée.
**Dépendances :** Aucune installation requise avant 05B-P.
**Exécutant :** JARVIS (Mission documentaire).
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission05A.md`.

## Fiche 05B-P : Préparation sécurisée
**Fonction :** Audit de préparation et validation des prérequis.
**Objectif :** Vérifier la faisabilité technique avant installation, sans action sur le système.
**Matériel/Composants :** Macmini8,1, configuration APT, sauvegardes logiques.
**Actions/Résultats :** Analyse des politiques de sécurité et des scripts maintscript (trigger initramfs différé). **GO conditionnel** émis sous réserve d'autorisation explicite et de sauvegarde vérifiée. Aucune installation ni modification GRUB/EFI exécutée.
**Réserves :** Génération réelle d’initramfs non déclenchée dans cette phase. Risque résiduel à confirmer en 05B.
**Dépendances :** Requiert autorisation utilisateur avant passage à 05B.
**Exécutant :** JARVIS (Préparation).
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission05B-P.md`.

## Fiche 05B : Installation contrôlée NVIDIA
**Fonction :** Installation du pilote et des composants de calcul.
**Objectif :** Installer la stack NVIDIA sans branchement du GPU externe (Core absent).
**Matériel/Composants :** Macmini8,1, noyau `6.18.54-1-t2-trixie`, paquets `nvidia-driver-595` (modules ouverts DKMS).
**Actions/Résultats :** Installation réussie via APT (retour 0), 29 ajouts de paquets. DKMS compilé avec succès pour le noyau actuel, mais émet **14 060 avertissements objtool** par build. Affichage Intel et SSH préservés.
**Réserves :** **NO-GO immédiat** pour brancher le Razer Core. Avertissements objtool à qualifier avant essai physique. Sécurité complète non affirmée.
**Dépendances :** Requiert qualification des avertissements (Mission 05B-A) et autorisation distincte pour la mission 05C.
**Exécutant :** JARVIS (Installation), autorisé par l'utilisateur.
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission05B.md`.

## Fiche 05B-A : Audit des avertissements objtool
**Fonction :** Analyse diagnostique des logs de compilation.
**Objectif :** Déterminer si les avertissements DKMS bloquent l'usage ou nécessitent une correction critique.
**Matériel/Composants :** Logs de build DKMS, fichiers `.ko` générés (`nvidia.ko.xz`).
**Actions/Résultats :** Examen des 14 060 lignes d'avertissement. Aucun motif de blocage opérationnel concret identifié dans l'analyse statique. **GO sous conditions** émis pour un premier branchement à chaud surveillé en Mission 05C.
**Réserves :** Risque résiduel de blocage système accepté explicitement. Non équivalent à une validation de production ou CUDA. Signature DKMS attestée mais non vérifiée cryptographiquement par le chargeur dans ce rapport.
**Dépendances :** Requiert autorisation distincte pour Mission 05C (branchement physique). Présence d'un opérateur local et SSH indépendant requis.
**Exécutant :** JARVIS (Audit lecture seule).
**Chemin :** `/home/adminjarvis/JARVIS/rapports/mission05B-A.md`.

---
*État des données : Rapports datés du 12 octobre 2026. Aucune validation en temps réel. Les conclusions historiques ne valent pas surveillance active.*