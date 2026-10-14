# Mission 13F — rapport de réception

14 octobre 2026 — Mac mini 2018, Debian 13 T2Linux. **GO AVEC RÉSERVES.** L'installation est modifiée, installée et testée réellement. La mission 14 n'a pas commencé. Cette réception ne vaut pas autorisation ni preuve de capacité à installer aujourd'hui le Dell.

## État initial vérifié

Lecture de ROADMAP.md sur GitHub et des rapports locaux 13A, 13B, 13C, 13E, incidents et tests. Pas de checkout Git local : workflow par connecteur GitHub et PR. Aucune instruction AGENTS.md trouvée localement ou à la racine GitHub.

| Composant | État avant intervention |
|---|---|
| Passerelle `/opt/jarvis/conversation`, service activé | Opérationnelle, échanges vocaux récents dans les journaux |
| Ollama, trois modèles, RTX 3090 | API opérationnelle, GPU disponible ; inférences réelles retestées |
| Open WebUI | Unité active ; santé HTTP retestée via l'adresse configurée existante |
| Whisper Small/Piper Tom CPU | Installés ; appels réels retestés, pas réinstallés |
| SQLite/FTS5 v2 | Intégrité OK, 2 conversations, 14 messages, 1 souvenir |
| Mémoire automatique, réponse orale séparée, VAD client | Manquantes |
| Correction agentique et terminal isolé | Manquants ; registre initial limité aux lectures et propositions |

La parole humaine de 13E est signalée comme confirmée par l'utilisateur. Aucun nouveau test acoustique humain n'est déduit de cette information.

## Changements réellement réalisés

AudioWorklet capture le microphone ; détection légère par énergie, pré-enregistrement et arrêt sur silence, échanges successifs, reprise et interruption vocale optionnelle. Push-to-Talk et arrêt manuel restent disponibles. Le VAD Whisper existant filtre ensuite les segments côté CPU.

Réponse écrite complète et `spoken_answer` distinct ; nettoyage des tableaux, commandes, chemins et URL, résumé supplémentaire si nécessaire. Longueurs courte/normale/détaillée, réglage UI et préférence persistante. Une demande de davantage de détails augmente la réponse orale pour ce seul tour.

SQLite v3 : préférences reliées aux souvenirs canoniques et historique de changements, transactions atomiques, dédoublonnage, remplacement, suppression et index cohérents. Catalogue automatique non sensible : langue, présentation, longueur vocale, tutoiement/vouvoiement, unités métriques, citation des sources et vérification des résultats. Autres souvenirs : proposition à valider ; aucun droit administratif automatique. Profil final : français, voix courte, sources citées et résultats vérifiés.

Registre étendu : inventaire matériel, services, journaux propres bornés, configurations publiques sélectionnées, recherche Internet, lecture de documents, terminal laboratoire et rapport. Identité v2 et boucle d'intervention jusqu'au rapport, conservation de l'objectif lors de la réduction du contexte, adaptation des appels textuels Ministral. Les rapports exigeant une recherche sont refusés tant que deux documents distincts n'ont pas réellement été lus.

Laboratoire Bubblewrap : `/usr` en lecture seule, seul `/work` dédié modifiable, pas de réseau hôte ni fichiers personnels, pas de sudo. Limites : 25 s par commande, CPU/ mémoire virtuelle/fichiers ouverts, surveillance de l'espace de travail 128 Mio/4096 fichiers ; unité passerelle limitée à 2 Gio et 128 tâches. AF_NETLINK ajouté pour initialiser la boucle réseau isolée. Aucune permission Dell activée.

## Résultats et mesures

27 tests backend passent ; 8 validations API réelles, 8 contrôles navigateur et 6 contrôles finaux passent. Le contrôle navigateur de silence est simulé ; les microphones sont artificiels et le mobile est une émulation de viewport.

Qwen a réellement réparé des services HTTP isolés, exécuté et corrigé une sauvegarde échouée, vérifié `HEALTH_OK`/HTTP 200 et enregistré les rapports. Essai final avec recherche, quatre consultations de deux documents distincts et correction : 125.51 s, 17 appels choisis par le modèle. Les scripts service/check sont identiques avant et après. Codex a créé les défauts et la passerelle ; il n'a pas exécuté les correctifs à la place de Qwen.

STT 4.07 s ; génération 1.95 s ; Piper 2.16 s ; total 8.17 s, audio 3.36 s. Rapport écrit 4239 caractères, synthèse orale 259 caractères ; résumé LLM 2.95 s. Ces essais ne sont pas un SLA ni un benchmark comparatif strict avec 13E.

90 relevés durant une intervention : GPU jusqu'à 17493 Mio, 100 % et 72 °C ; CPU hôte moyen 27.1 %, maximum 41.2 %. Mesures système partagées, pas attribution exclusive au modèle.

## Préservation et stabilité

Les 2 conversations, 14 messages et le souvenir initiaux sont identiques à la sauvegarde. Intégrité SQLite, clés étrangères et trois index FTS5 contrôlés. Sauvegarde finale privée et restauration vers une base neuve vérifiées. Service de sauvegarde systemd : succès, timer activé. Redémarrage réel, reconnexion, historique et préférences vérifiés. Ollama et WebUI actifs ; leurs unités et le modèle Tom ont les mêmes empreintes avant/après. Aucun poids, pilote, noyau ou accès distant modifié. Pas de reboot global.

## Réserves et mission 14

La qualité en bruit/écho réels, les périphériques physiques, Safari/iPhone/macOS et un vrai démarrage complet de la machine restent à valider. Le VAD client est heuristique ; l'interruption vocale est expérimentale et désactivée par défaut. La mémoire automatique couvre un catalogue explicite, pas toutes les phrases possibles.

Le modèle peut produire des explications approximatives : certains anciens rapports nomment mal l'exception ou inventent une consultation. Les traces et le contrôle de sources corrigent ce risque partiellement ; une sortie textuelle n'est pas une attestation. Aucune autonomie PXE, RAID, firmware, pilote Dell ou mission longue après reboot n'est démontrée.

Pour la mission 14 : transport et exécution bornés sur le Dell identifié, outils PXE/Ansible, VM UEFI avec snapshots et essais réseau, inventaire vérifié des deux NVMe FlexBay par identifiants stables, autorisation préalable du périmètre destructif, retour arrière et contrôleur de mission persistant. Reprendre l'étude existante : priorité RAID 1 Intel VROC/VMD si compatible et fiable sous Debian 13, repli mdadm après vérification. Aucune étude matérielle recommencée, aucun SSD touché.

Les sept rapports détaillent les procédures. GitHub suit une PR dédiée, sans fusion automatique ni publication des preuves brutes, bases, sauvegardes ou authentifiants.
