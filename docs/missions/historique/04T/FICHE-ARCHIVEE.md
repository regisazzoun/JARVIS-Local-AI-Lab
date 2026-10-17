> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-04t/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 04T

- Identifiant : 04T.
- Date ou période : 12 octobre 2026
- Objectif initial : JARVIS — Mission 04T : préparation du diagnostic pré-Linux de DEVEN
- Matériel mentionné : Mac mini / Macmini8,1
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

- mission04T.md (référence locale historique non publiée)

## Références et dépendances

Aucune référence explicite extraite.. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### mission04T.md (référence locale historique non publiée)

Date : 12 octobre 2026. Machine : Mac mini 2018 / Macmini8,1, Debian 13 T2Linux, noyau `6.18.54-1-t2-trixie`.

**Statut : préparation uniquement. Aucune expérimentation autorisée ou effectuée. Attente explicite d’une autorisation avant tout redémarrage, changement de branchement ou commande pré-Linux.**

## Décision recommandée

La première méthode à autoriser est une lecture à l’invite du **GRUB existant**, avant de choisir l’entrée Linux, avec `setpci -s 00:00.0 54.L`, répétée et photographiée. Elle ne nécessite ni installation, ni modification GRUB, ni écriture de configuration PCI, ni sauvegarde sur l’EFI. Les modules nécessaires sont présents sur disque ; leur chargement par le GRUB effectivement démarré reste à vérifier lors d’un essai autorisé.

Cette mesure répond à « DEVEN est-il déjà masqué avant Linux ? ». Elle ne suffit pas à répondre à « Apple ou GRUB a-t-il effectué le masquage ? », car le firmware et une partie de GRUB ont déjà fonctionné à l’apparition du menu. Une UEFI Shell démarrée directement constituerait une seconde expérience, avec un chemin de démarrage différent et une compatibilité Mac T2 non démontrée ici.

