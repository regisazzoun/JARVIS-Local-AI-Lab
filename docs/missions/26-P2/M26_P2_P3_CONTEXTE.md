# P3 — contexte, état du 27 octobre 2026

**EN COURS — NON VALIDÉ.** P2 historique reçu avec réserves, événement52932 ; P3 réellement transmise à JARVIS dans la continuation native `9e4a61d6faea4b73ad31251e72dcf7c1`. P4 attend la réception P3.

## Mécanismes Codex déployés

`mission_context_budget.py` protège le vrai chemin `Core.ollama` des missions. Capacité effective lue dans `/api/ps` et comparée à la configuration :24576 ; maximum théorique262144 distinct. Les endpoints de tokenisation essayés retournent404. Le budget utilise les octets UTF-8 comme estimation prudente, explicitement distincte des tokens mesurés par le backend. Réservation réponse4096 et marge1024 dans ce déploiement. Le `prompt_eval_count` réellement retourné est enregistré séparément.

Avant saturation, requête originale archivée intégralement dans le journal SQLite canonique ; checkpoint structuré (tâche, plan, décisions référencées, modifications, tests, compteurs P2/legacy/interface et effets inconnus) puis reconstruction du contexte actif. Aucun effacement des preuves ni nouvelle base mémoire. Un contrat ou une politique indispensable trop volumineux bloque avant inférence ; les revues structurées volumineuses ne sont pas arbitrairement tronquées et restent une limite explicite.

JARVIS dispose de `context_checkpoint`, `context_resume`, `context_recall` : rappel ciblé par référence numérique et fragment explicite, reprise depuis checkpoint manuel non masqué par les snapshots automatiques. Le modèle peut demander une pause technique ; un superviseur borné à une heure redémarre seulement les deux workers existants après fin des outils, journalise les PID réels et reprend. Aucune validation humaine ajoutée ni redémarrage Ollama.

« Bleue » désigne provisoirement le contexte actif, « verte » l'état opérationnel persistant. Cette correspondance est une convention Codex faute de définition propriétaire retrouvée, pas une décision historique prétendument consultée.

## Premières observations réelles et limites

Événements53562–53564 : archive/checkpoint puis requête passée de31176 à18423octets, sous budget estimé19456. JARVIS a déjà utilisé les nouveaux rappels et observé les ressources des deux Dell. Ces faits prouvent le raccordement, pas encore une mission longue reçue.

Un défaut de première intégration a perdu le dernier résultat outil dans le contexte réduit et entraîné des relectures stériles de checkpoints. Codex a corrigé la priorité de conservation du dialogue outil ; observations originales préservées. Incident de déploiement aussi conservé : rechargement commencé avant fin de copie, import manquant temporaire d'un worker ; mission interrompue pendant l'opération, copie terminée puis rechargement cohérent. Aucun incident attribué à JARVIS.

Quatorze tests logiciels du garde passent ; ils ne constituent pas une démonstration d'autonomie. La reprise réelle après redémarrage, l'absence de doublon distant et la réception croisée P3 restent à contrôler. Le plan initial JARVIS en cinq étapes préparatoires doit être révisé par lui en lots réceptionnables ; Codex ne revendique pas son écriture autonome.

## Preuves

[Lancement réel](p3/LANCEMENT.json), [premiers reçus de déploiement et budgets](p3/DEPLOIEMENT-CONTEXTE.json). Le journal complet reste dans le moteur, même mission et même SQLite. Code et tests sont publiés sur la branche Phase2, pas dans main.

## Relance supervisée et contrôle indépendant

La réduction priorise désormais le dernier résultat réel et la dernière instruction de coordination (ordre corrigé), et identifie les archives automatiques comme preuves de stockage à ne pas recharger récursivement. JARVIS persistait dans les relectures ; Codex a utilisé la barrière existante `authority_disabled_tools` pour demander sa révision de plan, sans écrire les étapes. Deux refus de format sont conservés. JARVIS a produit le plan version2 ; barrière levée automatiquement. Le plan conserve encore un lot préparatoire intitulé achevé, mais son état moteur reste running : ce titre ne constitue pas une réception.

Une mesure backend réelle est enregistrée53836 :4535tokens de prompt, capacité24576 et réponse réservée4096. Un premier contrôle distant JARVIS a réellement exécuté une lecture surDell1, mais affiché troisNone en utilisant des clés inexistantes du JSON. Code retour0 observé, aucune validation sémantique attribuée. Codex a signalé l'erreur de mesure et les noms exacts des champs ; correction du contrôle confiée à JARVIS. Une demande inspect sous le profil test-only a été refusée par schéma, trace conservée. P3 reste NON VALIDÉ, pas de P4 transmis.
