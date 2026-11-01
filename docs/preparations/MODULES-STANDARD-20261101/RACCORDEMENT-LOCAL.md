# Raccordement local natif — 1 novembre 2026

**🟡 Configuré, non testé.** Suite de l’installation brute, sur demande explicite du propriétaire : raccorder aujourd’hui les Skills/outils locaux à WebUI/Qwen et préparer les configurations/inventaires du lycée, sans tests, sans nouveau moteur, sans toucher aux missions ni redémarrer les serveurs.

Suivi : [issue42](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/issues/42). Livraison dans la [PR43](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/43), toujours en brouillon, sans fusion main.

## Ce qui est raccordé

| Parcours | Configuration effectuée | Limite de preuve |
| --- | --- | --- |
| WebUI → Skills | 18 Skills copiés dans `~/JARVIS/modules-standard-20261101/native-skills`, avec liens dans `~/JARVIS/qwen-code-projects/.agents/skills` | Chemins natifs configurés ; catalogue non interrogé |
| Profils WebUI | `builtinTools.skills=true` sur `jarvis-qwen-code-lab` et `jarvis-tools-conversation` ; terminal `jarvis-standard-terminal` conservé ; instructions de chargement à la demande ajoutées | Relecture de configuration persistée seulement ; aucun chat envoyé |
| WebUI → Office/PDF/pédagogie/Draw.io/conversion | Instructions natives et chemins absolus des scripts/interpréteurs fournis dans chaque Skill ; exécution prévue par le terminal existant | Aucun script, conversion ou document exécuté |
| Qwen Code standard → Skills | 18 liens dans `~/.qwen-standard/skills` ; même bibliothèque que WebUI | Découverte prévue à la prochaine session, CLI non lancé |
| Qwen Code standard → MCP locaux | Six entrées ajoutées au `mcp.json` natif : Filesystem, Draw.io, MarkItDown, Pandoc, Fetch et Ansible | Configuration enregistrée ; processus MCP non démarrés, aucun handshake |

Les Skills concernés restent les 18 sélectionnés lors de l’installation : Office, PDF, quatre Learning Commons, neuf pédagogiques Gareth Manning, DevOps Engineer, méthode NetBox et Draw.io. Les instructions NetBox sont accessibles, mais leur connecteur réseau reste en attente des accès.

La racine utilisée par Open Terminal0.14.7 est son dossier de travail : `~/JARVIS/qwen-code-projects`, d’après le service et le code `UserFS`. Les liens natifs y sont placés ; aucun lien global permanent ajouté à `~/.agents`. Le chemin Qwen Code standard est distinct grâce à `QWEN_HOME=~/.qwen-standard`. Les clients et moteurs historiques ne sont pas reconfigurés.

L’[intégration native Skills d’Open WebUI](https://docs.openwebui.com/features/workspace/skills/) expose les Skills du terminal et les charge à la demande. Les [Skills Qwen Code](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/skills.md) sont des dossiers d’instructions et de ressources. Ces mécanismes amont ont été confrontés au code installé ; aucun nouveau registre ou moteur maison ajouté.

## Adaptations des Skills

- Originaux conservés dans `skills/`, révisions et licences initiales inchangées.
- Copies natives : descriptions courtes en français, chemins d’exécution absolus, correspondance entre les anciens noms d’outils Hermes et les outils réellement disponibles.
- Interpréteur Office/PDF : `~/JARVIS/modules-standard-20261101/venvs/documents/bin/python`. Fichier d’environnement documentaire existant : `documents.env`. Aucun moteur Hermes installé.
- Les livrables sont dirigés vers `~/JARVIS/qwen-code-projects/livraisons`, sans écraser automatiquement les originaux.
- Skills chargés à la demande, pas injection des 18 contenus dans chaque message. Les règles existantes d’arrêt après résultat et de respect des cibles restent conservées.
- Les référentiels français CIEL/BTS et gabarits réels restent à fournir ; la description française ne constitue pas une adaptation pédagogique validée.

Pour Draw.io, le Skill permet notamment d’écrire des fichiers XML `.drawio` via le terminal. Le MCP Draw.io est configuré pour Qwen Code ; Draw.io Desktop et les exports facultatifs restent distincts.

## Configurations MCP locales

Les six commandes standard stdio sont enregistrées dans `~/.qwen-standard/mcp.json`, sans supprimer le serveur `jarvis` déjà présent. Elles démarreront seulement lors d’une prochaine session native qui les charge ; rien n’est lancé aujourd’hui.

Filesystem est limité au dossier de livrables, pas au domicile ni aux secrets. Le MCP Ansible utilise un workspace de préparation dont l’inventaire est vide et les collections isolées installées. Les transports Paramiko5.1.0, ansible-pylibssh1.4.0, pywinrm0.5.0 et pypsrp0.9.1 ont été ajoutés à son environnement, sans accès distant.

La lecture des fichiers du connecteur Pandoc a révélé un import `mcp.server.fastmcp` absent du SDK2.3 installé à brut. Sa dépendance est désormais limitée à `mcp>=1.24,<2`, résolue en1.30.0. Correction de compatibilité issue de lecture statique, pas d’essai d’exécution ; les autres environnements MCP restent séparés.

**WebUI direct n’a pas reçu de nouveaux endpoints HTTP MCP.** Ses Skills passent par Open Terminal, déjà actif. Une configuration MCPO locale à six connecteurs est préparée dans `connection-templates/mcpo-local.pending.json`, mais elle n’est pas chargée dans le service existant : la contrainte de ne toucher à aucun service est respectée. Le fonctionnement WebUI et celui de Qwen Code ne doivent pas être confondus.

## Ce qui est préparé pour le lycée

Tous les modèles se trouvent dans `connection-templates/`, copiés avec ce rapport :

- `infrastructure.csv` : fiche vide pour noms, rôles, OS, adresses, transports, comptes, références privées, empreintes et périmètres autorisés.
- `ansible/inventory.yml` : groupes Linux, Windows, Cisco, pfSense, Nagios, NetBox, **zéro hôte**.
- `ansible/ansible.cfg` : chemin des collections isolées, contrôle des clés d’hôte conservé.
- `ansible/group_vars/*.example` : options Linux SSH, Windows SSH/PowerShell ou WinRM alternatif, Cisco network_cli. Les fichiers `.example` ne sont pas activés.
- Testbed Cisco vide et copie intacte de l’exemple amont, à remplacer par les vrais équipements.
- Exemples NetBox, Nagios et pfSense sans identifiant réel ni secret.
- `mcp-lycee.pending.json` : candidats **non activés** NetBox Enhanced, Nagios, pyATS, pfSense et éventuel GitHub officiel. Ce dossier n’est pas une configuration client chargée.
- `RACCORDEMENT-LYCEE.md` : ordre de raccordement et de découverte autorisée, sans lancer de balayage.

GitHub continue d’utiliser son connecteur JARVIS déjà présent ; le binaire officiel préparé n’est pas ajouté en doublon. Les identités Google et SSH existantes restent inchangées.

## À faire au lycée

1. Fournir/confirmer la liste des machines et les cibles/plages de découverte autorisées ; après déplacement, relever adresses, routes, DNS et empreintes/certificats.
2. Compléter inventaires, comptes, privilèges, versions OS/IOS, testbed Cisco et transports Windows/AD. Aucun secret dans Git.
3. Raccorder NetBox Enhanced aux droits réellement accordés ; vérifier Nagios Core/CGI ; confirmer pfSense REST APIv2 et sa CA. Aucune installation automatique sur le pare-feu.
4. Décider si une exposition MCP HTTP directe supplémentaire à WebUI est utile ; la configuration préparée peut être reprise sans nouveau moteur. Aucune adresse de service inactive n’a été enregistrée comme fonctionnelle.
5. Fournir référentiels français et gabarits. Respecter les licences et l’attribution, notamment CC BY-SA.
6. Autoriser et exécuter les premiers tests réels : découverte des Skills, scripts Office/PDF, rendu visuel, conversions, schéma éditable, connexions et opérations ciblées ; vérifier sorties réelles, codes retour et arrêt après réussite/échec.

## Preuves de configuration et préservation

`manifest.json` relève les liens/empreintes des copies natives, les six noms MCP ajoutés, les changements des profils et les dépendances ajustées. La relecture des profils persiste `skills=true`, le terminal existant et la nouvelle consigne. **Il ne contient aucune preuve de fonctionnement.**

Sauvegardes privées avant modification dans `~/JARVIS/modules-standard-20261101-private/native-connection-before`, exclues de Git. Les autres paramètres des profils et le MCP JARVIS existant sont conservés. Les scripts de configuration sont joints pour attribution/reproductibilité et ne doivent pas être rejoués aveuglément : ils refusent les collisions.

Aucun appel `/skills`, `/skills/read`, `/execute`, conversation/modèle ou MCP effectué. Aucun outil documentaire exécuté ; aucun serveur/processus MCP démarré pour essai. Aucune commande de redémarrage/rechargement/activation de service, aucun accès aux Dell ou machines du lycée, aucune modification des missions, de la mémoire ou de MANUAL-HOLD. La relecture de configuration et des métadonnées est distincte d’un test fonctionnel. Aucune fusion main.
