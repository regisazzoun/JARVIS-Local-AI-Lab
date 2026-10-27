# Déblocage P3 — escalade54073, 27 octobre2026

P3 reste **NON VALIDÉ**. P3-01 est reçue avec réserves comme observation des données de capacité ; P3-02-run est exécutée par JARVIS sur les deux Dell. P4 n'est pas transmise.

## Diagnostic et corrections Codex

Les refus répétés du lecteur remplaçaient les sorties utiles du contexte actif. Les derniers résultats substantiels restent désormais visibles même après trois refus. Les notes et décisions anciennes étaient aussi réinjectées après changement de tâche/version : une isolation optionnelle par identité réelle de tâche et frontière de déploiement borne les preuves actives. Les compteurs restent communs, les journaux et plans antérieurs sont conservés. Le garde d'acceptation refuse les preuves d'une autre tâche ; accept n'est pas proposé tant que la tâche courante n'a pas deux tests réellement exécutés sur deux hôtes.

Le profil tests seuls autorise maintenant l'inspection diagnostique. Son erreur de provenance exige un TEST indépendant, et non une CORRECTION inexistante. Le message de répétition ne conseille plus mission_evidence, absent du profil. Les références de deux tests effectués sur le même Dell ne constituent pas une validation indépendante.

JARVIS a essayé `./Core.ollama`, qui n'existe pas : Core.ollama est une méthode du service central. Un tube vers head masquait l'échec du premier programme. Le lanceur utilise désormais bash pipefail. Deux tests avec de vrais sous-processus contrôlent respectivement le retour127 du programme inexistant et le succès d'un tube valide. Les anciens codes0 et messages «No such file» restent dans les reçus ; ils ne qualifient pas un test applicatif.

Sources : commit `105c4ff`, 67tests logiciels ciblés PASS, dont18pour le contexte. Ces tests ne constituent pas une preuve d'autonomie. Modifications sur les seuls composants du moteur existant, sauvegardes privées et rechargement des workers ; aucun remplacement de modèle, routage, base ou service conversationnel.

## Exécutions réellement reprises

JARVIS/Qwen80B a écrit ses programmes Python et exécuté ses générations surDell2 (54802) etDell1 (54841 puis54895). Le fichierDell2 contient859999octets ; contrôle indépendantCodex54862 : SHA-256 `f49035ce4a4e736b4b88609b03dbb37d481c4c653a78a3b5b6347915a848a8a8`, un fichier du préfixe à cet instant. Les écritures et les contrôles de longueur du programme appartiennent à JARVIS ; le contrôle indépendant et les adaptations du moteur àCodex.

JARVIS a demandé le checkpoint54911 et la pause54912. Le superviseur existant a réellement redémarré les deux workers54915 : PID70821/70819 →71258/71255. JARVIS a appelé context_resume54930 dans le nouveau PID71255 ; compteurs du ledger, compteurs Authority et compteurs d'interface conservés. L'ancien compteur3 n'a pas été remis à zéro. L'inférence Ollama n'a pas été redémarrée.

Réserve précise : les générations écrivaient de grands fichiers et n'émettaient qu'environ143octets stdout. La note JARVIS54963 confondait fichier/stdout et interprétait mal219000>100000. ErratumCodex55023 enregistré, originaux conservés. Le paquet suivant demande une lecture du contenu existant, sans régénération, et un contrôle de non-duplication du fichierDell2. Aucune idempotence générale n'est encore reçue.

## Supervision après le tour interactif

Le timer déjà installé `jarvis-m26-p2-supervision.timer` est reconfiguré pour P3 seule et son registre canonique. Il contrôle toutes les120secondes et déclenche, en cas d'arrêt ou de stagnation, un passageCodex limité à420secondes, maximum trois passages par cause stable. Le CLI a réellement retourné `M26_P3_SUPERVISION_READY`. Les anciens cas P2 restent dans received_tasks, sans relance. P4 n'est pas auto-lancée par ce superviseur.

Le superviseur de checkpoint est un one-shot : il a terminé avec succès après54915 ; il ne faut pas le décrire comme une surveillance générale toujours active. La surveillance des escalades est assurée par le timer réutilisé. Le marqueur MANUAL-HOLD est conservé pendant l'intervention et retiré au retour au moteur. Configuration exemple et source du one-shot sont publiées sous tools/mission26_phase2 ; journaux privés et secrets ne le sont pas.

[Preuves structurées](DEBLOCAGE-54073.json) · [État P3](../M26_P2_P3_CONTEXTE.md) · [PR29](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/29).

## Réception opérationnelle actualisée

**VALIDÉ AVEC RÉSERVES**, réceptionCodex55310. Les réserves en tête de cet instantané ont progressé : grandstdout55057 réellement219000octets dans un reçu completSHAcontrôlé ; contrôle indépendant55251 après reprise confirme le fichierDell2 inchangé et un seul artefact. Deux tâches natives validated et missionP3 completed. Rapport modèle original conservé, version corrigée conservée avec [errata faisant autorité](ERRATA-RAPPORTS.md). [Réception structurée](RECEPTION-P3.json). Les limites d'autonomie non guidée, de tokenizer et de revue structurée restent explicites. P4 démarre par un audit distinct sur le même moteur, sans rejeu des opérations reçues.
