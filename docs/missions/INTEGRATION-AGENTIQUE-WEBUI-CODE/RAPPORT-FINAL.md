# Intégration agentique Open WebUI / Qwen Code — bilan de livraison

**30 octobre2026 — ✅🟡 connecteurs déployés avec réserves ; réception globale incomplète.** Le critère final comprenant Google n’est pas entièrement satisfait ; la clôture native de la sonde assistée est reçue, sans preuve d’autonomie générale. Cette livraison ne clôture ni M26-P4, ni14A, ni les réserves historiques de rédaction libre.

## Résultats reçus

Open WebUI existant reste accessible à **https://jarvis-macmini.tail805e83.ts.net/** par Tailscale/Apache. Les nouvelles conversations utilisent Qwen27B Mac ; le profil développement utilise le80B existant de Dell1. Les outils appellent le registre, le broker, les Skills et les bases canoniques existants, avec reçus, pagination et prévention d’une double exécution au même identifiant. Aucun nouveau Mission Engine ni mémoire concurrente n’est créé.

Qwen Code0.26.4 ne reçoit plus les plafonds CLI de12tours/12appels. Deux sessions indépendantes ont accompli14étapes vérifiées en18puis29tours. Le profil réellement chargé impose32768tokens et la compression précoce ; les requêtes de résumé n’emportent plus inutilement les schémas des outils. Les contrats JSON et `stream=false` traversent correctement le relais Ollama. Les outils Goal sont autorisés ; deux objectifs simples ont été clôturés et relus. Le cas à historique complexe reste non reçu.

Une correction réelle de source par Code a réussi, avec test inchangé et contrôle indépendant Codex. Code a aussi lancé de vrais tests sur Dell1 et Dell2 via MCP/broker. JARVIS80B a ensuite produit et relu un manifeste exact sur Dell2 avec l’outil distant direct. Dell2 reste un exécuteur SSH ; aucune inférence Ollama sur Dell2 n’est annoncée.

Le cycle canonique de la sonde de service est allé de la création WebUI à la clôture native, avec [rapport factuel réellement produit](JARVIS-OBSERVATION-SERVICE.md). Une relecture réelle depuis le navigateur WebUI27B affiche completed, T1 validated et le SHA256 exact : [preuve](WEBUI-RESTITUTION-SONDE.json). Le moteur rédige les faits ; Qwen sélectionne les reçus et déclenche leur publication, sans publication de sa prose originale.

GitHub a été utilisé réellement depuis WebUI : lecture, recherche retournant un résultat incomplet explicite et publication via le Skill existant, avec contenu et arbre contrôlés indépendamment. Les appels longs des outils WebUI sont asynchrones ; l’interface répond pendant l’appel spécialiste.

## Réserves et tâches restantes

1. **Google non authentifié** : connecteur chargé et état réellement interrogé, mais aucune opération Google distante reçue. Le propriétaire a demandé un rappel et un accompagnement ; [le guide](GOOGLE-RACCORDEMENT.md) donne les commandes et la procédure OAuth initiale. Après connexion, les lectures/écritures de réception restent à exécuter.
2. **Planification et réception assistées** : la sonde864da7c457ef4d82b0b284d9ceb30eeb est désormais `completed`94109. Codex a corrigé l’interface cachant les observations pendant une vérification insuffisante. JARVIS a choisi trois lectures systemd, fait rejeter son ancien brouillon en FAIL, composé le relevé factuel et obtenu PASS puis validation T1. La lecture indépendante confirme le fichier exact et le service actif. Le plan initial confondait fichier unité et état runtime ; la reprise a été assistée. Cette sonde ne prouve pas une planification initiale complète ni la validité de tous les critères libres du plan. Voir [le correctif](CORRECTION-VERIFICATION-PENDANTE.md) et [le contrôle](CONTROLE-INDEPENDANT-SONDE.json).
3. **Rapports libres et finalisation Code** : un appel Code a annoncé réussir après un repli local alors qu’un résultat distant manquait. Le contrôle indépendant a rejeté ce succès. Les erreurs, refus et rectifications restent conservés. La correction d’un fichier ne prouve pas la fiabilité générale de la prose ni celle du reviewer Goal.
4. **Réception utilisateur et persistance machine** : accès HTTPS et services vérifiés ; microphone/Safari/iPhone et reboot complet non testés dans cette campagne. Les anciennes réceptions demeurent acquises dans leur périmètre.

## Validation et attribution

**93tests logiciels ciblés PASS**, **5contrôles vivants PASS** ; identité de huit fichiers déployés et état actif de sept services contrôlés. [Tests détaillés](TESTS-BOUT-EN-BOUT.md), [preuves structurées](PREUVES-JARVIS.json), [déploiement](DEPLOIEMENT.json).

Codex a développé/installé les adaptateurs, contrats, correctifs et fixtures ; il a effectué les contrôles indépendants et les reprises assistées explicitement tracées. JARVIS a choisi et appelé les outils depuis WebUI et le moteur ; Qwen Code a effectué la correction source et les commandes MCP distantes observées. Le manifeste final Dell2 a été réalisé par JARVIS via l’outil distant, pas par Code. Les tableaux déterministes restent attribués au moteur. Voir [ATTRIBUTION.md](ATTRIBUTION.md).

Sources : `40196e9`, `c9843d2` et `0ad2e8c`, sur `codex/integration-agentique-webui-qwen-code`, à la suite de PR34. Publication sans fusion automatique dans main. La pause propriétaire de M26-P4 et son MANUAL-HOLD sont conservés ; aucun modèle téléchargé, déplacé ou supprimé.

Directives effectivement consultées : AGENTS.md, charte, SUIVI/ROADMAP et états documentés référencés dans le diagnostic ; configurations et journaux actifs contrôlés. Autorisations d’intégration préservées ; aucune validation intermédiaire ajoutée. L’authentification Google est une dépendance technique de compte, pas une approbation de travaux déjà autorisés.

Publication : [PR35](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/35), empilée sur PR34 et sans fusion main.
