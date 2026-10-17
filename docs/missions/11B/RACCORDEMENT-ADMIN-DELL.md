# Mission 11B — raccordement permanent de l’administration Dell

Date : 17 octobre 2026. Branche : `jarvis/mission-11b-compute-expansion`.

## Référentiel et checkpoint

Directives consultées : AGENTS, charte JARVIS, rapport et architecture 11, SUIVI/ROADMAP, dernière réception 13D-E/14 et ordre 11B conservé dans la conversation canonique. Autorisations préservées : administration Dell IA sans validation intermédiaire, identités existantes, préservation du Mac/mémoire/voix/Bbox, une RTX alimentée, secrets privés, aucune fusion main. Exclusion : JL-02.

Le dernier checkpoint 11B retrouvé était un refus d’administration à cause du profil `dell-observe` en lecture seule. Aucun run durable 11B n’existait dans missions.sqlite : le checkpoint était conversationnel. Cette intervention ne crée pas de nouvelle mission numérotée. La branche prévue par l’ordre initial est réutilisée comme nom de branche de travail ; elle n’existait pas encore sur origin au début de l’intervention.

Le Dell est sous Debian 13.7, RAID1 [UU] sans resynchronisation. SSH adminjarvis et sudo non interactif ont été vérifiés. L’installation 13D-E/14 est réceptionnée : aucune réinstallation, aucun nouveau compte ou clé.

## Politique effectivement appliquée

`/etc/jarvis/host-policy.json`, propriété root et mode 0600, conserve `dell-observe` pour compatibilité. `allow_admin=true`, `ansible_enabled=true`. Le broker est activé au boot et recharge cette politique protégée ; les mises à niveau install.sh ne remplacent pas les droits existants. L’ancien provisionneur d’observation refuse maintenant de rétrograder un profil déjà administrable.

Droits propres au Dell, sans élargissement implicite aux autres profils :

- Fichiers : `/var/lib/jarvis/projects`, `/opt/jarvis/compute`, `/etc/jarvis/managed`, `/etc/ollama`. Les deux derniers utilisent sudo via une opération structurée ; pas de shell root général.
- Paquets IA/développement explicitement listés : outils Python, compilation, OpenBLAS, ffmpeg, outils système, pilotes NVIDIA/CUDA et dépendances courantes. Installation SSH et Ansible disponibles.
- Services : démarrage, redémarrage, activation et consultation de jarvis-ollama et nvidia-persistenced ; SSH reste consultable, sans arrêt accordé au modèle.
- Commandes prédéfinies : identité/sudo, ressources, services, catalogue Ollama et contrôle du stockage.

Avant chaque opération distante, SSH épingle la clé serveur existante puis exécute un garde root comparant DMI et identité exacte des deux NVMe au manifeste privé qualifié. Les séries sont comparées par empreintes, modèles et capacités exactes ; pas de sélection par ordre seul. Une divergence arrête l’opération avant mutation. Le garde est root et non inscriptible par l’agent.

Les clés et known_hosts existants restent sous leurs chemins privés ; le modèle reçoit les opérations disponibles, sans chemins des clés ou contenu des secrets. Les opérations sont journalisées dans le registre et les traces existants. Une sauvegarde de politique est conservée dans un répertoire root privé.

## Corrections livrées

| Fichier sous agentic/mission11/ | Changement |
| --- | --- |
| activate_dell_admin.py | Provisionnement opérateur reproductible : réception préalable, contrôle cible/stockage, sauvegarde et politique atomique, identités existantes. |
| host_bridge.py | Garde d’identité avant SSH/Ansible ; paquets/services par profil ; fichiers privilégiés dans les seules racines accordées ; politique exposée sans références au matériel SSH privé. |
| host_client.py | Descriptions d’outils actualisées : suppression de l’exclusion historique générale du Dell. |
| core.py | Suppression de la consigne périmée « Dell en cours d’installation » ; conservation de tous les profils distants lors de la réduction du contexte. La troncature précédente masquait le Dell derrière loopback et provoquait des lectures répétées. |
| activate_observer.py | Ne rétrograde plus l’administration permanente lors d’une exécution ultérieure. |
| reception_11b.py | Tests authentifiés : Qwen choisit et appelle les outils ; aucune réponse ou invocation de modèle simulée. Preuves brutes privées. |
| test_bridge.py | Vérifications du périmètre distant, absence de références aux clés et refus avant mutation en cas d’identité divergente. |

Le premier essai Qwen s’est mis à répéter host_policy avec l’ancien résumé tronqué. Il a été interrompu pour charger la correction ; cet essai interrompu ne vaut pas réception. Les traces sont conservées. Le second essai a atteint les actions réelles, avec encore plusieurs lectures répétées de politique : une réussite ciblée ne démontre pas une planification parfaite.

## Preuves et réception

Voir [PREUVES-RACCORDEMENT.json](PREUVES-RACCORDEMENT.json) pour les assertions et identifiants de preuves expurgées. Les traces intégrales restent dans un répertoire privé hors dépôt. Ne pas confondre réussite du raccordement et réception de toutes les fonctions Compute Expansion, notamment routage/repli automatique.

### Résultats vérifiés

- Qwen avant redémarrage : identité/sudo, Ansible ping, création du fichier par Ansible, relecture SSH et état actif d’Ollama ; tous les retours d’opération sont à zéro et identifiés `JARVIS-runtime` par le broker.
- Après redémarrage de `jarvis-host-bridge` et `jarvis-conversation` : Qwen relit la preuve précédente, écrit `stage=after-restart` via Ansible et la relit via SSH ; Ansible ping réussit encore. Les identifiants de preuves sont corrélés aux événements du broker, pas déduits du texte produit par Qwen.
- Observation indépendante Codex : garde d’identité réussi, contenu final `after-restart`, SSH et jarvis-ollama actifs.
- 12 tests des frontières du broker réussis, dont refus de lecture de /etc/shadow, refus d’arrêt SSH, paquet hors liste refusé et arrêt avant mutation sur identité divergente.
- 27 tests du backend conversationnel réussis après correction du contexte ; compilation Python réussie.

**GO pour le raccordement permanent SSH/Ansible du Dell.** Cela ne clôture pas à lui seul la mission Compute Expansion. Les répétitions d’appels Qwen restent une limite observée ; les écritures répétées de ce scénario portaient le même contenu de preuve. Le budget de réduction du contexte a été ajusté pour éviter de supprimer tout l’historique des opérations lorsque les instructions et souvenirs occupent déjà 9 000 caractères. La reprise durable 11B doit vérifier le routage/repli et les capacités restantes, sans réinstaller les composants acquis ni lancer JL-02.

## Reprise effective de 11B

Le checkpoint conversationnel a été transmis au planificateur existant via l’API authentifiée, par `resume_11b.py`. Exécution durable : `4d824f2bbc664b5789144f146e845e14`, état observé `running`, tentative 1. Qwen a enregistré le plan audit → modèles → expansion et exécuté des outils réels, dont SSH distant et lecture des ressources. Ce n’est pas une simple instruction laissée dans un fichier. Les observations durables sont conservées dans missions.sqlite ; les opérations acquises restent dans le checkpoint et ne demandent pas de réinstallation.

La reprise couvre les évaluations des modèles et les fonctions restantes, dont le repli en cas d’indisponibilité du Dell. Ces fonctions ne sont pas déclarées reçues au moment de ce rapport de raccordement. JARVIS doit produire sa documentation et son verdict 11B ; JL-02 reste exclu.
