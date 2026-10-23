# Reprise technique du23 octobre2026

Statut : 🟡 incomplet, retests JARVIS en cours. Ordre explicite du propriétaire : aider JARVIS à se construire et à résoudre les blocages ; aucune validation intermédiaire demandée. AGENTS, charte, mission26B, diagnostic et dernier rapport relus. Autorisations et périmètre conservés ; aucun14A/24-Old/Dell2.

## B : faux rejets du vérificateur

Le contrôleur déterministe comparait toute mention `observations : N` au nombre de reçus techniques. Il rejetait ainsi une citation explicitement erronée (« observations : 999 ») conservée dans l’historique, et confondait deux mesures CSV avec des dizaines de lectures d’outils. Les 98 événements concernés sont recensés dans ERRATA-COMPTEURS.json. Seul ce motif numérique ambigu est rectifié ; les autres erreurs, dont l’identifiant de mission tronqué, ne sont pas annulées. Les événements originaux restent intacts.

Le contrat26b.report.8 réserve les comparaisons déterministes aux métriques explicitement nommées observations_in_scope et plan_versions_count. Les nombres en prose libre passent toujours par la revue sémantique, avec leurs sources et leur référent. Une citation rejetée ne devient pas une nouvelle assertion positive. Les documents déclarés comme sources de contrats report sont exclus des preuves techniques de leur propre contenu ; leur lecture/réécriture ne fait plus croître artificiellement le compteur métier.

## C : documentation acquise et attente externe

JARVIS a validé six tâches locales et produit un rapport final. Le témoin externe reste réellement absent ; l’objectif demandait aussi d’enregistrer le blocage externe. Le moteur n’imposait pas ce dernier résultat. L’ancien rapport est archivé dans JARVIS-RAPPORT-C-AVANT-RECTIFICATION.md et son ancienne transition completed demeure au journal.

Le moteur extrait désormais un contrat de clôture de l’objectif brut, sans produire de tâches : comportement demandé si la ressource externe est indisponible, chemins exacts de l’objectif et citation d’origine. Les derniers reçus de lecture déterminent si le problème est encore observé ; une lecture réussie ultérieure peut lever l’ancien défaut, jamais une déclaration du modèle. La réception finale refuse un résultat externe non résolu. mission_block est disponible après validation des tâches locales et conserve leurs états/empreintes ; un blocage global exige une observation réellement échouée, pas une écriture de rapport.

Le premier retest du contrat25 a encore montré une extraction fautive : le modèle avait choisi report_only malgré « enregistre ce blocage externe ». Le contrat d’exigences26b.7 rejette ce déclassement explicite et demande au modèle de corriger sa propre extraction. Les chemins et la citation restent issus de l’objectif ; Codex n’a fourni aucun plan corrigé.

## A : correction indépendante du récit

La relecture originale trouve que event:13190 est tool_started ; event:13193 et event:14873 refusent l’omission des FAIL et/ou des références, plutôt qu’un titre simplement descriptif. Codex enregistre ces constats comme narrative_review avec acteur Codex-independent, clairement distinct d’une inférence JARVIS. JARVIS doit réviser son propre texte ; aucune prose métier n’est écrite à sa place. L’ancien rapport est archivé et les sept tâches validées restent intactes.

## Déploiement et tests

Déploiements25–27 : sauvegardes des modules, compilation, politique inchangée, même base et mêmes identifiants. Seul jarvis-conversation redémarre. Les autres missions du worker sont temporairement interrompues aux limites d’outils et reprises sans reset. Les deux missions externes à26B ne sont pas exécutées par Codex. Les contextes de réception A/B sont reconstruits depuis les preuves conservées ; cela est une assistance d’infrastructure Codex.

162 tests logiciels réussis (105 de départ +57 nouveaux). Les nouveaux cas vérifient les citations historiques, les mesures distinctes du comptage des reçus, l’exclusion des documents qui s’auto-prouvent, le dernier reçu externe, l’interdiction d’une clôture fictive, le maintien des validations lors d’une attente globale, le rejet d’une preuve de blocage réussie et la correction d’une extraction qui oublie l’attente explicite. Un premier test25 avait un artefact de prose non déclaré ; ce défaut de fixture est corrigé. L’échec initial est visible dans le journal d’exécution Codex ; tests-25.txt contient la relance réussie.

Ces tests valident le logiciel, pas la réception autonome. Les retests réels et leurs résultats doivent encore être consignés avant tout changement de statut final.14A reste ouverte.

Le retest26 a corrigé waiting_external mais conservé une citation du bilan d’accessibilité G2. Le contrat27 expose directement dans le schéma les seules valeurs et sources compatibles avec la demande littérale G3, puis les revalide localement. Cette réduction des erreurs de format concerne le contrat de clôture, sans inventer le plan. L’essai refusé reste dans les événements19103–19107.

## Réceptions ciblées et nouvelle réserve factuelle

Le test réel PROBE-27.json a détecté les trois fautes injectées (acteur, date, comptage), puis JARVIS a produit deux révisions jusqu’à PASS. La lecture indépendante de l’intégralité de la prose et des reçus confirme l’acteur JARVIS, la lecture du22 octobre2026 à00:09:44 UTC+02, les trois articles et la somme12, les quatre événements sémantiques PASS cités et le comptage de43 interventions Codex dans le snapshot de ce rapport. Voir PROBE-27-VERIFICATION-INDEPENDANTE.json. Ce test de composant est reçu sur ces faits ; ce n’est ni une quatrième mission autonome ni la réception globale de26B.

C a réellement utilisé mission_block après réextraction correcte de la clôture, puis atteint waiting_external (événements19152–19154), avec six validations locales intactes. Cela reçoit l’usage du mécanisme de clôture partielle ; la prose demeure refusée indépendamment : event10978 n’est pas un échec de couverture pour manifeste omis et event15355 n’est pas un verdict INSUFFICIENT. L’ancien PASS19151 est un faux positif du relecteur, conservé avec le texte original et C-PARTIEL-V1-VERIFICATION-INDEPENDANTE.json.

Le contrat de rapport26b.report.9 ajoute une comparaison déterministe des statuts directement attachés aux références d’événements prises en charge, puis une revue isolée des affirmations de source lorsque la revue générale est positive. Cette seconde vue fournit uniquement les passages concernés et chaque événement original, sans le récit global de mission. Le modèle extrait le statut/type/acteur allégués ; le moteur les compare aux champs originaux. Une cause citée doit être un passage exact du rapport et pointer vers un diagnostic original existant ; le contrôleur juge encore le soutien sémantique. Ce dernier contrôle reste un modèle, pas une preuve formelle de toute paraphrase.

Le retest réel du rapport C inchangé est maintenant FAIL : l’attribution PASS à event10978 contredit son FAIL original. Aucun texte n’est réécrit par Codex ; JARVIS reprend sa propre correction éditoriale, tout en conservant son blocage externe réel. 165 tests logiciels passent au déploiement28. Les tests supplémentaires vérifient le refus malgré une première revue modèle PASS, une fausse cause et un diagnostic original correct.

## Isolation des sources et rectifications liées — déploiements29–30

Le retest réel PROBE-SOURCES-28.json détecte les deux fautes de C mais sa raison pour15355 mélange des diagnostics de10978. L’original est conservé. Le contrat10 interroge donc le modèle séparément pour chaque événement, avec uniquement ses diagnostics, et le moteur joint lui-même le diagnostic sélectionné. Le retest PROBE-SOURCES-29.json rejette correctement la cause « manifeste omis » de10978 et le statut INSUFFICIENT attribué à15355. Les incohérences scalaires génèrent un constat déterministe plutôt que la justification libre du modèle. Le modèle conserve des limites d’interprétation ; ces essais ne valent pas garantie universelle.

B a réellement corrigé son identifiant de mission via host_edit_file puis rappelé mission_verify. Le contrôle ciblé a alors utilisé un ancien diagnostic de comptage retiré comme motif encore valable. Au contrat11, les rectifications exactes sont rattachées aux événements originaux concernés : événement canonique19287, acteur Codex. Seuls les constats réellement présents dans leurs issues sont annotés ; aucun verdict historique, autre diagnostic ou action JARVIS n’est effacé. Les revues et le contexte courant distinguent désormais l’ancienne erreur du contrôleur d’une erreur technique de l’application.

Une autre friction réelle de A était mission_evidence(id="13053") : ce numéro existait mais le préfixe event: manquait. L’interface accepte maintenant cette représentation non ambiguë, conserve les arguments originaux et relit le même événement de la même mission. Cela ne fabrique aucune preuve, ne lit pas une autre mission et ne permet pas de recevoir une tâche avec un simple événement de revue.

171 tests logiciels réussis, dont tests d’isolement des diagnostics entre inférences, alias numérique borné à la mission, rectification exacte sans effacement, refus d’une rectification étrangère ou d’une note modèle usurpant son autorité. Aucun nouveau moteur, worker, skill ou modèle installé. Les retests opérationnels des rapports continuent sur les mêmes trois missions ; les deux autres missions du worker sont conservées, sans opération métier de Codex.

## Séparer les défauts des classifications autorisées — déploiement31

Le rapport A attribuait toujours des refus à des titres descriptifs. L’interface d’échec de require_report retournait toutes les classifications de passages, dont les raisons positives not_factual. JARVIS les interprétait comme des motifs de rejet. Le message d’erreur contient désormais seulement les issues et passages contradicted/insufficient. Les vues modèle des anciennes erreurs bénéficient de la même séparation, sans changer leurs reçus originaux.

La préparation de correction conserve également les constats indépendants depuis le dernier PASS de la même portée. Un nouveau FAIL différent ne masque plus le constat antérieur de Codex-independent sur les causes historiques ; les issues exactes explicitement retirées restent annotées. Les constats anciens sont présentés comme éléments à recontrôler sur le brouillon courant, sans réintroduire une erreur déjà corrigée.

Le contexte de réception A est reconstruit depuis ces preuves et vues corrigées ; ses sept tâches et empreintes restent conservées. Cela est une aide d’infrastructure Codex, pas une autocorrection du moteur par JARVIS. 174 tests réussissent au déploiement31, avec trois cas supplémentaires sur la conservation des constats, le filtrage du message de rejet et la vue des anciennes erreurs non modifiées. Les trois rapports opérationnels restent à recevoir.

## Accès direct aux diagnostics et maîtrise du contexte — déploiements32–33

B a effectivement utilisé l’alias numérique de mission_evidence pour18397,18514,18527,19264. Il a ensuite paginé l’ancien événement18397 mais en a relu le début à plusieurs reprises jusqu’au refus de répétition improductive. Ses véritables issues étaient précédées de nombreuses classifications autorisées. L’interface26b.evidence.1 ajoute donc facts à côté de content : statut enregistré, acteur, date, diagnostics historiques non retirés, constats retirés et rectification liée. content reste l’original paginé, avec son empreinte ; les faits ne sont pas un résumé produit par le modèle et ne prouvent jamais un résultat applicatif courant.

B a aussi demandé include_evidence=true à mission_report_review. Ce retour complet a porté son contexte à267902 caractères avant réduction (événement19428). La vue26b.review-actionable.1 transmet désormais le verdict, les vrais défauts et les références, sans réinjecter tout le corpus de preuves ni les classifications positives. La réponse intégrale reste dans le reçu et la revue d’origine. Les données applicatives ordinaires portant des clés status/issues/claims ne subissent pas ce traitement sans les marqueurs de contrat de rapport.

178 tests logiciels réussis au déploiement33. Les quatre nouveaux tests vérifient l’accès aux diagnostics avant pagination, les constats rectifiés sans changement du FAIL original, la maîtrise du retour complet d’une revue et la conservation des données applicatives. Les tâches, preuves et entrées sont préservées. Les retests réels de réception demeurent ouverts ; les nouveaux outils doivent aider JARVIS à écrire son propre texte, jamais le remplacer.

## Journal factuel de grande taille — déploiements34–35

L’appel réel mission_report_facts de B renvoyait486770 caractères, dont d’anciens paramètres de plans refusés. La vue26b.ledger-view.1 conserve une sélection de métadonnées d’opérations, dernière lecture par chemin, dernier événement sémantique par tâche, états réels, versions, compteurs totaux et références des interventions Codex. La sélection signale explicitement les omissions ; elle ne présente pas une absence d’affichage comme une absence de preuve, ni un code0 comme réussite applicative.

CONTEXTE-MESURES.json mesure les reçus réellement produits :486770→18023 caractères pour le journal et192560→1425 pour une revue. Ces mesures sont Codex, pas de nouveaux progrès autonomes. Les reçus et leurs empreintes restent inchangés. Le dernier repli par extrait du checkpoint devait aussi conserver cette vue filtrée : il réintroduisait auparavant le corpus brut si le budget restant était encore trop petit. L’extrait prend désormais la vue filtrée et conserve taille/empreinte de l’original.

181 tests logiciels réussis au déploiement35. Les nouveaux cas vérifient la sélection de faits sans réinjection de vieux plans, la conservation des données applicatives ordinaires et le maintien du filtre dans un petit checkpoint. Les retests des trois rapports réels demeurent ouverts.

B a utilisé facts pour relire18397 et19462, puis édité lui-même son rapport afin de distinguer la mesure réelle2 du diagnostic numérique retiré. Un appel groupé incluant mission_evidence hors liste des lectures groupables a échoué partiellement ; les deux lectures hôte ont réussi et JARVIS a relancé séparément l’accès aux événements, sans correction Codex de cet appel.

Une réserve reste observée : la revue ciblée a refusé la description de18639 comme un manque de conservation des erreurs historiques, alors que le diagnostic original est Historical FAIL must be explicitly retained. Le modèle de contrôle peut donc encore émettre un faux refus ; un test réel isolé compare ce cas correct et la fausse cause10978 avant toute nouvelle évolution de la réception.

## Corriger le faux refus sans admettre une fausse cause — déploiement36

Le premier candidat (raisonnement privé activé uniquement dans un harnais) ne corrige pas le faux refus18639 ; il est écarté, avec sa sortie et ses métriques, sans publier de contenu de raisonnement privé. Le second candidat (périmètre historique plus explicite/ordre des champs) accepte B mais accepte aussi la fausse cause de C : il est NO-GO et n’a pas été déployé. Voir PROBE-RAISONNEMENT-36.json et PROBE-PERIMETRE-36.json.

Le contrat26b.report.13 ajoute une extraction à l’aveugle de la cause attribuée à l’événement, sans fournir ses diagnostics réels au classificateur. Le moteur compare ensuite cette catégorie aux diagnostics natifs reconnus, tels que Historical FAIL must be explicitly retained et At least one original receipt/event reference must appear. Les constats numériques retirés sont exclus des codes de soutien. Les assertions de statut/type/acteur restent comparées aux données originales et ne sont pas effacées par une catégorie correcte.

Pour les catégories ainsi reconnues, la comparaison native détermine le soutien causal ; l’ancienne opinion du modèle est conservée sous model_supported/model_reason, sans la transformer silencieusement en une réponse du modèle. La méthode est explicitement marquée support_method. Les causes non prises en charge restent soumises aux contrôles existants ; cette extension n’est pas une preuve de compréhension universelle de tout diagnostic libre. Une erreur de modèle ou un échec de format ne devient jamais une réussite applicative.

PROBE-CATEGORIES-36.json montre les extractions réelles : historique manquant pour B18639, livrable manquant dans le faux récit C10978. PROBE-INTEGRATION-36.json exécute le contrôleur candidat complet sur les textes gelés : B accepté, C refusé, attentes toutes satisfaites. Cela reçoit ce correctif de contrôle dans son périmètre, pas les missions opérationnelles complètes.185 tests logiciels réussissent, dont garde contre un faux positif NLI, maintien d’un statut incompatible, exclusion d’un ancien constat retiré et vérification que l’extracteur ne reçoit pas le diagnostic attendu.

Après installation36, les seuls contextes de réception A/B/C ont été archivés et reconstruits depuis les objectifs, plans, reçus et états durables. Les messages de travail hérités des anciens contrôleurs ne sont plus réutilisés comme contexte actif ; ils restent dans mission_context_archives avec leur empreinte. Les tâches/rapports déjà validés ne sont pas réinitialisés. Cette reprise est Codex, pas une autocorrection revendiquée de JARVIS. Les deux autres missions du worker restent actives dans leur propre périmètre ; aucune action métier de Codex ne leur est attribuée.
