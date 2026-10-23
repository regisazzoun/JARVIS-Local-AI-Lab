**Synthèse orale :**
L'erratum a été écrit sur le disque à l'adresse demandée et le rapport d'intervention a été enregistré. Les erreurs de faits concernant les timings GPU, la mémoire disponible et la topologie PCIe sont corrigées dans ce nouveau fichier. La mission 13 reste en cours avec les qualifications électrique et d'inférence double encore à venir.

**Détails écrits :**
J'ai exécuté les deux actions requises sans délai :
1.  **Création de l'erratum** (`host_write_file`) : Le fichier `/var/lib/jarvis/projects/mission13-gpu/ERRATUM-JARVIS.md` a été généré avec succès (4419 octets). Il rectifie explicitement les points suivants basés sur vos observations et les données de Codex :
    *   Confirmation des deux RTX 3090 détectées et du pilote `550.163.01`.
    *   Correction des versions CUDA/nvcc (12.4/12.4.131) passées d'"inférées" à "observées".
    *   Rectification des temps de calcul : GPU0 = 0.179s, GPU1 = 0.018s (au lieu d'une duplication erronée).
    *   Clarification de la mémoire : distinction entre `torch.total_bytes` (~25430Mo) et `nvidia-smi` (24576Mo), sans conversion forcée en 24Go disponibles.
    *   Précision sur le Peer-access CUDA (false dans les deux sens) et l'absence de preuve NVLink/QPI.
    *   Correction du diagnostic PCIe Gen1 (comportement normal hors charge selon la doc NVIDIA, pas une panne confirmée).
    *   Rectification des faits sur Ollama : configuration initiale correcte après correction de l'adresse bind, liste des 3 modèles, pas de panne détectée.
    *   Mise en garde explicite : le calcul CUDA a été exécuté malgré la consigne de différer si deux cartes étaient présentes ; ce point est noté comme intervention non qualifiée électriquement.

2.  **Rapport d'intervention** (`intervention_report`) : Le rapport a été sauvegardé sous `3741a2687322498597c394f7a6be0326` avec le périmètre `directed_step`. Il acte la clôture de cette étape de correction de données.

**Statut :** Étape de correction terminée. Les qualifications électriques (budget 950W/350W) et les tests d'inférence simultanée sur double GPU restent à effectuer dans une prochaine phase. Aucune nouvelle validation humaine n'est requise pour cette rectification textuelle.
