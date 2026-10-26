# Blocages et interventions

- Bootstrap Codex : première sonde Python exécutée mais échouée, NameError dû aux guillemets de la commande. Corrigée par shlex.quote ; sondes suivantes réussies sur les deux Dell. Ce n’est pas un test P2 échoué ni une action JARVIS.
- Première proposition de plan JARVIS : cinq phases internes, chacune recevant mécaniquement un contrat de réception P2 complet. Codex précise la granularité des lots ; le modèle conserve la décision du plan et de sa révision. Aucune tâche d’analyse n’est artificiellement marquée corrigée/testée.
- Capacités manquantes futures : dossier requis avec preuve, compteur et demande précise. Aucune intervention corrective P2 de Codex non justifiée n’est encore publiée.

## Escalade réelle — reçu tronqué

Trois lectures complètes du code sont réellement exécutées, mais le broker tronque le JSON de réponse à16000octets. Le modèle reçoit une erreur de décodage ; le garde arrête la mission et consigne trois incidents de délégation, zéro échec de correction. Codex répond à cette escalade d’outillage par un reçu complet persistant, une petite réponse et un transfert SHA. Deux sondes réelles40001caractères sur les deux Dell prouvent la récupération intégrale, sans changement des sources.

Le compteur historique3 reste conservé. Un pointeur de résolution Codex couvre ces trois incidents après correction technique ; il ne réinitialise pas le compteur applicatif et ne peut être produit par le modèle. La nouvelle stratégie reste bornée. Le fichier de transport est mis à jour sur les deux copies de travail avec sa provenance Codex, avant reprise JARVIS. Cela n’est pas l’implémentation de la machine à états P2, ni le budget de contexte P3.

## Supervision — Dell2 sans travail soutenu

Après les dix tests historiques réussis (événement41172), Qwen a utilisé Dell2 pour une lecture (41584), puis a repris des lectures déjà connues sur Dell1 (41634,41674,41690). Il ne s’agissait pas d’un défaut de télémétrie. La préparation de contexte41700 exposait82838caractères pour un budget annoncé62887. Cela ne démontre pas une saturation du modèle, mais prouve que la borne annoncée n’était pas respectée.

Intervention Codex41722 : sortie de cette répétition, conservation de l’historique et passage par un contexte court lié à la même mission. Travail confié à Qwen : préparer sur Dell2 un test unittest des lacunes P2 contre le vrai code, sans répéter la référence déjà reçue ni déployer. Les résultats restent à constater. Aucun résultat P3 ni parallélisme n’est revendiqué.

Le relais court a ensuite été réellement refusé avec `Requested context exceeds measured node profile: Dell1` après quatre lectures (41732/41735/41740/41745) ; aucun nouveau test n’a été produit lors de ce relais. Le texte refusé est conservé événement41746. Codex réduit le paquet à un extrait ciblé de la fonction réelle et demande un test importé, sans fourniture de sa logique d’implémentation. Ceci constitue une assistance sur blocage, pas une réception de P3.

Le paquet réduit a permis à Qwen d’écrire réellement sur Dell2 `engine/tests/test_budget_enforcement.py`, puis de tenter son exécution (41779, reçu11aba261b5164c0d8502dcd236471168). Le chargement a échoué : import d’un sous-module `jarvis.distributed_authority.budget` inexistant, alors que budget est une fonction du module. L’appel suivant41783 a été refusé pour paramètre action absent ; aucun test fonctionnel démarré. Codex a transmis la correction syntaxique d’import, les paramètres exacts et la réserve sur les assertions (vérifier les seuls compteurs historiques ne réceptionne pas les états P2). Retour au parent natif running, deux workers actifs ; réception P2 toujours NON VALIDÉ.

## Nouvel arrêt — collision d’identifiant

La mission a été interrompue à42376 après trois refus comparables `operation_id reused for different arguments` (escalade42375). Les workers actifs ne prouvaient donc pas une progression. Le test42365 échouait sur `.runtime/missions.sqlite`, chemin incorrect ; le constructeur installé crée déjà `runtime/missions.sqlite`. Aucune correction moteur ne peut être déduite de cette erreur de banc.

Codex enrichit l’erreur de collision avec arguments enregistrés/demandés, résultat connu ou inconnu et remède, sans exécuter de commande ni affaiblir le verrou ;16tests du garde réussis. Retour arrière disponible dans le répertoire privé avant installation. Aucun compteur effacé. Un premier relais a seulement lu six zones sur Dell1 et n’a produit aucun changement : cet échec de progression est conservé. Ses événements auxiliaires portaient à tort node=Dell2 hérité du script ; les reçus broker démontrent host=dell-observe. L’étiquetage du relais suivant utilise désormais l’hôte réellement demandé. Le paquet suivant fournit l’extrait pertinent du constructeur/journal et borne l’unité à un incrément d’états persistants et ses tests. P2 reste NON VALIDÉ.

## État constaté après les reprises bornées

**BLOQUÉ, sans clôture de mission.** Les deux artefacts Qwen suivants ont défini une classe en mémoire sans écrire la correction ni le fichier de test demandé ; les commandes de test ont échoué au chargement de modules absents (42465 et42472). Ce ne sont pas des tests fonctionnels P2 ayant échoué : les cibles n’ont pas été exécutées. Aucun mécanisme P2 nouveau reçu. La mission reste interrupted ; les services de workers sont conservés mais ne prouvent pas une activité. Les stratégies épuisées ne sont pas relancées automatiquement. [Dossier succinct](ESCALADE-INACTIVITE.json). L’escalade est désormais explicitement consignée par Codex ; aucune reprise autonome ou supervision Codex hors tour n’est annoncée. P3/P4 non transmises.
