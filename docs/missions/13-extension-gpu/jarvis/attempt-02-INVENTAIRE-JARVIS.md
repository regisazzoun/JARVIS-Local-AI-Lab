# Inventaire GPU - Mission 13 Extension
## Récupération technique Dell Precision 5820

**Date capture :** 2026-10-23T12:19:00+02:00 (UNIX: 1792750740)  
**Source :** host_remote action `gpu_extension_inventory` sur `dell-observe`

---

## 🎯 Résultat principal : **DEUX GPU détectés**

⚠️ **ALERTE CRITIQUE :** Les deux cartes fonctionnent en PCIe Gen1 au lieu de Gen3/4 attendu. Performance gravement limitée avant qualification électrique.

| Carte | Modèle | Mémoire | Température | Puissance | Lien PCIe | Largeur |
|-------|--------|---------|-------------|-----------|-----------|---------|
| GPU0 | RTX 3090 OEM | 24576 MiB (11 MiB utilisés) | 31°C | 18.20 W | Gen1/Gen3 | x16/x16 |
| GPU1 | RTX 3090 OEM | 24576 MiB (52 MiB utilisés) | 36°C | 28.90 W | Gen1/Gen3 | x8/x16 |

**Pilote NVIDIA commun :** `550.163.01`

---

## 🖥️ Système hôte

| Élément | Valeur |
|---------|--------|
| OS | Debian GNU/Linux 13 (trixie) |
| Kernel | 6.12.113+deb13-amd64 |
| Vendor | Dell Inc. |
| Modèle | Precision 5820 Tower X-Series |
| BIOS | Dell Inc., v2.8.0, 15/01/2021 |
| CPU | Intel(R) Core(TM) i9-10980XE @ 3.00GHz (36 threads) |
| RAM Totale | 263 631 320 KiB (~251 Go) |
| RAM Disponible | 260 188 008 KiB |
| Python | 3.13.5 |

---

## 🔌 Topologie PCIe (nvidia-smi topo -m)

```
        GPU0    GPU1    CPU Affinity    NUMA Affinity
GPU0     X      SYS     0-35            0
GPU1     SYS     X       0-35            0

Legend:
  SYS = Connection traversing PCIe as well as the SMP interconnect between NUMA nodes
```

**Analyse :** Les deux GPU communiquent via l'interconnect SMP (QPI/UPI), pas de NVLink détecté. Architecture attendue pour configuration multi-GPU sans liaison directe.

---

## ⚠️ Anomalies critiques identifiées

### 1. **Négociation PCIe sous-optimale**
- **GPU0 :** `pcie.link.gen.current=1` vs `pcie.link.gen.max=3`
- **GPU1 :** `pcie.link.gen.current=1` vs `pcie.link.gen.max=3`

**Impact estimé :** Bande passante réduite de ~90% par rapport à Gen3 (8 GT/s vs 128+ MT/s attendus pour RTX 3090).

**Causes probables :**
- Câblage PCIe endommagé ou de mauvaise qualité
- Slot PCIe non correctement reconnu par le BIOS
- Configuration BIOS incorrecte (ASPM, PCIe Link State Power Management)
- Alimentation insuffisante pour négociation haute vitesse

### 2. **Largeur de bus GPU1**
- `pcie.link.width.current=8` vs `pcie.link.width.max=16`

Le second GPU négocie en x8 au lieu de x16, potentiellement dû à :
- Slot PCIe x8 physique
- Partitionnement de bande passante du chipset
- Conflit d'adresse avec le premier GPU

---

## 📊 Adressage PCI détecté (lspci)

```
0000:17:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA102 [GeForce RTX 3090] [10de:2204] (rev a1)
0000:b3:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA102 [GeForce RTX 3090] [10de:2204] (rev a1)
```

**Note :** Les adresses bus `17` et `b3` indiquent un routing PCIe complexe via plusieurs bridges.

---

## 🔍 Limites de l'observation actuelle

1.  **Version CUDA Toolkit (nvcc) :** Non mesurée (exigerait exécution binaire)
2.  **Runtime PyTorch CUDA :** Non mesuré (exigerait import module)
3.  **Qualification électrique PSU :** Impossible sans instrumentation hardware
4.  **Température en charge :** Mesures idle uniquement (31°C/36°C)
5.  **Câblage physique :** Non vérifié visuellement

---

## ✅ Prochaines étapes requises

### IMMÉDIAT (avant toute charge GPU)
1.  **⚠️ NE PAS EXÉCUTER `gpu_extension_cuda`** tant que la qualification électrique n'est pas validée
2.  Vérifier les câbles d'alimentation PCIe supplémentaires sur le second GPU
3.  Inspecter physiquement le slot PCIe du GPU1 (x8 vs x16 physique ?)
4.  Examiner la configuration BIOS :
    - Initialisation rapide désactivée ?
    - ASPM désactivé pour les slots PCIe GPU ?
    - Priorité CPU/GPU configurée correctement ?

### À VALIDER AVANT CHARGE
- [ ] Qualification électrique de l'alimentation PSU (puissance réelle disponible)
- [ ] Test de stabilité avec charge progressive sur GPU0 seul
- [ ] Mesure réelle de bande passante PCIe (nvidia-smi dmon -c 1)
- [ ] Vérification température en charge maximale

---

## 📝 Recommandations JARVIS

**État actuel :** Les deux GPU sont **techniquement reconnus** mais **non opérationnels à pleine performance**.

**Risque :** Exécution de calcul CUDA avant qualification = risque de :
- Dégradation des performances (Gen1 bottleneck)
- Instabilité thermique non détectée en idle
- Problème d'alimentation sous charge simultanée

**Action demandée à Codex :** 
```json
{
  "status": "TWO_GPUS_DETECTED_WITH_PCIE_ANOMALY",
  "gpu_count": 2,
  "pcie_gen_actual": 1,
  "pcie_gen_expected": 3,
  "risk_level": "HIGH",
  "recommendation": "QUALIFICATION_ELECTRIQUE_REQUIRED_BEFORE_LOAD"
}
```

---

## 📚 Sources

- Outil : `host_remote` action `gpu_extension_inventory` sur `dell-observe`
- Commandes internes : `nvidia-smi`, `nvidia-smi topo -m`, `lspci`, `dmidecode`, `/proc/meminfo`
- Politique d'accès : single-persistent-owner-policy (SHA256: 98b597aa...)

**Note :** Aucune donnée personnelle ou sensible ne figure dans ce rapport. Toutes les valeurs sont extraites directement des outils de diagnostic système autorisés par la politique host_policy.

---

*Généré par JARVIS - Assistant local autonome*  
*Mission : 13D-E/Extension GPU*  
*Horodatage serveur : 2026-10-23T12:18:37+02:00*