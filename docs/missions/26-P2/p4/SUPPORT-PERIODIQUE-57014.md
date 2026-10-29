# Support ponctuel P4-AUDIT — 27 octobre 2026

🟡 Audit non reçu. Intervention limitée à la mission `d1b0d69639724c60b5bd1b2143b1a5fa`, après trois refus de relecture du même reçu (57008/57009). Aucun rejeu P2/P3.

Directives consultées : AGENTS.md, charte fondamentale, M26_P2_P4_CODE_REEL.md, lancement P4 et derniers événements/reçus ciblés. Autorisation propriétaire conservée sans validation humaine intermédiaire ; premier paquet sans déploiement.

Le reçu 56724 constate un chemin erroné `engine/core.py`. Son manifeste et celui de 56940 contiennent `engine/jarvis/core.py`, empreinte `a8d898f30cc51aa9e358fcadb8cd60c55b2fe40dadcb36055a28583afa072f55`. Cela ne démontre pas un défaut d'approvisionnement de la copie. Le reçu 56940 termine avec code 127, `git: command not found` : il ne prouve ni panne du moteur ni absence du fichier Python. Les reçus et diagnostics initiaux restent conservés ; ces corrections sont attribuées à Codex.

Changement concret : ajout temporaire de `authority_read_execution` aux outils désactivés pour cette seule mission, sauvegarde privée du spec et archivage du contexte par MissionStore. Instruction courte 57012 transmise sous acteur Codex pour être visible du filtre actuel de guidage, avec provenance Codex-periodic. Aucun changement du moteur, service, superviseur ou compteur. Contrôles réussis : lecteur masqué, instruction visible du moteur, égalité des compteurs de problèmes avant/après. Événement Codex-periodic 57014, puis état queued via MissionStore.

JARVIS/Qwen80B conserve les commandes, les essais distants et la production de l'artefact structuré hors engine. Les SHA disque ne prouvent pas les objets chargés en mémoire. La capacité d'attestation manquante reste à expliciter par JARVIS ; aucun mécanisme complet n'est installé par ce support. La remise en file ne vaut ni exécution réussie, ni réception de l'audit, ni validation de toute P4. Le registre ne porte donc pas encore de technical_review_recorded pour ce paquet.
