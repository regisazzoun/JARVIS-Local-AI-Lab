# JARVIS — Mission 05D : calcul CUDA réel et première inférence GPU

12 octobre 2026 — **SUCCÈS : première réponse de Llama 3.1 8B calculée sur la Quadro RTX 5000. GO pour poursuivre les essais Ollama locaux.**

## État et calcul CUDA

Noyau T2 6.18.54-1-t2-trixie, même boot ID d8f67bde-f785-4365-99ed-1af19afe9620. GPU 81:00.0, NVIDIA 595.91.07, UUID GPU-ae5d487a-5a70-e915-879c-71e3cb60729d. Intel i915 et GNOME PID 1270 maintenus ; SDDM et SSH actifs avant/après. Les dix empreintes des modules NVIDIA et l’inventaire/version des paquets dpkg sont inchangés.

Kernel PTX JIT exécuté via libcuda.so.1 et Python ctypes, sans CUDA Toolkit : quatre blocs de 256 threads calculent out[i] = 3*i + 7. Résultat vérifié côté CPU pour chaque élément (dernier = 3076). Première série : 100 kernels / 102 400 valeurs ; puis dix séries, 1000 kernels / 1 024 000 valeurs supplémentaires, avec création/libération des contextes et allocations. Tous les résultats mathématiques conformes et appels CUDA réussis. Ce sont de petits calculs, pas un stress test prolongé.

Incident applicatif réversible : premier PTX déclaré version 6.0, trop ancien pour cible sm_75, refusé par cuModuleLoadData (218). Correction du script vers PTX 6.4 ; aucun pilote ou système modifié. Les résultats conservés correspondent aux exécutions corrigées.

## Installation Ollama et sauvegarde

Archive officielle téléchargée depuis https://ollama.com/download/ollama-linux-amd64.tar.zst via HTTPS, inspectée (chemins bin/ et lib/, pas de chemins absolus ni ..), empreinte calculée avant extraction. Ollama **0.40.3** installé dans `/home/adminjarvis/JARVIS/ollama`. SHA-256 archive : ce6f8b671a699bf1ebafb28d60dbbabf4f37b30b499145fa308a8ba72de021d6.

L’empreinte est une trace locale, pas une signature éditeur indépendante. Le script officiel a été téléchargé pour inspection, **pas exécuté** : il peut créer un utilisateur/groupes, un service système activé au démarrage et installer des pilotes selon la détection. La méthode manuelle [documentée par Ollama](https://docs.ollama.com/linux) a été utilisée avec préfixe utilisateur. Aucun compte ni service système créé, aucun dépôt/APT modifié, aucune dépendance installée.

État préalable sauvegardé dans avant-installation.json : versions de paquets, ports, états services/GPU et absence du répertoire d’installation et des chemins système Ollama contrôlés. Aucune configuration précédente n’a été remplacée ; il n’y avait donc pas de fichier antérieur à restaurer pour cette installation. Scripts, manifeste, archive et logs conservés. Ollama peut créer ses clés utilisateur sous ~/.ollama ; ce répertoire n’a pas été supprimé et n’est pas inclus dans le rollback automatique proposé.

Serveur lancé comme adminjarvis, PID initial 54006, API uniquement `127.0.0.1:11434`. Paramètres : modèles dans JARVIS/ollama/models, contexte 4096, une requête parallèle, CUDA_VISIBLE_DEVICES fixé à l’UUID Quadro. Inhibition sleep:idle temporaire utilisée pendant téléchargement/calcul/inférence, puis levée. Le serveur reste actif pour utilisation locale ; pas de démarrage automatique après reboot.

## Modèle, preuves GPU et mesures

Modèle [llama3.1:8b officiel](https://ollama.com/library/llama3.1:8b), 8.0B, GGUF **Q4_K_M**, digest `46e0c10c039e019119339687c3c1757cc81b9da49709a3b3924863ba87ca666e`. Téléchargement ~4.9 GB, réussi avec vérification des blobs par Ollama.

Les logs identifient CUDA compute 7.5 / Quadro et **33/33 couches déchargées vers le GPU**. nvidia-smi détecte llama-server comme processus de calcul, notamment PID 54455 à 5162 MiB ; mémoire GPU totale maximale échantillonnée 5174 MiB. /api/ps rapporte size_vram = size = 5 271 715 839 octets pour le modèle chargé. Ces preuves, le calcul CUDA précédent et la réponse générée démontrent l’inférence GPU ; aucun simple succès CPU n’est présenté comme succès GPU.

| Mesure première requête | Résultat |
|---|---:|
| Chargement rapporté par Ollama | 33.99 s |
| Évaluation du prompt, 50 tokens | 25.28 s |
| Génération, 98 tokens | 1.393 s |
| Débit de génération | 70.38 tokens/s |
| Durée murale totale | 60.68 s |
| Contexte | 4096 tokens |

Le débit est celui du décodage, pas 98 tokens divisés par la durée totale. La première requête comprend chargement et échauffement/JIT ; l’évaluation initiale du prompt est lente. Ces mesures uniques ne constituent pas un benchmark stable.

Réponse effective :

> Bonjour, je suis JARVIS, le premier modèle local de l'intelligence artificielle. Un GPU, ou Graphics Processing Unit, est un processeur spécialisé qui permet à l'intelligence artificielle de traiter rapidement et efficacement de grandes quantités de données. Cela permet à l'IA de réaliser des tâches complexes telles que la reconnaissance d'images, la reconnaissance vocale et l'apprentissage automatique.

## Stabilité et limites

Aucun nouveau message noyau entre le début du calcul CUDA et la validation finale ; aucun Xid, Oops/panic, timeout GSP/RPC ou faute IOMMU dans cette fenêtre. SSH/SDDM répondent et GNOME conserve son PID. Les logs applicatifs montrent une génération HTTP 200, sans erreur bloquante constatée. Le taint/signature et la lacune RETHUNK documentés en 05C/05B-A ne sont pas corrigés par ce succès.

Aucun reboot, reset, retrait du Core, rescan/écriture PCIe, modification GRUB/EFI/noyau/initramfs/mitigations. Core laissé connecté. Veille, retrait à chaud, démarrage Core connecté et charge longue restent non qualifiés. Après levée de l’inhibition, la politique habituelle de veille s’applique : ne pas considérer la veille avec Core comme validée.

## Commandes utiles et retour arrière applicatif

Serveur actuel :

```bash
/home/adminjarvis/JARVIS/ollama/bin/ollama ps
/home/adminjarvis/JARVIS/ollama/bin/ollama run llama3.1:8b
nvidia-smi
```

Pour relancer ultérieurement le serveur s’il est arrêté, dans une session dédiée :

```bash
/home/adminjarvis/JARVIS/ollama/demarrer.sh
```

Retour arrière **préparé, non exécuté** : vérifier le PID actuel avec `ps -p 54006 -o pid,args` et ollama-processus.json ; s’il correspond encore au serveur installé, lui envoyer TERM (`kill 54006`) puis vérifier l’arrêt et celui de ses runners ainsi que la fermeture du port 11434. Aucun rmmod, reset GPU ou arrêt de service Intel. Une fois arrêté, renommer le répertoire JARVIS/ollama vers un nom daté libre pour sauvegarder binaires, modèles et launcher ; cela retire l’installation utilisateur sans supprimer les données. Les preuves mission05D-preuves restent conservées. Si le PID a changé, identifier le serveur par son chemin exact avant toute action ; ne pas tuer un PID recyclé. Pas de configuration APT/systemd à restaurer, pas de compte à supprimer. Conserver ~/.ollama sauf revue explicite de son contenu.

Les preuves complètes et scripts reproductibles sont dans [mission05D-preuves](mission05D-preuves/), notamment cuda-kernel.json, cuda-serie.json, inference-resultat.json, gpu-inference.json (115 échantillons), ollama-ps.json, model-show.json, ollama-serve.log, validation-finale.json et journal-noyau-final.txt.

Suite recommandée : quelques inférences supplémentaires et observation sous charge modérée, puis configuration applicative durable choisie avant Open WebUI. Aucun Open WebUI installé dans cette mission.
