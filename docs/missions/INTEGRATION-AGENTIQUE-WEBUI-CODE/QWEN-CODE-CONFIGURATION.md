# Qwen Code : tours, objectifs et contrats du fournisseur

Version installée : **0.26.4**. Lanceur : `/home/adminjarvis/.local/bin/qwen-local`. Le modèle reste `qwen3-coder-next:q4_K_M`, sur Dell1, via le relais local8091. Les espaces acceptés sont les projets dédiés historiques et `/var/lib/jarvis/projects/qwen-code/<projet>`.

## Origines constatées

1. Le lanceur imposait `--max-session-turns 12`, `--max-tool-calls 12` et une durée de dix minutes. Modifier le seul fichier utilisateur ne pouvait pas annuler ces arguments CLI.
2. La même commande excluait explicitement `get_goal` et `update_goal`. Leur refus était une règle locale de lancement, pas une absence de capacité du modèle.
3. `--bare` appelle `createMinimalSettings()` dans cette version : les réglages utilisateur de contexte étaient ignorés. `/context` affichait effectivement200000tokens avant correction, contre32768 demandés dans le fichier.
4. Le relais renvoyait du SSE même pour `stream=false`. Il ne transmettait pas non plus `response_format` au champ Ollama `format`. Le vérificateur Goal pouvait recevoir un contrat de réponse incorrect.
5. Le pilote Qwen Code ne génère les schémas JSON que pour l’endpoint OpenAI officiel. Un correctif ciblé active ce contrat pour l’adresse exacte du relais local, qui sait désormais le traduire.
6. La compression partageant le cache de la conversation emportait les onze définitions d’outils dans une requête de résumé. Les traces privées montrent notamment une requête de30698octets, refusée avant inférence. Le profil local désactive ce partage pour utiliser le chemin de compression sans les schémas inutiles.

## Configuration déployée

- `--max-session-turns=-1`, `--max-tool-calls=-1` ; aucune limite de durée de session dans le lanceur interactif.
- Outils Goal autorisés. Le prompt distingue l’objectif natif actif d’une tâche ordinaire, qui se termine par une réponse factuelle.
- MCP fourni explicitement par `~/.qwen/jarvis-mcp.json`.
- Profil local explicite : fenêtre32768tokens, déclenchement précoce de compression à0,18. Le plafond conservateur de transport27648octets et la sortie4096tokens restent inchangés. Octets et tokens ne sont pas assimilés.
- Deux correctifs de compatibilité versionnés sous `tools/qwen_webui/patch_*.py`, limités à0.26.4 et au fournisseur loopback. Ils conservent les sauvegardes du paquet installé ; un changement de version doit être revu.
- Une délégation automatisée possède un budget technique de660secondes par appel. Ce budget de travail est distinct de la suppression du plafond de tours d’une session. Le timeout conserve un résultat inconnu et n’autorise pas une réexécution aveugle.

Les processus ouverts avant les modifications conservent leurs paramètres. Ils ne sont pas arrêtés arbitrairement ; relancer `qwen-local` dans un projet autorisé charge le nouveau profil.

## Réception et limites

Les traces originales des sessions A/B/C/D/E et des objectifs sont conservées. A a dépassé douze tours mais a nécessité un rappel pour terminer sa dernière étape. B/C ont révélé les problèmes de transport et ne sont pas reclassées comme réussies. D a réalisé les quatorze avances et un appel MCP en18tours. Les derniers essais du profil final sont consignés dans `PREUVES-JARVIS.json` et `TESTS-BOUT-EN-BOUT.md`.

Le premier objectif natif a été clôturé puis relu dans une nouvelle invocation. Le second conserve ses échecs et refus : les raisons prétendant qu’aucune correction n’avait été effectuée ont été rejetées à juste titre. Une assistance Codex a rappelé l’historique factuel. Ne pas assimiler ce cas à une correction spontanée du compte rendu.

Références primaires : [réglages Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/), [Goal Runtime](https://qwenlm.github.io/qwen-code-docs/en/users/features/goals/), [API Ollama](https://docs.ollama.com/api/chat). Les constats de version reposent également sur le code du paquet réellement installé.
