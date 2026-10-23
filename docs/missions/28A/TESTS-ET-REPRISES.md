# Tests28A — état intermédiaire

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
