# JARVIS — Bilan actualisé du temps consacré au projet

**Date de référence : 11 octobre 2026 — actualisation après la Mission 04L**  
**Périmètre :** Mac mini 2018, Debian T2Linux, gestion distante et essais Thunderbolt / Razer Core / Quadro RTX 5000, avec Codex sur JARVIS et échanges de pilotage via ChatGPT.

## 1. Durées documentées : distinguer les indicateurs

| Indicateur | Durée ou valeur | Nature et limite |
|---|---:|---|
| **Traitement Codex enregistré** | **2 h 21 min 34 s** | Mesuré par les journaux Codex, relevé vers 21 h 59 ; n'inclut ni toutes les interventions humaines ni les traitements ultérieurs. |
| Sessions Codex | 8 conversations, 62 réponses terminées, 1 traitement interrompu | Même relevé local, non extrapolé. |
| Première activité Codex du relevé | 15 h 35 | Premier échange terminé enregistré ; pas nécessairement le début de la journée de travail humaine. |
| Dernière activité couverte par le relevé | 21 h 57 | Fin de la plage enregistrée par le relevé Codex. |
| **Plage horaire de projet attestée par les traces** | **15 h 35 → 22 h 16, soit 6 h 41 min** | Amplitude calendaire minimale entre le relevé et l'installation 04L ; **ce n'est pas 6 h 41 de travail actif mesuré**. Inclut pauses, préparation, tests physiques, attentes et échanges. |
| Contribution ChatGPT (analyse, choix des essais, prompts, interprétation) | **Réelle mais non chronométrée** | Plusieurs interventions attestées dans ce fil ; les heures actives ne sont pas reconstructibles précisément à partir du contenu seul. |
| Intervention humaine (clavier, branchements, GRUB, SSH, contrôle de stabilité) | **Réelle mais non chronométrée** | Des actions sont attestées ; aucune mesure de début/fin par tâche n'est disponible. |
| Temps actif humain total à date | **Non quantifiable précisément** | Ne pas assimiler les 2 h 21 de traitement Codex au temps humain ; ne pas additionner Codex + ChatGPT + amplitude, ces durées se chevauchent. |
| Temps cumulé depuis le lancement du projet, tous les jours | **Non établi** | Le présent relevé ne couvre que les activités documentées le 11 octobre ; des sessions précédentes et leur durée sont à consolider. |

**Repère utilisable pour le bilan :** au moins **6 h 41 d'amplitude de suivi du projet ce 11 octobre**, dont **2 h 21 min 34 s de traitement Codex effectivement mesuré** avant 21 h 59. Les **4 h 19 min 26 s restantes de cette amplitude** sont simplement du temps hors fenêtres de traitement Codex mesurées (ou postérieures au relevé), **pas une mesure de travail humain**. Le traitement Codex postérieur à 21 h 59 n'est pas comptabilisé : le total Codex journalier réel est donc supérieur ou égal à la valeur affichée.

## 2. Travaux réalisés lors du suivi ChatGPT / Codex

| Phase | Travail concrètement documenté | Résultat |
|---|---|---|
| Noyau T2 et accès | Démarrage T2, écran Intel i915, Ethernet et connexions SSH de surveillance | Fonctionnels lors des contrôles documentés |
| 04C–04E | Isolation de Nouveau, branchement surveillé d'un Razer Core | Bureau stable ; Quadro détectée ; BAR 1 et 3 non attribués |
| 04F–04H | Essai `pci=realloc=on`, contrôles PCIe et journaux privilégiés | Toujours pas d'attribution des BAR 1/3 |
| 04I–04J | Ajout et démarrage avec `pci=hpmmioprefsize=512M` | Réserve demandée, fenêtres amont inchangées (224 / 112 Mio) |
| 04K | Étude des types 64 bits, des fenêtres ACPI et du ciblage des ponts | Piste `resource_alignment` identifiée |
| 04L | Analyse du noyau installé, vérification ACPI privilégiée et installation d'une entrée GRUB distincte | Entrée **« JARVIS — T2 eGPU réallocation ciblée PCIe »** installée et contrôlée ; **pas encore démarrée ni testée** au dernier rapport |

**Important :** les phases ci-dessus décrivent de l'activité et des résultats techniques, **pas un décompte d'heures par phase**. Les horodatages individuels ne suffisent pas à en déduire une durée active fiable.

## 3. Actualisation du prévisionnel initial

Document de référence : **JARVIS_Bilan_Temps_Homme_IA.docx**, situation de cadrage du 11 octobre 2026.

| Indicateur du document initial | Valeur initiale | Statut après les missions 04 |
|---|---:|---|
| Charge classique totale théorique | 100–160 h, valeur centrale ≈ 130 h | **Prévision inchangée**, non mesurée |
| Charge assistée théorique totale | 39–73 h, valeur centrale ≈ 56 h | **À réestimer**, difficulté eGPU supérieure à celle présupposée |
| Travail « réalisé » théorique assisté | 9–16 h | **Ne pas présenter comme du temps effectivement effectué** |
| Avancement global initial | ≈ 25 % | **Obsolète en tant que mesure précise**, car T2 a progressé, mais CUDA et services IA non validés |
| Nouveau temps réellement tracé | — | 2 h 21 min 34 s de traitement Codex dans le relevé du 11 octobre (minimum connu), plus temps humain non mesuré |

La phase **Apple T2 / pilotes systèmes** a progressé : le noyau T2 démarre et l'affichage, le réseau et le stockage fonctionnent lors des contrôles réalisés. La phase **Thunderbolt / eGPU** a produit un diagnostic précis des fenêtres PCIe mais **n'a pas encore livré de GPU fonctionnel pour CUDA**. L'installation des services Ollama, Open WebUI, modèles, RAG et agents reste à évaluer sur des preuves de déploiement séparées. Il serait incorrect de déduire automatiquement un nouveau pourcentage global d'avancement de ces éléments.

## 4. Quotas : relevé historique, pas temps de travail

| Fenêtre de quota Codex | Consommation au relevé vers 21 h 59 |
|---|---:|
| 5 heures | 28 % |
| Hebdomadaire | 14 % |

Ces pourcentages ne sont ni des heures humaines ni une mesure de la durée du projet.

## 5. Méthode pour obtenir le **vrai temps effectif total**

Pour un bilan final sans double comptage, consolider **par jour et par phase** :

1. **Temps humain actif** : relever les heures réellement passées à préparer, superviser, brancher, tester, lire et arbitrer, en excluant pauses et attentes non surveillées.
2. **Temps Codex actif** : fusionner les intervalles `task_started` → `task_complete` / `turn_aborted` de chaque journée, sans additionner leurs chevauchements.
3. **Temps ChatGPT** : utiliser un relevé d'activité humaine des échanges ; les horodatages de messages ou leur amplitude ne suffisent pas à eux seuls à prouver une présence active continue.
4. **Temps machine autonome** : facultatif et séparé du temps humain, pour apprécier le gain d'automatisation.
5. **Temps de projet écoulé** : amplitude entre démarrage et dernier événement, communiquée séparément.

**Pour actualiser le cumul depuis le tout début du projet**, il faut les journaux Codex des autres jours et, pour la part humaine/ChatGPT, un relevé d'intervention ou une estimation explicitement assumée. Sans ces données, donner un total d'« heures effectives » serait inventer une mesure.

## 6. Sources et traçabilité

- `utilisation-2026-10-11.md` : relevé Codex à 21 h 59, issu des JSONL de `/home/adminjarvis/.codex/sessions/2026/10/11/`.
- `mission04L(1).md` : installation GRUB finalisée à **22:16:56**, aucune mise en service du candidat à cette date.
- Missions 04E, 04H, 04I, 04J et 04K : constats matériels PCIe et évolution des essais.
- `JARVIS_Bilan_Temps_Homme_IA.docx` : prévisionnel antérieur **non assimilable à du temps mesuré**.

*Bilan actualisé : priorité donnée aux temps vérifiés ; temps ChatGPT/humain signalés séparément jusqu'à mesure fiable.*
