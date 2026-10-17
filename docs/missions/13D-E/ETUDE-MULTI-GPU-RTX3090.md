# Mission 13 — Dell n°1 : étude de répartition multi-GPU (17 octobre 2026)

## Périmètre et état avéré
- Dell Precision 5820, RAM système annoncée 256 Go, cible deux RTX 3090 de 24 Go chacune.
- **Une seule RTX 3090 actuellement complètement alimentée** : NVIDIA/CUDA, Ollama et inférences Qwen/Ministral/Llama déjà reçus sur celle-ci. La **deuxième RTX 3090 reste à monter/raccorder correctement et à tester**. Ne pas présenter 48 Go de VRAM comme disponibles aujourd'hui.
- L'installation de la seconde carte ne remet pas en cause la réception du Dell n°1 ; c'est une extension matérielle et une nouvelle campagne *ciblée* d'essais modèles.

## Terminologie
Les cartes du Dell sont des GPU internes PCIe et non des eGPU Thunderbolt. « Répartition multi-GPU » désigne le placement de charges indépendantes sur deux GPU ou le partitionnement d'un modèle sur plusieurs GPU. La somme nominale 24 + 24 = 48 Go n'est **pas** un bloc monolithique de mémoire : allocations, KV cache, buffers et communications inter-GPU limitent l'espace utilisable.

## Trois configurations à tester
1. **Un seul modèle <= 24 Go sur un seul GPU** : point de référence, généralement meilleur pour la latence car moins de trafic inter-GPU. Ollama choisit en principe un GPU si le modèle et son contexte y tiennent entièrement.
2. **Deux modèles ou instances distinctes, un par RTX 3090** : parallélisme utile pour agents/outils, demandes concurrentes ou modèles spécialisés. Ollama peut placer différents modèles selon mémoire disponible ; pour un placement déterministe, envisager deux services Ollama séparés, chacun borné par `CUDA_VISIBLE_DEVICES` et un port spécifique. Vérifier la version et les limites de l'ordonnanceur.
3. **Un gros modèle réparti sur deux RTX 3090** : Ollama répartit les couches/poids sur les GPU disponibles si le modèle ne tient pas sur un seul. Le découpage évite une partie du hors-chargement CPU, mais introduit transferts PCIe et buffers additionnels ; mesurer tokens/s et latence plutôt que présumer un gain de vitesse. Si nécessaire comparer llama.cpp (contrôle explicite du split) et vLLM (tensor parallelism, compatibilité modèle/VRAM à qualifier).

## Aspects à mesurer après montage
- Reconnaissance des deux cartes via `nvidia-smi -L`, PCIe, pilotes, températures, consommation et alimentation/câbles réellement corrects.
- `nvidia-smi` durant inférence ; `ollama ps` pour confirmer CPU/GPU et résidence ; métriques délai premier jeton, tokens/s, VRAM par carte, utilisation simultanée, stabilité.
- Avec même modèle, mêmes prompts, longueurs de contexte et quantification : essai mono-GPU, split multi-GPU, puis deux modèles/instances indépendants.
- Tester quelques tailles raisonnables selon quantification, architecture, mémoire du KV cache et longueur de contexte. **Aucun choix définitif de modèle maintenant**. Déterminer si un modèle 30–32B quantifié tient sur une carte et si un modèle ~70B quantifié peut tenir *en pratique* sur deux cartes, à valider avec taille exacte, format et contexte ; ce ne sont pas des garanties.
- PCIe : vérifier le câblage/lignes effectives des deux slots ; NVLink uniquement si cartes, pont et logiciel le permettent, jamais présumer qu'il est disponible ni que le runtime l'utilise.
- Avec 256 Go RAM, un offload CPU partiel est possible mais souvent plus lent ; distinguer « démarre » de « utilisable ».

## Points d'attention connus
- Documentation Ollama FAQ : privilégie une seule carte lorsque le modèle y tient, répartit sinon sur les GPU ; charge concurrente et longueur de contexte accroissent la VRAM requise.
- Issues Ollama : attribution à un GPU précis par modèle limitée ; plusieurs démons et `CUDA_VISIBLE_DEVICES` sont une solution de placement explicite. Rapport de bogue septembre 2026 sur comptage VRAM multi-GPU selon index GPU : vérifier la version réellement installée et la consommation réelle, ne pas généraliser le bogue à toutes les versions.
- Ne pas appeler « répartition intelligente dynamique » le simple split d'un modèle : routage par charge en temps réel et migration d'instance sont des problèmes différents.

## Séquence décidée
1. Terminer le raccordement physique/électrique de la **seconde RTX 3090** (intervention propriétaire).
2. Contrôle ciblé NVIDIA/CUDA des deux GPU et du bus PCIe.
3. Mesurer les trois stratégies avec les modèles candidats dans Ollama ; alternative runtime seulement si Ollama empêche l'objectif.
4. **Revoir le modèle principal JARVIS sur données réelles** : qualité pour outils agentiques, contexte, latence, débit, charge multi-utilisateurs, efficacité mémoire.
5. Consigner commande/version/résultat/date pour chaque mesure, sans inventer de succès.

## Sources
- Ollama FAQ : https://github.com/ollama/ollama/blob/main/docs/faq.mdx
- Ollama GPU assignment : https://github.com/ollama/ollama/issues/10172
- Ollama multi-model GPU placement : https://github.com/ollama/ollama/issues/9637
- Ollama multi-GPU VRAM accounting (septembre 2026) : https://github.com/ollama/ollama/issues/18349
- Ollama scheduling dynamique (discussion) : https://github.com/ollama/ollama/issues/11810
- vLLM parallelism : https://docs.vllm.ai/en/latest/serving/parallelism_scaling/

## Cohérence référentiel
Consultés sur cette branche : `AGENTS.md`, `docs/CHARTE_DIRECTIVES_JARVIS.md`, `docs/missions/13D-E/RAPPORT-TRANSITOIRE-REPRISE.md`, `docs/missions/13D-E/PROMPT-INSTALLATION-AUTONOME.md`, `docs/missions/13D-E/RAPPORT-FINAL.md`, `SUIVI.md` et `ROADMAP.md`. Les directives les plus récentes et la réception réelle priment sur les notes historiques. **Aucune relance de l'installation et aucune fusion vers main.**
