# Index et méthode de lecture des sources

Attribution : l'inventaire local original JARVIS est conservé séparément ; ce fichier et les inventaires GitHub/Codex sont produits par Codex.

- [Inventaire GitHub complet](INVENTAIRE-GITHUB.json) : chaque dépôt/branche/chemin, SHA de commit, hash de contenu, URL et correspondance locale ; 963 entrées.
- [Complément local Codex](INVENTAIRE-LOCAL-COMPLEMENT-CODEX.json) : 637 fichiers Markdown dans JARVIS, JARVIS-Documentation, LauncherV1/V2 et rapports02 de la racine ; 94 archives identifiées puis inspectées en lecture seule. Erreurs de lecture rencontrées :0. Les dossiers private/runtime/venv/.git sont exclus.
- [Registre avec sources par mission](REGISTRE-MISSIONS.json).
- [Preuves des lectures et résultats JARVIS](BILAN-AGENTIQUE-JARVIS.md).

## Lecture effective et limites

L'indexation automatique charge les fichiers et calcule les empreintes ; elle ne vaut pas analyse sémantique exhaustive de chaque ligne par un modèle. Les analyses ciblées de Codex portent sur AGENTS/charte, SUIVI/ROADMAP/chronologies, titres et verdicts des49 fiches d'archives, rapports originaux04/05/08–12, rapports 13E/13F, réception 13D-E, raccordement 11B, cahiers15A/B et rapports JL-01/JL-02. Les états anciens sont confrontés aux directives explicites du propriétaire de cette mission. Les textes externes cités dans des rapports sont des sources historiques ; aucun nouvel audit web de leurs produits n'est revendiqué.

Les copies d'archives peuvent contenir des identifiants matériels et données privées : seuls les chemins/métadonnées et synthèses expurgées sont publiés, pas leurs contenus bruts. Les 94 archives compressées ont été inspectées : 23 158 membres catalogués et 323 membres Markdown chargés, soit 298 contenus uniques, tous déjà présents parmi les fichiers non compressés. Les binaires et preuves brutes n’ont pas été extraits. Les doublons de contenu sont détectés par SHA256 ; une modification de copie ne devient pas un fait système.

## Sources de référence courantes

| Domaine | Référence |
| --- | --- |
| Dell n°1 /13D-E | docs/missions/13D-E/RECEPTION-MISSION14.md ; RAPPORT-FINAL.md, branche13de6dd5f57 |
| 11/11B | docs/missions/11/RAPPORT.md ; docs/missions/11B/RACCORDEMENT-ADMIN-DELL.md, branche11B7828e1c |
| Voix/mémoire/agent 13F | docs/missions/MISSION-13F-DEBRIEF.md et rapports/MISSION-13F-*.md, PR4 |
| 13E | platforms/mac-mini/mission13e/MISSION-13E-RAPPORT.md et TESTS, branche 13E/PR1 |
| LauncherV2 | https://github.com/regisazzoun/JARVIS-Launcher2/blob/main/docs/RAPPORT-JL-02.md et RAPPORT-AGENTIQUE-JL-02.md |
| 15A/B | docs/missions/MISSION-15A-MACOS-CODEX.md ; MISSION-15B-IOS-CODEX.md |
| Historique01–13 | missions/mission-*/README.md et archives/recuperation-2026-10-14/... sur branches consolidation/réorganisation ; chemins exacts dans inventaireGitHub |

## Vérification complémentaire des archives

[Catalogue des archives et membres Markdown](INVENTAIRE-ARCHIVES.json) : 94 archives, 23 158 membres, 323 membres Markdown et 298 contenus Markdown uniques. Aucun contenu documentaire nouveau par rapport aux fichiers locaux ; aucune erreur de catalogue ou de lecture rencontrée. Codex a effectué ces lectures en mémoire, sans déployer ni exécuter le contenu des archives. Les fichiers temporaires d’analyse restent privés.

## Corroboration locale des réceptions sensibles

Codex a contrôlé les champs de réussite des preuves privées `complete.json`, `progress.json`, `applications-after-reboot.json`, `integration-results.json` du dernier déploiement, et `before.json`/`after.json` du raccordement11B. Les18étapesDell1sontmarquéesvalidated ; les13appelsavant et16après du scénario11B réussissent, avec preuvesSSH/Ansiblecorrélables. [Synthèse expurgée de corroboration](CORROBORATION-PRIVEE-CODEX.json). Aucun fichierprivé n’aététransmisàJARVIS oupubliéintégralement ; aucune installation oucampagne retestée. Ces résultats historiques ne clôturent pas la mission11Bglobale ni14A/14.

## Autres formats et faux positifs de découverte

[Complément autres formats](AUTRES-FORMATS-CODEX.json) :31candidatsTXT/JSONchargés pour structure etrattachement. Ilscomprennent audits techniques, anciennesréceptions, index04W etdesrapports de compétencesd’unprojettiersarchivé pourétude11. Ces derniers ne sont PASdesexécutionsJARVIS. Aucun rapportprojetPDF/DOCXsupplémentaire n’aété retrouvéparcette recherchedenoms ; aucun troudenumérotation n’estcomblé parhypothèse. Les contenusbruts depreuves etjournauxrestentprivés.

[Rapports récupérés sur JARVIS]( ../historique/README.md ) : 100 documents historiques repris avec provenance et expurgation.
