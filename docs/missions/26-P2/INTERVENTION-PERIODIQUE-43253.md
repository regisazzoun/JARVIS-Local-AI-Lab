# Intervention ciblée Codex-periodic — 26 octobre 2026

P2 reste 🟡 non reçue. Mission native inchangée `3aa717f3887e49daa7daf7e883ee52e4` ; P3/P4 non confiées.

Cause observée : escalade43248 après trois appels authority_read_execution avec start_line=0. La lecture43239 avait réussi : aucune panne du stockage des reçus. Le schéma de cette seule mission précise désormais la numérotation depuis1, sa valeur par défaut et la possibilité d’omettre ce champ. La borne minimale reste1 ; aucune lecture ambiguë n’est réactivée.

Vérification :24tests logiciels du garde/lecteur réussis. Lecture réelle43251 du reçu SHA de42832 réussie, conservant observed_process_returncode=1. Cette lecture d’un ancien échec ne qualifie pas le candidat actuel. Un premier contrôle ad hoc du Registry a échoué faute de mémoire temporaire initialisée ; corrigé dans le contrôle seulement, sans écriture dans la mémoire canonique. Sauvegarde du code installé et reçus restent privés.

Les événements plus récents attestent la correction SQL JARVIS43152 et la synchronisation du source. Elle n’a pas été rejouée. Le test43189 contient FAILED(errors=2) malgré un code processus0 : la commande Qwen terminait par un pipeline head. Ce résultat ne constitue aucun PASS. Les tests attendent encore une référence chaîne ou un SUCCESS sans référence ; la consigne43252 exige leur correction avec événements utiles réels dans une base temporaire, les cas négatifs conservés, puis tests directs sans pipeline et contrôle Dell2 avec source et tests synchronisés. La nature utile de la preuve doit également être vérifiée ; un événement de plan ne suffit pas.

Réparation de présentation du schéma attribuée à Codex-periodic, événement43253 ; aucune autocorrection Qwen revendiquée. Mission déjà interrupted, aucun worker ne détenait de mission running. Les deux workers ont été arrêtés proprement et observés inactive avant remise en file queued, puis redémarrés pour charger le schéma. Aucune opération inconnue tuée. Instruction canonique43252, acteurs Codex/Codex-periodic explicités pour le mécanisme existant. Compteurs failed_cycles=4 et correction_resolved_through=3 conservés ; aucun compteur du superviseur modifié.

Directives relues : AGENTS, charte, SUPERVISION-CODEX, contrat/lancement et dernier rapport P2, événements et code réel. Autorisations autonomes conservées. Aucun MANUAL-HOLD créé pour ce passage déjà verrouillé, aucun agent Codex supplémentaire, aucun autre périmètre modifié. Les dix cas réels P2 restent requis ; aucune réception implicite ni fusion main.
