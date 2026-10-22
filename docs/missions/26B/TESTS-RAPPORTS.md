# Tests des rapports26B — campagne en cours

Statut : 🟡 incomplet. Les 153 tests logiciels passent ; cela ne démontre pas à lui seul une correction autonome de la prose par JARVIS.

La réception attend trois rapports réels : réussite locale complète (A), échec du programme puis correction (B), résultat local vérifié avec dépendance externe impossible à observer (C). Aucun de ces trois rapports n’est encore reçu au déploiement21.

Les tentatives originales sont conservées dans narrative_review avec texte intégral, empreinte, preuves et verdicts par passage. Les FAIL et INSUFFICIENT historiques ne sont pas effacés. Les défauts de format du relecteur sont journalisés séparément ; ils ne prouvent pas que la prose du rédacteur était factuellement fausse.

Le test de B demande explicitement un premier brouillon au comptage faux « observations : 999 ». C’est une injection de test par Codex annoncée dans l’objectif, pas une erreur spontanée imputable au modèle. Il reste à constater son rejet et la rédaction corrigée dans l’exécution réelle. Le test complémentaire d’attribution, d’horodatage et de comptage a été exécuté comme composant pendant la campagne, sur des reçus réels de A. Les détails et limites figurent ci-dessous.

Une revue positive du modèle ne remplace pas les contrôles indépendants : exactitude des JSON, empreintes du manifeste, exécution effective du producteur, conservation du banc et absence du témoin externe. Une réception partielle de rapport ne clôture pas une opération techniquement incomplète.

## Test réel de composant v1 — réserve détectée

PROBE-RAPPORTS-v1.json conserve le premier essai réel : le brouillon initial est FAIL. Sa liste issues signale bien les fautes d’acteur, de date et de comptage, mais le relecteur classe contradictoirement les trois passages comme not_factual. Le booléen all_three_faults_detected est donc false. Le modèle rédacteur JARVIS a corrigé sa prose en deux tentatives jusqu’à une revue PASS, conservée dans JARVIS-RECTIFICATION-PROBE-v1.md ; cela ne démontre pas la détection correcte des trois affirmations par le contrôleur.

Codex a développé le harnais et injecté les trois fautes ; les revues et réécritures proviennent du modèle installé, avec les vrais reçus. Aucune réponse du modèle n’est simulée, aucun rapport opérationnel n’est remplacé et ce test n’est pas compté comme une quatrième mission autonome. Il a été avancé pendant la campagne, sans attendre la clôture de A, car ses reçus réels étaient déjà disponibles.

Cette défaillance a motivé le contrat26b.report.2 et un nouvel essai réel est en cours. Aucun résultat positif de ce second essai n’est encore annoncé ici. La conservation des retours de correction pendant la réduction du contexte est une correction d’infrastructure Codex distincte d’une réécriture de rapport effectuée par JARVIS.

## Rectification de notre lecture du premier essai

La première synthèse Codex disait à tort que seul le compteur avait été détecté : les issues originales mentionnaient aussi l’acteur et l’horodatage. Le booléen all_three_faults_detected=false mesurait les verdicts de passages incohérents, pas une absence totale de signalement. Les originaux restent inchangés et cette rectification est publiée explicitement.

## Second essai et vérification indépendante

PROBE-RAPPORTS-v2.json : les trois passages fautifs sont insuffisamment étayés, puis le modèle rédacteur corrige sa prose en une tentative jusqu’à une revue PASS. La lecture indépendante du texte complet trouve cependant une confusion de type d’événement et un regroupement inexact de causes historiques ; PROBE-v2-VERIFICATION-INDEPENDANTE.json conserve donc PARTIAL. Un PASS du modèle n’est pas promu automatiquement en réception indépendante.

Le contrôle par événement du contrat26b.report.3 a ensuite détecté des défauts historiques et obtenu une nouvelle rédaction acceptée par le modèle, mais celle-ci déclarait encore à tort un vrai identifiant de mission et deux vrais reçus inconnus ou inventés. Le contrat26b.report.4 borne donc le contexte et donne un index complet des références connues. Ce retest reste à recevoir ; les versions erronées ne sont pas remplacées silencieusement.

## Premières étapes opérationnelles

A/T1 et B/T01 sont reçues par le moteur. La lecture indépendante du rapport B/T01 confirme le code, les données et les causes des deux refus cités11167/11197. Le programme B a réellement été lancé sans correction du délimiteur : la commande ajoute `|| true`, donc le shell annonce0 tandis que le programme émet un traceback. Le contrôle indépendant le classe comme échec applicatif masqué, sans compter une réussite du producteur. La correction fonctionnelle et les trois missions complètes restent à recevoir.
