# TTS-01 — architecture de reprise

Le moteur de missions, le broker et JL-02 existants sont étendus. Aucune nouvelle base, identité SSH ou boucle de missions concurrente n’est créée. Le worker et le chat authentifié peuvent servir à la coordination ; leurs preuves sont distinguées et reliées explicitement à l’identifiant canonique TTS-01.

## Exécution distante

`host_remote` conserve le profil Dell identifié `dell-observe`. Chaque opération passe par la clé serveur épinglée et le garde matériel déjà qualifié. Le projet `tts-01` est explicitement accordé dans la politique root, avec racine `/opt/jarvis-lab/tts-01`. Le modèle ne dispose ni des clés ni d’un shell root.

`project_exec` exécute les opérations JARVIS dans cette seule racine inscriptible, avec réseau hôte, système de fichiers `/usr` en lecture seule et périphériques NVIDIA accordés à ce projet. Les alternatives Debian doivent aussi être visibles en lecture seule pour résoudre les liens des outils et bibliothèques NVIDIA. Ce terminal est destiné à l’installation et à la génération ; il ne peut pas servir de preuve de lecture indépendante par simple changement d’étiquette.

`project_probe` exécute des programmes fixes, sans argument de commande ou code fourni par le modèle. La racine du projet est montée en lecture seule, avec un temporaire éphémère pour les caches d’exécution. Quatre sondes sont proposées :

| Sonde | Lecture et périmètre |
| --- | --- |
| gpu_inventory | Nom GPU, pilote, mémoire GPU et versions Python/noyau réellement observés |
| archive_inventory | `references.zip` : intégrité,14 WAV hors métadonnées, durées/débits/niveaux calculés, pleine échelle et empreintes |
| tts_runtime | Interpréteur `venv/bin/python` : import PyTorch, disponibilité CUDA et somme effectivement calculée sur GPU ; présence du paquet TTS |
| script_syntax | `bash -n` sur `lancer_tts.sh` et `desinstaller_tts.sh` ; ce contrôle ne lance pas la désinstallation et ne prouve pas à lui seul le fonctionnement du TTS |

Le vérificateur sémantique accepte ces sondes comme observations indépendantes. Il refuse les sources `project_exec` dès validation du contrat. Un import réussi, un schéma JSON conforme ou un code retour0 ne reçoit pas l’ensemble de la mission : les trois vraies générations, leur signal, leurs mesures et leur lecture restent à contrôler.

## Transferts et restitution

`project_upload` et `project_download` utilisent les accès SSH existants, limitent racines/types/taille et comparent les SHA256. Les données binaires ne sont pas recopiées dans le contexte du modèle. L’écriture d’une destination locale s’effectue sous l’identité technique, sans donner au chemin sélectionné une autorité d’écriture root.

JL-02 sert les WAV des projets via son API déjà authentifiée, avec `audio/wav`, signature RIFF/WAVE et limite16MiB. Les sorties de racine, liens symboliques sortants et dossiers privés restent refusés. Le panneau de preuves propose un lecteur aux artefacts WAV. Aucun fichier de film n’est publié dans Git ou sur un service public ; seuls des rapports et mesures sont publiables.

## Contrats et attribution

Le plan initial JARVIS a accumulé41 versions avant les opérations. La vue de travail compacte désormais les répétitions ; toutes les versions et leurs auteurs restent indexés et les définitions originales consultables. Les contextes précédents sont archivés.

Les plans42–44 sont des interventions Codex : contrats corrigés, sondes indépendantes puis ajout du seul contrôle de niveau/saturation manquant. Ce sont des opérations d’orchestration dirigée. Pour TTS-01, le contrôle expérimental automatique de couverture26B est désactivé ; le mode sémantique26 et la réception indépendante restent utilisés.26B demeure clôturée incomplète, sans levée rétroactive de ses réserves.

Le transfert de l’archive a été réalisé par JARVIS via le chat JL-02 existant, sur ordre ponctuel de Codex. Ses trois reçus réels sont corrélés au broker et liés à la mission par un événement de coordination ; ils ne sont pas inventés comme appels internes du worker. JARVIS a ensuite recontrôlé l’archive depuis sa tâche durable. Les premiers rapports erronés restent conservés et appellent des errata distincts.
