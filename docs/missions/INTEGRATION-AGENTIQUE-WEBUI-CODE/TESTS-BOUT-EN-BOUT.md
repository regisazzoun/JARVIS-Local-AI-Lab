# Réception ciblée — 30 octobre 2026

Code livré : `40196e9`, sélection des profils `c9843d2`, correction du workflow de rapport `0ad2e8c`. Les preuves structurées sont dans [PREUVES-JARVIS.json](PREUVES-JARVIS.json) ; les sorties originales et secrets restent dans le stockage privé de mission. Les tests logiciels ne constituent pas une preuve d’autonomie.

| Parcours | Résultat observé | Réception et limites |
|---|---|---|
| A Conversation | Vrai navigateur Chromium, profil conversation Qwen27B Mac, réponse et outils affichés ; historique relu par API WebUI | ✅ Reçu pour ces échanges ; aucun essai physique Safari/iPhone ou microphone ajouté |
| B Recherche | Appel réel `web_search`, résultat retourné au modèle dans WebUI, reçu38 | ✅ Appel et restitution reçus ; ne prouve pas l’exhaustivité du Web |
| C GitHub | Lecture116, recherche42, publication via Skill48 ; contrôle indépendant du contenu et de l’arbre99 | ✅🟡 Lecture/écriture reçues ; recherche exécutée mais zéro résultat et `incomplete_results=true` |
| D Google Drive | JARVIS appelle le connecteur, reçu70 : `AUTH_REQUIRED` | 🟡 Authentification locale absente ; aucune lecture/écriture Google distante reçue |
| E Qwen Code | WebUI/JARVIS appelle le spécialiste ; source `price.py` corrigée, test inchangé, unittest réussi ; contrôle Codex indépendant | ✅ Correction source et test reçus ; pas de déploiement d’application déduit |
| F Deux Dell | Qwen Code/MCP exécute réellement unittest sur Dell1 et Dell2, reçus65/67 ; après défaut de bilan, JARVIS80B utilise l’outil distant direct pour écrire/lire le manifeste Dell2, contrôlé indépendamment118 | ✅🟡 Commandes et fichiers reçus ; finalisation autonome Code distribuée réservée |
| G Plus de12tours | D :18tours et14avances réelles ; E :29tours,14avances,697303ms, chaîne de nonces vérifiée et source inchangée | ✅ Deux sessions indépendantes ; les erreurs A/B/C restent archivées |
| H Objectifs natifs | Premier Goal clôturé puis relu ; nouveau smoke Goal avec fichier JSON42,4tours,54,433s, complet et relu après réouverture | ✅🟡 Permissions et persistance reçues ; cas à historique complexe encore en pause/non reçu |
| I Skill existant | Découverte puis exécution réelle de `github-publish`v1 par JARVIS, run13a842ffa056491aac2356dd133965c8 | ✅ Reçu sur branche d’essai sans fusion |
| Mission canonique | Création WebUI de864da7c457ef4d82b0b284d9ceb30eeb ; worker80B démarre ; plan plat accepté après correction d’interface ; fichier unité lu et brouillon écrit | ✅🟡 Clôture native94109 après correctif structurel, PASS94064/94067 et validation T194089 ; réception assistée, pas autonomie initiale du plan |

## Échecs conservés et rectifications

Le premier plan bulk a été refusé neuf fois sur la sonde. Le profil de création des nouveaux clients sélectionne désormais les interfaces plates et les gardes existantes. Le modèle a alors produit un plan accepté : ce résultat n’est pas une clôture de mission.

La sonde a écrit un nouveau brouillon dans `/var/lib/jarvis/projects/mission26-phase2/reports/jarvis-conversation-status.md`, au lieu d’un espace propre à IntegratedClients. La lecture antérieure constatait ce fichier absent ; il n’est pas déclaré rapport historique remplacé. Le brouillon original est conservé. La mission P4 historique n’a pas été reprise.

La vérification de ce brouillon a échoué. Le moteur a borné les refus de `mission_block` faute d’observation réellement associée à la tâche. Après sélection explicite par Codex du profil d’observation de service, la reprise est restée sur la vérification pendante ; une nouvelle instruction ne remplace pas cette étape durable. Événement93896 : escalade, compteur4 incluant les trois refus antérieurs, sans remise à zéro. Cette reprise assistée n’est pas présentée comme respect autonome de trois cycles nouveaux. Aucun essai supplémentaire identique n’est lancé et aucune fausse clôture n’est enregistrée.

La correction structurelle0ad2e8c a ensuite rouvert les outils de lecture manquants pendant la phase verify : événement93898, reprise du même historique. Qwen a exécuté trois lectures systemd93926/93950/93974, fait vérifier et rejeter l’ancien brouillon94001, composé et écrit le relevé corrigé94024–94041, puis vérifié le fichier94064/94067 PASS. T1 validée94089 ; clôture native94109. Tous les anciens INSUFFICIENT, FAIL et refus sont conservés. Le [contrôle indépendant](CONTROLE-INDEPENDANT-SONDE.json) compare le fichier direct aux trois reçus et vérifie à nouveau le service actif. La génération factuelle est attribuée au moteur, pas à une prose libre du modèle.

Deux appels spécialiste illustrent les limites du rapport libre : le job20261030T163014.659151 s’est arrêté avec erreur après de vraies commandes sur les Dell ; le job20261030T165316.139746 a retourné0 malgré des paramètres distants refusés puis un repli local. Le contrôle indépendant a rejeté ce prétendu succès. L’outil direct a ensuite permis à JARVIS de produire un vrai manifeste Dell2. Le dernier manifeste n’est pas attribué à Qwen Code.

Le premier essai de14avances a affirmé terminer alors que13seulement étaient présentes. Ce bilan est conservé avec son rappel correctif. Les sessions D/E reçues sont distinctes et vérifiées sur leur journal réel.

## Contrôles logiciels et déploiement

- **93 tests ciblés PASS** :32nouveaux tests de façade/idempotence, contrats Ollama, connecteur Google, GitHub, asynchronisme et spécialiste ;61contrôles ciblés MCP/Skills/compteurs et workflow de rapport historiques.
- **5 contrôles vivants PASS** : proxy Apache, authentification de l’adaptateur, taille des missions retournées, refus de contexte trop gros avant inférence et refus d’un chemin de projet invalide.
- Identité de **8 fichiers déployés** vérifiée ; sept services centraux contrôlés actifs et HTTPS200. Détails dans [DEPLOIEMENT.json](DEPLOIEMENT.json).
- Cinq relevés réels de disponibilité WebUI pendant un appel Code : environ10–33ms. Ce sont des requêtes de santé/HTTP, pas les percentiles de conversation.
- Aucun reboot complet ni arrêt arbitraire des sessions interactives utilisateur ; les services modifiés ont été rechargés après contrôle de leur activité.

## Restitution finale WebUI

Après clôture, un nouveau parcours Chromium authentifié sur le profil27B a fait appeler réellement `jarvis_missions read`. Le fil affiche `completed`, `T1 validated` et le SHA256 exact du rapport. Les quatre contrôles de contenu sont vrais ; [preuve de restitution](WEBUI-RESTITUTION-SONDE.json), sorties et capture originales privées. Aucune nouvelle mission créée par cette lecture.

## Isolation des profils et disponibilité après recharge

Le profil standard conserve les contrats plats, les contrôles de revue et la finalisation factuelle générale, sans imposer le compositeur limité aux reçus systemd. Les options de composition de service et FACTS_ONLY sont appliquées seulement au profil explicite `service_observation` (`f66b0c8`). Les tests refusent la contamination du profil standard ; la configuration du profil service actuel correspond à celle de la sonde reçue. Aucune mission historique n’est réécrite.

Un lancement de la suite vivante immédiatement après le dernier redémarrage de l’adaptateur a rencontré trois refus de connexion pendant son initialisation ; l’original `live-tests-immediate-restart.log` reste conservé. Après disponibilité réelle, les cinq contrôles repassent PASS. Cet incident de démarrage n’est ni un test fonctionnel exécuté puis échoué ni un résultat masqué.
