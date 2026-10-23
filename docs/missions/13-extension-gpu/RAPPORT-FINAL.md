# Mission13 — réception partielle de l’extension GPU

**23 octobre2026 — 🟡 Incomplet : détection et CUDA double reçus, alimentation et inférence double non reçues.** [PR23](https://github.com/regisazzoun/JARVIS-Local-AI-Lab/pull/23), branche `codex/mission-13-extension-dual-rtx3090`, sans fusion. Le complément est livré en l’état documenté ; il reste à reprendre au checkpoint matériel, sans réinstallation.

Le dernier historique reçu ne reconnaissait qu’une3090 alimentée. Cette reprise observe **deux RTX3090 de24576MiB chacune**, pilotes NVIDIA550.163.01 initialisés et sous-systèmes Dell identiques1028:3880. JARVIS a exécuté un petit calcul CUDA sur chaque appareil :120.0 attendu et obtenu sur0 et1. Les reçus sont corrélés aux événements root du broker ; le contrôle PCI/services indépendant concorde.

## Critères propriétaire

| Critère | Résultat à cette réception |
| --- | --- |
| Alimentation résolue et documentée | 🟡 Non : PSU950W déclaré, références PDB/faisceaux, pinout et intensités non établis |
| Seconde carte physiquement présente | ✅ Deux fonctions graphiques reconnues ; montage précis réalisé hors session et non documenté |
| DeuxGPU reconnus Debian/NVIDIA | ✅ Relevés JARVIS et lecture PCI indépendante |
| Calcul CUDA sur chacune | ✅ Deux petits calculs réels ; ne valent pas qualification électrique |
| Services JARVIS préservés | ✅ Lectures de santé/backend/broker et services Dell ; aucun pilote ou service remplacé |
| Inférence multi-GPU évaluée | 🟡 Préparation seulement ; aucune nouvelle mesure d’inférence double |
| Choix de modèles réexaminé | ✅ Étude préparatoire/catalogue actuel ; choix définitif non arrêté faute d’essais |
| Résultats/limites publiés | Documentation, code et preuves sur branche dédiée/PR, sans fusion main |

## Résultat matériel prioritaire

Les deux cartes annoncent350W chacune. Le poste graphique700W dépasse l’enveloppe600W de la fiche Dell5820. Le guide constructeur transversal distingue deux/quatre prises6+2 selon châssis et exclut les configurations doubles GeForce3080/3090 de sa matrice. Il ne suffit donc pas de remplacer deux faisceaux par deux modèles doubles pour obtenir une qualification. TV5X6/VVFXD ne sont pas une identification validée de faisceau ni un pinout.

Les schémas livrés sont fonctionnels, avec inconnues explicites. Aucun branchement sur une sortie10broches/CPU ou adaptateur au câblage incertain n’est proposé. Une limitation logicielle250–300W par GPU est une piste de budget, non appliquée et non suffisante pour qualifier les sorties. Aucun changement matériel, de limite de puissance, de BIOS ou de pilote effectué par Codex/JARVIS ici.

## Logiciel et modèles

Debian13.7, noyau6.12.113, i9-10980XE,251,42GiB exposés à Linux, toolkit12.4.131 et PyTorch2.6.0+cu124 sont observés. L’accès pair CUDA est faux, la topologie est SYS. PCIeGen1 au faible usage et x16/x8 courants appellent une mesure sous charge, sans diagnostiquer une panne sur ce seul relevé.

Ollama0.40.3 est actif mais épinglé à un seul UUID : il n’utilisera pas automatiquement la seconde carte. Contexte4096, parallélisme1 et un modèle résident maximum observés. Le catalogue existant Qwen27B/Ministral14B/Llama8B est conservé. Les candidats32B/70B et les quantifications sont étudiés à partir des catalogues officiels ; aucun téléchargement ni benchmark présenté comme réel. Deux24Go ne deviennent pas un GPU monolithique48Go. La préparation locale ne lance pas la mission28.

## Exécution et limites agentiques

Codex a développé les scripts et deux commandes fixes, corrigé une sortie tronquée et l’adresse de lecture d’Ollama. JARVIS a réellement utilisé ces fonctions ; il a également répété27fois l’inventaire et atteint la limite de sa première conversation sans rapport d’étape. Sa continuation ciblée a écrit un erratum et un rapport d’étape réel. Total33appels natifs et32reçus broker corrélés ; ce ne sont pas33essais indépendants. Le petit calcul a été lancé malgré la consigne de différer si deux cartes étaient présentes ; aucune charge prolongée n’a suivi.

Les rapports bruts restent erronés sur certains points malgré l’erratum guidé. Les [rectifications Codex](ERRATA-CODEX.md), les octets exacts et les reçus priment. Ni autonomie complète, ni amélioration du raisonnement par le seul ajout de VRAM ne sont revendiquées.26B reste clôturée incomplète,14A ouverte, TTS-01 suspendue.

## Livrables et reprise

[Inventaire](INVENTAIRE-DELL.md) · [Alimentation](ETUDE-ALIMENTATION-GPU.md) · [Références](REFERENCES-FAISCEAUX.md) · [Schémas](SCHEMAS-CABLAGE.md) · [Préparation logicielle](PREPARATION-NVIDIA-CUDA.md) · [Tests](TESTS-DEUX-GPU.md) · [Modèles](EVALUATION-MODELES-IA.md) · [Bilan28](BILAN-MISSION-28.md) · [Attribution](ATTRIBUTION-CODEX-JARVIS.md).

Étapes restantes : identifier les références et le raccordement réellement présents, qualifier brochage/courants/budget/refroidissement, puis essais ciblés de charge et d’inférence avec observations par carte. Conserver la reconnaissance et les petits calculs reçus ; ne pas refaire l’installation13D-E. Le propriétaire réalise la partie physique. Les autorisations informatiques restent acquises, sans nouveau processus de validation générale.
