> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS/rapports/mission07.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# JARVIS — Mission 07 : compréhension, raisonnement et contexte conversationnel

12 octobre 2026 — **Amélioration démontrée sur les tests, sans changement de poids/modèle ; limites de raisonnement persistantes.** La configuration finale est appliquée et vérifiée dans Open WebUI après redémarrage applicatif. Aucun redémarrage Debian ni changement des pilotes, du noyau, de GRUB/EFI/initramfs ou de PCIe.

## 1. Résultat pratique

Recharger Open WebUI : le même ID `llama3.1:8b` porte maintenant le nom **JARVIS — Qualité (Llama 3.1 8B)**. Une surcouche de paramètres Open WebUI a été créée pour le modèle natif existant ; aucun autre modèle, aucun nouveau poids et aucun téléchargement de modèle. Les messages/conversations sauvegardés ne sont pas réécrits.

Réglages retenus : **num_ctx=8192, temperature=0.1, top_p=0.9, num_predict=2048**, instruction qualité renforcée. Récupération documentaire : **top_k=8**, passages ajoutés au message système, question utilisateur conservée séparément, réécriture automatique des recherches désactivée. **La recherche par embeddings et les pièces jointes restent utilisables** ; le mode texte intégral reste disponible pour un fichier si choisi. Pas de réindexation ni suppression de documents.

Le test de mémoire retrouve cinq contraintes sur cinq après dix tours à 8K, contre zéro à 4K dans la séquence longue utilisée. Le chemin RAG corrigé retrouve la version 0.12.0 et le débit 70,53 tokens/s là où le chemin documentaire initial échouait. Le diagnostic de signature interprète correctement les preuves ultérieures de chargement/CUDA. Ce n’est pas une garantie générale : le modèle ne pose pas toujours une clarification et peut encore attribuer une valeur à la mauvaise opération ou recommander une mauvaise prochaine étape.

## 2. Sauvegarde, état initial et données conservées

Sauvegarde complète avec le mécanisme 06 : **/home/adminjarvis/JARVIS/open-webui/sauvegardes/20261012-185912**. Base arrêtée pendant l’archivage, puis conteneur relancé. SHA-256 vérifiés, tar lisible avec webui.db et données ; comptes, clés, conversations, fichiers et index sauvegardés. Unités actives et API show du modèle conservées séparément dans les preuves, avec paramètres, template, instructions et environnement. Sauvegardes intermédiaires avant les changements RAG et le profil ; sauvegarde finale **20261012-192850** avec les réglages et données actuels.

Répertoire de preuves mode 0700, captures privées. Ne pas publier db-avant-prive.json, db-apres-prive.json, rejeu-prive.json ou transmissions-privees.jsonl : ils peuvent contenir du texte de conversations/documents. Aucun jeton HTTP ou clé WebUI imprimé dans les sorties ou ce rapport.

Initialement : 4 conversations, 1 fichier, aucune entrée config persistée, aucun profil de modèle personnalisé, aucune base Knowledge et aucune fonction/pipeline enregistré en base. Paramètres utilisateur : version de l’interface, sans température/contexte/prompt système personnalisé. Conversation documentaire : custom_params vide. Paramètres applicatifs stockés en base bien examinés, pas seulement le fichier Compose. ENABLE_PERSISTENT_CONFIG=false concerne les réglages Config, **pas la persistance des profils Model** ; le profil final est bien conservé en base malgré cette option.

Paramètres effectifs de référence : contexte serveur **4096**, modèle GGUF Llama 3.1 8B Q4_K_M, pas d’instruction système native. Options par défaut de cette version Ollama : temperature=0.8, top_p=0.9, top_k=40, num_predict=-1, num_keep=4, seed=-1, repeat_penalty=1.0, repeat_last_n=64, num_batch=512. Le modèle définit ses stop tokens. Les requêtes documentaires rejouées n’imposaient pas d’options de génération supplémentaires. Aucun plafond 256 tokens persisté retrouvé ; les 256 de Mission 06 étaient une option de test, non un réglage général. [Valeurs de la version Ollama 0.40.3](https://github.com/ollama/ollama/blob/v0.40.3/api/types.go).

Pendant la mission, deux conversations et un fichier supplémentaires sont apparus. Les scripts Mission 07 n’appellent aucune API d’écriture de chat/fichier. Les quatre conversations initiales conservent **tous leurs messages et contenus à l’identique** ; seul last_read_at d’une conversation a changé. Le fichier initial est identique. Le rollback préparé restaure seulement les paramètres, sans remplacer la base par l’ancienne sauvegarde et sans effacer les ajouts intervenus pendant la mission.

## 3. Diagnostic de transmission et des 2050 tokens

Six réponses de la conversation existante ont prompt_eval_count/input_tokens **2050**, avec un contexte serveur 4096. Ce constat seul ne suffisait pas. Les journaux apportent une preuve distincte : par exemple à 18:46:47, **truncating input prompt, limit=2050, prompt=6551, keep=4, new=2050**. D’autres occurrences conservées attestent la même réduction.

Le code de cette version explique cette limite : en cas de dépassement, il conserve num_keep et réduit le prompt selon **num_ctx − floor((num_ctx−num_keep)/2)** ; avec 4096 et 4, cela donne **2050**. Ce n’est pas une mystérieuse limite de lecture documentaire ni le nombre maximal de tokens de sortie. La suppression de messages anciens lors de la préparation d’un long historique constitue aussi un mécanisme distinct : le test 4K perd les faits du premier tour alors que l’API reçoit l’historique fourni. Un indicateur final `truncated=0` du runner ne réfute pas une réduction préalable du prompt. [Implémentation Ollama 0.40.3](https://github.com/ollama/ollama/blob/v0.40.3/llm/llama_server.go).

Une capture temporaire en boucle locale a enregistré les corps réellement envoyés d’Open WebUI à Ollama, sans journaux d’en-têtes/secrets. Le proxy a relayé vers 11434 et a été retiré à la fin. Sur le rejeu d’une chaîne existante : **11 messages transmis**, mêmes rôles ; les dix premiers contenus restent identiques. Sans fichier, dernier message de 137 caractères ; avec RAG, dernier message de 3286 caractères incluant les sources et la question. Ce rejeu précis donne 1114/1966 tokens d’entrée, pas 2050 : il ne reproduit pas à l’identique les anciens prompts et n’autorise pas à localiser chaque élément historiquement perdu.

Dans la configuration initiale, les passages RAG étaient placés **dans le dernier message utilisateur**, via un template contenant aussi la question. Ce n’est pas un effacement global de l’historique : la question est réinsérée, mais entourée de contexte documentaire. Une requête supplémentaire générait les recherches à partir de la conversation récente. Les fichiers persistants attachés déclenchent ce traitement à chaque tour ; aucun pipeline personnalisé n’explique les répétitions. La compaction automatique Open WebUI est désactivée par défaut, sans override en base : aucun résumé automatique opaque établi ici. [Traitement Open WebUI v0.12.0](https://github.com/open-webui/open-webui/blob/v0.12.0/backend/open_webui/utils/middleware.py).

Paramètres RAG initiaux : top_k=3, chunk_size=1000, overlap=100, seuil=0, recherche hybride désactivée, full_context=false, génération des recherches activée, RAG_SYSTEM_CONTEXT=false. Des requêtes larges récupéraient des passages sans les chiffres demandés : JARVIS concluait à tort que le rapport ne contenait pas de mesures. Avec l’instruction qualité, la réécriture des recherches coûtait parfois ~15 secondes sur un simple tour de mémorisation. Les réponses génériques ont donc plusieurs causes : couverture documentaire, emballage du prompt, réduction du contexte et limites du modèle lui-même.

Les métriques des anciennes réponses sont présentes dans les chats/export, **pas automatiquement dans les messages role/content reçus par Ollama**. Le modèle ne peut pas connaître sa durée précédente par introspection. Quand on lui transmet les métriques de la requête concernée, il peut répondre avec ces valeurs ; sinon il doit indiquer l’inconnu. prompt_eval_duration couvre le traitement du prompt complet, pas séparément la lecture/extraction du document.

## 4. Batterie et méthode de notation

**296 appels principaux** : 140 pour A–G, 20 pour H, 20 pour la référence réelle A0, 64 pour la comparaison WebUI avant correction, 52 après correction. S’y ajoutent le rejeu diagnostique, les appels internes de génération de recherches et les validations finales. Prompts exacts, historiques, réponses, métriques et paramètres conservés dans les JSON ; les conversations existantes n’ont pas servi à enregistrer les tests.

Les demandes restent les mêmes pour les configurations comparées. Exceptions méthodologiques explicites : les deux durées fournies dans le test 2 proviennent de la requête précédente propre à la configuration ; les réponses de programmation/mémoire sont réintroduites naturellement dans les tours suivants. Les tests indépendants repartent d’un historique neuf ; seuls les enchaînements document→durée, code→modification et dix tours de mémoire partagent leur contexte. Le cache peut changer les temps de traitement, pas les conversations de test.

A–H utilisent seed=42 pour limiter la variabilité ; ce contrôle est une différence avec la référence quotidienne. **A0** reprend les options initiales, seed=-1, sans instruction : il perd aussi les cinq faits et en invente d’autres. A0 est conservé comme contrôle réel, sans le mélanger au classement à graine fixée. Une seule réalisation par configuration, évaluation non aveugle, pas de validation indépendante. Une activité utilisateur simultanée est attestée par les ajouts en base ; les temps muraux peuvent inclure de l’attente, même si les historiques de test restent distincts : les notes sont un outil comparatif, **pas des mesures parfaitement objectives ou une certification de raisonnement**.

| Test | Critères vérifiables | Points |
|---|---|---:|
| 1 Document mission06 | Trois résultats correctement attribués (6), deux limites réelles (6), prochaine étape cohérente (3) | 15 |
| 2 Durées | Inconnu sans métriques (5), deux durées correctes lorsqu’elles sont fournies (5), lecture documentaire distincte du traitement du prompt (5) | 15 |
| 3 Autocorrection | Compare demande/réponse (5), reconnaît l’erreur (5), donne 1.392528 s (5) | 15 |
| 4 Mémoire, dix tours | Alias NOEUD-CERISE, 730 euros, 42 minutes, redémarrage interdit, ZEBRE17 : 4 points par fait exact | 20 |
| 5 Avec/sans document | Pas d’UUID inventé sans source (5), version 0.12.0 et débit 70.53 avec document (2.5 chacun) | 10 |
| 6 Ambiguïté | Question de clarification pertinente (5), aucune durée inventée (5) | 10 |
| 7 Programmation | Somme paire inclusive correcte (5), ValueError pour n négatif sans régression (5) | 10 |
| 8 Journal | Distingue warning de signature et chargement/CUDA réussis ; pas de correction injustifiée | 5 |

Le test de mémoire est **volontairement long** : dix tours, annotations neutres de remplissage, environ 5K tokens au dernier tour. Il ne démontre pas que dix échanges courts échoueraient à 4K. Le test de code est contrôlé par AST restrictif puis assertions dans un processus limité : total_pairs(0,1,2,4,5) = (0,0,2,6,6), et ValueError pour −1. Aucune recommandation système générée par le modèle n’a été exécutée.

Le script evaluer.py produit des propositions lexicales/numériques. Le classement final corrige manuellement la fidélité documentaire : 391 attribué au crible au lieu de la multiplication, observation positive présentée comme limite, moyenne/temps mal nommé, prochaine étape impropre. F perd deux points pour les commentaires qui annoncent total_pairs(10)=55 alors que le résultat est 30, malgré des fonctions correctes. Les raisons et sous-notes sont dans scores-finaux.json ; les sous-critères lexicaux peuvent encore manquer une nuance, ce qui limite la précision des totaux.

## 5. Comparatif et choix

| Configuration | Description | Note /100 | VRAM maximale relevée, MiB | Débit médian, tokens/s |
|---|---|---:|---:|---:|
| A | 4K, valeurs initiales | 60 | 5190 | 70.61 |
| B | 8K, valeurs initiales | 81.5 | 5824 | 70.41 |
| C | 16K, valeurs initiales | 81.5 | 6864 | 70.29 |
| D | 8K, température 0,3, sortie 2048 | 84.5 | 5824 | 70.15 |
| E | 8K, température 0,1, sortie 2048 | 80 | 5824 | 70.23 |
| F | D + instruction proposée | 81.5 | 5824 | 69.72 |
| G | E + instruction proposée | 88.5 | 5824 | 67.76 |
| H | E + instruction renforcée | 93 | 5824 | 69.23 |

Les paramètres non mentionnés restent constants, dont top_k et répétition ; D/E ajoutent le plafond de sortie demandé de 2048, pas seulement une température différente. F/G évaluent d’abord l’instruction proposée sans renforcement. H ajoute des règles générales : ne pas remplacer une question précise par un résumé, clarifier un référent manquant, distinguer résultats/limites/recommandations, lire la chronologie des logs et vérifier les exemples de code. Aucun chiffre de réponse attendu ou formule du test n’a été ajouté au prompt système.

| Configuration | Doc /15 | Durées /15 | Correction /15 | Mémoire /20 | Doc présent/absent /10 | Ambiguïté /10 | Code /10 | Journal /5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 7.5 | 15 | 15 | 0 | 7.5 | 5 | 10 | 0 |
| B | 9 | 15 | 15 | 20 | 7.5 | 5 | 10 | 0 |
| C | 9 | 15 | 15 | 20 | 7.5 | 5 | 10 | 0 |
| D | 12 | 15 | 15 | 20 | 7.5 | 5 | 10 | 0 |
| E | 12.5 | 10 | 15 | 20 | 7.5 | 5 | 10 | 0 |
| F | 8.5 | 15 | 15 | 20 | 10 | 5 | 8 | 0 |
| G | 8.5 | 15 | 15 | 20 | 10 | 5 | 10 | 5 |
| H | 13 | 15 | 15 | 20 | 10 | 5 | 10 | 5 |

**H retenue.** 8K améliore la conservation des faits ; l’instruction renforcée corrige le test de chronologie et conserve les fonctions Python correctes. La température 0.1 seule n’est pas supérieure sur toutes les tâches et ne crée pas une capacité de raisonnement : E reste inférieur à D sur cette batterie. F/G apportent la réponse documentaire précise mais conservent des erreurs de diagnostic ; F ajoute un exemple numérique faux. H reste imparfaite, notamment sur l’ambiguïté (5/10 au lieu de 10).

16K tient intégralement sur le GPU, environ 6864–6870 MiB relevés, sans débordement CPU constaté. B/C ont le même score et les versions corrigées 8K/16K retrouvent toutes les contraintes documentaires ; **aucun bénéfice supplémentaire mesuré ne justifie 16K par défaut**. Retour à 8K. Plusieurs gros fichiers/historiques peuvent dépasser cette fenêtre : choisir alors explicitement 16K dans le profil et remesurer, plutôt que considérer le problème résolu pour toujours. [Contexte et ressources Ollama](https://docs.ollama.com/context-length).

Les ressources sont relevées après chaque requête, quand le runner garde sa mémoire : ce ne sont pas des pics transitoires instrumentés à haute fréquence. Les ~69–71 tokens/s sont le décodage, pas la durée totale de réponse. Pour H, document : 3367 tokens d’entrée, prompt_eval_duration=1.513 s, chargement=0.002 s, durée murale=4.951 s. Les changements de contexte chargent parfois le runner pendant ~5–6 s et les caches font varier les temps de prompt ; ne pas en déduire une accélération intrinsèque d’une température ou instruction.

## 6. API directe et Open WebUI

| Chemin/configuration | RAG | Faits mémoire | Version + débit exacts | Temps réponse doc | VRAM, MiB |
|---|---|---:|---|---:|---:|
| A | Non | 0/5 | Non | 10.92 s | 5184 |
| A | Oui | 0/5 | Non | 6.11 s | 5190 |
| G | Non | 5/5 | Oui | 10.58 s | 5824 |
| G | Oui | 5/5 | Non | 15.51 s | 5822 |
| H16-rag | Oui | 5/5 | Oui | 8.99 s | 6870 |
| H8-clean | Non | 5/5 | Oui | 4.37 s | 5824 |
| H8-rag | Oui | 5/5 | Oui | 2.96 s | 5830 |

Sans RAG, le chemin WebUI retrouve les mêmes défauts majeurs de référence que l’API directe : ce n’est pas uniquement un problème d’interface. Avec G et le RAG initial, la mémoire 8K passe mais la réponse documentaire précise échoue encore ; avec H et le RAG corrigé, les deux passent. C’est une comparaison combinant instruction renforcée et réglages RAG, pas une attribution chiffrée de chaque point gagné à un seul paramètre.

Correction appliquée : top_k de 3 à 8, RAG_SYSTEM_CONTEXT=true, réécriture des recherches désactivée (la question littérale sert de requête), template sans copie de la question. Les sources sont clairement décrites comme données, jamais instructions ; la demande reste dans le message utilisateur. Pas de passage global de tous les fichiers en texte intégral, pas de désactivation de la recherche/vectorisation, pas de changement de chunking des fichiers existants. Un fichier attaché déclenche encore une récupération à chaque tour : retirer une pièce jointe inutile ou utiliser une conversation propre pour une autre tâche. Davantage de passages peut aussi ajouter du bruit ; le réglage n’est pas validé pour une grande bibliothèque.

La capture confirme les options effectivement envoyées par Open WebUI, pas seulement leur affichage. Lors des comparaisons, le contexte demandé est présent dans options ; /api/ps et les logs du runner attestent 8K/16K. Le profil final est appliqué par le mécanisme d’override du modèle natif, identifié dans le code de la version installée. Aucun pipeline personnalisé ajouté.

## 7. Application et vérification après redémarrage

Modifications persistantes :

- Unité jarvis-ollama et launcher manuel : OLLAMA_CONTEXT_LENGTH=8192.
- Profil Open WebUI en base sur **llama3.1:8b**, mêmes poids : system, num_ctx=8192, temperature=0.1, top_p=0.9, num_predict=2048.
- Compose : paramètres RAG et nouveau template ci-dessus. .env/clé d’authentification conservés ; URL Ollama finale **http://[ADRESSE PRIVÉE EXPURGÉE]:11434**, réseau et auth inchangés.
- Instructions, tests, documentation et script de rollback créés dans le répertoire utilisateur.

Le premier essai d’application du profil a échoué sur un refus de connexion pendant l’initialisation de WebUI après sauvegarde ; le profil n’avait pas été créé. Les tests de cet essai sont conservés à part, non comptés comme validation finale. Reprise après health disponible, création réussie, redémarrage des applications et nouvelles vérifications.

Après redémarrage : requêtes sans options ni instruction explicites dans le client, profil chargé depuis la base ; corps transmis à Ollama contient **8192/0.1/0.9/2048 et l’instruction complète**. Version/débit du document exacts ; avertissement signé correctement distingué d’une panne ; demande graphique reçoit un tableau/textuel sans affirmation d’outil exécuté. Après retrait du proxy et nouvelle recréation du conteneur, réponse réelle **« 1.392528 secondes. »** et contexte chargé 8192. Le proxy ne reste pas une dépendance de démarrage.

Ollama natif n’a pas de réglage global magique de température/instruction : son défaut de contexte est 8K, mais un client direct doit fournir les paramètres qualité et le message système. Dans WebUI, le profil impose les paramètres aux prochains appels sur ce même modèle, sans modifier les textes sauvegardés ; pour un nouveau benchmark WebUI de référence, il faut sauvegarder puis désactiver temporairement cet override et restaurer les réglages initiaux. La batterie API directe reste reproductible sans modifier le profil WebUI.

## 8. Restauration sans perte des conversations

```bash
cd /home/adminjarvis/JARVIS/open-webui
python3 restaurer-mission07.py                 # montre seulement le plan
python3 restaurer-mission07.py --appliquer     # retour aux paramètres antérieurs
```

Le script vérifie que le profil n’a pas été modifié depuis la mission, sauvegarde l’état courant, supprime uniquement l’override Open WebUI via son API (pas le modèle Ollama), restaure Compose original, unité et launcher 4096, puis redémarre les seules applications. Il ne remplace jamais webui.db ni les fichiers uploadés. Le mode plan a été exécuté ; le rollback réel n’a pas été exécuté pour conserver la configuration retenue.

Les archives complètes sont utilisables en cas de récupération de données, mais restaurer aveuglément la base initiale ferait perdre les nouveaux échanges/fichiers survenus après cette sauvegarde. Toujours archiver l’état courant et décider séparément d’une restauration complète. Réversibilité vérifiée par lisibilité/hashes, snapshots, existence des anciennes configurations, test de persistance et lecture du code des API ; pas de test destructif sur les données actives.

## 9. Limites et recommandations

- Gain net mesuré : mémoire longue et précision documentaire, pas intelligence générale démontrée. Notes 60→93 sur une batterie exploratoire, graine unique et critères mixtes ; un jeu indépendant est nécessaire pour confirmer la généralisation.
- L’ambiguïté n’est pas complètement corrigée : plusieurs variantes disent ne pas savoir sans poser la question attendue. H peut encore confondre une moyenne avec une mesure du test 2 ou proposer de redémarrer le mauvais composant dans un résumé. Vérifier les recommandations techniques.
- Les métriques temporelles ne sont pas automatiquement accessibles au modèle ; aucun découpage « lecture du document » inventé n’est justifié. Les fournir depuis la réponse concernée si nécessaire.
- Fenêtre 8K finie ; pas de mémoire durable commune entre conversations créée. Les conversations persistantes ne signifient pas que tous leurs tokens seront toujours transmis/traités, et un ancien contexte déjà perdu dans une réponse ne peut pas être réparé rétroactivement.
- Instructions et température ne créent pas un mode de raisonnement interne. Si la compréhension reste insuffisante, comparer un modèle instruct/raisonnement plus capable dans une mission séparée, compatible avec les 16 Go et évalué sur les mêmes tests plus un jeu inédit. **Aucun autre modèle installé ici.**

SSH/SDDM/GNOME et Intel restent fonctionnels, GNOME PID 1270, noyau T2 et dix modules NVIDIA inchangés. Services applicatifs actifs/enabled ; Core conservé branché ; inhibition temporaire de test levée. Maintenir le contournement de démarrage sans Core. Les preuves privées, grille détaillée, prompts et réponses sont dans mission07-preuves (référence locale historique non publiée).
