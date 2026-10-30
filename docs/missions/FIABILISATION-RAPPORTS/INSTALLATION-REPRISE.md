# Installation et retour arrière

Branche `codex/fiabilisation-rapports-preuves`, issue de `aaf72cc` (PR33). Aucun remplacement du modèle ni des services Ollama.

Les correctifs ont été appliqués à `/opt/jarvis/conversation/jarvis/` par ajouts ciblés sur les fichiers installés : `mission_assurance.py`, `durable_cycle.py`, `verification.py`, `attempt_ledger.py`, ainsi que `tools.py` et `mission_reporting.py`, et nouveau `report_claims.py`. Les ajouts historiques du runtime, absents de l’arbre Git, ont été préservés. Le patch runtime et le manifeste de réception permettent de contrôler les modifications réellement installées.

Sauvegardes privées : `/home/adminjarvis/JARVIS/fiabilisation-rapports-preuves-private/`. Les fichiers `.before` correspondent au début de l’intervention. Les événements et les écritures originales restent dans `runtime/missions.sqlite`.

Avant changement : interrompre la seule sonde concernée et attendre absence de lease **et** absence de calcul en cours. Après installation : compiler/importer, contrôler les empreintes, puis recharger seulement les deux workers de mission au repos. Aucune nécessité de redémarrer conversation, JL-03, Apache, Open WebUI ou Ollama.

Retour arrière : restaurer les six `.before` depuis le dossier privé et retirer le nouveau module si tous ses appels ont été retirés, puis recharger les workers inactifs. Désactiver les deux options de cette sonde avant reprise avec l’ancien parcours. Le rollback du code ne restaure pas un ancien PASS invalidé et n’efface jamais les compteurs ou les preuves. Ne pas remettre en file M26-P4 ; son MANUAL-HOLD est conservé.

Tests logiciels reproductibles depuis la racine du dépôt :

```sh
/opt/jarvis/conversation/.venv/bin/python tools/optimisation_interconnexions/run_checks.py
```

Ces tests utilisent des fixtures explicites. Ils ne prouvent pas une exécution autonome de JARVIS. Les événements natifs sont publiés séparément.


La sonde active en plus `proof_bound_report_write`. Cette option ajoute dynamiquement l’adaptateur de rapport dans la phase de correction ; elle ne crée pas un service ni un second moteur. Pour le rollback du parcours, désactiver également cette option. La prose et les reçus de ses essais restent dans le journal canonique.


Le mode reçu de repli utilise `proof_bound_explanation_mode=facts_only` après l’escalade des commentaires libres. Il impose une explication vide et une comparaison exacte avec la sortie du moteur, avec événement de provenance. Désactiver ce mode pour revenir à des commentaires libres exige de les qualifier de nouveau ; la réception factuelle n’autorise pas à les considérer fiables par défaut.
