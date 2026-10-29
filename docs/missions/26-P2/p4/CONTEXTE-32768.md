# Fenêtre Qwen80B de 32768 tokens — 27 octobre2026

Le propriétaire demande un essai réel à32768tokens, adoption conditionnée à la VRAM, et une limite empêchant les requêtes trop grandes. Il précise que cette fenêtre doit figurer comme objectif de résultat lors du découpage, avant transmission.

## Résultat mesuré

Deux essais Codex sur le Qwen80B existant de Dell1 ont réussi. Le paquet initial a consommé18876tokens de prompt et64tokens de sortie (49,35s, dont16,44s de chargement). Un second essai avec données neutres a consommé26614tokens de prompt et5tokens de sortie (6,98s, préfixe partiellement en cache). Ce dernier temps ne constitue pas une mesure d'une requête entièrement froide. Les réponses de test n'ont déclenché aucun outil.

Le backend annonce une fenêtre effectivement chargée de32768tokens. Les minima échantillonnés de VRAM libre sont1129Mio surGPU0 et1163Mio surGPU1 ; températures maximales observées56°C/62°C sur les deux essais réunis. Pas d'erreur mémoire retournée. Ces essais courts démontrent le fonctionnement de cette allocation, pas une endurance prolongée ni une marge disponible pour un second modèleGPU simultané.

## Politique installée

Profil Dell1 `inference_num_ctx=32768`, `hard_context_limit=32768`. Réponse réservée4096tokens et marge de gabarit1024 : entrée maximale27648tokens. Le profil conversationnel duMac reste16384 et le modèle resteQwen27B. Aucun modèle remplacé.

Le garde existant conserve une estimation conservatrice en octetsUTF-8 sérialisés : il ne s'agit pas d'un tokenizer exact. Il compacte les paquets au-dessous de27648octets estimés, archive les originaux et conserve politiques, exigences, compteurs et prédicats. Cette règle peut encore refuser des entrées qui tiendraient réellement en tokens ; elle privilégie une admission prudente et ne convertit pas arbitrairement les octets par un facteur4. Le premier vrai appel JARVIS repris a envoyé24924octets après compaction, mesurés par le backend à7812tokens, fenêtre32768.

Le routeur effectue un second contrôle avant HTTP, refuse les fenêtres supérieures au plafond, réserve la réponse et la marge, et passe `truncate=false` pour empêcher la suppression silencieuse du contexte par Ollama. Une admission refusée ne peut pas basculer vers leMac pour contourner la règle. Les paquets trop grands doivent être redécoupés ; aucun succès de tâche n'est déduit de la seule taille.

## Critère écrit avant transmission

Les nouvelles missions enregistrent `context_result_objective` dans leur spécification. Leurs plans recopient cette exigence dans le contrat des tâches non reçues, sans réécrire les tâches validées. Chaque paquet d'inférence reçoit aussi ce critère explicitement, avec événement `task_context_result_objective` préalable. PourWP5, le plan a été versionné parCodex avec cette seule exigence supplémentaire, en conservant les six prédicats originaux. Qwen conserve la responsabilité des étapes et des décisions techniques.

## Déploiement et preuves

Les modules ont été installés surleMac et dans les deux copiesDell. Configuration et sources précédentes sauvegardées en privé ; restaurer les fichiers sauvegardés et recharger les services pour revenir en arrière. Workers et service conversation rechargés lors du déploiement ; JL03 demeure actif. Les compteurs de l'escalade de capacité restent à3 ; résolution technique enregistrée sans remise à zéro.

Tests logiciels ciblés :91PASS après la dernière correction de schéma. Contrôles réels Codex sur chaqueDell :22tests de contexte puis15tests de routeur ; après ajout des régressions,23tests de contexte et16tests de routeur. Ces nombres correspondent à des suites successives, pas à un cumul de tests uniques. La restriction d'alias `active:N` a ensuite été explicitée dans le schéma proposé au modèle, car celui-ci reconstruisait incorrectement un contrat depuis le résumé. Les erreurs restent archivées.

La reprise de l'inférence JARVIS est démontrée. JARVIS a ensuite exécuté les six critères par lectures réelles surlesdeuxDell : tousPASS (58724–58759), puis les a répétés une fois (58774–58809) ; cette répétition est conservée et ne constitue pas une preuve supplémentaire d’autonomie. La réception complète deWP5 et du code réellement chargé ne découle pas de cet essai. P4 reste non reçue.

[Mesures et installation](CONTEXTE-32768.json) · [Tests deuxDell](TESTS-GARDE-32768-DELL.json) · [Refus sans contournement](TESTS-GARDE-FALLBACK-32768.json) · [Schéma des références](SCHEMA-REFERENCES-32768.json).

[Reçus natifs JARVIS et tokens réels après reprise](JARVIS-REPRISE-32768.json). SourcesAPI de référence : [Ollama — contrôle et troncature du contexte, version0.40.3](https://github.com/ollama/ollama/blob/v0.40.3/server/prompt.go).
