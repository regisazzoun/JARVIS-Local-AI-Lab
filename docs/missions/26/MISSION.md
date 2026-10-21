# Mission 26 — Mission Engine résilient, planification autonome et vérification des preuves

**Statut actuel : ✅🟡 reçue avec réserves le21 octobre2026.** [Rapport de réception](RAPPORT-FINAL.md). Statut initial du cahier : 📋 planifiée ; ce lancement a ensuite été explicitement autorisé et exécuté par Codex avec JARVIS opérateur.
**Priorité validée par le propriétaire le 21 octobre 2026 :** 25 (reçue) → **26** → épreuve finale 14A (distincte et différée) → **24-Old Mémoire enrichie et AutoDream** → 27 JL-03 → 28/29/30/31.

## Objectif

Développer et déployer un **moteur de mission réellement plus autonome** à partir de la pile existante, capable pour JARVIS de : objectif brut → plan qu'il élabore et versionne → exécution avec outils MCP/skills → détection d'erreur → diagnostic/correction/reprise → vérification sémantique par observation indépendante → compte rendu sourcé. Les succès déjà reçus ne sont pas à rejouer. Mission 26 vise à **renforcer** les points ouverts de 14A, pas à clore automatiquement 14A ni à lancer l'épreuve finale autonome réservée pour plus tard.

## Référentiel vérifié au 21 octobre

- `AGENTS.md` ; `docs/CHARTE_DIRECTIVES_JARVIS.md`.
- `docs/missions/CYCLE-23-31.md`, `ROADMAP.md`, `SUIVI.md`.
- `docs/missions/25/MISSION.md`, `docs/missions/25/RAPPORT-FINAL.md`, `docs/missions/25/BILAN-14A.md`, `docs/missions/25/TESTS-REPRISES.md`, `docs/missions/25/VERIFICATION-INDEPENDANTE.json`.
- Contrat historique `docs/missions/13D-E/AGENT-14A.md`, uniquement comme trace : ses restrictions VM/hôte antérieures ne prévalent pas sur les autorisations récentes.
- Rapports et preuves des missions 11/11B, 14A, 21, 22, 23C, 24 et 25 à retrouver par Codex et vérifier au lancement.
- Références à analyser pour inspiration : Grominet95/jarvis-OS (patterns de planification/résilience) sans copier de code avant vérification de licence.

## Situation de départ et acquis

Mission25 ✅🟡 : 47 outils natifs dont six interfaces nouvelles, quatre skills actifs (trois Codex et `config-repair` créé par JARVIS), MCP réellement exécuté, 89 tests logiciels, quatre tâches reçues et réutilisation réelle de skill. Le broker rétabli par24 est opérationnel ; persistance de tâches/checkpoints et publication GitHub déjà reçues.

**Trois manques ciblés :**
1. **Planification globale :** Codex a donné le graphe de quatre lots ; aucune preuve d'un plan global inédit entièrement proposé par JARVIS.
2. **Vérification :** le skill créé valide parfois seulement code0 et présence de `status`; ses sorties avaient été validées séparément par Codex, mais le vérificateur de JARVIS ne prouve pas toujours la sémantique de ses effets.
3. **Restitution :** certains rapports du modèle se trompent sur les entrées réelles, le comportement de `config_repair.py`, le nombre de skills/tests et l'attribution de `argv` à Codex.

## Travaux à exécuter dans une mission unique

### A — Moteur de planification autonome
Partir d'un objectif utilisateur non prédécoupé dans le moteur. JARVIS produit un `mission_plan` structuré, persisté, avec tâches, dépendances, critères de réussite, outils/skills candidats, artefacts et conditions d'arrêt réelles. Autoriser la révision automatique du plan après observation d'échec ; versionner ancienne et nouvelle proposition et conserver provenance JARVIS/Codex.

### B — Orchestrateur et reprise
Faire coopérer le Mission Engine existant, broker, MCP/skills, checkpoints et journaux. Gérer plan→exécution→observation→diagnostic→correction→nouvel essai, avec reprise après interruption ciblée, opérations idempotentes et détection de doublons. Ne pas créer un second système concurrent de missions ni réinitialiser les checkpoints reçus.

### C — Vérification sémantique
Introduire des contrats de réussite adaptés à la tâche (valeur/structure attendue, contenu réellement écrit, absence de perte de champs, sortie SSH/systemd/GitHub effectivement observable, etc.). Une déclaration `success`, une présence du mot `status` ou un code de retour 0 seuls ne prouvent plus un résultat métier. Créer des contrôles indépendants du même modèle ou de l'action initiale, attribuer état PASS/FAIL/INCOMPLET selon preuves, conserver les échecs et indiquer l'incertitude non vérifiée.

### D — Diagnostic/autocorrection
JARVIS doit pouvoir traiter une erreur reproductible : isoler la cause, consulter les résultats du broker et les informations techniques utiles, adapter un plan, un paramètre, un skill ou un outil dans le périmètre permis, retester uniquement l'étape concernée, puis reprendre le plan. Codex peut corriger une lacune d'infrastructure réelle, mais doit ensuite refaire vérifier par JARVIS que les outils nouvellement disponibles fonctionnent. Attribuer distinctement les contributions.

### E — Rapport fiable fondé sur les preuves
Construire le rapport final depuis journaux/reçus/artefacts exacts : objectifs, changements, actes réellement exécutés, succès et échecs, contrôles indépendants, codes et versions exacts, attribution Codex/JARVIS, décisions et incertitudes. Vérifier la cohérence des données clés avant publication. Conserver les rapports bruts erronés avec erratum plutôt que les maquiller ; tout résumé sans preuve doit être qualifié.

### F — Réception opérationnelle ciblée
Tester au moins un objectif **réel et non prédécoupé** confié à JARVIS, impliquant plusieurs outils/skills existants sur Mac mini et/ou Dell1 et publication de preuves GitHub. Observer la création du plan, la correction d'un échec, la vérification sémantique et le compte rendu. Ajouter des tests ciblés du moteur pour les cas de fausse réussite, erreur de donnée, reprise, idempotence et attribution. Ne pas refaire la recette LiveKit 23D, la remise en service broker24, ni les 89 tests de25 autrement que par non-régression adaptée.

## Limite de périmètre et statut 14A

**La mission26 n'est pas l'« épreuve finale14A »** documentée dans `docs/missions/25/BILAN-14A.md`. Cette épreuve reste 📋 à exécuter ultérieurement sur ordre du propriétaire. La26 peut améliorer et documenter les critères14A, sans convertir automatiquement14A en ✅ et sans créer de validations humaines intermédiaires.

Ne pas lancer `24-Old Mémoire enrichie` ou AutoDream durant26, ne pas prétendre la mémoire persistante intégrée à LiveKit 23D. Conserver SQLite/FTS5, modèles, accès Tailscale/SSH/Ansible, services, GitHub, JL-02, Dell1 et Dell2 hors mission. Aucune réinstallation OS/RAID, ni changement matériel, ni fusion `main` implicitement permis ou nécessaire pour cet objectif de moteur.

## Responsabilités et livraison

Codex orchestre, implémente l'infrastructure manquante, vérifie indépendamment ; **JARVIS élabore et réalise réellement les plans et opérations du scénario**. Ne pas substituer de scripts Codex au résultat présenté comme une action JARVIS. Dès que le propriétaire lance le prompt, exécuter toutes les étapes de26 jusqu'à leur résultat dans le périmètre déjà autorisé, sans validation humaine intermédiaire. Un blocage concret doit être documenté précisément.

Sur branche dédiée `codex/mission-26-mission-engine`, publier :
- `docs/missions/26/RAPPORT-FINAL.md` et `BILAN-14A.md`
- `PLAN-JARVIS.md` + plan(s) machine exploitables/versionnés
- `TESTS-ET-REPRISES.md`, traces corrélées, vérifications sémantiques et comparatif avant/après
- `ATTRIBUTION-CODEX-JARVIS.md`, `ARCHITECTURE.md`, `INSTALLATION-UTILISATION.md`
- Mise à jour de `SUIVI.md`, `ROADMAP.md`, registre en conservant historiques et preuves.

Verdicts selon charte ✅, ✅🟡, 🟡, ❌ : signaler preuves et limites ; ne pas confondre un test logiciel local avec une exécution autonome du modèle. PR dédiée sans fusion `main`.
