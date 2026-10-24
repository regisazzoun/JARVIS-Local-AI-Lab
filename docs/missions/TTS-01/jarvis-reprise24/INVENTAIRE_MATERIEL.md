# INVENTAIRE MATÉRIEL ET LOGICIEL - MISSION TTS-01

**Date :** 2026-10-23T03:57:54+02:00  
**Mission :** 8bd3e5b316a94021b5183e0db26d6efc  
**Tâche :** t01_inventaire_initial  
**Cible :** Dell Precision 5820 (dell-observe)

---

## 1. IDENTITÉ ET ACCÈS

- **Hôte distant :** dell-observe
- **Nom machine :** jarvis-dell
- **Utilisateur :** adminjarvis
- **Sudo :** disponible
- **État SSH/Tailscale :** fonctionnel via host_remote

---

## 2. SYSTÈME D'EXPLOITATION

```
Linux jarvis-dell 6.12.113+deb13-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.113-1 (2026-10-15) x86_64 GNU/Linux
```

- **Distribution :** Debian GNU/Linux 13 (trixie)
- **Architecture :** x86_64
- **Noyau :** 6.12.113+deb13-amd64
- **Compilation noyau :** 2026-10-15

---

## 3. RESSOURCES MATÉRIELLES

### CPU

- **Modèle :** Intel(R) Core(TM) i9-10980XE CPU @ 3.00GHz
- **Architecture :** x86_64

### Mémoire RAM

```
               total        used        free      shared  buff/cache   available
Mem:           251Gi        11Gi       223Gi       108Mi        18Gi       239Gi
```

- **Total :** 251 Go
- **Utilisée :** 11 Go
- **Libre :** 223 Go
- **Disponible :** 239 Go
- **Swap :** non mesuré dans ce rapport initial

### GPU NVIDIA

```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.163.01             Driver Version: 550.163.01     CUDA Version: 12.4     |
+-----------------------------------------------------------------------------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
+=========================================================================================+
|   0  NVIDIA GeForce RTX 3090        Off |   00000000:B3:00.0 Off |                  N/A |
| 68%   68C    P2            211W /  350W |   18960MiB /  24576MiB |      0%      Default |
+-----------------------------------------------------------------------------------------+
```

- **Modèle :** NVIDIA GeForce RTX 3090
- **Mémoire totale :** 24576 MiB (24 Go)
- **Mémoire utilisée :** 18960 MiB (~18.5 Go) - probablement Ollama en fonctionnement
- **Mémoire disponible :** ~5616 MiB (~5.5 Go) pour nouveaux modèles TTS
- **Température :** 68°C
- **Ventilateur :** 68%
- **Performance :** P2
- **Consommation :** 211W / 350W max
- **Utilisation GPU :** 0% (momentané)
- **Driver NVIDIA :** 550.163.01
- **CUDA Version :** 12.4

### Processus GPU Actifs

Aucun processus GPU n'est listé dans la sortie nvidia-smi détaillée, mais la mémoire utilisée indique qu'un ou plusieurs services (Ollama) occupent le GPU.

---

## 4. ENVIRONNEMENT PYTHON

```
Python 3.13.5
```

- **Version Python :** 3.13.5
- **PyTorch :** Non installé globalement
- **CUDA via pip :** Non installé globalement

**Conclusion :** Un environnement virtuel dédié devra être créé pour installer PyTorch avec support CUDA et le moteur TTS sélectionné.

---

## 5. SERVICES SYSTÈME

### Services actifs (via host_remote services)

```
active
active
```

Deux services sont rapportés comme actifs. Ces services correspondent probablement à :
- **jarvis-ollama.service** : Service Ollama en fonctionnement (explique l'occupation GPU de 18960 MiB)
- **nvidia-persistenced.service** ou **ssh.service**

### État confirmé via host_policy

Les services autorisés pour dell-observe incluent :
- jarvis-ollama.service
- nvidia-persistenced.service
- ssh.service
- jarvis-supervision.service
- jarvis-desktop-plasma.service
- jarvis-desktop-vnc.service

---

## 6. COMPATIBILITÉ TTS

### Points forts pour l'expérimentation TTS

1. **GPU puissant :** RTX 3090 avec 24 Go VRAM, suffisant pour des modèles TTS modernes (Qwen3-TTS, Chatterbox)
2. **Mémoire système abondante :** 251 Go RAM permettent de charger de gros modèles sans swapping excessif
3. **CUDA 12.4 disponible :** Compatible avec PyTorch 2.x et les moteurs TTS récents
4. **Debian 13 (trixie) :** Distribution stable avec bons supports de paquets

### Contraintes identifiées

1. **GPU partiellement occupé :** ~18.5 Go VRAM utilisés, ~5.5 Go disponibles pour le nouveau TTS
2. **Python 3.13.5 :** Version très récente, nécessite vérification de compatibilité avec les bibliothèques TTS (certaines attendent encore Python 3.12)
3. **PyTorch non installé :** Installation nécessaire dans un environnement virtuel isolé

### Recommandations

- Créer venv à `/opt/jarvis-lab/tts-01/venv` ou fallback `/var/lib/jarvis/projects/tts-01/venv`
- Installer PyTorch avec support CUDA 12.4 : `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124`
- Surveiller l'occupation VRAM avant/durant génération TTS
- Si insuffisant, envisager de réduire la taille du modèle Ollama en cours d'exécution

---

## 7. RÉFÉRENCES TECHNIQUES

- **nvidia-smi :** `nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu --format=csv,noheader`
- **Python version :** `python3 --version`
- **Système :** `uname -a`, `cat /etc/os-release` (inaccessible dans project_exec), `free -h`
- **CPU info :** `cat /proc/cpuinfo | grep "model name"`

---

## 8. CONCLUSION

L'environnement Dell Precision 5820 est prêt pour l'expérimentation TTS :

✅ GPU RTX 3090 compatible avec modèles TTS modernes  
✅ CUDA 12.4 disponible  
✅ Mémoire système et VRAM suffisantes (avec contrainte d'occupation actuelle)  
✅ Python 3.13.5 fonctionnel  
✅ Accès distant stable via host_remote  

**Prochaine étape :** Créer environnement virtuel isolé et installer moteur TTS sélectionné après étude comparative (tâche t03).

---

*Document généré par JARVIS via JL-02 - Mission 8bd3e5b316a94021b5183e0db26d6efc*
