# État de mission

Généré par JARVIS-engine depuis les checkpoints réels. Les rapports sont rédigés par le modèle.

| Tâche | État | Rapport vérifié |
| --- | --- | --- |
| t01_analyse_docs — Analyser les documents GitHub de référence pour comprendre le contexte et l'architecture | validated | ea2410c369b3aea22e290e51501f51bc759788b97c12e7464750e79882ee446b |
| t02_etat_labo — Évaluer l'état actuel du laboratoire : services, ressources, interfaces existantes | validated | d45bfdd2cd711404a119ac8897e07e8b8e5303c10ae45c728e4cc314a195b357 |
| t03_conception_livekit — Concevoir l'architecture LiveKit avec les composants disponibles (Whisper, Piper, Ollama) | validated | ec0e2b5f5ad6ac38fd86d6b5d876bf8b9cc81babba2458a59269bbdc7b9fb228 |
| t04_install_livekit_server — Installer et configurer LiveKit Server sur le Mac mini | validated | e8cc6c6918f7229a2e003bf8240f4aa0f3a247eec1501f67a8b014d3fc98bd35 |
| t05_dev_agent_python — Développer l'agent Python LiveKit avec adaptateurs STT/TTS/LLM | validated | 3b746227fd5f8187c8a18aefdecb602ddf073f442df519755406722de495f057 |
| t06_dev_client_web — Développer un client Web de démonstration pour tester le prototype | validated | 7ac0843f0886c3d6723c9ef67ed63b77c05679b12fd65fbcc5ed1fdc0e852965 |
| t07_integration_services — Intégrer les services : démarrage, gestion sessions, journalisation | validated | 4fc142dd57c2c31a9cd001e01472ae10d9bf65fde6336f66f17c12488e157a6c |
| t08_tests_fonctionnels — Exécuter les tests fonctionnels : connexion, audio, reconnaissance, synthèse, interruption | validated | c2e1e88e1c1be5b1ec582873d183d410a6840d669ad38c37c9c79e068ac212d6 |
| t09_mesures_latence — Mesurer les latences et l'utilisation des ressources (CPU/GPU) | validated | 95d47da34726e2a46f88a97c0e3aa632068d07474633330d2687ee186c14cb0e |
| t10_correction_erreurs — Corriger les erreurs rencontrées et réitérer les tests | validated | 180d904e445272813f40190dce7221c08f4e160bca5b1609cc5be4d45c4d69bd |
| t11_test_tailscale — Tester l'accès distant via Tailscale depuis le Mac | validated | 6da40600e35ac4dd03a453718ce6da4db5a43d295af445c0193a0e6091ec53e6 |
| t12_code_github — Publier le code, configs et documentation sur une branche GitHub dédiée | validated | db28d98d115822a04ef6a0f5babfc6f9c177e27f74de2d28b3bd65aab4249463 |
| t13_rapport_final — Rédiger le rapport final avec preuves, résultats et évaluation de l'autonomie | blocked | f61e3e98ba6a47d2c36281022d10c4faca4400f6a676ec7c5d57ce1b5549bade |

Les livraisons GitHub sont vérifiées séparément dans le Sandbox ; une tâche validée n’est pas une affirmation de livraison distante.

État de réception Codex du 20/10/2026 : t01–t12 conservées validated; t13 blocked (barge-in échoué sur réponse audible, aucune clôture). Le rapport canonique inclut le nouveau run Piper warmup / délai LLM.
