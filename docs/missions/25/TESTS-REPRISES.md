# Essais, reprises et réception indépendante

Les [reçus de mission](PREUVES-JARVIS.json), [runs de skills](REGISTRE-SKILLS.json), [vérifications indépendantes](VERIFICATION-INDEPENDANTE.json) et [relectures GitHub](VERIFICATION-GITHUB.json) sont les références factuelles. Les sorties textuelles du modèle sont conservées séparément.

## Essais logiciels Codex

89 tests réussis :80 régressions existantes et9 contrôles nouveaux sur stdin hérité non bloquant, échappement des arguments littéraux, refus d'activation après échec, séparation des versions/test, désactivation persistante, validation avant effet, reprise/checks rejoués, idempotence des définitions, protocole MCP réel et promotion durable des mutations. Certains contrôles sont regroupés dans une méthode ; ce nombre est celui du runner, pas un nombre d'essais opérationnels JARVIS. [Journal](TESTS-LOGICIELS.txt).

```bash
PYTHONPATH=agentic/engine_v2 /opt/jarvis/conversation/.venv/bin/python -m unittest discover -s agentic/engine_v2/tests
```

Le test MCP utilise réellement le SDK et un sous-processus stdio installé. Les assertions des autres tests restent des tests logiciels, distincts des appels réels du modèle.

## Scénarios JARVIS

- **Inventaire :** outils/schémas, fichiers et GitHub ; échecs réels, correction de sélecteurs après consultation de politique, stdin Ansible retesté après correctif Codex.
- **Debian/Dell/MCP :** processus/journaux/service, test et utilisation des skills ; refus Unix d'un chemin distant puis correction par JARVIS vers `/opt/jarvis/compute`, dépôt Ansible relu en SSH ; découverte MCP puis appel `host_service is-active` dans une session stdio réelle. Le moteur refuse une première clôture sans cet appel, puis reçoit la tâche après son exécution.
- **Développement :** deux documentations Python lues, programme écrit/modifié par JARVIS, manifests refusés ou candidats révisés, échecs de templates répétés, intervention Codex ajoutantargv, adaptation au tableauargv par JARVIS, test/activation/exécution réussis. Lecture indépendante de `source-a-final.json`, port8091 et autres champs conservés ; JSON invalide réellement rejeté avec code1.
- **Réutilisation :** désactivation suivie d'un refus attendu, réactivation, même code et même révision6 sur `source-b.json`, port chaîne corrigé, deux empreintes de sortie identiques, publication par le skill GitHub et vérification des blobs ; PR créée par JARVIS.

Les premiers tests shell du programme utilisaient `; echo EXIT_CODE` : leur code de retour extérieur0 ne prouvait pas un succès du programme. Le reçu négatif ultérieur avecargv transmet bien le code1. Il n'est pas compté comme une panne du Skill Lab.

## Persistance et préservation

[PERSISTANCE-REGISTRE](PERSISTANCE-REGISTRE.json) compare tâches reçues, versions, activations et runs avant/après redémarrage ciblé. [Second relevé](PERSISTANCE-REGISTRE-ARGV.json) conserve aussi l'état pendant l'ajoutargv. Les fichiers du modèle ne sont pas remplacés par Codex. La même mission reprend sans nouveau plan ni effacement.

Contrôle final :43 tâches historiques reçues ont les mêmes états et empreintes ; mémoire canonique `quick_check=ok`,5 souvenirs et4 préférences antérieurs identiques ; services concernés actifs. La seconde tâche réutilise un programme inchangé et reçoit zéro nouvelle instruction de coordination. Ces vérifications ne constituent ni un reboot global ni un nouveau test vocal23D.

## Erratum de réception des rapports du modèle

- **Inventaire :** les mauvais hôte/action et dépôt ne signifient pas que Dell1 est exclu ; la panne Ansible était stdin et non une révocation. Le catalogue réel remplace les champs supposés du rapport. Voir [inventaire contrôlé](INVENTAIRE-INITIAL.md).
- **Skills :** `/var/lib/jarvis/projects` figure dans le périmètre distant mais le compte n'a pas pu créer le répertoire demandé. Le refus Unix ne prouve pas une absence du chemin dans la politique. Les preuves Dell restent persistantes, elles ne sont pas intrinsèquement éphémères. Le rapport a précédé l'appel MCP réel ajouté après refus de réception ; seul le reçu ultérieur prouve l'appel.
- **Développement :** source-a contient0 ; source-b contient`"invalid"`. Le code utilise`json.loads` et considère valide un entier positif non booléen ; il ne corrige pas systématiquement tous les ports différents de8091 et ne vérifie pas une borne65535. Le rapport décrit ce comportement de manière erronée. L'interfaceargv est ajoutée par Codex ; l'adaptation du manifeste et le programme sont JARVIS.
- Les `evidence_id` des rapports désignent parfois l'identifiant d'invocation du moteur et non un reçu broker ; la correspondance explicite du JSON fait foi. Les heures saisies par le modèle ne remplacent pas les horodatages du journal.

La vérification interne de `config-repair` reste faible (`status` dans stdout). Les sorties demandées sont néanmoins réellement correctes et relues indépendamment dans ce scénario. Le [bilan14A](BILAN-14A.md) conserve cette limite pour les futurs cas, sans nier le succès concret des deux opérations.

La synthèse finale brute est elle aussi conservée avec réserves : elle mélange la version23C.1 du broker Unix et le serveur MCP (SDK1.30.0), compte trois compétences actives en omettant la quatrième qu'elle décrit pourtant, et reprend l'ancien compteur86 des tests. Les valeurs reçues sont quatre skills actifs et89 tests. Sa mention «mémoire SQLite inchangée» signifie uniquement préservation des données antérieures : la base a naturellement reçu la mission, les messages et documents nouveaux. Les références générales de directives décrivent le corpus consulté par Codex et transmis en résumé ; elles ne prouvent pas que JARVIS a lui-même relu tous ces fichiers. La validation acoustique physique qu'elle cite n'est pas un critère de cette mission ni une remise en cause de la réception propriétaire23D.
