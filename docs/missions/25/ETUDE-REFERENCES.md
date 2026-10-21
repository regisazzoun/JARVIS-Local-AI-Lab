# Étude des références et interopérabilité

Sources consultées réellement le21 octobre2026 via GitHub, code téléchargé en espace privé sans exécution. Commits, licences et empreintes des fichiers consultés : [REFERENCES.json](REFERENCES.json). Aucune portion de code tiers n'a été importée dans notre moteur.

| Projet | Architecture observée | Choix pour notre laboratoire |
| --- | --- | --- |
| [Grominet95/jarvis-OS](https://github.com/Grominet95/jarvis-OS) | Registre de classes Python, ABI publique `skills.*`, cycle de vie SQLite distinct du chargement, candidats et essais avant promotion ; licence AGPL-3.0. | Retenir versionnement/états/tests/provenance ; conserver notre backend/broker et écrire une implémentation indépendante. Sa promotion humaine n'est pas reprise : le propriétaire a autorisé la mission complète. |
| [Grominet95/jarvis-skills](https://github.com/Grominet95/jarvis-skills) | Standard de skills conversationnels `skill.yaml` + classe Python et éventuels outils, schéma machine, prérequis applicatifs ; licence MIT. | Ajouter des étapes et vérifications exécutables aux métadonnées ; ne pas confondre injection d'un prompt et opération démontrée. |
| [sosoj92/jarvis-assistant-vocal](https://github.com/sosoj92/jarvis-assistant-vocal) | Adaptateur MCP dérivé du registre, journal dédié, transports stdio/HTTP, filtrage d'exposition ; licence MIT. | Conserver une seule source de schémas et d'exécution ; utiliser SDK officiel compatible avec notre version, stdio local et habilitations JARVIS existantes. |

## Fusion360 — étude, aucune activation fictive

Le skill tiers consulté cible macOS/Windows et requiert Fusion ouvert avec l'add-in FusionMCP. Il enveloppe des scripts Python Fusion et la lecture/capture de document ; sa présence dans un catalogue ne fournit ni application CAD ni instance accessible à JARVIS sur Debian. Le fichier manifeste indique un add-in séparé `faust-machines/fusion360-mcp-server` ; il n'a pas été installé ni validé dans cette mission.

Pour une mission mécanique future : identifier un poste macOS/Windows effectivement accessible, installer/vérifier Fusion et son API/add-in sur ce poste, relier un adaptateur distant autorisé, tester d'abord un document dédié, puis comparer géométrie/dimensions et export. Les capacités génériques SSH/MCP développées ici préparent ce raccordement. Aucun dessin ou export Fusion n'est revendiqué et aucune présence de Fusion sur Debian n'est supposée.

Autodesk confirme l'absence de support natif Linux dans sa [fiche officielle](https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Is-there-any-way-to-install-Fusion-360-in-Linux.html) ; les scripts/add-ins sont décrits dans son [manuel API](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/WritingDebugging_UM.htm). La page dynamique `help.autodesk.com/view/fusion360/ENU/?guid=GUID-FB144260-1E4C-4DD5-ABE6-9E7F2026F661` n'a pas été accessible par l'outil web ; aucune lecture de son contenu n'est prétendue.
