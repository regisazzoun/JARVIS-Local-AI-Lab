# Utilisation et installation

## Accès disponible

Depuis un équipement autorisé connecté à Tailscale : **http://jarvis-macmini.tail805e83.ts.net/**. Se connecter avec le compte Open WebUI existant. Le test distant Dell1 emploie `curl --resolve` pour isoler le transport ; MagicDNS/Safari/iPhone ne sont pas requalifiés par cet essai. L'accès historique LAN reste `http://192.168.1.99:3000`.

L'URL cible **https://jarvis-macmini.tail805e83.ts.net/** reste non opérationnelle tant que HTTPS/Serve n'est pas activé dans l'administration du tailnet existant. Le client a fourni son lien d'activation, conservé dans les traces privées. Après activation, exécuter `tools/qwen_webui/enable_tailnet_https.sh` ; il vérifie le certificat avec le magasin système avant de retirer HTTP. Ne pas activer Funnel. Le microphone sur une URL distante HTTP n'est pas réceptionné ; son accès navigateur exige HTTPS.

Dans Open WebUI, choisir **JARVIS — Développement Qwen Code (expérimental)**. Le profil utilise le80B existant, sans téléchargement de poids. Demander par exemple : « Utilise qwen_code pour lire prices.py et exécuter python3 -m unittest -v dans le projet acceptance ; ne modifie aucun fichier. » Les outils de consultation et de création de mission canonique sont également disponibles. Ne pas demander la reprise d'une ancienne mission suspendue par inadvertance.

## Qwen Code sur le Mac

```bash
cd /home/adminjarvis/JARVIS/qwen-code-projects/acceptance
/home/adminjarvis/.local/bin/qwen-local
# Appel borné, sortie structurée :
/home/adminjarvis/.local/bin/qwen-local-task 'Lire les sources, exécuter python3 -m unittest -v et rendre un bilan factuel, sans modifier les tests.'
```

Le profil effectif est fourni par les arguments explicites du wrapper `--bare` et par le garde ; il ne dépend pas d'un fichier de réglages global Qwen.

Créer d'autres projets Git sous le même répertoire parent. L'adaptateur accepte uniquement un identifiant de projet existant, jamais un chemin libre. Il ne clone pas arbitrairement un dépôt sur instruction du modèle. Le profil est destiné aux espaces expérimentaux autorisés ; les opérations applicatives distribuées ordinaires continuent d'utiliser JARVIS.

## Composants et fichiers

| Élément | Installation |
|---|---|
| Open WebUI0.12.0 | `/home/adminjarvis/JARVIS/open-webui/compose.yaml`, volume existant |
| Apache2.4.69 | `/etc/apache2/ports.conf`, `/etc/apache2/sites-available/jarvis-openwebui.conf` |
| Tailscale1.104.2 | `tailscaled.service`, Serve en arrière-plan |
| Qwen Code0.26.4 / Node22.23.4 | `/home/adminjarvis/JARVIS/qwen-code-runtime/node_modules/` |
| Garde OpenAI→Ollama natif | `jarvis-qwen-guard.service`, loopback8091 |
| Outils/audio | `jarvis-webui-tools.service`, loopback8092 |
| Projet d'essai Git | `/home/adminjarvis/JARVIS/qwen-code-projects/acceptance` |
| Journaux, clés, sauvegardes | `/home/adminjarvis/JARVIS/qwen-code-openwebui-private/` mode700 |

Sources sous `tools/qwen_webui/`. `config/runtime-package.json` et `config/runtime-package-lock.json` permettent de reconstruire le préfixe npm par `npm ci` après copie sous les noms `package.json` et `package-lock.json`. Le binaire Node22 est installé dans ce même préfixe ; aucune mise à niveau du Node système.

Apache nécessite `proxy`, `proxy_http`, `proxy_wstunnel`, `headers`. Son port8088 est lié exclusivement à127.0.0.1 ; le site Apache par défaut est désactivé. Le fragment `config/compose.integration.yaml` s'applique au **service existant**, jamais à un second conteneur. La clé `QWEN_ADAPTER_KEY` est fournie dans le `.env` privé, jamais dans ce fragment. Conserver `WEBUI_SECRET_KEY`, l'image et le volume originaux. Les réglages vocaux sont dans l'environnement pour survivre à `ENABLE_PERSISTENT_CONFIG=false`.

Importer `webui_tool.py` dans les outils du compte administrateur, renseigner les valves privées, puis importer `config/webui-model.json` comme profil. Cette procédure utilise les endpoints réellement vérifiés `/api/v1/tools/create`, `/api/v1/tools/id/.../valves/update`, `/api/v1/models/create`. Ne jamais publier les valves. Les modifications d'API audio ponctuelles seules seraient perdues au redémarrage dans cette configuration ; employer le fragment persistant.

## Reprise et retour arrière

Les trois unités Apache/garde/adaptateur sont activées au démarrage. Le drop-in Open WebUI attend l'adaptateur. Les redémarrages de ces composants et la recréation contrôlée du conteneur sont vérifiés ; aucun reboot global ni redémarrage Tailscale susceptible de couper un accès n'a été effectué.

Pour retirer cette intégration : arrêter/désactiver les deux nouvelles unités et Apache si aucun autre usage ne lui a été ajouté, retirer seulement le proxy Serve HTTP80 de cette mission, restaurer compose et `.env` depuis la sauvegarde privée de mission, puis recréer **le même** conteneur sans supprimer son volume. Supprimer seulement le nouveau profil/outil par l'interface si souhaité. Conserver les nouvelles conversations ; une restauration globale de la base antérieure les supprimerait et n'est donc pas le retour arrière normal. Les anciennes unités/services/branches JARVIS sont préservées. Ne jamais exécuter `docker compose down -v`.

Les logs Qwen Code et reçus permettent de diagnostiquer un retour non nul. Un test PASS figurant dans un appel finalement arrêté ne suffit pas à déclarer cet appel complet réussi. Ne pas répéter une commande dont l'exécution est inconnue avant relecture du reçu et de l'état Git.
