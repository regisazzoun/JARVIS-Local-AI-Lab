# Inventaire GitHub — Codex

Référence :17 octobre 2026. Découverte via `gh repo list`, toutes les branches distantes récupérées par `git fetch`, arbres et contenus examinés avec `git ls-tree`/`git show`. **963 entrées document/branche**, **455 contenus uniques**, **15 références de branches**, **6 PR**. Les 15 références comprennent les branches Pages, qui n'ont pas nécessairement de document de mission ; les deux `main` des Launcher et le `main` du laboratoire restent distingués dans le JSON. Les dépôts personnels sans lien JARVIS (`Regis-AZZOUN`, `FormulairePFMP`) ont été retrouvés mais exclus du périmètre fonctionnel.

L'inventaire exhaustif avec tous les champs demandés est [CSV](INVENTAIRE-GITHUB.csv) et [JSON](INVENTAIRE-GITHUB.json). « Courant dans sa branche » ne signifie pas autorité globale : la résolution se fait rapport par rapport, selon le contenu et la décision propriétaire. La date Git est celle du dernier commit du chemin dans la branche, pas une date de test. Les dates apparentes de contenu et limites de lecture sont dans l'inventaire local ; une date documentaire certaine n'est pas inventée pour un fichier non daté. La correspondance locale repose sur SHA256 des contenus, pas sur le seul nom. L'absence de correspondance signifie non retrouvée dans les racines parcourues, pas inexistence absolue.

## Branches observées

| Dépôt | Branche | Commit observé | Documents indexés |
| --- | --- | --- | --- |
| JARVIS-Local-AI-Lab | codex/jarvis-documentation-consolidation | f6bba526df7a6f69d30231e66eb2d9571ed369dd | 357 |
| JARVIS-Local-AI-Lab | codex/jarvis-reorganisation-documentaire | 6ed9af8b38b00511b9d3328a3d960de99d1cc064 | 363 |
| JARVIS-Local-AI-Lab | codex/jl-02-launcher-v2 | 43c31a947977586fea74ff171071a5b261551153 | 43 |
| JARVIS-Local-AI-Lab | codex/mission-11-agentic-enablement | c9fcd90a89ba3089c9c3527c401ee86a79d4d430 | 41 |
| JARVIS-Local-AI-Lab | codex/mission-13de-preparation | 6dd5f572a68fc3182f3a56692cbe3466d74c86da | 32 |
| JARVIS-Local-AI-Lab | codex/mission-13f-20261014-a0ed2a | a0ed2a844c3573966704ef3d89a0b682590204fe | 25 |
| JARVIS-Local-AI-Lab | jarvis/mission-11b-compute-expansion | 7828e1c47c18c1fff6dfbc7641110f9fd6841c1a | 43 |
| JARVIS-Local-AI-Lab | jarvis/mission11-proof-20261017 | 4fddc12d753fe43882202ad61df60a69c662123d | 13 |
| JARVIS-Local-AI-Lab | main | f77742296e347f38d7eb0aefa50d03ca08fd7697 | 12 |
| JARVIS-Local-AI-Lab | mission13e-integration-20261014 | 0e679df50e67e4cddcf4568d9b11885ce2ca859a | 14 |
| JARVIS-Launcher | codex/jl-01-jarvis-launcher | ce95648d7672729b8b5c1c8e29de2f92c16f1732 | 8 |
| JARVIS-Launcher | gh-pages | d0ef414a12cb4491964801563a8ef0768235d5af | 0 |
| JARVIS-Launcher | main | d5902c6252b10320bcd0972bc1a506616e1ce9c5 | 1 |
| JARVIS-Launcher2 | gh-pages | 1be57e01742ce9462a0f3813881ab792d62a49e5 | 0 |
| JARVIS-Launcher2 | main | 164d4b455bd324bd88ed082d3c810a9ae708e8b5 | 11 |

## Pull requests observées

| Dépôt / PR | Branche | État | Lien |
| --- | --- | --- | --- |
| JARVIS-Local-AI-Lab #5 | codex/mission-13de-preparation | OPEN ; fusion : None | https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/5 |
| JARVIS-Local-AI-Lab #4 | codex/mission-13f-20261014-a0ed2a | OPEN ; fusion : None | https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/4 |
| JARVIS-Local-AI-Lab #3 | codex/jarvis-reorganisation-documentaire | OPEN ; fusion : None | https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/3 |
| JARVIS-Local-AI-Lab #2 | codex/jarvis-documentation-consolidation | OPEN ; fusion : None | https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/2 |
| JARVIS-Local-AI-Lab #1 | mission13e-integration-20261014 | OPEN ; fusion : None | https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/1 |
| JARVIS-Launcher #1 | codex/jl-01-jarvis-launcher | OPEN ; fusion : None | https://github.com/regisazzoun/JARVIS-Launcher/pull/1 |

## Sources publiées hors main

- Rapports et archives historiques exhaustifs : branches `codex/jarvis-documentation-consolidation` et `codex/jarvis-reorganisation-documentaire`, PR2/3 ouvertes.
- Passerelle 13E : `mission13e-integration-20261014`, PR1 ouverte.
-13F : `codex/mission-13f-20261014-a0ed2a`, PR4 ouverte.
- Réception complète Dell n°1 : `codex/mission-13de-preparation` au commit6dd5f57, PR5 ouverte dont le titre préparatoire est périmé.
- Administration 11B : `jarvis/mission-11b-compute-expansion`, raccordement et reprise7828e1c.
- Livraison JL-02 et directives récentes : `codex/jl-02-launcher-v2`,43c31a9 ; code V2 dans son dépôt distinct.

Aucune de ces branches n'a été fusionnée automatiquement. La branche00 est basée sur la référence Dell la plus récente ; les documents11/11B et directives JL-02 ont été repris explicitement, sans merge ni remplacement aveugle du suivi.

## Historique pertinent

[Historique documentaire et branches confirmées](HISTORIQUE-PERTINENT.json) : 104 commits touchant les directives, rapports, index et documents de suivi ont été recensés. Les 15 branches distantes ont été confirmées en lecture seule par `git ls-remote --heads`. Les passages de préparation à réception, les reprises11B et la publicationJL02 sont conservés ; une date de commit ne vaut pas preuve d’exécution du contenu.
