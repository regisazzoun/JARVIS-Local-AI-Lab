# Mission 04V

- Identifiant : 04V.
- Date ou période : 12 octobre 2026
- Objectif initial : JARVIS — Mission 04V : préparation de la mesure DEVEN en fin de GRUB
- Matériel mentionné : Macmini8,1
- Logiciels mentionnés : Debian / T2Linux / NVIDIA
- État final documentaire : **NON VÉRIFIÉ**. Documents retrouvés ; réception finale non établie dans cette première passe.

## Actions et résultats confirmés

Documents retrouvés ; réception finale non établie dans cette première passe.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Documents retrouvés ; réception finale non établie dans cette première passe.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [mission04V.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04V.md)

## Références et dépendances

Aucune référence explicite extraite.. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [mission04V.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04V.md)

Date : 12 octobre 2026. Machine Macmini8,1, Debian 13 T2Linux. **Préparation uniquement : aucune expérimentation exécutée, aucun redémarrage, aucune modification de configuration ou du matériel. Le seul fichier créé est ce rapport.**

## Faisabilité et méthode retenue

**Oui : le GRUB installé permet de charger le noyau et l’initrd existants, puis de lire DEVEN avant de lancer le noyau. La méthode recommandée est la console interactive, commande par commande.** Après `linux` et `initrd`, elle reste à l’invite aussi longtemps que nécessaire pour photographier G1. Le lancement n’intervient qu’à la saisie volontaire de `boot` suivie d’Entrée. Aucun `sleep` n’est nécessaire pour cette pause.

G0 et G1 sont donc deux lectures dans le même démarrage, encadrant les commandes de chargement. **G1 ne mesure pas la fin des Boot Services ni le dernier instant précédant l’entrée CPU dans Linux** : `boot` exécute encore les hooks, la préparation vidéo et le transfert EFI. Un résultat G1=3f, L=0f laissera ces étapes et Linux précoce à départager.

Il ne faut pas simplement ajouter `sleep --interruptible` après `initrd` dans l’éditeur et supposer qu’Échap annule le démarrage : **une entrée exécutée possède un `boot` implicite à sa fin**. Interrompre la pause peut laisser le script se poursuivre. Cette variante est possible techniquement, mais ne fournit pas le contrôle manuel et la récupération de la console.

