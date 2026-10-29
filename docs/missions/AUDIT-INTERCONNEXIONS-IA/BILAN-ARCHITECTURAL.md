# Bilan architectural — état observé avant corrections

**✅ Audit réalisé. L'architecture présente des fonctions démontrées, des réserves et des défauts reproduits.** Ce verdict reçoit le diagnostic, pas l'absence de panne. Audit du 29 octobre 2026, base75d3161, branche `codex/audit-interconnexions-ia`. Les preuves E01–E12 et les réceptions précédentes sont conservées.

Le propriétaire autorise désormais les corrections et optimisations nécessaires sans validation intermédiaire. Elles suivent après gel de ce bilan, sur une branche distincte ; leurs résultats ne réécrivent pas cet état initial.

## Réponses aux dix questions

1. **Pourquoi Llama8B dans Open WebUI ?** Le service impose encore `DEFAULT_MODELS=llama3.1:8b`, conservé depuis le profil de mission07. « JARVIS — Qualité » personnalise ce vrai modèle8B ; il ne désigne pas Qwen27B. Les anciennes conversations gardent leur modèle. Le choix28A de JARVIS n'a pas migré le défaut de cette autre interface.

2. **Qwen27B reste-t-il conversationnel pour JARVIS ?** Oui : configuration actuelle, réponse directe sur Mac, API avec outils limités et conversation réelle via JL03 le prouvent. Cependant, l'API canonique sans restriction d'outils renvoie503 : la fenêtre calculée dépasse le profil Mac16384. Il serait faux de déclarer toute la conversation cassée, ou tous ses chemins fonctionnels depuis la seule sonde de santé verte.

3. **Qwen Code utilise-t-il le80B de Dell1 ?** Oui. Le wrapper appelle le garde8091 puis l'API native11435 du modèle existant, avec32768 de contexte. Nouveau correctif réel en5tours/32,889s, puis3testsPASS vérifiés par Codex. Les outils s'exécutent sur Mac ; l'inférence est sur Dell1.

4. **Open WebUI peut-il lancer Qwen Code ?** Oui : appel navigateur réel reçu lors de l'installation précédente, outil et sources toujours présents. Le nouvel essai CLI utilise le même modèle et le même garde. Cela ne constitue pas une intégration de Qwen Code comme worker du Mission Engine.

5. **Peut-il lancer une mission JARVIS ?** L'outil `jarvis_task` appelle l'API canonique, mais la création puis l'exécution d'une mission ne sont pas reçues par cet audit. La consultation réelle des51missions fonctionne. Une configuration raccordée ne vaut pas une mission exécutée ; ce contrôle reste à réaliser dans la suite autorisée.

6. **Quel est le niveau d'autonomie de Qwen Code ?** Sur le petit projet neuf : lecture, analyse, édition et tests sans correction source de Codex pendant l'essai. Le profil n'active ni MCP ni sous-agents. Des arrêts à12tours malgré des testsPASS ont été conservés précédemment ; une consigne d'arrêt améliore un cas sans fournir une garantie générale. Aucun déploiement applicatif n'est reçu par ce test.

7. **Qui utilise Dell2 ?** Le broker, SSH/Ansible et les commandes distantes de JARVIS pour des tests et vérifications croisées reçus en26. L'inventaire actuel utilise aussi SSH, sous attribution Codex. Aucun Ollama ou LLM actif n'est trouvé ; les GPU3090+3080 sont au repos. Aucun Tailscale installé ou actif n'est trouvé aux emplacements contrôlés.

8. **Quelles fonctions sont déjà fournies par les produits installés ?** Open WebUI apporte conversation, historique, profils, voix et outils d'interface. Qwen Code apporte lecture, édition, shell et tests de développement. Ils ne remplacent pas la mémoire canonique, les compteurs durables, la vérification du code déployé ou la délégation Dell reçue.

9. **Quels composants personnalisés restent indispensables ?** La politique et les identités du broker, la mémoire, les missions et checkpoints, les preuves/version/provenance et les fonctions spécifiques de JL03. Le garde de contexte reste nécessaire au raccordement choisi. Ces composants doivent réutiliser les fonctions existantes plutôt que reconstruire un framework de programmation complet.

10. **Que simplifier ?** Aligner les défauts de modèles, retirer le choix aléatoire du serveur, partager l'admission des consommateurs et réemployer Qwen Code comme spécialiste. Une consolidation des deux Ollama Dell nécessite d'abord une revue des consommateurs de11434. Les poids32B/70B ou les copies intermachines ne sont pas supprimés par présomption d'inutilité.

## Connexions et niveau de preuve

Le [diagramme](DIAGRAMME-ARCHITECTURE-REELLE.md), la [matrice F01–F27](MATRICE-INTERCONNEXIONS.md) et l'[inventaire](INVENTAIRE-SERVICES-MODELES.md) distinguent les connexions reçues, configurées et absentes.

Les cinq GPU ne constituent pas un pool automatique. Les deux instances Ollama de Dell1 partagent le stockage, mais possèdent des résidences et ordonnanceurs indépendants. Les catalogues du Mac et du Dell sont indépendants. Dell2 exécuteur de commandes n'est pas Dell2 serveur d'inférence.

La cartographie précise est : **JL03=8766 ; prototype vocal23D=8783 ; broker hôte=socket Unix**. Une page200 sur8783 ne prouve pas le fonctionnement de JL03. L'audit vérifie les PID, titres HTML et points d'entrée, puis teste réellement la conversation sur8766.

## ask_user : défaut et prudence causale

Sept réponses historiques sont du JSON textuel, conservé comme `message`, sans appel structuré. Leur affichage brut est reproduit en rouvrant la conversation. L'outil existe et un nouvel essai sur le même profil affiche correctement son formulaire.

La cause immédiate prouvée est donc **du texte au lieu d'un appel structuré reconnu**. Le template ou parseur du modèle8B, le mode d'appel et l'historique restent des causes possibles non départagées, faute de capture Ollama historique brute. Ni un outil globalement absent ni une panne Apache/TLS ne sont démontrés. Voir [l'analyse ciblée](AUDIT-OPENWEBUI-LLAMA8B.md).

## Proposition de simplification

| Famille | Changement proposé | Portée |
|---|---|---|
| Configuration | Défaut WebUI27B et filtres de catalogue par fournisseur | Aligner28A sans changer les poids |
| API | Offrir les outils utiles en conversation, respecter le profil de contexte | Corriger503 sans relever la limite |
| Interconnexion | Tester une mission courte depuis l'outil WebUI | Réutiliser le moteur canonique |
| Interconnexion | Étudier une admission commune WebUI/Code/Engine | Préserver priorités et ressources ; éviter une nouvelle file concurrente |
| Réemploi | Garder chat/voix WebUI et outils de développement Qwen Code | Éviter installations et réécritures inutiles |
| Spécifique | Garder broker, mémoire, compteurs, vérification P4 | Ces fonctions ne sont pas remplacées par les produits installés |
| Architecture éventuelle | Consolider Ollama ou ajouter une inférence Dell2 | Non appliqué pendant l'audit ; besoin à justifier selon le matériel réel |

## Attribution et limites

Codex effectue les inventaires et contrôles, prépare la fixture et vérifie indépendamment les résultats. Qwen Code80B choisit et réalise sa correction. Les preuves distribuées historiques proviennent de JARVIS et gardent leurs réserves d'assistance.

P2/P3 sont reçues avec réserves ; P4 reste non reçue et en pause, MANUAL-HOLD conservé. Aucun Safari/iPhone, microphone physique, reboot hôte ou repli vers une inférence Dell2 n'est prétendument testé. Les corrections autorisées suivantes disposeront de sauvegardes, d'un retour arrière et de preuves séparées.
