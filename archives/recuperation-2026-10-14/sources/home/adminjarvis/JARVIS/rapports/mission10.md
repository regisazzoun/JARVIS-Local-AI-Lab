# JARVIS — Mission 10

12 octobre 2026. **Qwen utilisable dans Open WebUI ; meilleure couverture du diagnostic, sécurité encore insuffisante.**

- **Compatibilité / installation : OK**, Ollama **0.40.3 conservé**, aucune mise à jour nécessaire. Modèle officiel [qwen3.5:27b-q4_K_M](https://ollama.com/library/qwen3.5:27b-q4_K_M), 26,9B, manifeste `64ae5b1d651f`, environ 17,5 Go téléchargés avec vérification SHA par Ollama. Aucun modèle existant supprimé.
- **GPU : OK**, RTX 3090, pilote 595.91.07, contexte **8192**, **65/65 couches GPU**, `ollama ps` **100% GPU**, API `size_vram=size`. Buffer hôte accessoire 682 Mio ; aucune couche déportée sur CPU. VRAM totale maximale observée : **17489 Mio / 24 576 Mio** ; température **74 °C**, puissance **349.99 W**. Surveillance environ 0,25 s, aucune anomalie observée.
- **Génération : 37,99 tokens/s sans document ; 37,78 avec document**, raisonnement interne compris. Réponses complètes (`stop`), durées totales **55,2 s / 61,0 s**. Le premier calcul court avait coûté 56,8 s chargement compris ; son débit froid de 7,47 tokens/s ne représente pas les essais suivants.

| Modèle | Sans document /100 | Avec mission06.md /100 |
|---|---:|---:|
| Llama 3.1 8B — moyenne Mission 08 | 34,7 | 54 |
| Ministral 3 14B — moyenne Mission 08 | 60 | 53,3 |
| Qwen 3.5 27B — un essai par condition | **62** | **74** |

Prompt exact et système commun Mission 08, document intégral injecté comme données, graine 42. Même grille 20/25/15/20/10/10, revue subjective non aveugle ; vitesse exclue des notes. Qwen utilise ses [paramètres natifs de raisonnement](https://huggingface.co/Qwen/Qwen3.5-27B) : température 1, top_p 0,95, top_k 20, min_p 0, presence_penalty 1,5, repeat_penalty 1, budget 4096. Les différences de réglages et un seul essai Qwen limitent la comparaison ; aucun benchmark Llama/Ministral relancé.

**Incidents qualitatifs :** sans document, Qwen propose explicitement de supprimer le volume Open WebUI : violation de conservation des comptes/conversations/documents. Tag `llama3` inadapté au modèle testé, référence d’image incorrecte et causalités trop affirmatives. Avec document, volume préservé mais règle de compatibilité WebUI/Ollama inventée, seuil de température de génération abusivement causal et rollback sans revue des migrations. Aucune commande suggérée exécutée ; aucune réinstallation de pilote recommandée. Petit essai initial avec fragment chinois ; essais WebUI à 64/512 tokens coupés pendant le raisonnement, puis validation avec le budget normal réussie : **17 × 23 = 391**, fin naturelle.

**Profil ajouté : JARVIS — Qwen 3.5 27B Qualité**, raisonnement activé, paramètres natifs ci-dessus, instruction générale de conservation renforcée. Cette instruction n’est pas une garantie et n’a pas servi à améliorer rétroactivement les notes. Profils précédents vérifiés identiques, Llama reste par défaut, un modèle chargé à la fois. Aucun changement Docker, comptes, conversations, noyau, GRUB ou pilote ; aucun redémarrage Debian.

**Recommandation :** utiliser Qwen comme assistant consultatif pour les diagnostics documentés, avec revue humaine des commandes ; conserver Llama par défaut. Amélioration indicative avec document, supériorité générale non démontrée, administration autonome déconseillée.

Réponses intégrales, raisonnement interne, requêtes, métriques et sous-notes : [mission10-preuves](mission10-preuves/), notamment [reponses-et-notes.md](mission10-preuves/reponses-et-notes.md) et `evaluations-qwen.json`. Profils avant/après archivés ; retour arrière applicatif limité à la suppression du seul profil Qwen via l’interface, sans supprimer ses poids ni modifier les autres profils.
