# Tâche 05 — Modification réelle du Dell par JARVIS via Ansible idempotent

**Mission :** 21  
**Date :** 2026-10-18  
**Cible :** Dell n°1 (profil `dell-observe`, IP [adresse privée masquée])  
**Action :** Déploiement idempotent de fichier de configuration de supervision  

---

## Résumé Exécutif

Mutation réelle confirmée sur le Dell n°1 via Ansible. Un fichier de configuration JSON a été déployé dans `/etc/jarvis/managed/mission21-supervision.json`. La seconde passe Ansible confirme l'idempotence avec `"changed": false`. Lecture à distance vérifiée et conforme.

**Résultat : VALIDÉ**

---

## 1. Accès et Identification

### 1.1 Vérification d'identité distante
**Preuve :** `9f8b033a5f274e48acfe0df38003c74a`  
**Résultat :**
```
TARGET_IDENTITY_OK
adminjarvis
SUDO_OK
```

### 1.2 Connexion Ansible
**Preuve :** `f35e97ee4304498e8946f37f86f13745`  
**Résultat :** Ping réussi, interpréteur Python `/usr/bin/python3.13` détecté.

---

## 2. Déploiement du Fichier de Configuration

### 2.1 Premier déploiement (création)
**Preuve :** `8b1fcaec13e243538e01d70468e8898d`  
**Résultat :** `"changed": true` — Fichier créé avec succès

Détails :
- **Destination :** `/etc/jarvis/managed/mission21-supervision.json`
- **Taille :** 141 octets
- **Checksum SHA1 :** `aea305bbc3d44cfbd0f44ff5cb5bbd0dafc22175`
- **Permissions :** `0644`, propriétaire `root:root`

### 2.2 Contenu déployé
```json
{
  "mission": "21",
  "enabled": true,
  "interval_seconds": 300,
  "description": "Configuration de supervision légère pour mission 21"
}
```

**Caractéristiques :**
- JSON valide
- `interval_seconds` : entier (300 secondes = 5 minutes)
- `enabled` : booléen true
- Non critique, ne touche aucun service actif

### 2.3 Seconde passe Ansible (idempotence)
**Preuve :** `c80fe230484f4668881acc1874785bd8`  
**Résultat :** `"changed": false` — Idempotence confirmée

Détails :
- Même checksum que le premier déploiement
- Aucun changement effectué, fichier déjà conforme
- Preuve d'idempotence du mécanisme Ansible

---

## 3. Vérification à Distance

### 3.1 Lecture directe via SSH
**Preuve :** `ce9badd500764a2cb3993af68fece7cc`  
**Résultat :** Contenu exact reçu, conforme au dépôt Ansible

```json
{
  "mission": "21",
  "enabled": true,
  "interval_seconds": 300,
  "description": "Configuration de supervision légère pour mission 21"
}
```

---

## 4. Analyse des Résultats

### 4.1 Preuve de mutation réelle
- ✅ Premier déploiement : `"changed": true` (création)
- ✅ Second déploiement : `"changed": false` (idempotence)
- ✅ Lecture distante confirme le contenu exact
- ✅ Checksum cohérent entre les trois points de contrôle

### 4.2 Localisation sécurisée
- **Chemin :** `/etc/jarvis/managed/mission21-supervision.json`
- **Zone autorisée :** `/etc/jarvis/managed` (défini dans `host_policy`)
- **Non critique :** N'affecte aucun service système, BIOS, RAID ou clé SSH

### 4.3 Reversibilité
Le fichier peut être supprimé sans impact sur les services existants :
```bash
sudo rm /etc/jarvis/managed/mission21-supervision.json
```

Ou remplacé par un contenu différent via une nouvelle passe Ansible.

---

## 5. Observations et Limites

### 5.1 Points positifs
- Accès SSH et Ansible fonctionnels sur le Dell
- Idempotence Ansible confirmée (meilleure pratique)
- Fichier placé dans emplacement autorisé par la politique
- Configuration utile pour la tâche 06 (supervision systemd)

### 5.2 Limites identifiées
- Une erreur initiale `"'content'"` est survenue lors d'une tentative intermédiaire sans le paramètre `content` requis — résolue par l'appel correct subséquent
- La vérification ne couvre pas l'utilisation future de ce fichier par un service (tâche 06)

### 5.3 Élément nouveau pour mission 21
Ce déploiement démontre la capacité opérationnelle de JARVIS à :
1. Administrer le Dell n°1 via Ansible authentifié
2. Déployer des fichiers dans un emplacement persistant autorisé
3. Vérifier l'idempotence et la lecture distante

---

## 6. Références et Preuves

| Étape | Outil | Evidence ID |
|-------|-------|-------------|
| Identité Dell | `host_remote` | `9f8b033a5f274e48acfe0df38003c74a` |
| Ping Ansible | `host_ansible` | `f35e97ee4304498e8946f37f86f13745` |
| Déploiement 1 | `host_ansible` | `8b1fcaec13e243538e01d70468e8898d` |
| Déploiement 2 | `host_ansible` | `c80fe230484f4668881acc1874785bd8` |
| Lecture distante | `host_remote` | `ce9badd500764a2cb3993af68fece7cc` |

---

## 7. Conclusion

La tâche 05 est **complètement validée**. Une mutation réelle et vérifiée a été effectuée sur le Dell n°1 via Ansible, avec preuve d'idempotence et lecture distante confirmée. Le fichier de configuration est prêt à être utilisé par la tâche 06 (supervision systemd).

**Prochaine étape :** Tâche 06 — Supervision légère systemd du Dell.
