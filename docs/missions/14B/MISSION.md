# Mission 14B — Déploiement autonome du Dell n°2 et intégration au laboratoire JARVIS

**Date de décision :** 24 octobre 2026. **Statut :** 📋 préparation documentée, mission non lancée. **Exécution future :** JARVIS, en réutilisant les automatisations existantes ; Codex coordonne et intervient sur blocages techniques effectifs. Aucune validation humaine intermédiaire une fois la mission lancée par le propriétaire.

## Décisions nouvelles du propriétaire (24 octobre 2026)

1. **14B est un prolongement de la mission 14**, distinct de la mission 14A (capacité agentique), et dédié au Dell n°2.
2. **Dépendance explicite à la mission 28A.** L'architecture de calcul distribué existe déjà. Le Mac mini Debian reste coordinateur, mémoire et missions canoniques, conversation sous `qwen3.5:27b-q4_K_M` ; le Dell n°1 reste nœud de calcul des missions sous `qwen3-coder-next:q4_K_M` (80B MoE). **Ne pas redéfinir cette répartition ni réexécuter le screening des modèles.**
3. Le propriétaire **essaiera de démarrer le Dell n°2 avec ses deux RTX 3090 dès le départ**, pour éviter une reconfiguration ultérieure. C'est une évolution de la décision précédente de commencer avec une seule carte ; l'inventaire réel et la capacité d'alimentation doivent être constatés au démarrage. Si une seule carte peut être alimentée correctement, l'installation reste évolutive, sans transformer la seconde en prérequis fictif. Ne jamais alimenter une RTX 3090 avec un câblage de compatibilité électrique non établi.
4. **Reprendre les versions déjà validées sur le Dell n°1** plutôt que relancer une sélection générique : Debian 13, pilote NVIDIA 550.163.01, Ollama 0.40.3, CUDA opérationnel. Ce sont les versions de référence prouvées par la réception 13D-E/14 historique ; un écart matériel réel éventuel est à expliquer, pas à introduire silencieusement.
5. Préserver le Mac mini, le Dell n°1, les services, la mémoire SQLite, les clés/accès et les interfaces JARVIS existants. Aucune réinstallation ni migration du coordinateur. Les capacités MCP, skills, missions persistantes et routage déjà développées doivent rester utilisables.

## Base technique déjà acquise et sources à relire avant le prompt d'exécution

- `AGENTS.md` et `docs/CHARTE_DIRECTIVES_JARVIS.md` : directives du propriétaire, contrôles d'identité matériel et exécution autonome après lancement.
- `docs/missions/13D-E/RECEPTION-MISSION14.md` : réception **du premier Dell** malgré son intitulé historique, versions et résultats réels ; **ne pas confondre avec l'installation future du Dell2**.
- Sur la branche `codex/mission-28a-routage-modeles` : `docs/missions/28A/RAPPORT-FINAL.md`, `ARCHITECTURE-HYBRIDE.md`, `DELL2-PREPARATION.md`, `INSTALLATION-UTILISATION.md`, et `operations/mission28a/dell2-profile.json`. La 28A a été clôturée **incomplète** sur décision du propriétaire le 24 octobre ; son **cœur hybride est installé et exploitable**, son Dell2 est désactivé et son profil logique n'est pas un matériel installé.
- Consulter également le dernier suivi et les procédures PXE/Ansible 13D-E avant toute exécution ; préserver les corrections de scripts déjà acquises, notamment la réserve sur reboot forcé du contrôleur PXE.

## Travaux prévus pour 14B, pas encore exécutés

1. Inventorier localement le Dell2 (DMI, NVMe, BIOS, réseau, CPU, RAM, nombre de RTX 3090 réellement alimentées et détectées). Ne copier ni l'identité ni les adresses du Dell1.
2. Réutiliser l'installation Debian 13, RAID1/ESP et le socle réseau, SSH, Tailscale, Ansible, NVIDIA/CUDA et Ollama des recettes validées, après identification des disques propres au Dell2. La mission ne vaut pas permission d'effacer des disques inconnus.
3. Intégrer le Dell2 au profil logique déjà défini par 28A : nom/adresse privés réels, authentification, catalogue de modèles effectivement installés, sondes de disponibilité/VRAM, critères d'admission et routage. Activer seulement après constat effectif du nœud.
4. Garder le moteur de missions et la mémoire sur le Mac ; vérifier sans duplication que les requêtes éligibles arrivent au bon nœud, et que l'indisponibilité du Dell2 ne perturbe ni la conversation ni le Dell1.
5. Documenter séparément le comportement réel à un ou deux GPU, les paramètres Ollama et la répartition éventuelle des modèles ; **ne pas confondre 2 × 24 Go de VRAM avec une carte monolithique de 48 Go**.
6. Publier mesures et preuves d'installation, statut et réserves sur une branche GitHub dédiée ; préparer une réception fondée sur les résultats réels. La mission 14B n'est **pas lancée** par cette documentation.

## Décision d'architecture

L'ajout du Dell n°2 **étend** l'architecture de la mission 28A et **ne déclenche pas une refonte** des modèles, de la mémoire ou de la coordination. L'utilisation simultanée des deux RTX 3090 sur Dell2 est un objectif matériel désormais prioritaire, soumis à la disponibilité réelle des alimentations et aux observations de démarrage. Ne pas reprendre les vérifications déjà acquises sur Dell1 comme si elles restaient à refaire sur ce serveur.

**Conformité :** directives consultées : AGENTS.md, docs/CHARTE_DIRECTIVES_JARVIS.md, réception historique 13D-E/14 et dernière clôture 28A ; autorisations préservées : installation autonome après lancement, aucun GO humain intermédiaire, identité de cible et disques vérifiée, services existants préservés ; évolution explicite : tentative de démarrage Dell2 avec deux RTX 3090 plutôt qu'une seule.
