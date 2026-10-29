# Qwen Code : installation et intégration effectivement observées

Qwen Code0.26.4 etNode22.23.4 sont dans le préfixe privé duMac ;Node20.19.2 système est conservé. Entrée :`~/.local/bin/qwen-local`, limitée aux projets sous `JARVIS/qwen-code-projects/`. Le wrapper fournit explicitement le modebare, le modèle80B et l'API locale8091. Le garde refuse les requêtes de plus de27648octets, traduit vers l'API native Dell1:11435 et impose32768contexte/4096sortie. Aucun poids téléchargé.

La trace réelle indique le80B, les outilsread_file/edit/notebook_edit/run_shell_command et `mcp_servers=[]`. Des agents sont enregistrés dans le logiciel, mais les outilsagent/list_agents/send_message sont exclus par le wrapper. **Présence de sous-agents dans le produit ≠ délégation activée dans ce profil.** Aucun serveurMCP n'est raccordé à cette session. Les sessions/transcriptions Qwen persistent séparément ;elles ne sont pas la mémoire canonique JARVIS.

## Nouvel essai indépendant

ProjetGit dédié `audit-interconnexions`, différent de l'ancienacceptance. DéfautCodex :`enabled('false')` renvoieTrue via bool(value). Trois tests inchangés :false-string,false/truebools,true-string. Avant :1FAIL/2PASS. Qwen lit, choisit ses appels, exécute le test, ajoute le traitement des chaînes et relance le test. **Code0,5tours,32,889s ;3PASS.** Codex relit le diff, vérifie le test inchangé et exécute indépendamment les3testsPASS. E04 contient les événements, commandes, paramètres, métriques et empreinte de la trace. Il n'y a aucune correction sourceCodex pendant cet essai.

Le total d'entrée20614tokens est **cumulé sur cinq requêtes**, pas la taille d'un seul contexte. Sortie cumulée406tokens. Le80B est observé chargé surDell1-missions avec32768contexte et environ47,7GoGPU ;Mac exécute les outils. Les deux3090 sont occupées à environ23285/23090Mio après l'essai. Ces mesures partagées ne sont pas une attribution exclusive de chaque octet au projet.

La correction traite les valeurs testées et les variantes de casse de'false'. Elle ne constitue pas un contrat général de validation de toute chaîne, ni un déploiement d'application. Le programme reste dans la fixture, sans intégration àJL03 ou aux services actifs. Le rapport du modèle ne remplace pas les tests indépendants.

## Interconnexions et autonomie

- **Open WebUI→Qwen Code :fonctionnement historique reçu et raccordement actuel conservé.** Le profilCode porte toolIds=jarvis_qwen_local ;son outilqwen_code appelle8092, qui démarre le wrapper dans le projetGit. Les reçus navigateur de la mission précédente prouvent l'exécution réelle ;l'audit neuf vérifie laCLI et les mêmes sources/points d'entrée, sans rejouer tout ce scénario.
- **Qwen Code→Mission Engine :pas de délégation automatique observée.** La même boîte à outils WebUI possède jarvis_task, mais c'est une autre fonction appelant le moteur canonique. Une juxtaposition de boutons n'intègre pas Qwen Code à ses checkpoints, reçus de déploiement, compteurs et admission.
- **Qwen Code→Dell2 :pas de worker spécialisé ouMCP configuré.** Le shell du compte pourrait appelerSSH avec les accès existants, mais cette possibilité n'est pas une répartition automatique reçue. Le profil standard travaille surMac.
- **Fiabilité :avec réserves.** Les arrêts à12tours malgré testsPASS de la mission précédente sont conservés. Le wrapper borne12tours/12outils/10minutes et donne une consigne d'arrêt ;ce n'est pas un compteur sémantique universel de trois corrections.

Les capacités lecture/édition/shell/tests sont utiles et recouvrent des outils développés dansJARVIS. Elles ne rendent pas inutiles la politique du broker, les états durables, la mémoire canonique, les validations croisées et le contrôle du code déployé.
