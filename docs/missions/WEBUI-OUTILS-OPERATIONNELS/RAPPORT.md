# Accès opérationnel aux outils depuis Open WebUI

**✅🟡 GO avec réserves : accès outils reçus et mission clôturée après assistance.** Google personnel et Éducation, GitHub, SSH/Ansible sur les deux Dell, Skill et mission ont été utilisés depuis le navigateur Open WebUI. Réception indépendante de la tâche et de sa clôture native ; autonomie générale et prose libre non reçues. L’extinction du Mac mini reste inexpliquée. Aucune fusion dans main.

## Sources, autorisations et périmètre

Directives effectivement consultées : AGENTS.md et docs/CHARTE_DIRECTIVES_JARVIS.md ; descriptions/discussions et derniers rapports PR35, PR37, PR38 ; cahiers INTEGRATION-AGENTIQUE-WEBUI-CODE et GOOGLE-MCP-OAUTH ; SUIVI courant ; procédures de déploiement et sources réellement actives. Base 9e059cf208a86e87b8673cddc38fc0a39dbfeb72, PR38. La préparation initiale reste dans le commit ba4bab4 et son historique.

L’ordre courant donne priorité aux accès opérationnels WebUI. Il conserve les autorisations propriétaire, les services, comptes, clés, mémoires et modèles existants. M26-P4/MANUAL-HOLD ne sont pas repris. Aucun nouveau moteur, connecteur concurrent, inventaire général, modèle ou installation système. Le propriétaire a confirmé explicitement le déploiement du code et de l’outil WebUI, le rechargement des quatre services et l’exposition des méthodes Google, dont envoi/invitations/corbeille.

## Avant / après

| Point | Avant | Après vérification |
|---|---|---|
| Identités Google | Jetons séparés, façade commune à paramètre profile | Deux entrées natives liées à leur compte : google_personal / google_education ; ancien accès compatible |
| Exposition Google | ALLOWED et overrides masquent des méthodes existantes | Catalogue amont des familles Drive/Docs/Sheets/Calendar/Gmail/time ; schémas d’envoi, réponses/invitations, suppression Calendar et corbeille Drive réellement découverts |
| Client/MCP | Projections différentes ; MCP historique 9 outils | Deux identités accessibles par registre, catalogue client et MCP historique (11 outils observés) |
| Appels WebUI | Paramètres optionnels vides rejetés ; chaînes JSON imbriquées fragiles | Champs vides omis ; jarvis_skill_run accepte un objet structuré, encode selon le manifeste actif et appelle le Skill existant |
| Concurrence Google | BUSY sans exécution possible pendant une lecture concurrente | Verrou par compte conservé ; les appels attendent leur tour, sans refus BUSY positif trompeur |
| Observation du service WebUI | jarvis-webui-tools.service absent de la politique systemd | Ajout des seules lectures status/show/is-active/is-enabled ; politique relue par le broker à chaque requête |
| Services | Actifs, pas de mission active avant déploiement | Conversation, adaptateur, broker, deux workers actifs ; rechargement final des quatre services autorisés sans tâche active |

Les méthodes de téléchargement/pièces jointes conservent leurs racines autorisées. Les jetons et clés restent privés ; les méthodes d’authentification ne sont pas exposées au modèle. Les droits effectifs des ressources restent ceux de Google et GitHub.

`Tool is outside the exposed client catalog` vient du garde de Capabilities.schema : il attend un nom de registre JARVIS. Une méthode imbriquée comme drive.search doit passer par l’outil Google lié au compte, avec action/name/arguments. Le message donne désormais cette route. La recherche ciblée dans les chats WebUI n’a pas retrouvé l’appel historique précis : son nom fautif n’est donc pas déclaré identifié.

## Réception réelle depuis le navigateur WebUI

| Capacité | Reçus WebUI et contrôle indépendant |
|---|---|
| Drive personnel / Éducation | Dossiers de test créés 382/386, recherchés depuis WebUI, relus séparément 394/396 ; IDs et type dossier concordants |
| Docs personnel / Éducation | Créations 234/320 et relectures exactes des marqueurs ; nouvelle lecture indépendante PASS sur chacun |
| Sheets personnel / Éducation | Création, écriture A1:B1, relecture ; nouvelle lecture indépendante du marqueur et de la valeur 42 PASS sur chacun |
| Calendar personnel / Éducation | Événements de test créés sans invités, relus depuis WebUI et séparément ; titre et description exacts PASS |
| Gmail personnel / Éducation | Brouillons adressés à soi-même créés ; contenus relus indépendamment PASS ; lecture personnelle WebUI retestée après BUSY. Aucun email envoyé |
| Identités effectives | Organisateurs Google distincts ; chaque compte est effectivement refusé lorsqu’il lit le document privé de test de l’autre (364/366) |
| SSH Dell1 / Dell2 | Commandes Python distantes 248/255, noms de machines distincts et marqueurs exacts, codes 0 ; secondes connexions de contrôle 316/318 concordantes |
| Ansible Dell1 / Dell2 | Ping réel, SUCCESS/pong, codes 0, reçus 264/268 |
| GitHub lecture | AGENTS.md réellement lu depuis WebUI 276 |
| GitHub écriture / Skill | github-publish exécuté depuis WebUI, run 709e462c2b2f4d7aa69197ba32a67e17, passed, reçu 343 ; commit 14b64389960a254a8c64aae501bd4f110d545000 |
| Réception GitHub indépendante | Connecteur GitHub séparé : contenu exact du seul fichier publié ; blob 9c9283b5f930432cae6eea32c457be224e1dfc95 identique au hash-object local |

Branche de test : `jarvis/webui-operationnel-reception-20261031`, fichier `docs/receptions/WEBUI-OPERATIONNEL-20261031.md`. Fixture préparée par Codex ; publication par le Skill existant déclenché par Qwen dans WebUI. Pas de PR ni fusion pour la branche d’essai.

Les chats et captures sont conservés sur JARVIS ; leurs URL sont archivées dans le dossier privé. Leur rapatriement n’a pas été possible après la perte d’accès SSH. Les conversations de réception restent enregistrées dans WebUI. Le chat de réception relit les reçus persistants SSH/Ansible/Skill et l’état de mission. Les données et IDs Google restent dans le répertoire privé, pas dans cette PR. Les huit relectures indépendantes Docs/Sheets/Calendar/Gmail et les deux Drive sont des contrôles de résultats, distincts des textes du modèle. Les méthodes d’envoi/suppression sont exposées, mais aucun envoi ni suppression n’a été utilisé comme test.

## Mission reçue et raccordement final

Même identifiant `3f64e6c1adc640e9847c9311d3350d8b`, même tâche et plan JARVIS conservés. Après trois incidents de capacité, le propriétaire a explicitement autorisé mesure, résolution native et reprise. Nouvelle mesure isolée : 25333 octets pour un budget conservateur de 27648, fenêtre inchangée de 32768 tokens. Résolution native 94844 : total historique d’incidents toujours 3, infra_resolved_through=3, sans effacement des historiques.

La reprise a exécuté des écritures et vérifications réelles. Deux FAIL sont conservés : brouillon modèle incorrect, puis provenance du rendu à reprendre. Le rapport finalement écrit était exact, mais le cycle restait en correction lorsqu’une recomposition réutilisait légitimement les mêmes octets après un ancien FAIL. Correctif ciblé de legacy_attempts : une recomposition terminée et sa nouvelle provenance peuvent reproposer mission_verify. Aucun PASS ni remise à zéro n’est produit par ce correctif ; une écriture inconnue, une autre tâche ou un contenu différent ne sont pas débloqués par ce cas.

JARVIS a ensuite choisi mission_verify : **PASS 95216**, tâche validée par mission_task_complete 95241, bilan déclenché par intervention_report, **completed 95261**. Réception indépendante : lecture broker 406, comparaison exacte au rendu des reçus PASS. SHA256 du rapport de tâche : `3cafb06bb64814c540e242a8df838faec2ab95e03086774b252af61982647c6b`. SHA256 du rapport final : `7fa558fe701e5e78dcc60ee8656e2e9f77e207a6eb0b90ec5105e10c75947a7d`.

[Rapport de tâche reçu](RAPPORT-TACHE-RECU.md) · [Rapport final canonique reçu](RAPPORT-MISSION-RECU.md). Ces copies sont inchangées. Le relevé distingue les instants des reçus historiques d’une mesure actuelle ; il inclut aussi les lectures de préparation d’un service voisin. La déduction initiale erronée du plan « non autorisé donc absent » reste historique et n’est pas reçue comme observation.

Attribution : Codex a corrigé les adaptateurs, permissions et interfaces ; JARVIS a choisi son plan, appelé les outils, sélectionné les preuves et déclenché vérification/clôture. Les tableaux et le bilan factuel sont assemblés par le moteur existant. **Réception assistée ; aucune affirmation d’autonomie générale de planification ou de prose libre.** Pas de campagne générale de fiabilisation ni nouvelle réception14A.

## Persistance après redémarrage et résultats visibles

Après le démarrage manuel signalé par le propriétaire : cinq services actifs, quick_check SQLite mémoire/missions = ok, sources déployées conservées. Dans le navigateur WebUI, profil80B existant : Docs personnel398 et Éducation400 réellement relus, service402 actif, mission affichée completed/validated. Une lecture GitHub mal routée par Qwen vers SSH a été refusée404 ; ajout d’une entrée native jarvis_github vers le broker existant, puis lecture réelle GitHub408 et marqueur exact affiché. Aucun nouveau broker ni droit SSH n’a été ajouté pour contourner ce refus.

Le contrôle27B après reboot a été arrêté pendant un long prétraitement à froid ; il n’est pas déclaré reçu. Les réceptions27B antérieures restent acquises. Le profil80B était déjà déployé ; aucun changement de modèle ou de routage global.

[Conversation de réception dans WebUI](https://jarvis-macmini.tail805e83.ts.net/c/28b38c07-9361-47e3-ad61-501ac9032038). Les résultats des outils et le rapport de tâche y sont consultables ; les accès Google demeurent ceux du compte explicitement choisi.

## Extinction : réserve matérielle/réseau conservée

Le Mac mini s’est éteint ; le propriétaire l’a démarré. La fin du journal précédent est à21:49:40, onze secondes après le rechargement des services réalisé par Codex. Aucune trace examinée d’arrêt ordonné, OOM ou panic et aucun pstore conservé ne permettent d’établir la cause. La proximité est documentée, sans attribution ni exclusion de responsabilité non démontrée. [Traces et limites](EXTINCTION-ET-REPRISE.md).

## Tests, déploiement et retour arrière

**93 tests distincts PASS au cours de la livraison :33 accès/transport et60 cycle de rapport.** La régression de recomposition échoue sur l’ancienne version ; elle passe après correction avec les cas négatifs et les tests existants. diff --check PASS. Pas de rejeu de campagne générale.

Cinq modules runtime et l’outil WebUI correspondent aux sources, empreintes dans PREUVES.json. Le correctif de phase a nécessité la seule recharge des deux workers, sans mission active ; l’adaptateur natif GitHub a été actualisé par l’API WebUI, sans redémarrage. Les bases, comptes, clés, jetons, modèles et services sont préservés. Aucun main fusionné automatiquement.

Sauvegardes privées : modules, outil/valves et politique, répertoire700 et réglages privés600. Les changements locaux du worktree ont été archivés et sauvegardés par stash avant synchronisation en avance rapide avec les publications GitHub faites pendant l’indisponibilité. Aucun changement local n’a été jeté.

Retour arrière ciblé : restaurer les seules versions sauvegardées et, si nécessaire, le seul ajout de lecture du service WebUI ; recharger les seuls services concernés après contrôle des tâches. Conserver bases, incidents, missions, reçus et archives. Tous les échecs initiaux (champs vides, brouillon sans destinataire, BUSY, transport Skill, mauvaise route GitHub, blocages de capacité et FAIL de rapport) restent tracés ; aucun succès n’est rétroactivement attribué aux essais refusés.
