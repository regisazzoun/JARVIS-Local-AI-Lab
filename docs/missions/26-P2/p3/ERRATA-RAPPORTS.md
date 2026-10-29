# Errata et attribution des rapports P3

Le premier rapport final JARVIS est conservé dans JARVIS-RAPPORT-ORIGINAL-1.md ; sa révision demandée55297 est JARVIS-RAPPORT-CORRIGE.md, empreinte7f6976b0aa9442baeb8149c5aa073e878e2dd95ccca8c85023040c76f4a65a0c.

| Affirmation ambiguë ou erronée | Fait vérifié |
|---|---|
| Dell2 stdout859999octets | Reçu55210 : stdout283octets ; le FICHIER contient859999octets. |
| 55057 exécutait Core.ollama | Lecture réelle via cat surDell1 ; stdout219000octets. Core.ollama est une méthodePython, pas un binaire. |
| 55238 est le grandstdout219000 | Sa sortie réelle fait2087octets. Le grandstdout complet est55057, vérifié par le reçu complet et sonSHA. |
| Checkpoint54911 fait passer lesPID |54911 enregistre ;54915 redémarre ;54930 est la reprise réelleJARVIS. |
| SHA5ad719f6 du «rapport canonique» | C'est le rapport de TÂCHE P3-02-run. Le rapport FINAL corrigé vaut7f6976b0… ; les deux sont conservés. |
| Codex55251 est l'acceptation croisée native | Codex55251 est le contrôle indépendant du fichier/non-duplication ; la validation croisée nativeQwen est référencée séparément dans RECEPTION-P3.json. |

Attribution : Codex développe le garde, corrige interfaces/pipefail/isolation, exécute67tests logiciels et contrôles indépendants, restreint temporairement les outils pour sortir des lectures stériles. JARVIS/Qwen80B choisit et écrit ses programmesPython, exécute surlesdeuxDell, demande son checkpoint, reprend après le vrai redémarrage et rédige ses rapports. Les interventionsCodex ne sont pas des autocorrections du modèle. La non-duplication reçue concerne le seul effetDell2 observé ; aucune idempotence universelle n'est annoncée.
