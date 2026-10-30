# Installation et retour arrière

Branche : `codex/diagnostic-boucles-ia`, sur PR32. Les anciens rapports et branches ne sont pas réécrits. Le relais déployé importe son module voisin de la même réalisation, plus une copie figée dans l’ancienne branche. L’admission ComputeQueue, les modèles, ports, bases et plafonds sont conservés.

| Élément | Emplacement installé |
|---|---|
| Identité active, inchangée | `/opt/jarvis/conversation/identity/JARVIS-v2.md` (configuration13e) |
| Secours corrigé, non chargé par la sonde | `/opt/jarvis/conversation/identity/JARVIS-v1.md` |
| Contexte et interfaces | Modules ciblés sous `/opt/jarvis/conversation/jarvis/` |
| Wrapper Code | `/home/adminjarvis/.local/bin/qwen-local` |
| Relais | `tools/optimisation_interconnexions/inference_gateway.py` de cette branche |
| Service | `jarvis-qwen-guard.service`, port local8091 |
| Audio/WebUI | Adaptateur8092 existant conservé |
| Stockage | SQLite missions/mémoire existants, aucun moteur concurrent |

Les fichiers installés comportent des évolutions récentes non commités de la mission précédente. Ils ont été sauvegardés et patchés **par portions**, jamais remplacés par un ancien arbre Git. Le diff de déploiement est conservé dans `PATCH-RUNTIME.diff`. Les nouvelles fonctions sont versionnées dans cette branche. Les sauvegardes d’origine restent sous `/home/adminjarvis/JARVIS/diagnostic-boucles-ia-private` ; elles ne contiennent pas de nouvelle mémoire canonique.

Redémarrages limités aux processus JARVIS concernés, effectués après arrêt ciblé de la sonde et vérification qu’aucun appel n’était encore engagé. Le démarrage HTTP n’est pas instantané : un refus de connexion avant disponibilité a été observé, puis `/api/health` a répondu200 avant la reprise. Aucun service Ollama ni donnée WebUI n’a été réinstallé/redémarré pour ce diagnostic.

Les nouvelles instances de Core relisent l’identité configuréev2, inchangée. Le correctifv1 concerne seulement le secours. Les workers et la conversation ont été rechargés ; les anciennes attributions à v1 pour la sonde sont rectifiées par91407. JL03 conserve son service et son port distincts. Les modèles et fichiers de données existants ne sont ni déplacés ni supprimés.

Retour arrière : interrompre uniquement la sonde concernée, attendre fin réelle des calculs/outils, restaurer les fichiers sauvegardés correspondants ou inverser les portions du patch après contrôle de leur base. Restaurer `guard-unit-before.txt`, recharger systemd puis redémarrer le garde et les seuls workers/conversation concernés. Ne pas restaurer une ancienne base SQLite ni supprimer plans, compteurs ou événements. Un rollback invalide le manifeste de réparation et ne doit pas recevoir artificiellement le plan. Les tâches en pause restent en pause.

Validation logicielle reproductible :

```sh
/opt/jarvis/conversation/.venv/bin/python tools/optimisation_interconnexions/run_checks.py
```

Comparaison de contexte à partir d’une capture privée authentique :

```sh
python3 tools/qwen_webui/replay_context.py /chemin/prive/requete.json --output /chemin/prive/comparaison.json
```

Le script interroge le même80B à travers l’admission locale8091 et ne déclenche aucun outil proposé dans ses réponses. Ne pas publier de conversations privées avec les preuves synthétiques.

## Profils ciblés et reprise des rapports

L’expérience neuve emploie `planning_context_compact`, `structured_action_calls`, `structured_action_two_stage`, `read_only_service_snapshot` et un `report_workspace` propre. Ce sont des options du moteur existant, pas un nouvel orchestrateur. L’original reste interrompu après l’escalade native90621 ; M26-P4 reste également interrompue.

`AttemptLedger.resolve_report_interface` est un chemin de coordination privilégié, absent du catalogue du modèle. Il exige le code installé réellement différent et contrôlé, une preuve antérieure, une preuve nouvelle et le problème exact de rapport arrêté. Migration SQLite additive : colonne `correction_resolved_through`, défaut0 ; aucun journal, compteur ou checkpoint supprimé. Les tests couvrent migration, faux acteur, mauvaise empreinte, absence de changement réel, prédicat applicatif refusé, réemploi d’une réparation et nouveau blocage après trois échecs.

Le contrôleur affiche séparément total historique et échecs actifs depuis cette frontière. Aucun simple redémarrage, nouveau contexte, alias ou formulation différente ne remet ce seuil à zéro. Le retour arrière logiciel conserve la colonne additive et ses preuves ; ne jamais restaurer les données à une date antérieure.

La revue existante des rapports est activée dans cette expérience par `bounded_narrative_review=true` et `narrative_review_max_segments=4`. Un paquet encore trop grand se divise davantage, sans ignorer ses assertions ni recevoir les seuls morceaux réussis. Les erreurs de capacité n’ajoutent pas un FAIL de correction fonctionnelle.

Les retries worker utilisent eux aussi la frontière d’infrastructure résolue. Les totaux restent visibles. L’actualisation factuelle devient un prérequis de rédaction lorsque le contrat de références manque ou que de nouvelles observations périment les faits lus. Le feedback historique de planification est référencé depuis le checkpoint pendant la correction du rapport ; il n’est plus dupliqué dans le contexte d’exécution.

`pending_report_feedback` sépare désormais les SHA de brouillons : constats actifs du texte courant, références vers les anciens FAIL. Une ancienne erreur corrigée n’est plus réinjectée comme constat présent. Les constats indépendants de la même empreinte restent actifs ; aucun PASS n’est fabriqué par cette séparation. Les tests historiques 26B correspondants ont été exécutés explicitement avec les nouvelles régressions.

Le profil de photographie expose les totaux déterministes par unité/action/valeur dans `service_snapshot_summary`, sans conclusion automatique de santé. Le prompt court de ce profil garde l’identité et les contrats complets dans l’état ; les autres missions conservent leurs profils et ne sont pas reprises. L’enveloppe broker `ok=false` n’écarte plus une observation achevée non nulle lorsque durée, preuve et diagnostic d’exécution l’établissent. Les refus de permission restent refusés.

Comparaison des facteurs de restitution, à partir des entrées réelles figées (aucun outil hôte exécuté) :

```sh
python3 tools/qwen_webui/replay_service_report.py \
  docs/missions/DIAGNOSTIC-BOUCLES-IA/ENTREES-FACTEURS-RAPPORT.json \
  --output /chemin/prive/rejeu-rapports.json
```

Ces quatre inférences ne relancent aucune mission et ne remettent aucun compteur à zéro. Les quatre réponses observées sont conformes au JSON mais non reçues factuellement. La sonde reste interrompue après son escalade ; sa reprise suppose une stratégie technique réellement différente et vérifiée, pas le rejeu inchangé de sa vérification. La revue automatique d’un segment trop grand reste une réserve ouverte, explicitement non livrée comme corrigée.

Le contexte actif est sérialisé en JSON compact sans modifier ses valeurs ; les sérialisations/hashes canoniques restent inchangés. Le redémarrage final de la conversation a été suivi d’un bref refus de connexion avant disponibilité, puis HTTP200 ; les sept services contrôlés sont actifs et WebUI HTTPS retourne200/TLS0. Les trois missions contrôlées sont interrompues sans lease/calcul actif, dontP4avec MANUAL-HOLD.
