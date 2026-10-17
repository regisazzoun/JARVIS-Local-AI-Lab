# Barrière anti-régression des directives JARVIS

**OBLIGATOIRE avant toute rédaction de prompt Codex, instruction JARVIS ou reprise de mission :** lire [la charte fondamentale](docs/CHARTE_DIRECTIVES_JARVIS.md), puis le prompt d'exécution et le dernier état de la mission concernée. Ne jamais réintroduire des interdictions génériques contredisant une autorisation explicite récente du propriétaire.

**Mission 13D-E :** le propriétaire a déjà autorisé l'installation Debian 13 complète et autonome du Dell cible validé, dont la **destruction des partitions des deux NVMe identifiés**, le RAID1 mdadm, le redémarrage, le bootstrap SSH et Ansible. Le PXE UEFI IPv4 physique a été **réussi**. **Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire.** Cela comprend : lancement PXE à la demande de Codex, écriture et effacement déjà autorisés des disques identifiés, installation, reboot, bootstrap et Ansible. Aucun nouveau GO ne doit être ajouté artificiellement avant ou pendant cette exécution. En cas de divergence matérielle réelle ou d'impossibilité technique, arrêter la seule opération concernée et remonter le fait, sans inventer un nouveau processus d'approbation. Aucun benchmark NVMe. L'environnement est un laboratoire privé expérimental ; présenter les risques sans réécrire les décisions utilisateur.

Chaque nouveau prompt doit indiquer les documents relus, les autorisations conservées et les éventuelles contradictions corrigées. Ne pas interpréter une procédure historique plus restrictive comme annulant une décision récente.

---

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
