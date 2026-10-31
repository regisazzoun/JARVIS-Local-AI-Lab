# Accès opérationnel aux outils depuis Open WebUI

**✅🟡 Accès outils déployés et reçus ; 🟡 réception globale de mission incomplète.** Google personnel et Éducation, GitHub, SSH/Ansible sur les deux Dell et le Skill ont été utilisés depuis le navigateur Open WebUI. La nouvelle mission a démarré et exécuté des lectures réelles, mais reste **interrupted**, sans rapport final reçu. Aucune fusion dans main.

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

## Mission JARVIS : résultat et réserve essentielle

La mission `3f64e6c1adc640e9847c9311d3350d8b` a été créée depuis WebUI avec le profil existant service_observation. JARVIS a rédigé son propre plan, puis exécuté des lectures systemd. La politique initiale ne proposait pas son service cible ; après correction et import d’un reçu broker réel, status/show/is-active de jarvis-webui-tools.service ont réussi (94768/94788/94808).

Assistance Codex explicitement tracée : arrêt après répétitions de host_policy, sélection de l’interface de plan existante, correction de la permission manquante, sélection des références compactes et d’un périmètre d’outils pour cette seule tâche. Aucun plan ni rapport de sonde écrit à la place de JARVIS. Le plan contient une ancienne déduction erronée « non autorisé donc absent » ; elle reste historique et n’est pas reçue comme observation.

Trois incidents ContextCapacityError ont ensuite arrêté la mission. Son entrée obligatoire dépassait le budget conservateur de 27648 octets estimés, pour une fenêtre serveur inchangée de 32768 tokens. Aucun OOM ni réduction de fenêtre n’est déduit de ces erreurs. Une mesure sur copies SQLite isolées du contrat compact donne **25333 octets**, sans inférence, sans résolution d’incident et sans modification de la mission réelle. Cette mesure n’est pas une réception d’exécution.

Le contrôle automatique d’approbation a rejeté l’enregistrement d’une résolution d’incident et la reprise après ce stop persistant. Motif : preuve locale jugée insuffisante pour lever l’escalade sans autorisation explicite de cet acte. Le propriétaire a ensuite explicitement autorisé la mesure, la résolution native et la reprise de cette même mission, avec tous les compteurs et historiques conservés. Cette autorisation n’a pas encore pu être exécutée : le Mac mini est inaccessible. **Rapport final de la sonde et autonomie sans assistance NON REÇUS.** Aucun succès global n’est déduit des lectures ou de la création de mission.

## Tests, déploiement et retour arrière

**31 tests ciblés PASS**, diff --check PASS : capacités client, Google MCP/OAuth/identités, transports WebUI et concurrence du même profil. Les deux défauts observés dans le navigateur ont des régressions ciblées. Aucun rejeu des anciennes campagnes générales.

Les quatre modules actifs et le contenu de l’outil WebUI correspondent aux sources de cette branche ; empreintes et services dans PREUVES.json. Le fichier tools.py préserve une description d’artefacts déjà différente au runtime avant cette mission ; cette ligne n’est pas attribuée au présent développement. Les services sont rechargés avec la dernière correction après vérification d’absence de mission active.

Sauvegardes privées : quatre modules, outil WebUI/valves et politique hôte. Répertoire protégé 700, fichiers de réglages privés 600. Retour arrière ciblé par restauration de ces seules versions, restauration du seul ajout de politique si nécessaire, puis rechargement des mêmes services. Ne pas supprimer bases, missions, archives, jetons ou accès.

Échecs conservés : dix découvertes initiales rejetées à cause du champ query vide ; brouillon personnel initial refusé pour destinataire vide ; BUSY d’une lecture ; répétitions de transport JSON Skill avant l’adaptateur structuré ; refus/arrêts et incidents de la sonde. Leurs reçus et empreintes sont conservés dans les preuves et archives privées, sans réception fictive.

## Incident de transport au contrôle final

Après les réceptions et le rechargement final, les nouvelles connexions SSH au Mac mini ont expiré (Operation timed out). L’état actuel des services ne peut donc plus être reconfirmé : leur dernier contrôle positif reste historique à cette session. La cause réseau/hôte n’est pas établie. Aucune panne applicative ni causalité du déploiement n’est affirmée. La publication des sources et du présent rapport est poursuivie par le connecteur GitHub indépendant ; la copie de travail distante devra être resynchronisée avec cette branche avant toute nouvelle modification.

## Reprise autorisée — accès hôte indisponible

Le propriétaire a répondu « Oui, mesurer puis résoudre l’incident et reprendre ». Aucun nouvel accord de mission n’est nécessaire. Contrôle de reprise : Tailscale local Running, sans alerte ; pair jarvis-macmini Offline, dernière présence 2026-10-31T20:50:00.1Z (21 h 50 à Paris). SSH expire par l’adresse Tailscale et par l’adresse LAN documentée, avec la clé hôte existante conservée. Le Dell1 est en ligne, mais aucune clé hôte Dell n’est enregistrée sur ce MacBook : aucun nouvel accès n’a été créé.

Aucune mesure nouvelle sur JARVIS, résolution de registre ou reprise de mission n’a été appliquée pendant cette tentative. La mesure isolée antérieure de 25333 octets demeure historique. Vérifier l’alimentation et le réseau du Mac mini ; à son retour, relire le checkpoint, remesurer le contrat compact, puis appliquer le mécanisme natif de résolution autorisé et reprendre le même identifiant. Ne pas effacer les incidents ni recréer la mission. Réconcilier également le worktree distant avec les publications GitHub effectuées durant l’indisponibilité, en conservant ses changements.
