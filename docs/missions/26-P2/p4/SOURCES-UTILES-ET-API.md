# Reprise P4 : sélection des preuves et API utilisable

P4 reste **NON VALIDÉE**. Les corrections ci-dessous sont développées et
installées par Codex ; leur utilisation applicative par JARVIS reste à vérifier.
Même mission `d8fe752876db480cbe5f22cd5525e2dd`, même plan JARVIS version 3,
mêmes compteurs persistants. Aucun rejeu de la réception P2/P3.

## Défaut constaté

Après les corrections d’identifiants, d’édition et de références, JARVIS
continuait à inspecter les sources sans modifier le candidat. L’audit du contexte
a montré une erreur concrète : un appel `authority_read_execution` réussi au
niveau outil pouvait contenir la sortie stderr d’un processus rc1. Cette page
était alors choisie comme `latest_successful_read`, évinçant le code déjà observé.
Exemple : `cat: run/main/worker.py: No such file or directory`, issu d’une mauvaise
interprétation du nom des fonctions. Ce chemin n’est pas celui de worker.py.

La conservation d’une seule page favorisait également les retours alternés entre
deux fichiers et les sorties ne contenant qu’un chemin. Les métadonnées historiques
ne doivent pas remplacer les observations utiles à la correction actuelle.

## Correction du contexte — f90790e

- La sélection exige une observation de processus rc0 et un flux stdout.
  L’erreur reste dans les observations et archives ; elle n’est pas requalifiée.
- Les pages sont limitées au manifeste actuellement observé et à la tâche selon
  ses règles de portée. Une ancienne version n’est pas réintroduite comme courante.
- Deux pages distinctes sont conservées, avec priorité aux fenêtres substantielles
  complètes. Les doublons inclus dans une autre page ne chassent pas l’autre source.
- Un stdout abrégé est récupéré depuis son reçu local immuable, après confinement
  du chemin et contrôle SHA-256. Aucune commande distante n’est rejouée.
- La seconde fenêtre active est bornée à 1 000 caractères avec indication explicite
  de la coupure et de sa référence complète. La première peut être réduite à
  2 400 caractères sous pression ; le checkpoint et le reçu gardent l’original.
- Les faits d’API restent visibles. Les contraintes, objectifs, critères et compteurs
  ne sont pas tronqués. La limite finale reste bloquante si le paquet ne tient pas.

Les tests ajoutés contrôlent l’erreur rc1 sous enveloppe outil réussie, deux pages
distinctes malgré les relectures, la récupération d’un reçu complet et le refus
d’un reçu altéré. Les fixtures antérieures ont été renseignées avec les véritables
champs de résultat du lecteur, notamment le code retour observé et les lignes.

## Correction de l’API d’attestation

`AttestRuntime.measure_module` permettait déjà de choisir des symboles, mais
`attestation_report` ne transmettait pas cette sélection. Le worker comporte un
décorateur qui rend une comparaison globale insuffisante. La fonction pratique
accepte maintenant `symbols=None`, dictionnaire module → liste de symboles.
Omettre cet argument conserve le comportement antérieur. Chaque résultat conserve
la sélection explicite : il ne certifie pas les fonctions non sélectionnées.

Les nouveaux tests exécutent le helper sur les vraies fonctions importées du
worker, puis contrôlent divergence et symbole absent. Une observation dans le
processus de test ne constitue toujours pas une attestation du service actif.
Le helper est installé seulement dans les candidats Dell ; aucun nouveau module
d’attestation n’est installé dans les services actifs du Mac pendant ce paquet.

## Installation et résultats

145 tests logiciels ciblés réussis localement ; 17 tests d’attestation et
33 de contexte réussis sur **chaque** Dell. Ces contrôles sont exécutés par Codex.
Installation 64398, sauvegardes des anciens fichiers et reçus dans
`SOURCES-API-DEPLOIEMENT.json`. API observée réellement sur Dell1 à 64399.

Préflight 64402 sans inférence : **27 016 octets** pour un budget conservateur de
27 648, worker complet conservé, seconde page et faits d’API présents, compteurs
inchangés. Les octets sont une estimation conservatrice distincte des tokens
effectivement mesurés par le backend ; la fenêtre reste 32 768 tokens.

Deux erreurs de sauvegarde rencontrées par Codex avant toute mutation distante
sont conservées à 64401 : suffixe local incompatible puis répertoire de staging
non accessible au compte technique. Corrections : extension `.py` conservée et
propriété du répertoire ajustée. Ce ne sont pas des tests échoués de JARVIS.

Workers rechargés, instruction courte et reprise sur le plan existant. Le prompt
du superviseur a été réduit à un paquet courant, son ancien texte archivé ;
ni script ni compteurs de supervision ne sont réinitialisés.

## Suite et retour arrière

JARVIS doit encore écrire l’instrumentation du worker candidat, tester une
divergence réelle, faire vérifier la même version sur l’autre Dell et rendre
un rapport fidèle. Aucun succès applicatif n’est déduit des 145 tests.

Pour retour arrière : interrompre la mission et vérifier l’absence d’appel
démarré, restaurer `mission_context_budget.py` Mac et les deux fichiers candidats
depuis les sauvegardes privées du reçu64398, puis recharger les workers. Garder
événements, reçus, compteurs et candidats originaux. Aucun déploiement de worker
applicatif actif n’a été réalisé pendant cette intervention.
