# Mission 01

- Identifiant : 01.
- Date ou période : 11 octobre 2026
- Objectif initial : Mission 01 — Audit de JARVIS
- Matériel mentionné : Mac mini / Macmini8,1
- Logiciels mentionnés : Debian / T2Linux / NVIDIA / Ollama / Open WebUI
- État final documentaire : **PARTIEL**. Audit matériel en lecture seule ; accès hôte limité par le bac à sable.

## Actions et résultats confirmés

Audit matériel en lecture seule ; accès hôte limité par le bac à sable.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Audit matériel en lecture seule ; accès hôte limité par le bac à sable.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- [rapport_jarvis.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/rapport_jarvis.md)

## Références et dépendances

Aucune référence explicite extraite.. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### [rapport_jarvis.md](../../archives/recuperation-2026-10-14/sources/home/adminjarvis/rapport_jarvis.md)

Date de l’audit : 11 octobre 2026. Machine : `JARVIS-MacMIini`.

## Périmètre et méthode

Audit en lecture seule du matériel, des périphériques, du réseau, du partitionnement, du démarrage EFI/GRUB, du noyau, des firmwares et de Thunderbolt. Vérification de sudo et SSH sans modification de leur configuration.

Aucun paquet installé, aucun service reconfiguré et aucun redémarrage effectué. Ce rapport est enregistré à la demande explicite de l’utilisateur ; sa création constitue la seule écriture effectuée pour cette demande.

Les relevés proviennent d’un environnement d’exécution isolé : restrictions réseau, `NoNewPrivs: 1`, propriétaires remappés et montages en lecture seule. Les refus observés dans cet environnement ne doivent pas être interprétés comme des pannes de l’hôte. Les caractéristiques issues de PCI, sysfs et des fichiers système sont distinguées des vérifications impossibles.

