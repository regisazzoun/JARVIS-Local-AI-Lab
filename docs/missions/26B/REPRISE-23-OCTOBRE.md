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

162 tests logiciels réussis (105 de départ +57 nouveaux). Les nouveaux cas vérifient les citations historiques, les mesures distinctes du comptage des reçus, l’exclusion des documents qui s’auto-prouvent, le dernier reçu externe, l’interdiction d’une clôture fictive, le maintien des validations lors d’une attente globale, le rejet d’une preuve de blocage réussie et la correction d’une extraction qui oublie l’attente explicite. Un premier test25 avait un artefact de prose non déclaré ; ce défaut de fixture est corrigé, le résultat initial est conservé en privé.

Ces tests valident le logiciel, pas la réception autonome. Les retests réels et leurs résultats doivent encore être consignés avant tout changement de statut final.14A reste ouverte.

Le retest26 a corrigé waiting_external mais conservé une citation du bilan d’accessibilité G2. Le contrat27 expose directement dans le schéma les seules valeurs et sources compatibles avec la demande littérale G3, puis les revalide localement. Cette réduction des erreurs de format concerne le contrat de clôture, sans inventer le plan. L’essai refusé reste dans les événements19103–19107.
