# Réception BILAN-20261031

**✅🟡 GO avec réserves pour le bilan documentaire.** Ce verdict reçoit la collecte, les comparatifs et les recommandations dans les limites décrites. Aucune architecture cible n’a été déployée.

## Couverture et comptages

| Élément | Résultat |
|---|---|
| Machines observées / inaccessibles |3 /0 |
| Groupes applicatifs |24 ;72 fiches par machine |
| Entrées logiciels |4935 lignes APT/Python/npm |
| Composants et contrats |144 ; pas144 produits indépendants |
| Développements analysés |16 domaines : A5, B6, C2, D2, E1 |
| Amonts identifiés |15 familles, dont12 à licence libre explicitée |
| Domaines de recouvrement |3 ; aucune suppression |
| GPU physiques |4 RTX3090 et1 RTX3080 |
| Modules runtime comparés |51, dont6 différents de la base Git |

[Inventaires CSV et comptages](STATISTIQUES.json) · [comparatif matériel](02-COMPARATIF-DELL1-DELL2-MATERIEL.md) · [comparatif applicatif](04-COMPARATIF-DELL1-DELL2-APPLICATIONS.md).

## Conclusions techniques

Dell1 possède256GiB de RAM et deux3090 ; Dell2 possède128GiB et3090+3080. Les CPU, noyaux, pilotes NVIDIA et toolkits CUDA des Dell sont identiques au relevé. Le BIOS diffère :2.8.0 contre2.24.0. Les liens Ethernet actifs sont à1Gb/s. Les miroirs RAID1 sont sains[UU]. Aucune qualification physique supplémentaire n’est prétendue.

Le Mac charge le27B ; Dell1 charge le80B sur ses deux GPU via Ollama11435. Les deux services Ollama Dell1 partagent le catalogue. Dell2 dispose de SSH/CUDA et de candidats applicatifs, mais aucun Ollama ou modèle n’y est observé. Les copies du moteur et de SQLite sur les Dell ne sont pas des moteurs canoniques actifs.

TTS, bureau et Tailscale sur Dell1 sont des spécialisations historiques. L’absence de Git/npm limite certains projets de développement ; Ansible sur le seul contrôleur Mac est en revanche une répartition cohérente. Aucun service système en échec au relevé. Les dix services centraux contrôlés en fin d’audit restent actifs ; WebUI HTTPS, JL03 et l’API répondent. Ces contrôles ne reçoivent pas le microphone, Safari ou un nouveau scénario agentique.

Six modules sur disque diffèrent de cette branche. Leurs empreintes sont publiées ; cet écart est un risque de reproductibilité, pas une preuve de panne ni une attestation du code chargé en mémoire.

## Attribution et limites agentiques

Codex a effectué la collecte principale, les contrôles, la recherche des solutions existantes et la documentation. Qwen Code a effectué deux essais réels. Le premier s’est arrêté après7tours sur une erreur de compaction/admission : estimation12946tokens, limite utile annoncée9768. Cela ne démontre ni réduction de la fenêtre serveur32768, ni OOM.

Le second essai, guidé explicitement par Codex, a réussi deux lectures distantes en 11,5s : reçus190/Dell1 et192/Dell2. Son résumé invente des disques et des unités mémoire. **Les appels sont reçus ; sa restitution est NON VALIDÉE.** [Original](JARVIS-OBSERVATION-ORIGINALE.md), [erratum](ERRATUM-JARVIS.md), [sorties réelles](preuves/observations-dell-qwen.json). Aucun inventaire autonome exhaustif n’est attribué à Qwen.

Google Éducation a désormais réussi les lectures Drive/Calendar/Gmail164/166/168. L’ancien rapport bloqué reste historique. Aucune nouvelle réception globale Google n’est prononcée : écritures et parcours clients Éducation restent à vérifier. Les jetons sont séparés, mais la façade reste commune avec un paramètre de profil ; deux interfaces indépendantes avec droits distincts ne sont pas encore reçues.

## Rationalisation proposée et réception

Réutiliser Qwen Code, Open WebUI, Ollama, MCP, Ansible et les collecteurs éprouvés ; limiter le code spécifique aux contrats de mission, d’identité, de permissions et de preuve. LangGraph/Temporal ou MCPO ne sont pas des remplacements équivalents par leur seule existence. [Comparatif](COMPARATIF-STANDARDS.md) et [plan avec efforts, risques et critères](12-PLAN-DE-RATIONALISATION.md).

Réserves : découverte de fichiers bornée, instantanés non simultanés, dépendances transitives non toutes attribuées individuellement, limites physiques non rejouées, prose Qwen incorrecte, P7 non reçu et P4 suspendue. Les comptages et sources sont explicités ; aucune absence d’observation n’est transformée en échec.

Branche `codex/bilan-20261031`, base exacte `501887131c88bad692e1a1c108dbce808f55d5b0` issue de PR37. Les notes P7 et les directives PR36 ont été consultées sur leurs branches distinctes, sans fusion silencieuse. [Sources](SOURCES.json) · [contrôles documentaires](CONTROLES.json).

Aucun redémarrage, installation, suppression de modèle, changement de routage ou migration de base. M26-P4 et MANUAL-HOLD restent en pause. Aucune clôture14A, aucun lancement24-Old. Publication sur PR dédiée, sans fusion automatique dans main. Les transformations proposées constituent une suite distincte ; elles ne sont pas nécessaires à la réception de ce bilan.
