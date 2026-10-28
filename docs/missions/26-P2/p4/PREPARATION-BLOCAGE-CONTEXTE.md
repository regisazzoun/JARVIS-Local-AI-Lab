# P4-ACTIVE-PREP — diagnostic périodique du 28 octobre 2026

🟡 Préparation interrompue, non reçue. Unité inchangée
`e98fd4bbe37c492b922db9b5a1d782aa`, plan version 0.
Passage périodique 1/3, commencé65571, diagnostic Codex65572.

Les derniers outils natifs prouvent la lecture du paquet : reçus65528/65537,
processus rc0 ; la répétition suivante est refusée. Aucune observation des
services canoniques ni plan canari/rollback reçu à ce stade. Zéro outil started
au contrôle. Les trois incidents de capacité sont conservés65567/65568,
zéro échec fonctionnel et aucun effet inconnu déclaré. Aucun quatrième essai.

Le rejeu local sans inférence de l'archive65564/checkpoint65565 reproduit
l'erreur65566 : minimum compacté27855octets, plafond27648, dépassement207.
Le champ objective et owner_goal répètent exactement le même objectif1987octets.
Ce n'est pas un nombre de tokens mesuré ; fenêtre32768, réserves4096+1024.

Correctif **Codex dans la branche seulement** : lorsque les deux textes sont
strictement identiques, conserver objective intégral et remplacer owner_goal
par une référence explicite à objective et à la mission canonique. Les objectifs
distincts restent entiers ; checkpoint/archive/contraintes/compteurs inchangés.
38 tests locaux du budget passent, dont deux régressions dédiées. Le rejeu du
véritable reçu avec ce source passe à27515octets, marge133octets : admission
ponctuelle seulement, aucune garantie sur les prochains tours.

Runtime non installé, services inchangés, mission non remise en file, aucun
déploiement actif dans ce paquet de préparation. La correction est prête pour
traitement technique de l'escalade ; toute reprise doit vérifier le code utilisé
et un préflight courant avant envoi, sans remise à zéro ni tentative identique.
Qwen conserve son choix de plan et d'observations. Aucune nouvelle unité pour
contourner ce blocage. L'intégration applicative attend la réception technique
réelle de cette préparation ; aucune nouvelle validation humaine à ajouter.

Documents relus : AGENTS, charte, état ciblé SUIVI/ROADMAP, supervision,
LANCEMENT-ACTIF-PREPARATION.json, PAQUET-SUIVANT-ACTIF.md et dernier état de
RECEPTION-CANDIDAT-WORKER.md. Autorisations autonomes conservées ; pas de
contradiction ajoutée. Aucun MANUAL-HOLD. Registre reçu inchangé ; P4 et phase2
restent non validées. Candidat65474/P2/P3 non rejoués, aucune autre mission.

## Reprise interactive autorisée du28octobre2026

Le propriétaire demande « reprend ». Codex installe le correctif7470d62 dans
le SDK d’orchestration canonique (65588), après38tests PASS avec le venv réel.
Un premier lancement avec le Python système manquait jsonschema : erreur de
l’environnement de test, corrigée en réutilisant le venv, sans installation.
Préflight courant65587 :27371octets/27648, objectif complet conservé,
aucune inférence ni outil exécuté pendant ce préflight. La marge277octets reste
faible et ne prouve pas l’admission des tours suivants.

Même mission remise en file après changement réel du code, et seulement après
vérification de l’absence d’appel started dans cette mission. Les trois
incidents d’infrastructure et zéro échec fonctionnel restent conservés ; le
problème est marqué RESOLVED, sans effacer l’escalade ni les compteurs.
Sauvegarde privée du module avant installation ; retour arrière par restauration
du module et redémarrage des deux workers. Aucune autre mission relancée,
aucun déploiement de l’attestation applicative candidate dans cette correction.
Instruction65583 : le paquet a déjà été lu, enregistrer le plan choisi parQwen
puis observer les services, sans refaire la lecture.

### Boucle de relecture repérée pendant la reprise

Le budget corrigé a laissé passer plusieurs inférences réelles (premier paquet
26192octets,65595), mais Qwen a essayé de nouveaux chemins vers le même paquet.
Codex a interrompu cette stratégie avant toute opération applicative et ajouté
une portée optionnelle `planning_tools` au filtre de planification existant.
La mission courante expose seulement mission_plan/mission_note/mission_progress
pendant le plan ; après acceptation de la couverture, les outils des tâches
choisis parQwen restent disponibles. Aucun plan ni commande technique écrit par
Codex. Les missions sans option gardent les sept outils historiques du plan.
L’option ne peut pas ouvrir host_exec avant le plan même si son nom est fourni.
Cinq tests de portée PASS ; source3c1065d installé dans les workers,65658.
Même mission, compteur d’incidents3 conservé, aucune réinitialisation des erreurs.
