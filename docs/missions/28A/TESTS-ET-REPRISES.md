# Tests28A — historique et réception ciblée

> Décision propriétaire du24 octobre2026 : mission clôturée incomplète,80B conservé pour les missions Dell,27B conversationnel sur Mac. Les états «en cours» ci-dessous documentent les essais antérieurs ; leurs critères non reçus sont différés, sans relance automatique. Le RAPPORT-FINAL.md de clôture prévaut.

🟡 En cours au23 octobre2026. Les résultats ci-dessous ne valent pas réception globale.

| Contrôle | Observation | Portée |
|---|---|---|
| Suite logicielle dans le venv actif |217 tests réussis |210 acquis/routeur et7 tests du contrat de téléchargement ; fixtures distinctes des essais JARVIS |
| Conversation locale pendant worker Dell |6 réponses simples, environ1,074 à1,864s |Requêtes «OK» sans outils ; pas une mesure de dialogue complexe |
| Conversation locale avec charge CPU de fond et Dell |6 réponses simples, environ1,070 à1,183s |Même limite de portée ; échantillon court |
| Quota CPU de fond au repos interactif |cpu.max900000/100000 ; ~75,3% agrégés sur8s |L’écart d’échantillonnage ne modifie pas le plafond du noyau |
| Adaptation pendant interaction |Quotas300% et900% observés |Réduction/restauration réelle, pas simple configuration |
| Pointe GPU par JARVIS |699,37W cumulés ; maximum66°C |Fenêtre de profil~10,17s, pas charge prolongée |
| Retour profil normal |250W/carte, relecture indépendante |Pas d’erreur détectée dans la fenêtre mesurée |
| Installation32B |Tag exact installé, lecture indépendante et reprise JARVIS après attente |Inférence et comparatif encore à recevoir |

Le benchmark froid initial local mesure directement Ollama et n’est pas un équivalent du benchmark API chaud après routage. Aucun gain avant/après comparable ne doit en être déduit.

L’incident32B et l’erreur de révision de plan Codex sont documentés dans [INCIDENT-INSTALLATION-32B.md](INCIDENT-INSTALLATION-32B.md). Les contextes sont archivés avant reprise ; les plans1–3, appels invalides, faux identifiants de preuve et erreurs de premier rapport restent conservés. Un premier lancement logiciel avec le Python système a échoué faute de jsonschema ; la suite dans le venv installé passe217tests.

Restent notamment le comparatif qualitatif des modèles, le choix du moteur Dell, la vérification opérationnelle du repli et une mission JARVIS complète avec preuves/résultat/rapport. Aucune réserve26/26B ni14A n’est levée par ces tests seuls.

## Complément — reprise du test après la boucle

221tests logiciels passent après corrections du contexte et du vérificateur. JARVIS a réellement lancé les six inférences32B :3/6après correction d’un faux FAIL dû au vérificateur Codex, verdict2/6initial conservé. Les résultats ne valent pas gain qualitatif. Le transfert a rencontré un dossier créé root par Codex ; ce seul propriétaire a été corrigé, la réutilisation par JARVIS est suivie dans la mission. Le70B a été remplacé provisoirement par le pilote27B connu après des erreurs d’appel répétées ; ce repli n’est pas le choix final du modèle Dell. Voir INCIDENT-REPRISE-TESTS.md.

## Suite actuelle et résultats acquis

238tests logiciels passent dans le venv installé après correction des références parent de vérification, garde de clôture sémantique des missions dirigées, contextes stables, découverte d’outils, verrouillage multi-slots et vue bornée compute_status. Les jeux logiciels sont des fixtures ; ils ne prouvent pas l’autonomie de JARVIS.

Le comparatif effectif est terminé :18réponses27/70/80B, scores4/6,2/6,5/6 ;32B3/6sur ses six réponses précédentes. Le cas coverage est ambigu et la revue indépendante n’en déduit pas une incapacité générale. Le80B est installé comme pilote Dell, le27B reste conversationnel sur Mac.

C et D sont reçus indépendamment sur leurs preuves : priorité critique entre inférences, repli après erreur TCP réelle sur copie de configuration, conversations locales pendant charge, quotas et retour GPU250W/carte après la campagne JARVIS699,37W. Aucun essai matériel déjà reçu n’est répété.

Deux missions canoniques sont observées running en parallèle ; leurs opérations sont distinctes et leur file GPU commune. La première observation sans chevauchement (mission secondaire draft) est conservée ; Codex a corrigé son dispatch. Six réponses API locales pendant chevauchement prennent0,828–0,961s.

## Programme de consolidation : fausse réussite détectée

Une première sortie JSON écrite directement avec les valeurs attendues ne prouve pas le programme demandé : elle a été rejetée par Codex. JARVIS a ensuite écrit consolider.py ; sa première version additionne11succès sur18cas pour chacun des trois modèles. Le vérificateur protégé observe FAIL sur quatre variantes malgré les codes retour0 et les manifestes valides. Les entrées changent des évaluations, retirent et ajoutent un cas, sans mettre à jour summary : le programme doit réellement lire les cas par modèle. Les originaux restent inchangés. La correction et sa réception sont encore suivies ; aucun PASS fictif attribué.

## Incident de contexte pendant la réception

Les métriques sérialisées de tous les jobs compute_status gonflaient le contexte et provoquaient des réponses répétitives sur des états anciens. Codex a borné la vue aux huit jobs récents et à leurs métriques utiles, en conservant tous les reçus SQLite. Une interruption technique bornée des workers permet le déploiement au checkpoint et la reconstruction du contexte ; elle n’est pas un abandon ni une nouvelle demande d’autorisation. Le modèle doit ensuite réutiliser réellement la fonction corrigée.

Le dernier correctif isole les observations, notes et signatures de progression à la tâche active. Les tâches déjà reçues gardent leurs résumés et toute preuve peut être relue explicitement. Les238tests incluent la conservation en base et l’absence de contamination par une conclusion de tâche précédente. Voir INCIDENT-RECEPTION-80B.md pour la coordination et les limites agentiques.
