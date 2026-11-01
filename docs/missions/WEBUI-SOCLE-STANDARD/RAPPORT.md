# WebUI — retour au socle standard

Décision propriétaire du 1 novembre 2026 : « Je veux du standard qu’on personnalisera à la fin ». Cette décision remplace, pour les nouvelles tâches WebUI, l’approche consistant à corriger le moteur durable maison. Les historiques et les services JARVIS restent conservés ; aucune fusion automatique dans main.

## Avant / après installé

| Fonction | Avant | Socle standard installé |
|---|---|---|
| Boucle d’exécution WebUI | Filtre propriétaire créant une mission JARVIS | Appels d’outils natifs Open WebUI ; filtre désactivé et détaché des deux profils |
| Mission / rapport | Contrats, revues et compaction spécifiques JARVIS | Aucune création automatique de mission maison dans ce parcours ; Qwen Code d’origine pour les tâches qui lui sont confiées |
| Inférence | Relais local et transformations spécifiques | Connexions Ollama natives ; WebUI et nouveau Qwen Code contournent le relais maison |
| Contexte | Fenêtres différentes, contrôle en octets maison | Deux profils à 32 768 ; compaction native WebUI activée à 24 000 ; gestion native Qwen Code |
| Commandes et processus longs | Adaptateur spécifique avec attente maximale | Open Terminal officiel, intégré dans la section Terminal native de WebUI |
| Connecteurs | Fonctions Python WebUI spécifiques | Serveur MCP existant exposé par MCPO officiel ; mêmes accès et permissions broker |
| Qwen Code | Paquet modifié et lanceur avec prompt/réglages spécifiques | Même version 0.26.4, archive npm officielle vérifiée, sources non modifiées, configuration native dans un `QWEN_HOME` dédié |
| Identité / mémoire | Injection automatique par filtre spécifique | Personnalisation différée ; mémoire et historiques précédents conservés, aucune nouvelle mémoire maison |

Le connecteur MCP et le broker réutilisés restent du code JARVIS : il ne s’agit pas de prétendre que tout le laboratoire est devenu un produit amont. Le pilotage et les processus de ce nouveau parcours sont ceux des composants standard. La seule modification de source du connecteur dans cette branche expose `jarvis_call.arguments` comme objet structuré ; la chaîne JSON historique reste acceptée. Aucun nouveau moteur, reviewer, filtre de contexte ou ordonnanceur développé.

## Versions et configuration

- Open WebUI 0.12.0 existant, image non remplacée.
- Qwen Code 0.26.4 d’origine ; empreinte et contrôle d’intégrité npm dans les preuves.
- MCPO 0.0.20 ; environnement propre avec versions du verrou officiel de cette version, SDK MCP 1.17.0. Le premier environnement avec dépendances les plus récentes échouait au démarrage ; il n’est pas utilisé par le service final. Aucun correctif de code amont.
- Open Terminal 0.14.7, installation Python isolée, écoute locale authentifiée et connexion native réservée aux administrateurs existants.
- Nouveau profil Ollama `qwen3-coder-next:jarvis-standard-32k` : alias de paramètres à 32 768 partageant les poids existants. Aucun téléchargement de modèle ; modèle original conservé.

Les deux profils existants `jarvis-tools-conversation` et `jarvis-qwen-code-lab` sont conservés avec appels natifs, fonctions natives activées, prompt système spécifique vide, outils MCP standard et filtre propriétaire retiré. Dans le chat, le terminal se sélectionne avec le bouton nuage : « Mac mini — Open Terminal standard ». Qwen Code est disponible par `qwen-standard`. Aucun lancement par le vieux moteur de missions n’est nécessaire.

Le serveur MCP conserve les connecteurs Google personnel et Éducation, GitHub, SSH/Ansible et Skills. L’outil MCP de création de missions maison est exclu du nouveau parcours ; les anciennes interfaces et preuves restent historiques. Les jetons, comptes et autorisations n’ont pas été recréés. Les écritures Google/GitHub reçues dans PR39 ne sont pas présentées comme de nouveaux tests effectués dans cette branche.

## Réception réelle

1. **Qwen Code natif en terminal** : lecture de `input.txt`, production de sa version en majuscules dans `output.txt`, relecture ; résultat exact vérifié indépendamment. Quatre tours natifs ; modèle réellement chargé à 32 768 sur Dell1. Le premier essai sans profil Ollama explicite n’avait pas accompli le travail : conservé comme échec, non reçu.
2. **WebUI → Open Terminal** : chat `b64a2684-3ff4-4a24-a363-78f67e65c023`, création et relecture de `ui-result.txt`, résultat exact vérifié. Le modèle a utilisé une commande shell directe, malgré la demande de délégation : ce cas ne prouve pas l’utilisation de Qwen Code.
3. **WebUI → Open Terminal → Qwen Code d’origine** : chat `bb43bf6a-5c7e-4b64-981b-9a7e2d1578bb`, commande explicite `qwen-standard`, attente par `get_process_status`, relecture de `ui-qwen-result.txt` et réponse affichée. Journal natif Open Terminal relu indépendamment : processus `20261101-120213-8bf9a0`, fin réelle avec code 0 ; fichier exact et empreinte reçus. C’est une réception de raccordement sur commande explicite, pas une preuve de délégation universelle en langage naturel.
4. **27B dans WebUI** : chargement réel à 32 768 sur Mac, appels réels de découverte MCP et de schéma. Pas de réponse finale reçue sur cette sonde ; arrêt Codex, traces conservées. Ne pas transformer l’arrêt en succès fonctionnel.

Les artefacts de tests sont dédiés. Les données privées, résultats bruts et clés restent en dehors du dépôt ; seules références, empreintes et synthèses expurgées sont publiées. Les sources du connecteur compilent ; les environnements finaux MCPO et Open Terminal passent le contrôle de dépendances. Aucun résultat de la suite historique de 176 tests n’est attribué à cette nouvelle réception.

## Mesures déjà acquises et réserves

Le souvenir du propriétaire est confirmé : `docs/missions/22/RESSOURCES-FINALES.json` atteste déjà Qwen27B à 32 768 sur Dell1 avec `size_vram` égal à la taille chargée. Aucun nouveau benchmark Dell imposé. Le Mac était historiquement resté à 16 384 ; son nouveau chargement à 32 768 est observé ici.

Sur le Mac, le relevé actuel indique `size_vram=0`, et `nvidia-smi` ne communique pas avec le pilote. Ce fait est distinct de la fenêtre de contexte. Le module NVIDIA est présent pour le noyau courant selon un contrôle à blanc ; aucun chargement forcé, changement de pilote, de noyau ou redémarrage effectué. La cause n’est pas établie par cette mission.

Le propriétaire signale une grosse copie Dell1 → Dell2 pendant les essais. Elle peut affecter réseau/disques côté Dell ; aucune mesure ne permet de lui attribuer toute la lenteur, notamment l’inférence locale CPU du Mac. Aucun benchmark, arrêt ou modification du transfert. La réception de performance est NON REÇUE dans ces conditions.

Le socle standard est déployé et le parcours Qwen Code explicite est reçu. L’autonomie générale du modèle, la justesse de toutes ses conclusions et la performance du 27B ne sont pas déclarées reçues. La sonde durable historique `30dde783…` reste interrompue avec ses compteurs ; elle n’est ni relancée ni annoncée terminée par ce remplacement de parcours. M26-P4 et MANUAL-HOLD préservés.

## Retour arrière

Les configurations WebUI, connexions, profils, lanceurs et fichiers précédents sont sauvegardés dans le répertoire privé `webui-standard-private`. Restaurer uniquement ces configurations si nécessaire et désactiver les deux nouvelles connexions/services standard. Ne restaurer aucune base historique en arrière, ne supprimer aucune mémoire ni trace. Les anciens services et paquets demeurent présents ; les nouveaux profils et le nouveau CLI n’ont pas besoin de leurs mécanismes maison de pilotage.

## Sources amont

[Open WebUI MCP](https://docs.openwebui.com/features/extensibility/mcp/) · [MCPO](https://github.com/open-webui/mcpo/tree/v0.0.20) · [Open Terminal](https://docs.openwebui.com/features/open-terminal/setup/installation/) · [Connexion native Terminal](https://docs.openwebui.com/features/open-terminal/setup/connecting/) · [Qwen Code](https://github.com/QwenLM/qwen-code) · [Contexte natif WebUI](https://docs.openwebui.com/troubleshooting/context-window/).
