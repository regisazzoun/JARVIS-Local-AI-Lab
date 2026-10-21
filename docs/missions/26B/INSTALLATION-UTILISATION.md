# Installation et utilisation

Installateur : `sudo /opt/jarvis/conversation/.venv/bin/python agentic/mission_engine26b/install.py`. Il compile les sources avant copie, refuse une mission en cours, sauvegarde les anciens modules sous `/var/backups/jarvis/mission-engine26b/`, contrôle que la politique hôte reste identique et ne redémarre que jarvis-conversation. Les bases, broker et services LiveKit ne sont pas remplacés. Empreintes et sauvegardes : [INSTALLATIONS.json](INSTALLATIONS.json).

Les nouveaux objectifs autonomes soumis au moteur utilisent `spec.assurance=true` par défaut ; les specs historiques ne sont pas modifiées. L’API reçoit un objectif brut, sans tableau tasks. JARVIS utilise le même mission_plan qu’en26 ; l’extraction et le contrôle de couverture sont automatiques. Le retour contient version courante, coverage et execution_allowed. Un FAIL demande au modèle sa propre révision append/patch ; il n’autorise pas les opérations.

mission_progress expose les exigences extraites, plans, audits, catalogue de preuves et exemples actifs. L’interface décode les tableaux/objets envoyés comme chaînes JSON valides, puis les valide sans transformer les types scalaires. Les diagnostics de schéma indiquent le champ concerné. Les versions ne s’incrémentent pas pour un schéma refusé ; un candidat valide mais incomplet est conservé avec audit FAIL et exécution suspendue.

Les rapports restent en prose libre. mission_report_review reçoit content et scope task/mission pour une prélecture ; les outils de réception/publication l’imposent aussi. Le modèle doit reprendre lui-même son texte depuis les faits contradictoires/manquants. Chaque tentative reste dans narrative_review. Les références attendues sont des ids d’invocation, event:N, plan:N ou task:id réellement présents dans le journal.

Les contrats de lecture sont explicites : source={tool:host_read_file,arguments:{path:chemin}}. JSON utilise des JSON Pointers (/count) ; text utilise le contenu exact equals ou son SHA256 ; service observe seulement l’état systemd réel. Le nouveau kind digest relit un manifeste JSON et son fichier cible baseline_source, puis compare le champ /sha256 à l’empreinte réelle. Il ne requiert ni empreinte devinée ni commande fournie par Codex. Un résultat indisponible conserve INSUFFICIENT et ne reçoit pas la tâche.

Pour le cas partiel : conserver le rapport reçu par mission_report_review, puis mission_block avec une preuve réelle et le rapport local. L’exécution attend alors la dépendance externe ; ce n’est pas une clôture technique réussie.
