# Réception du diagnostic des boucles IA — 30 octobre 2026

**✅🟡 Correctifs techniques déployés avec réserves. Sonde JARVIS 🟡 incomplète ; rapport libre ❌ NON VALIDÉ.** 185tests logiciels ciblés PASS. La finalisation Qwen Code est reçue sur les essais ciblés. L’autonomie générale, les missions historiques et la prose libre JARVIS ne sont pas reçues.

## Origines isolées

| Composant | Conclusion étayée | Correction réellement déployée |
|---|---|---|
| Qwen Code | Sur le même historique, l’ancien prompt déclenche un nouvel outil malgré PASS ; le prompt court termine, avec ancien comme nouveau transport. L’identité JARVIS n’est pas dans cette requête CLI. | Prompt court, même modèle et mêmes limites. Deux contrôles CLI terminent avec une commande chacun ; une correction réelle termine avec trois tests indépendants PASS. |
| Relais Ollama | Mauvaise association des résultats d’outils, limite de sortie ignorée et troncature annoncée comme fin normale. Ces défauts n’expliquent pas seuls la répétition dans l’A/B. | Association par tool_call_id, tool_name correct, limites respectées, finish_reason=length conservé et vérifié réellement. |
| Anciennes consignes JARVIS | Consignes contradictoires de revérification/correction et accumulation des erreurs de tous les anciens brouillons jusqu’au prochain PASS. La v1 obsolète est un secours non chargé par cette sonde, qui utilise v2. | Constats rattachés au SHA courant, archives des anciens FAIL, vérification après mutation pertinente et faits actualisés avant rédaction. v1 corrigée en secours, v2 active inchangée ; erratum91407. |
| Contexte et interfaces | Permissions perdues à la compaction, propositions refusées réinjectées comme faits, révisions globales ignorées, outils de reprise décrits mais masqués. | État structuré conservant provenance, politique, cible exacte, refus précis et contrats versionnés. Révision et retrait limité des étapes jamais tentées. |
| Planification et reprises | Faux progrès après ancienne réparation, revue trop grande qui ne rendait pas la main au planificateur ; compteurs worker ignorant la frontière d’une réparation vérifiée. | Garde basé sur preuves récentes, revue non exécutée distincte de FAIL, baselines de réparation explicites et historiques intacts. |
| Vérification éditoriale | Des erreurs du modèle subsistent ; le vérificateur a également confondu preuve absente et preuve exclue de sa projection. | Références éligibles explicites, heures ISO originales, errata conservés, revue découpée existante activée et contrôle indépendant. Une permission ne prouve toujours pas un état de service. |

La piste du propriétaire est fondée pour la règle de réinjection des anciens constats et les consignes de workflow JARVIS. L’ancienne identité v1 n’était pas la cause de cette sonde ; notre attribution initiale est rectifiée. Elle ne constitue pas une explication unique des deux logiciels. Le détail des expériences, contre-exemples, limites et régressions introduites puis corrigées par Codex figure dans [DIAGNOSTIC.md](DIAGNOSTIC.md).

## Résultats réels

- **Code : fonctionnement démontré sur les essais ciblés.** Le défaut de seuil est modifié par Qwen, les tests restent inchangés, et le CLI rend son bilan. Une mention de devise euro non demandée reste une inférence injustifiée dans sa prose ; aucune certification générale des rapports.
- **Sonde originale27fc9d… : incomplète et interrompue.** Le garde corrigé finit nativement après trois stagnations, événements90621/90622, sans arrêt opérateur. Trente et une versions de plan restent consultables, aucun succès rétrospectif.
- **Comparaison999923… : plan propre accepté89591 et opérations réelles.** Même objectif initial, contexte neuf, lien explicite vers l’original. Les commandes de service et les écritures de rapports sont effectuées par JARVIS via le broker Mac mini ; les décisions/inférences proviennent du80B sur Dell1. Aucun travail Dell2 ni aucune autonomie de développement distribué n’est revendiqué dans cet essai.
- **Rapports :** les premiers FAIL/INSUFFICIENT, originaux et corrections sont conservés. Les contrôles indépendants90417 et91012 détectent respectivement heures/fausse absence de modification, puis comptage/fausse absence de modification. Les réparations d’interface et de contexte sont attribuées à Codex, les textes au modèle.

## Verdict final de la sonde et isolation du facteur modèle

La dernière écriture a bien été exécutée par JARVIS (91837). Le modèle corrige les totaux mais inverse encore3/4 et décrit deux unités comme absentes/masquées sans preuve ; le `status` de systemd-networkd indiquait pourtant Loaded: loaded. Contrôle indépendant réellement exécuté :92030/92031, FAIL. La revue automatique reste **INSUFFICIENT**, car un segment et ses sources dépassent encore l’entrée malgré le découpage ; ce contrôle non exécuté n’est pas présenté comme un test échoué.

La dernière correction reçoit donc un **échec indépendant Codex** distinct :6échecs historiques, frontière de réparation3, soit3dans ce segment ; escalade persistante et interruption. Les deux sondes n’ont plus de lease ni de calcul actif. Il n’y a pas de quatrième correction autonome. Le bilan exact des observations est livré séparément par Codex, avec attribution explicite, dans [RELEVE-FACTUEL-CODEX.md](RELEVE-FACTUEL-CODEX.md).

Quatre comparaisons supplémentaires interrogent le **même80B, identitév2, seed42, température0,1**, sans aucun outil hôte ni reprise de mission. Tous les paquets sont inférieurs au plafond ; les quatre JSON respectent leur schéma1800caractères. Une conformité de format n’est pas une conformité factuelle.

| Contexte expérimental | Résultat observé |
|---|---|
| Ancien brouillon, sans référence officielle | Conserve l’inversion3/4 et les attributions de source incorrectes. |
| Contexte neuf, sans référence | Mapping encore faux,10actifs annoncés pour9énumérés. |
| Ancien brouillon + référence officielle | Conserve l’interprétation3=absent malgré la source fournie. |
| Contexte neuf + référence officielle | Corrige le mapping3/4, mais annonce8actifs pour9énumérés et nie une lecture networkd pourtant fournie. |

Le vieux brouillon peut donc renforcer une fausse interprétation. Le modèle reste également capable de déformer des faits dans un paquet neuf et correctement sourcé. Ces quatre échantillons ciblés ne permettent pas une loi universelle ; ils réfutent une résolution générale par le seul prompt. La déformation est présente dans le texte produit en JSON natif, avant toute écriture hôte : les corrections du relais OpenAI n’en sont pas l’explication. [Entrées figées](ENTREES-FACTEURS-RAPPORT.json), [sorties originales et contrôle](PREUVES-FACTEURS-RAPPORT.json).

Restent non reçus : restitution libre fiable, revue automatique de ce grand bloc source, et autonomie de cette sonde sans assistance Codex. Une future stratégie devra réduire les preuves par affirmation et contrôler les faits fermés indépendamment de la prose du même modèle. Aucun de ces développements futurs n’est prétendu livré ici.

## Attribution et limites

Codex a développé et installé les adaptations, préparé les captures/A/B et le défaut de programme, vérifié les sorties, corrigé deux de ses propres régressions, et fourni les constats de ses contrôles indépendants. Qwen Code a exécuté la correction de programme sur le Mac mini avec inférence Dell1. JARVIS a produit les plans, choisi les lectures, déclenché le broker et écrit ses rapports. Ces contributions ne sont pas interchangeables.

La qualité générale du vérificateur sémantique reste réservée : la revue modèle n’a pas relevé tous les défauts ensuite démontrés par comparaison exacte. La marge d’admission conservatrice est distincte du nombre réel de tokens ; aucun plafond32768 n’a été relevé. Les anciens flux XML mal formés n’ayant pas été capturés, leur attribution caractère par caractère au modèle/parseur reste indémontrable.

M26-P4 est toujours interrompue et MANUAL-HOLD conservé. Aucun modèle, système, service Ollama ou base canonique n’a été remplacé. Pas de réception14A/26B/P4, ni de fusion main.

## Installation et preuves

Code : `7a6f4eb`, `1823b7f`, `accc640`, `5373123`, `b9d597c`, `18539cd`, `006781f`, `7708308`, `71b26db` et historique de cette branche ; manifeste des fichiers réellement installés disponible. Le diff installé préserve les ajouts antérieurs non commités et ne remplace pas le runtime par un ancien arbre Git.

- [Installation et retour arrière](INSTALLATION-REPRISE.md), [manifeste installé](MANIFESTE-INSTALLATION.json), [patch runtime](PATCH-RUNTIME.diff).
- [Preuves Code et A/B](PREUVES-QWEN-CODE.json), [preuves JARVIS sélectionnées](PREUVES-JARVIS.json).
- [Arrêt natif de la sonde originale](PREUVE-ARRET-NATIF.json), [préflight deux étapes](PREUVE-BUDGET-DEUX-ETAPES.json).
- [Contrôle final indépendant](CONTROLE-RAPPORT-FINAL.json), [santé et états finaux](VERIFICATION-INDEPENDANTE.json), [original JARVIS non validé](JARVIS-BROUILLON-NON-VALIDE.md).
- [Tests logiciels](TESTS-LOGICIELS.txt). Ces tests ne sont pas des preuves fictives d’autonomie du modèle.

Publication : [PR33](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/33), branche `codex/diagnostic-boucles-ia`, base [PR32](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/32). Sans fusion automatique. Les quatre empreintes des requêtes du script public de comparaison ont été reproduites exactement depuis les entrées figées, sans nouvelle inférence ; cela vérifie la reproductibilité des paquets, pas la justesse de leurs réponses.
