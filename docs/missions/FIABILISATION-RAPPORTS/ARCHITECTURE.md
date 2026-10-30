# Rapports confrontés aux preuves et revue bornée

Suite autorisée au diagnostic du 30 octobre 2026, sans reprise de M26-P4.
Les anciens verdicts restent historiques et ne sont pas réécrits.

## Deux défauts ciblés

1. Le modèle déformait des résultats corrects : codes systemctl, existence d’une unité, nombres, heures et attributions.
2. Un segment de rapport et toutes ses sources dépassaient le budget d’admission, même après un premier découpage.

Le nouveau module `agentic/engine_v2/jarvis/report_claims.py` étend le vérificateur existant. Les reçus, événements, plans, tentatives et empreintes restent dans la base canonique. Aucun nouveau moteur ni stockage de missions.

## Contrôle et rédaction

- Extraction de faits depuis les lectures réellement terminées du broker, y compris leurs codes non nuls. Un refus, timeout ou résultat tronqué ne devient pas une observation réussie.
- Comptages déterministes distincts : unités uniques, commandes exécutées, sorties non nulles. Les lignes `Loaded:` et `Active:` de status demeurent des observations séparées de `is-active`.
- Contradictions fermées contrôlées avant inférence : inversion des codes, nombre incompatible avec une liste, UUID inconnu, reçu associé à la mauvaise unité, heure/code altéré et unité déclarée absente malgré `Loaded: loaded`.
- Les contrôles ne remplacent pas toute interprétation de texte libre. Les autres affirmations passent dans la revue sémantique existante. Un PASS modèle a effectivement été contredit pendant cet essai ; son erratum est conservé.
- La réécriture part des faits structurés, de l’objectif propriétaire et du contrat actif. Le vieux brouillon reste archivé avec son empreinte ; son corps erroné n’est pas réinjecté comme source.
- Le rapport reste rédigé par JARVIS. Codex fournit l’infrastructure et les constats de ses contrôles, pas le texte final présenté comme autonome.

## Revue sous budget

Les passages conservent leurs positions exactes dans le texte original. Chaque ligne de tableau devient un segment avec ses colonnes et sa section. Un lot contient au plus quatre segments ; seules les sources citées ou correspondant aux unités nommées sont jointes. Les agrégats possèdent des références typées explicites. La politique d’autorisation ne prouve pas l’état d’un service.

Le même garde d’admission s’applique à chaque appel. En cas de dépassement, subdivision ; un singleton impossible reste refusé. Toutes les affirmations et références événementielles doivent être couvertes. Aucun PASS global n’est déduit d’une revue partielle.

Fenêtre inchangée : 32768 tokens, réponse réservée 4096 et marge 1024. L’entrée est bornée à 27648 octets UTF-8 sérialisés comme estimation conservatrice, **pas comme mesure exacte de tokens**. Le plafond rédactionnel de 1800 caractères a été porté à3200, puis à8000 après trois refus de textes complets de3852,3279 et4201 caractères. Les refus sont archivés ; cette correction de format ne relève pas la fenêtre d’inférence. La lecture ciblée du vieux brouillon dispose séparément d’une limite de8000octets ; au-delà, son corps ne rentre pas dans le contexte actif mais reste conservé.

## Faux PASS et compteurs

Une nouvelle méthode de coordination `AttemptLedger.rectify_report_success` réouvre un rapport seulement en mission interrompue, avec un FAIL observé plus récent sur le même SHA et le même contrat que le PASS original. L’ancien résultat demeure dans `original_success_result` et les événements originaux restent intacts. L’échec réel est comptabilisé une seule fois. La méthode n’est pas exposée au modèle et ne remet aucun compteur à zéro.

Les profils `atomic_report_review` et `report_rewrite_from_facts` sont activés dans la sonde existante. Les missions non activées conservent leur parcours antérieur ; cette livraison ne réceptionne pas automatiquement tous les rapports historiques ni M26-P4.


## Rédaction avec faits liés aux preuves

Les essais ont confirmé qu’un contrôle sémantique du même modèle peut encore accepter un récit faux. Les PASS92273 et92553 sont conservés avec leurs rectifications92330 et92562. Ajouter une consigne ne suffisait pas.

Le nouvel adaptateur `mission_report_compose` réutilise les mêmes reçus et le même `host_write_file`. JARVIS choisit les références originales complètes et rédige une explication ; le moteur assemble les champs factuels exacts. Chaque unité conserve sortie, code, date et UUID de sa lecture ; les lectures status restent séparées. Le tableau ne confond plus le nombre d’unités avec le nombre d’appels. Son auteur est explicitement JARVIS-engine, avec infrastructure Codex, et non le modèle.

Dans ce profil de photographie de services, le commentaire est consacré aux limites, hypothèses ou contrôles suivants. Les champs numériques, dates, codes et identités de reçus appartiennent au tableau et ne sont pas recopiés dans la prose. Le schéma refuse les chiffres dans le commentaire ; le backend refuse aussi les recomptages de services écrits en lettres. Les autres affirmations passent encore par les contrôles déterministes et la revue sémantique. Ce mécanisme réduit la surface de déformation ; il ne rend pas universellement fiable toute phrase du modèle.

Le texte explicatif original est archivé avant revue. Aucun fichier n’est écrit avant PASS. Le broker existant effectue ensuite une écriture avec son propre reçu enfant et le même compteur persistant. Une nouvelle `mission_verify` relit le fichier réel avant la clôture habituelle. Une interruption survenue pendant une revue empêche une écriture tardive, même si la revue termine avec PASS.

Le contexte propre conserve désormais le dernier refus de schéma et le dernier résultat de composition sous une forme courte, avec références. Une première version de cet adaptateur perdait ce retour lors de la reconstruction du contexte ; cette régression Codex est corrigée et testée. Les sorties et refus originaux ne sont pas effacés. Les contradictions déterministes sont contrôlées avant réutilisation d’un PASS en cache.


## Repli après trois refus : réception factuelle, prose libre réservée

Le modèle n’a pas respecté le contrat qualitatif sur les trois essais autorisés : il recomptait encore les unités, y compris avec des nombres en lettres. Le moteur a refusé ces explications avant écriture et a escaladé. Codex n’a pas relancé une quatrième rédaction libre.

Un mode explicite `proof_bound_explanation_mode=facts_only` impose ensuite une explication vide. JARVIS sélectionne les reçus et déclenche l’écriture du tableau factuel complet par le moteur. Le rapport indique clairement qu’aucune explication libre du modèle n’est publiée. Les autres modes conservent la faculté de rédiger une explication soumise aux contrôles ; ils ne sont pas réceptionnés comme universellement fiables.

Dans ce repli, la validation recompute exactement le rapport depuis les reçus originaux et exige l’événement de préparation avec le même contenu, SHA et ensemble complet de références. Un octet modifié ou une provenance manquante provoque FAIL. Ce n’est pas une approbation du modèle : le vérificateur porte le nom `broker-read+canonical-evidence-render`. Après l’écriture, la même comparaison suit une nouvelle lecture broker du fichier réel.

Les nombres de revues et états de boucle ne sont plus recopiés dans le corps du rapport : ils continuent d’évoluer au fil de sa vérification et restent dans le journal/les preuves. Ainsi, une vérification supplémentaire n’invalide pas mécaniquement le rapport qu’elle vient de lire. Les comptes techniques stables des lectures de service, eux, sont présents et calculés exactement.

**Limite de réception :** ce mécanisme sécurise la publication factuelle de ce profil et le respect du budget. Il ne démontre pas une rédaction libre corrigée de manière autonome, ni la justesse générale des avis du reviewer. Ces réserves ne sont pas levées par le repli.
