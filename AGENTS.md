# Politique de déploiement JARVIS

Décision explicite du propriétaire, 16 octobre 2026, à conserver pour les prochains déploiements.

- Une demande explicite de déploiement complet autorise l'effacement des partitions, l'installation automatisée et le redémarrage sur les seuls disques du profil cible identifié et validé. Ne pas demander de confirmation à chaque commande de ce périmètre.
- Une demande de préparation ou de découverte seule n'autorise pas l'effacement. Une cible ou un disque inconnu ne devient pas autorisé par cette règle : découvrir, associer au profil et arrêter en cas d'ambiguïté.
- Conserver les contrôles UUID/DMI, séries, modèles et capacités exactes. Ne jamais sélectionner un disque par sa seule capacité ou par l'ordre de détection.
- Pour une demande explicite d’installation complète autonome, l’accord couvre les services temporaires nécessaires, l’effacement des seuls disques du profil validé, le reboot, le bootstrap SSH, l’accès permanent et le socle Ansible. La seule intervention humaine est le lancement PXE ; pas de validation intermédiaire. Une demande limitée à la préparation/découverte conserve son périmètre limité. Les contrôles automatiques ne sont jamais supprimés.
- Ne jamais verrouiller le bootstrap avant preuve positive d'une nouvelle connexion indépendante par clé et validation de sudo. Aucun secret ni identifiant matériel unique dans Git.
- Préserver les services, comptes, clés, SSH/Tailscale et SQLite du Mac mini, le DHCP Bbox et les paramètres BIOS/VROC/VMD. Pas de benchmarks NVMe, de fusion automatique, ni de seconde RTX 3090 sans alimentation validée.
- Exécuter les opérations autorisées réellement et rapporter les résultats. Si une action physique reste indispensable faute d'accès distant, l'expliquer sans prétendre l'avoir réalisée.

Prompt de référence : [installation autonome](docs/missions/13D-E/PROMPT-INSTALLATION-AUTONOME.md). Cette règle exprime la demande du propriétaire ; elle ne permet pas d’effacer une cible inconnue ou de prétendre qu’un test a été réalisé.
