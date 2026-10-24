# Réception TTS-01 — 24 octobre2026

**✅🟡 GO avec réserves.** Qwen3-TTS fonctionne réellement en français sur Dell1. JARVIS a écrit/corrigé le générateur, exécuté les synthèses et transféré les trois nouveaux WAV. Codex a développé les capacités manquantes, guidé les reprises et vérifié les résultats indépendamment. L’autonomie sans assistance reste **non validée** ; les défauts de prose et les reprises dirigées sont documentés.

## Résultat technique

Modèle `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, voix native `Uncle_Fu`, langue `French`, instruction générique calme et professionnelle. Révision du cache `0c0e3051f131929182e2c023b9537f8b1c68adfe`, qwen-tts0.1.1, PyTorch2.6.0+cu124, BF16 sur GPU0, attention eager. Aucun extrait de film ne conditionne la voix.

| Fichier | Durée audio | Synthèse et écriture WAV | RTF |
| --- | ---: | ---: | ---: |
| accueil.wav |6,16s |11,266s |1,829 |
| diagnostic.wav |8,24s |14,391s |1,746 |
| conversation.wav |7,60s |13,388s |1,762 |

WAV24kHz,mono,PCM16bits. Chargement commun du modèle4,789s, une seule fois depuis le cache disque ; les trois occurrences de cette valeur dans le JSON ne sont pas trois chargements. Commande native48,745s, reçu `2d7ca821218b4bf1b62cc5a66f11488b`, invocation JARVIS `28bab9ea96de407c81990c80e872d80c`, réservation GPU `19c1789eb45c4b2ca6a8fa7314a1f3d9`. Les nombres bruts restent dans [MESURES_PERFORMANCES.json](MESURES_PERFORMANCES.json), avec leur [contexte et limites](MESURES-CONTEXTE.json).

Le programme mesure la mémoire/charge globale du GPU0 par NVML avant/après chaque phrase : environ4747–4981Mio utilisés dans cette série. La mémoire RAM relevée est celle du système entier, pas le RSS du processus. Une seconde observation SSH/nvidia-smi a conservé38instantanés, dont34 avec le Python TTS présent : maximum échantillonné du processus4642Mio, GPU0 à38% et152,29W, température maximale59°C dans cette fenêtre. Ces instantanés ne garantissent pas les maxima physiques instantanés et ne sont pas confondus avec les mesures NVML. Le GPU1 ne porte pas la synthèse de ce petit modèle. Aucun nouvel essai700W n’a été lancé.

## Vérification indépendante

- La sonde fixe relit les trois WAV et leurs métadonnées :3/3 conformes, signal non nul, aucune valeur PCM en pleine échelle, durées/RTF/version cohérents. [Reçu original](SONDE-WAV-FINALE.json).
- Une transcription locale Whisper-small hors ligne retrouve les trois textes demandés. Les différences sont de ponctuation/capitalisation, sans mot manquant constaté. [Transcriptions et empreintes](TRANSCRIPTION-INDEPENDANTE.json).
- Les transferts JARVIS conservent les empreintes ; l’API authentifiée renvoie exactement les mêmes octets, MIME audio/wav, HTTP200. Une requête sans session reçoit401.
- Chromium authentifié depuis JL-02 décode et lit chacun des trois fichiers jusqu’à `ended`. [Preuves de lecture](CONTROLE-AUDIO-FINAL.json). Les services conversation, broker, workers, Ollama et LiveKit sont actifs après réception ; les deux endpoints Dell répondent sur leurs adresses configurées ([contrôle final](SERVICES-APRES-RECEPTION.json)). Le navigateur est muet : aucune écoute physique ni réception esthétique n’en est déduite.
-246tests logiciels passent après les correctifs de réservation, de contrats et de continuation. Ils vérifient l’outillage ; ce ne sont pas246preuves d’autonomie du modèle.

## Écouter les trois échantillons

Ouvrir [JL-02 connecté](http://localhost:8765/launcher2/) par le tunnel habituel, conserver la session, puis :

1. [Accueil](http://localhost:8765/api/launcher/artifact?path=%2Fvar%2Flib%2Fjarvis%2Fprojects%2Ftts-01%2Faudio%2Faccueil.wav)
2. [Diagnostic](http://localhost:8765/api/launcher/artifact?path=%2Fvar%2Flib%2Fjarvis%2Fprojects%2Ftts-01%2Faudio%2Fdiagnostic.wav)
3. [Conversation](http://localhost:8765/api/launcher/artifact?path=%2Fvar%2Flib%2Fjarvis%2Fprojects%2Ftts-01%2Faudio%2Fconversation.wav)

Ces liens sont privés et nécessitent l’origine locale/tunnel et une session propriétaire active ; ils ne sont pas des URLs publiques GitHub. Les WAV restent sous `/var/lib/jarvis/projects/tts-01/audio/`, avec originaux Dell dans `/opt/jarvis-lab/tts-01/generated/`. Les extraits de film restent dans le stockage privé et ne sont pas publiés.

## Reprise et corrections

La mission persistante `8bd3e5b316a94021b5183e0db26d6efc` a été conservée, avec anciens plans, checkpoints, sorties et erreurs. Les inventaires/archive/installations antérieurs sont réutilisés. La branche reprend la clôture28A `62b7334`, et conserve27B conversation Mac et80B missions Dell.

Les vrais obstacles successifs comprennent une mauvaise API Coqui dans le premier générateur JARVIS, un appel au Python système sans torch, la dépendance pynvml absente, puis une OOM lors d’un chargement direct hors réservation. Les avertissements SoX/flash-attn ne sont pas la cause de ces échecs. Une ancienne déclaration conversationnelle d’OOM sans aucun outil n’était pas une preuve d’exécution ; elle reste distincte de l’OOM réellement observée ensuite.

Codex a étendu la file de calcul existante : `compute_project_gpu` réserve Dell1, libère la résidence80B de l’instance missions, vérifie sa libération et exécute le broker normal. Aucun service ni modèle n’est supprimé. Codex a également ajouté la sonde WAV, corrigé son enum client, et permis `mission_verify contract=active:0` pour utiliser le contrat enregistré sans recopier ses nombres/types. Les vérifications restent strictes. Une continuation liée qui ne produit aucun outil opérationnel réussi ne peut désormais publier une réponse de succès comme résultat reçu ; cela ne constitue pas un validateur général de toutes les phrases du modèle.

L’exécution a nécessité des continuations dirigées par Codex, un arrêt ciblé des workers pour éviter leur concurrence avec ces continuations, et une réception documentaire manuelle du choix de moteur. Aucun reset des missions/mémoires/skills ; aucun second moteur créé. Les opérations réelles de génération/transfert appartiennent à JARVIS, pas à Codex.

## Réserves et verdicts séparés

**Fonctionnement TTS : ✅🟡 GO avec réserves.** Trois phrases françaises réellement produites, mesurées et accessibles. Le RTF agrégé est1,775 : la synthèse batch est plus lente que le temps audio. Le temps avant premier segment n’a pas été mesuré, l’API utilisée n’étant pas streaming. La faible latence d’une conversation vocale future n’est donc pas réceptionnée ici. Chatterbox n’a pas été benchmarké. La continuation par chat liée peut conserver le verrou conversationnel pendant son étape : une conversation simultanée non bloquante pendant cette génération n’est pas démontrée. Le modèle conversationnel et ses ressources restent conservés ; ce constat ne vaut pas réception de fluidité vocale.

**Autonomie JARVIS : ✅🟡 GO pour l’exécution supervisée ; autonomie complète non validée.** JARVIS installe, écrit, corrige, génère et transfère avec les outils réels. Codex a encore dû fournir des diagnostics, des consignes ciblées et corriger l’infrastructure. Les plans révisés par Codex et la réception finale Codex ne sont pas des succès autonomes JARVIS.

**Rapports libres : réserves persistantes.** Les rapports bruts ont encore confondu identifiant de mission, fichiers avec/sans accent, vérification annoncée et appel réellement fait, quantités et heures. Les originaux sont conservés avec [rectifications](RECTIFICATIONS-FINALES.md). La présente réception consolidée est Codex ; aucune levée automatique des réserves26B ni clôture14A.

**Qualité vocale : appréciation propriétaire attendue**, sans blocage technique. Le preset est d’origine chinoise, utilisé en français ; timbre, accent et proximité esthétique restent à juger à l’écoute. Aucune imitation de Philippe Faure, aucun remplacement automatique de Piper, aucun lancement14A/24-Old/Dell2/TTS de production.

[Installation et réutilisation](INSTALLATION_TTS_01.md) · [Programme réellement exécuté](generate.py) · [Exécution et attribution](RAPPORT_EXECUTION_AGENTIQUE.md) · [Preuves de reprise](REPRISE24-PREUVES-JARVIS.json).
