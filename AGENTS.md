# Barrière anti-régression des directives JARVIS

**OBLIGATOIRE avant toute rédaction de prompt Codex, instruction JARVIS ou reprise de mission :** lire [la charte fondamentale](docs/CHARTE_DIRECTIVES_JARVIS.md), puis le prompt d'exécution et le dernier état de la mission concernée. Ne jamais réintroduire des interdictions génériques contredisant une autorisation explicite récente du propriétaire.

**Mission 13D-E :** le propriétaire a déjà autorisé l'installation Debian 13 complète et autonome du Dell cible validé, dont la **destruction des partitions des deux NVMe identifiés**, le RAID1 mdadm, le redémarrage, le bootstrap SSH et Ansible. Le PXE UEFI IPv4 physique a été **réussi**. **Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire.** Cela comprend : lancement PXE à la demande de Codex, écriture et effacement déjà autorisés des disques identifiés, installation, reboot, bootstrap et Ansible. Aucun nouveau GO ne doit être ajouté artificiellement avant ou pendant cette exécution. En cas de divergence matérielle réelle ou d'impossibilité technique, arrêter la seule opération concernée et remonter le fait, sans inventer un nouveau processus d'approbation. Aucun benchmark NVMe. L'environnement est un laboratoire privé expérimental ; présenter les risques sans réécrire les décisions utilisateur.

Chaque nouveau prompt doit indiquer les documents relus, les autorisations conservées et les éventuelles contradictions corrigées. Ne pas interpréter une procédure historique plus restrictive comme annulant une décision récente.

---

# Politique de déploiement JARVIS

Décision explicite du propriétaire, 16 octobre 2026, à conserver pour les prochains déploiements.

- Une demande explicite de déploiement complet autorise l'effacement des partitions, l'installation automatisée et le redémarrage sur les seuls disques du profil cible identifié et validé. Ne pas demander de confirmation à chaque commande de ce périmètre.
- Une demande de préparation ou de découverte seule n'autorise pas l'effacement. Une cible ou un disque inconnu ne devient pas autorisé par cette règle : découvrir, associer au profil et arrêter en cas d'ambiguïté.
- Conserver les contrôles UUID/DMI, séries, modèles et capacités exactes. Ne jamais sélectionner un disque par sa seule capacité ou par l'ordre de détection.
- Pour une demande explicite d’installation complète autonome, l’accord couvre les services temporaires nécessaires, l’effacement des seuls disques du profil validé, le reboot, le bootstrap SSH, l’accès permanent et le socle Ansible. La seule intervention physique normalement attendue est le lancement PXE. Une fois la mission lancée par le propriétaire, JARVIS et Codex doivent exécuter l'ensemble des opérations sans demander de validation humaine intermédiaire. Enchaîner les opérations prévues ; n'arrêter qu'en cas de divergence de cible ou de blocage technique réel. Une demande limitée à la préparation/découverte conserve son périmètre limité. Les contrôles automatiques ne sont jamais supprimés.
- Ne jamais verrouiller le bootstrap avant preuve positive d'une nouvelle connexion indépendante par clé et validation de sudo. Aucun secret ni identifiant matériel unique dans Git.
- Préserver les services, comptes, clés, SSH/Tailscale et SQLite du Mac mini, le DHCP Bbox et les paramètres BIOS/VROC/VMD. Pas de benchmarks NVMe, de fusion automatique, ni de seconde RTX 3090 sans alimentation validée.
- Exécuter les opérations autorisées réellement et rapporter les résultats. Si une action physique reste indispensable faute d'accès distant, l'expliquer sans prétendre l'avoir réalisée.

Prompt de référence : [installation autonome](docs/missions/13D-E/PROMPT-INSTALLATION-AUTONOME.md). Cette règle exprime la demande du propriétaire ; elle ne permet pas d’effacer une cible inconnue ou de prétendre qu’un test a été réalisé.
