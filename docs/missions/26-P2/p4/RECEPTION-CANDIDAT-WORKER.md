# Candidat d’attestation du worker — réception ciblée

**VALIDÉ AVEC RÉSERVES**, réception indépendante65474. **P4 globale non validée.**

Le raccordement produit désormais un rapport depuis le processus qui exécute
réellement `worker.run`, avec `Core` et `Missions` réels. Le test utilise un runtime
privé vide, sans publier ni exécuter de mission utilisateur ; il arrête ce worker
par son véritable gestionnaire SIGTERM. Aucune fonction du worker n’est recopiée
dans l’oracle et aucun ordonnanceur simulé n’est substitué.

| Contrôle | État réellement obtenu |
|---|---|
| Fonctions chargées conformes au candidat | PASS |
| `Core.chat.__code__` modifié uniquement dans le processus de test | FAIL détecté |
| Répertoire candidat absent | INSUFFICIENT |
| Option désactivée | Aucun rapport, démarrage et arrêt propres |

Le code reste identique pendant chaque suite. Le PID du rapport correspond au
processus enfant observé par l’oracle. Ces PID appartiennent à l’espace de PID
de l’exécution projet : leur identité se lit **avec le reçu broker**, jamais comme
le PID d’un service systemd canonique.

## Preuves et attribution

- PlanJARVIS3 conservé ; même mission `d8fe752876db480cbe5f22cd5525e2dd`.
- Trois propositions natives64834/64855/64876 non recevables ; aucune quatrième
  inférence autonome autorisée sur ce source inchangé.
- InterventionCodex après escalade64932 : diagnostic et exemple d’API réels.
  Première assistance64937 refusée64938, erreur d’import reproduite ; assistance
  corrigée64943 donnant la proposition64944.
- **Code du raccordement : Qwen80B assisté parCodex**, pas autocorrection pure.
- **Application JARVIS surDell1 :64975/64982**, répétition64994 renvoyée du cache,
  sans seconde écriture. SHA worker :
  `c90962cee9e18e88c2c782b17149962b78857522def075b67d9d9338a14519ef`.
- **Synchronisation JARVIS :65185**, espace identique.
- **Tests JARVIS :65099 surDell1,65210 surDell2**, puis rejeu65331 surDell2.
  Trois exécutions de quatre cas, pas douze scénarios distincts.
- **Acceptation native :65447**, correctionDell164975 liée au testDell265210.
  Manifeste identique :
  `495d5650f667d66c5885d600f3d5b12ba766ecefa7bb9c4417d3e6474285581f`.
- **Oracle et contrôle indépendant :Codex**,65022/65023, seconde lecture des SHA
  sur les deux Dell et contrôle des reçus immuables dans65474.

Le source de la branche reproduit exactement les octets du worker ainsi testé,
y compris ses deux lignes blanches avec espaces. La correspondance avec le
candidat reçu est privilégiée à une modification cosmétique après tests.

## Réserves

L’assistance de diagnostic/import et les instructions de passage aux étapes
suivantes ont été nécessaires. Les synchronisations/retests redondants sont
conservés dans l’historique : la clôture n’a pas été entièrement autonome.

Le rapportJARVIS original est conservé dans `JARVIS-RAPPORT-CANDIDAT-ORIGINAL.md`.
Ses références et états des quatre cas sont corrects, mais il omet les aides et
les propositions refusées. « Aucun service déployé modifié » doit se lire comme
**aucun déploiement du raccordement applicatif candidat** : Codex a bien modifié
le SDK d’orchestration Mac et rechargé ses workers pendant les déblocages.
La validation native a déjà eu lieu65447 ; ce qui restait était la réception
indépendante Codex puis l’intégration dans les services actifs. Ces précisions
n’effacent pas le texte original.

Le mécanisme couvre les fonctions Python sélectionnées (`run`, `main`,
`Core.ollama`, `Core.chat`), pas les globals, valeurs de closures/défauts ni le
code natif. Le rapport est émis au démarrage : sa fraîcheur sur une longue
exécution reste à traiter. Aucun service systemd canonique n’est attesté par
ces essais isolés. Les huit situations P4 de déploiement/provenance/retour arrière
restent à réceptionner séparément. Ni14A ni24-Old ne sont lancées ou clôturées.

Les évolutions du moteur passent161 tests logiciels ciblés après intégration du
source reçu. Ce nombre ne constitue pas une mesure d’autonomie. Les observations
structurées et reçus sont dans `RECEPTION-CANDIDAT-WORKER.json`.
