# Barrière anti-régression des directives JARVIS

**OBLIGATOIRE avant toute rédaction de prompt Codex, instruction JARVIS ou reprise de mission :** lire [la charte fondamentale](docs/CHARTE_DIRECTIVES_JARVIS.md), puis le prompt d'exécution et le dernier état de la mission concernée. Ne jamais réintroduire des interdictions génériques contredisant une autorisation explicite récente du propriétaire.

**Mission 13D-E :** le propriétaire a déjà autorisé l'installation Debian 13 complète et autonome du Dell cible validé, dont la **destruction des partitions des deux NVMe identifiés**, le RAID1 mdadm, le redémarrage, le bootstrap SSH et Ansible. Le PXE UEFI IPv4 physique a été **réussi**. **Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire.** Cela comprend : lancement PXE à la demande de Codex, écriture et effacement déjà autorisés des disques identifiés, installation, reboot, bootstrap et Ansible. Aucun nouveau GO ne doit être ajouté artificiellement avant ou pendant cette exécution. En cas de divergence matérielle réelle ou d'impossibilité technique, arrêter la seule opération concernée et remonter le fait, sans inventer un nouveau processus d'approbation. Aucun benchmark NVMe. L'environnement est un laboratoire privé expérimental ; présenter les risques sans réécrire les décisions utilisateur.

Chaque nouveau prompt doit indiquer les documents relus, les autorisations conservées et les éventuelles contradictions corrigées. Ne pas interpréter une procédure historique plus restrictive comme annulant une décision récente.

---

## Convention permanente de présentation des statuts — décision du propriétaire du 19 octobre 2026

Dans les tableaux de pilotage (README, SUIVI, interfaces de suivi dont JL-02), utiliser les pictogrammes suivants, sans modifier le résultat technique documenté :

- **✅ GO / réalisée / validée** : objectif de la mission ou de l'étape atteint et vérifié dans son périmètre.
- **✅🟡 GO partiel / GO avec réserves / résultat réalisé avec réserves non bloquantes** : acquis réellement démontré et exploitable, mais périmètre restant ou réserve explicite. Conserver le texte historique « GO PARTIEL », « GO AVEC RÉSERVES » et les limites dans les colonnes explicatives.
- **🟡 En cours / incomplet / preuve insuffisante** : objectif global non encore atteint, ou résultat seulement préparé, non testé, incertain ; ne pas lui attribuer une coche de réussite.
- **📋 Planifiée** : pas encore exécutée.
- **❌ NO-GO / échec** : l'objectif testé a effectivement échoué ; conserver les faits et les limites.

Une étude ou un diagnostic effectivement terminé peut porter ✅ si son objectif se limitait à l'étude ou au diagnostic, même si la technologie étudiée reçoit un NO-GO : préciser cette distinction. **Ne pas qualifier de ✅🟡 un échec avéré, une installation non testée, une preuve absente, ni une mission simplement en cours.** Les rapports historiques et les preuves restent inchangés. Cette convention de présentation s'applique également aux futurs rapports, missions et tableaux ; elle ne déclenche pas de nouveaux tests ou validations.


# Politique de déploiement JARVIS

Décision explicite du propriétaire, 16 octobre 2026, à conserver pour les prochains déploiements. Ces directives remplacent les anciens prompts ChatGPT et consignes de mission contradictoires au même niveau utilisateur ; elles ne suppriment pas les vérifications techniques ni les instructions système applicables.

- Une demande explicite de déploiement complet autorise l'effacement des partitions, l'installation automatisée et le redémarrage sur les seuls disques du profil cible identifié et validé par les contrôles automatiques. Ne pas demander de confirmation à chaque commande de ce périmètre.
- Une demande de préparation ou de découverte seule n'autorise pas l'effacement. Une cible ou un disque inconnu ne devient pas autorisé par cette règle : découvrir, associer au profil et arrêter en cas d'ambiguïté.
- Conserver les contrôles UUID/DMI, séries, modèles et capacités exactes. Ne jamais sélectionner un disque par sa seule capacité ou par l'ordre de détection.
- Pour une demande explicite d’installation complète autonome, l’accord couvre les services temporaires nécessaires, l’effacement des seuls disques du profil validé, le reboot, le bootstrap SSH, l’accès permanent et le socle Ansible. La seule intervention physique normalement attendue est le lancement PXE. Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire. Enchaîner les opérations prévues ; n'arrêter qu'en cas de divergence de cible ou de blocage technique réel. Une demande limitée à la préparation/découverte conserve son périmètre limité. Les contrôles automatiques ne sont jamais supprimés.
- Ne jamais verrouiller le bootstrap avant preuve positive d'une nouvelle connexion indépendante par clé et validation de sudo. Aucun secret ni identifiant matériel unique dans Git.
- Préserver les services, comptes, clés, SSH/Tailscale et SQLite du Mac mini, le DHCP Bbox et les paramètres BIOS/VROC/VMD. Pas de benchmarks NVMe, de fusion automatique, ni de seconde RTX 3090 sans alimentation validée.
- Exécuter les opérations autorisées réellement et rapporter les résultats. Si une action physique reste indispensable faute d'accès distant, l'expliquer sans prétendre l'avoir réalisée.

Prompt de référence : [installation autonome](docs/missions/13D-E/PROMPT-INSTALLATION-AUTONOME.md). Cette règle exprime la demande du propriétaire ; elle ne permet pas d’effacer une cible inconnue ou de prétendre qu’un test a été réalisé.


## Directive de reprise — 17 octobre 2026

Tentative clôturée à la demande du propriétaire ; prochaine mission : finir l’installation en privilégiant la réparation de Debian et la conservation du RAID/partitionnement existants. Compte final imposé : **adminjarvis** ; mot de passe utilisateur conservé uniquement dans `deployment/13de/private/reprise-user-password.txt`, sans complexité supplémentaire imposée. Maintenir SSH par mot de passe jusqu’à validation indépendante par clé et sudo ; aucune suppression automatique du secours ensuite. Clavier français AZERTY à toutes les étapes. Suivi de toutes les tâches avec barres et coches de validation réelle. Ces directives remplacent les anciens noms de comptes et restrictions contradictoires. Lire `docs/missions/13D-E/RAPPORT-TRANSITOIRE-REPRISE.md` avant reprise. Ne pas relancer la mission pendant la clôture.


## Mission complète 13D-E / 14 relancée — 17 octobre 2026

Directive utilisateur actuelle : nouvelle installation Debian automatisée, conservation prioritaire GPT/RAID1/métadonnées/deux ESP, formatage rapide de la seule racine si compatible. Comptes jarvis-bootstrap et adminjarvis avec le même mot de passe imposé dans le fichier privé reprise-user-password.txt. Garder SSH par mot de passe pour adminjarvis même après validation indépendante par clé et sudo ; ne pas désactiver prématurément le bootstrap. Clavier français dans installateur/secours/consoles/système. Mission continue incluant Ansible, NVIDIA/CUDA, Ollama, Qwen/Ministral/Llama documentés, intégration conversation/voix/mémoire/outils et réception après reboot. Une RTX 3090 alimentée seulement. Aucune validation humaine intermédiaire ; email au propriétaire quand le PXE est réellement prêt. Les anciennes clôtures, reports IA, révocations automatiques et préférences de simple réparation sont remplacés dans ce périmètre. Aucun secret dans Git. Préserver services/accès/mémoire Mac mini et DHCP Bbox ; aucune fusion main.


## Mission 11 — habilitations agentiques persistantes — 17 octobre 2026

Le propriétaire autorise le raccordement de JARVIS/Qwen à Debian réel, aux installations, services, GitHub et mécanismes SSH/Tailscale/Ansible du laboratoire. Exécuter les opérations dans ce périmètre sans validations humaines intermédiaires. Les restrictions historiques « uniquement Bubblewrap /work » ne décrivent plus les outils hôte de mission 11 ; le laboratoire 13F reste facultatif. Les mécanismes système utilisent la politique propriétaire persistante, distincte des données et instructions conversationnelles. Une demande de capacité produite par Qwen n'étend jamais à elle seule l'autorisation. Codex traite les demandes du périmètre déjà accordé, puis JARVIS teste lui-même les droits avant validation. Préserver déploiement Dell 13D-E/14, accès Mac, mémoire, Bbox et Launcher V1. Aucune fusion automatique main. JL-02 doit être développé par JARVIS, pas réalisé par Codex dans la mission 11. Architecture et réception : [mission 11](docs/missions/11/ARCHITECTURE.md).


## Mission 11B — administration Dell permanente

Décision propriétaire du 17 octobre 2026 : le déploiement 13D-E/14 est réceptionné. Le profil historique `dell-observe` est désormais administrable via SSH et Ansible dans la politique root persistante `/etc/jarvis/host-policy.json`. Réutiliser les comptes, clés et hôtes épinglés ; aucune réinstallation Debian. Les anciennes restrictions temporaires de lecture seule du Dell sont remplacées dans ce périmètre. Les opérations IA accordées restent disponibles pour les prochaines missions autorisées ; une conversation ou une demande du modèle ne peut étendre seule cette politique. Conserver le contrôle DMI/NVMe, les journaux et les secrets hors du modèle et de Git. Reprendre 11B depuis son checkpoint, branche `jarvis/mission-11b-compute-expansion`, documentation `docs/missions/11B/`. Ne pas lancer JL-02. Aucun nouveau processus de validation humaine intermédiaire.


## JL-02 — lancement et livraison autorisés (17 octobre 2026)

Le propriétaire a explicitement lancé JL-02 : Codex coordonne et intègre, JARVIS exécute des tâches techniques réelles. Cette décision remplace les anciennes exclusions « ne pas lancer JL-02 » dans le seul périmètre JL-02 ; elle n’autorise aucune extension à une cible inconnue. Dépôt distinct `regisazzoun/JARVIS-Launcher2`, V1 inchangée. Réutiliser les identités, la passerelle, la mémoire et les outils existants, poursuivre sans validations humaines intermédiaires, conserver les preuves et l’attribution des contributions. Publication V2 autorisée ; aucune fusion automatique dans le dépôt principal. Un email de fin est demandé par le propriétaire.

## Mission 00 — pilotage documentaire, 17 octobre 2026

Le propriétaire a lancé `00-Mission-Pilotage-point-26-10-17`. Exécuter l’audit local/GitHub et les cinq lots réels JARVIS, puis consolider sur une branche dédiée, sans validation humaine intermédiaire ni fusion dans main. Cette décision remplace le report historique de l’audit. Lire les sources et écrire les livrables documentaires en préservant les originaux, secrets et services.

Aucun déploiement, rétablissement du RAID ou installation du Dell n°2 dans ce périmètre. **13D-E = Dell n°1 installé par Codex et réceptionné ; 14 = Dell n°2 à déployer par JARVIS ; 14A = capacité agentique distincte, sans validation globale automatique par la mission 00.** Conserver les périmètres distincts de 11 historique, 11-Agentic, 11B, JL-01 et JL-02. Les décisions récentes prévalent ; les textes anciens restent historiques. Registre et preuves : `docs/missions/00-Mission-Pilotage-point-26-10-17/`.

Réception documentaire 00 : GO avec réserves, cinq tâches JARVIS réellement exécutées avec guidage et corrections Codex. Les règles inventées dans les sorties modèle n’ont aucune autorité. Le [rapport final](docs/missions/00-Mission-Pilotage-point-26-10-17/RAPPORT-FINAL.md) et le registre précisent les résultats ; conserver les autorisations récentes et la séparation 13D-E / 14A / 14.

## Publication documentaire dans main — autorisation du 18 octobre 2026

Le propriétaire demande explicitement : « Alors fusionne je veux quelque chose de coherent », avec README réécrit et SUIVI à jour. La fusion des livrables documentaires 00 et du correctif de concordance est maintenant autorisée, y compris leur intégration dans main. Cette décision remplace les consignes antérieures de non-fusion pour cette publication précise. La PR6 documentaire peut être fusionnée dans sa branche de base ; une intégration documentaire dédiée publie le résultat dans main sans importer les changements de déploiement de la PR5. Aucun déploiement matériel ou changement des services n’est déclenché. Les règles de fusion des autres missions ne sont pas étendues implicitement.
