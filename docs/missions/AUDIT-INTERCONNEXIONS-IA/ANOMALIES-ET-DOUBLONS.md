# Anomalies et simplifications justifiées

| Priorité | Observation | Classe | Correction proposée après bilan |
|---|---|---|---|
|P0|APIconversation8765 sansallowed_tools expose le catalogue complet, calcule une fenêtre supérieure au profilMac, puis503 ;avec[] et viaJL03,200|❌ Reproduit deux fois, E09/E12|Sélection conversationnelle bornée au point d'entrée commun ;respect du profil16384 ;nepas augmenter silencieusement lafenêtre |
|P1|DEFAULT_MODELS WebUI reste8B alors queJARVISconversation utilise27B|❌ Incohérence démontrée|DéfautWebUI27B ;conserver anciensprofils et conversations |
|P1|WebUI fait random.choice entreMac/Dell pourlesmodèles dupliqués|❌ Routage incompatible avecaffectation souhaitée|Filtre de catalogue parfournisseur :conversationMac, missions80BDell |
|P1|Sept réponsesask_user sont du texteJSON, sans véritableappel|❌ Affichagehistorique reproduit ;générationneuve fonctionne|Profil compatible/native, essai vrai formulaire ;pas d'exécution d'unJSON textuel arbitraire |
|P1|WebUI etQwen Code contournent l'admissionHybridRouter|🟡 Interconnexion manquante|Envisager même admission/receipts en amont ;Ollama sérialise déjà son instance, mais ne reprend pas lesprioritésJARVIS |
|P1|Pas d'Ollama/Tailscale surDell2, nœudIA désactivé|🟡 Infrastructure non installée, pas une panne d'inférence|Ne pas confondreSSH etIA ;choisir ensuite s'il faut unnœudIA selon lematériel réel |
|P1|P4nonreçue, processusconversation antérieur aux modificationssource surdisque|🟡 Provenance chargé/disque non reçue|Redémarrage maîtrisé après tests/rollback des changements autorisés ;pas de déclaration déploiement depuisseul fichier |
|P2|DeuxOllamaDell partagent lespoids mais ont desrésidences/ordonnanceurs distincts|✅🟡 Fonctionnel, compétitionpossible|Recenser consommateurslegacy11434 avantconsolidation ;aucun arrêt pendant l'audit |
|P2|Trois modèles existent surMac etDell ;32/70B historiques enplus|✅ Installationshistoriques, utilité àreconsidérer|Ne pasdéduire «inutile» duseul repos ;garder comparatif/fallback ou supprimer seulement après revueconsommateurs |
|P2|Qwen Code etmoteurmaison recouvrent lecture/édition/shell/tests|✅ Doublonfonctionnelpartiel|RéemployerCode commespécialiste borné ;ne pasreconstruireunframework deprogrammationgénéral |
|P2|HistoriqueWebUI etmémoireJARVIS distincts|✅🟡 Deuxhistoriques d'interface, pas deuxautoritésdésirées|Garder mémoiredurablecanonique ;raccordement explicite des références, pasfusion implicite desbases |
|P2|HealthOK maisAPIplainchat503|❌ Fauxsentiment desanté fonctionnelle|Ajouter une sonde sémantique bornée duchemin conversationnel, distincteduhealth infrastructure |
|P2|8766/8783 confondablesdanslesdiagnostics|❌ Cartographiecorrigée|JL03=8766 ;23D=8783 ;broker=socketUnix ;liensidentifiés parPID/titre/source |

Aucun nouveau modèle, arrêtservice, changementd'architecture oucorrectifapplicatif n'est appliqué dansl'instantané d'audit. La fixtureQwenCode est le seul codecréé/modifié pourl'essai autorisé. Les corrections ultérieures autorisées par lepropriétaire seront tracées séparément.

## Ce qui ne peut pas être déclaré inutile

Le broker porte la politique propriétaire, lesidentitésSSH etlesreçus ;il reste nécessaire. LeMissionEngine porte tâchesdurables, compteurs, plans, inconnus etescalades ;les sessionsQwenCode ne leremplacentpas. SQLite/FTS5 reste lamémoirecanonique. Le gardeQwen rétablit uncontrat decontexte que lemodeOpenAI d'Ollama ne permetpas directement ;il n'est pas simplementunproxy décoratif. JL03 garde consolemission, télémétrie etorbe qu'unWebUIstandardn'apportepasdanscetteinstallation.

Les fonctionnalités dechat, historique, importdeprofils etSTT/TTS deWebUI évitent de redévelopper unsecondchatcomplet pourl'usageoùellesconviennent. Les outilsdevstandard deQwenCode peuvent éviter de nouveauxadaptateursd'éditiongénériques. Ces réemplois requièrentlesinterfacesd'admission/provenance manquantes ;aucun remplacement global n'est reçu surune listedecapacités.
