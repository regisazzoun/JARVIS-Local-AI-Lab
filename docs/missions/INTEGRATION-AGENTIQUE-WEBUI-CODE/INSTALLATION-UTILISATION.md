# Installation et utilisation

## Accès quotidien

Ouvrir **https://jarvis-macmini.tail805e83.ts.net/** sur le tailnet. Le profil par défaut des nouvelles conversations est **JARVIS — Conversation et outils**, utilisant le Qwen27B existant du Mac mini. Le profil **JARVIS — Développement Qwen Code (expérimental)** utilise le Qwen80B Dell1. Les conversations antérieures ne sont pas réécrites.

Exemples : demander l’état du Mac, une recherche web ou la lecture d’un fichier GitHub. Pour les outils génériques : découvrir `jarvis_catalog`, obtenir `jarvis_schema`, appeler `jarvis_call` puis lire les reçus. Le catalogue est paginé ; une projection partielle ne signifie pas que les données absentes n’existent pas.

`jarvis_remote_project(host, project, command)` fournit un contrat direct pour les commandes sur les Dell, en réutilisant `host_remote/project_exec`. Il ne remplace pas une opération distante par une opération locale.

`qwen_code_status` expose l’occupation du spécialiste, ses derniers résultats et leurs `client_audit_id`. Ceux-ci permettent de relire les résultats via `jarvis_receipt`, y compris après déconnexion de l’interface. En cas de409, aucun nouveau travail n’a été lancé : attendre une fin observée plutôt que changer arbitrairement d’identifiant.

## Qwen Code

```bash
cd /var/lib/jarvis/projects/qwen-code/integration-acceptance
/home/adminjarvis/.local/bin/qwen-local
```

Le lanceur conserve le modèle existant et accepte les projets dédiés autorisés. Les nouvelles sessions disposent des outils locaux et du raccordement MCP. Les objectifs natifs se lancent avec `/goal set ...`, se consultent avec `/goal`, et les reprises restent attachées à leur projet/session.

Le reçu d’un appel spécialiste distingue le processus terminé du résultat indépendamment vérifié. Une sortie0 ou une phrase « terminé » ne valide pas une exécution sur le Dell demandé. Vérifier le profil distant, le fichier réel, les empreintes et le résultat du test.

## Déploiement reproductible et retour arrière

1. Sauvegarder les fichiers actifs, les unités systemd, les profils/outils WebUI et les réglages Qwen avant modification ; préserver les ajouts historiques absents de la branche.
2. Copier les nouveaux modules `client_capabilities`, `client_mcp`, `qwen_specialist` et `google_workspace` dans `/opt/jarvis/conversation/jarvis/`. Ajouter leurs registrations ciblées dans le registre, sans remplacer les autres modifications du runtime.
3. Installer le lanceur et le fichier MCP de `tools/qwen_webui/`. Appliquer les scripts de compatibilité au paquet0.26.4 effectivement installé ; les versions différentes sont refusées et nécessitent une revue.
4. Installer l’adaptateur dans `/opt/jarvis/webui-tools/webui_adapter.py` et son unité livrée. Le service utilise le Python de la conversation.
5. Mettre à jour les outils Open WebUI par ses API d’administration, en conservant les valves privées et les versions originales. Le contenu des deux classes d’outils doit être asynchrone. Les profils livrés exposent le connecteur canonique et désactivent les outils intégrés concurrents de mémoire.
6. Déployer la fonction de relais Ollama compatible avec JSON/non-streaming dans le garde existant. Le détail des sources réellement actives figure dans les preuves finales. Contrôler les appels en cours avant de recharger un service.
7. Pour les essais distants, ajouter uniquement le projet isolé `integration-agentique` aux deux profils SSH existants, racine `/opt/jarvis-lab/integration-agentique`, sans GPU et sans modifier leurs accès historiques.
8. Relancer uniquement les services modifiés et inactifs au moment du contrôle. Vérifier ensuite l’interface et les outils chargés.

Les sauvegardes privées de cette intervention sont sous `integration-agentique-webui-qwen-code-private/`. Pour revenir en arrière : restaurer les fichiers ciblés et unités sauvegardés, les versions d’outils/profils WebUI précédentes et les chunks Qwen sauvegardés, puis recharger les seuls services concernés. Ne pas supprimer les bases, missions, historiques et reçus de cette campagne. Les paquets Google ajoutés ne nécessitent pas de retrait pour restaurer les anciens services.

La connexion Google initiale est détaillée dans [GOOGLE-RACCORDEMENT.md](GOOGLE-RACCORDEMENT.md). Les jetons et clés restent locaux ; aucun secret n’est livré dans GitHub.


## Profils de mission et sources actives

La création depuis les clients sélectionne les contrats plats et la restitution factuelle déjà développés. `profile=standard` ne verrouille pas les missions en lecture seule ; `service_observation` est un choix explicite réservé aux objectifs d’observation systemd. Ces options ne fournissent pas de plan à JARVIS et ne valent pas réception de toute nouvelle mission. La sonde de cette livraison a été clôturée nativement après correction structurelle de la disponibilité des observations pendant la vérification ; son historique assisté reste documenté.

Le garde actif utilise `/opt/jarvis/inference-gateway/optimisation_interconnexions/inference_gateway.py`, avec le relais sous `/opt/jarvis/inference-gateway/qwen_webui/ollama_guard.py`. L’adaptateur actif est `/opt/jarvis/webui-tools/webui_adapter.py`. Les services n’utilisent plus les fichiers du worktree de développement pour ces deux composants. Identités et contrôles : [DEPLOIEMENT.json](DEPLOIEMENT.json).

Le complément de correction0ad2e8c déploie aussi `jarvis/durable_cycle.py`. Sa sauvegarde privée est `durable_cycle.before-observation-recovery.py` ; retour arrière par restauration de ce seul fichier puis recharge des workers sans mission active. La réception de la même sonde après correction figure dans `CORRECTION-VERIFICATION-PENDANTE.md`.

Le compositeur de relevé systemd est réservé au profil `service_observation` ; il n’est pas imposé aux objectifs généraux du profil standard. Après une recharge systemd, attendre que le port applicatif réponde avant les contrôles HTTP : l’état active du processus ne garantit pas la fin de son initialisation.
