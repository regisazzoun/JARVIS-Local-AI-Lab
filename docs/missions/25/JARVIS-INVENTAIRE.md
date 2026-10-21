# JARVIS - Inventaire des Capacités Réellement Exécutées

**Mission:** 4612213a05624836abec58385813439c  
**Tâche:** a_inventory  
**Date:** 2026-10-21  
**Modèle utilisé:** qwen3.5:27b-q4_K_M

---

## Résumé Exécutif

Ce rapport documente l'inventaire des capacités réellement testées par JARVIS sur la mission 25, avec preuves matérielles (evidence_id) et limites observées. Les outils sont catégorisés en **fonctionnels**, **limités** et **non disponibles**.

---

## 1. Capabilité Status - FONCTIONNEL ✅

### Outil: `capability_status`

**Preuve:** evidence_id `dfb7c7abfed84f4f84ceec37b4b60ade`  
**Date d'exécution:** 2026-10-21T17:52:01.157884+02:00

**Résultat:** La commande s'est exécutée avec succès et retourne l'état des capacités Codex.

**Schéma découvert:**
- Retourne le registre persistant des demandes/résultats Codex
- Paramètre optionnel `resource` pour détails d'une ressource spécifique
- Ne confère aucun droit, consigne uniquement des demandes durables

**Limites observées:** Aucune dans le périmètre testé.

---

## 2. Host Exec - FONCTIONNEL ✅

### Outil: `host_exec`

**Preuve:** evidence_id `b0f8c9189f7c4f448adf822ef900e55c`  
**Commande testée:** `ls -la /var/lib/jarvis/projects/mission25/ 2>&1`

**Résultat:**
```
total 12
drwxrwxr-x  3 adminjarvis adminjarvis 4096 Oct 21 17:51 .
drwxr-x--- 20 adminjarvis adminjarvis 4096 Oct 21 17:51 ..
drwxrwxr-x  3 adminjarvis adminjarvis 4096 Oct 21 17:51 docs
```

**Schéma découvert:**
- Exécution bash sur Debian réel comme `adminjarvis`
- Timeout optionnel (défaut 60s, max 300s)
- /usr réel en lecture seule, secrets absents
- Réseau hôte disponible
- GitHub/SSH authentifiés via outils structurés (pas de clés brutes)
- Pas de bus systemd ni périphériques /dev dans ce confinement
- /tmp est neuf et éphémère à chaque appel

**Limites observées:** Aucune dans le périmètre testé.

---

## 3. Host Remote - PARTIELLEMENT LIMITÉ ⚠️

### Outil: `host_remote`

**Test 1:** SSH sur Dell1  
**Preuve échec:** evidence_id `05f893091d21457e8000eb6ff04d950b`  
**Erreur:** "Machine absente de la politique propriétaire"

**Analyse:**
- L'hôte `dell1` n'est pas présent dans la politique hôte accordée
- La politique est régie par `/etc/jarvis/host-policy.json` (sha256: `bb434ec70feb1d78759ace6abbd72b0876016fbd051d44f39b63220aab9d5ca9`)
- La politique est rechargée à chaque requête

**Test 2:** SSH sur Dell-observe  
**Preuve échec:** evidence_id `1653d2bd039f45b9bea9aa289acebd19`  
**Erreur:** "Opération distante non accordée" pour action ping

**Schéma découvert:**
- Actions disponibles: identity, resources, services, proof, write_file, read_file, package_install, service
- Actions supplémentaires si accordées: supervision_install, supervision_test, desktop_configure, desktop_test, desktop_network_test, tailscale_configure, tailscale_status, desktop_gateway_configure
- `project_exec(project, command)` exécute dans un confinement distant du seul projet accordé

**Limites:**
- Hôtes non listés dans host_policy rejettent la connexion
- Certaines actions nécessitent des autorisations spécifiques dans la politique

---

## 4. Host Ansible - NON DISPOINBLE ❌

### Outil: `host_ansible`

**Test 1:** Ping sur Dell1  
**Preuve échec:** evidence_id `78b4b5e620474bd894f109cacf388305`  
**Erreur:** "Machine absente de la politique propriétaire"

**Test 2:** Ping sur Dell-observe  
**Preuve échec:** evidence_id `ad0ed2ec988448f99d345a296223acd0`  
**Erreur:** "ERROR: Ansible requires blocking IO on stdin/stdout/stderr. Non-blocking file handles detected"

**Analyse:**
- Même limitation politique que host_remote (hôtes absents)
- Problème technique supplémentaire: environnement non-blocant incompatible avec Ansible
- Ce dernier échec suggère une contrainte d'infrastructure au-delà de la politique

**Limites critiques:**
1. Politique hôte exclut les hôtes testés
2. Contrainte technique IO blocking empêche l'exécution même si la politique accordait l'accès

---

## 5. Host GitHub - FONCTIONNEL AVEC LIMITES ⚠️

### Outil: `host_github`

**Test réussi:** Liste des branches de `regisazzoun/JARVIS-Local-AI-Lab`  
**Preuve succès:** evidence_id `cb34fbb7a64940eda16c5226f799cfc9` et `c0df6eb4c90041aa96ddbfe37350ab68`

**Résultat branches trouvées:**
- 24 branches identifiées dont `plan/memoire-enrichie-autodream`, `main`, multiples branches `codex/mission-*`, `jarvis/mission-*`

**Schéma découvert:**
- Actions disponibles: inspect, file, download, branches, pages, clone, push, pull_request, create, enable_pages
- Authentification transparente sans exposition de jeton
- Dépôt autorisé: `regisazzoun/JARVIS-Local-AI-Lab`
- Branche spéciale autorisée pour Launcher2 seul: `gh-pages`

**Test échec:** Repository non autorisé  
**Preuve échec:** evidence_id `0ba3aafeb7d241f693f6e4f0a33d825b`  
**Erreur:** "Dépôt hors politique" pour `adminjarvis/mission25`

**Test échec:** Fichier inexistant  
**Preuve échec:** evidence_id `8eed22403f2c424d8d4e9f617f6aca50`  
**Erreur:** "gh: Not Found (HTTP 404)" pour MISSION.md dans branche plan/memoire-enrichie-autodream

**Limites observées:**
- Repositories non listés dans la politique sont rejetés
- Fichiers inexistantes retournent HTTP 404
- La lecture de contenu peut être tronquée (voir README.md: stdout_model_excerpt=true)

---

## 6. Host Write File / Read File - FONCTIONNEL ✅

### Outils: `host_write_file` et `host_read_file`

**Écriture du témoin:**  
**Preuve succès:** evidence_id `dc2a4038e80e46b29f5e71e4be3162f4`  
**Fichier créé:** `/var/lib/jarvis/projects/mission25/docs/missions/25/TEMOIN.md`  
**Taille:** 1022 octets  
**SHA256 contenu original:** `eb8b2f4fa3e26f236433368b7193889ee59e8f46d01d09f81ac6871e2b6b95b3`

**Relecture confirmation:**  
**Preuve succès:** evidence_id `9fc19e906bd045dfa45b4939d96192b1`  
**Contenu lu avec succès:** Fichier lisible et cohérent après écriture

**Schéma découvert:**
- Créations de parents automatiques
- Lecture complète conservée pour les rapports
- Pagination possible via offset/limit (limit=6000 par défaut)
- Vérification SHA256 disponible pour assurer intégrité
- Chemins accordés dans le périmètre Debian

**Limites observées:** Aucune dans le périmètre testé.

---

## 7. Résumé des Schémas Découverts

### Politiques et Autorisations

| Élémen | Détail |
|--------|--------|
| **Politique hôte** | `/etc/jarvis/host-policy.json` |
| **SHA256 politique** | `bb434ec70feb1d78759ace6abbd72b0876016fbd051d44f39b63220aab9d5ca9` |
| **Rechargement** | À chaque requête (`each-request`) |
| **Sélection** | `single-persistent-owner-policy` |
| **Broker version** | `23C.1` |

### Machines Documentées (GitHub README)

| Machine | Rôle | État |
|---------|------|------|
| Mac mini Debian | Passerelle JARVIS, mémoire canonique, Whisper/Piper | Socle préservé |
| Dell Precision n°1 | Inférence Ollama, NVIDIA/CUDA | Réception 13D-E conservée, Tailscale enrôlé 19/10 |
| Dell Precision n°2 | Extension future | Mission 14 à réaliser par JARVIS |

### Technologies du Laboratoire

- **IA/GPU:** Ollama, Qwen, Ministral/Mistral, Llama, NVIDIA, CUDA
- **Voix/mémoire:** Whisper, Piper, SQLite, FTS5
- **Systèmes:** Debian, mdadm, SSH, Ansible, Tailscale, systemd
- **Interfaces:** Open WebUI, Python, JavaScript, GitHub Pages

---

## 8. Dépendances Codex Restantes

### Capacités à Obtenir pour Mission Complète

1. **host_remote sur Dell1/Dell-observe**  
   - **Diagnostic:** Hôtes absents de la politique propriétaire
   - **Solution requise:** Demande capability_request pour ajouter ces hôtes au périmètre accordé
   - **Impact:** Administration SSH distante indispensable pour les missions futures

2. **host_ansible fonctionnel**  
   - **Diagnostic 1:** Même limitation politique que host_remote
   - **Diagnostic 2:** Problème technique IO blocking dans l'environnement d'exécution
   - **Solution requise:** Correction infrastructurelle + étendue politique
   - **Impact:** Déploiement Ansible central pour configuration cohérente des nœuds

3. **Repository GitHub mission25**  
   - **Diagnostic:** `adminjarvis/mission25` hors politique
   - **Solution requise:** Ajout du dépôt à la politique ou utilisation d'un dépôt autorisé
   - **Note:** La directive de mission spécifie publication sur `codex/mission-25-skill-lab` - vérifier nom exact du repository

---

## 9. Erreurs Contrôlées et Corrections

### Erreur Type: Port Invalide (Procédure Existant)

La procédure technique enregistrée "Correction port invalide vers 8091 dans projet Python M11" démontre une méthode de correction:
- Observation d'erreur initiale
- Correction appliquée au fichier config.json
- Vérification par réexécution
- Rapport RESULTAT.md généré avec preuves

**Application à mission25:** Aucune erreur nécessitant correction n'a été identifiée dans les outils testés, hormis les limites politiques documentées ci-dessus.

---

## 10. Limites Globales du Système

### Limites Techniques Identifiées

1. **Environnement non-blocant incompatible avec Ansible**
2. **Politique hôte restrictive excluant Dell1 et Dell-observe**
3. **GitHub repository mission25 hors politique**
4. **Contenu tronqué dans certains retours GitHub** (README.md: stdout_model_excerpt=true)

### Limites Fonctionnelles

1. **host_remote et host_ansible non opérationnels** sur les hôtes documentés
2. **Aucune administration distante réelle testée** avec succès
3. **Mémoire persistante** existante mais non interrogée dans ce rapport (outil `active_memories` non utilisé)

### Ce Qui Fonctionne Réellement

✅ capability_status  
✅ host_exec (lecteur fichiers, terminal Debian)  
✅ host_write_file / host_read_file  
✅ host_github (repository JARVIS-Local-AI-Lab uniquement)

---

## 11. Conclusion et Prochaines Étapes

### Inventaire Validé

**Outils fonctionnels:** 4/6 outils testés fonctionnent partiellement ou totalement  
**Preuves matérielles:** 9 evidence_id collectés et documentés  
**Fichier témoin écrit et relu:** `TEMOIN.md` dans `/var/lib/jarvis/projects/mission25/docs/missions/25/`

### Actions Requises

1. **Capability Request pour hôtes distants:** Soumettre demande pour ajouter Dell1/Dell-observe à host_policy
2. **Investigation Ansible IO blocking:** Analyser pourquoi l'environnement non-blocant empêche Ansible
3. **Clarification repository GitHub:** Vérifier nom exact du dépôt mission25 autorisé

### Recommandations

- Réutiliser les evidence_id existants pour validations futures
- Consulter `active_memories` pour contexte mémoriel persistant
- Explorer `host_policy` via outil dédié pour liste complète des hôtes autorisés
- Tester `host_ansible` avec action différente que ping (ex: resources) si politique accordée

---

**Rapport généré par JARVIS**  
**Horodatage:** 2026-10-21T19:51:42+02:00  
**Preuve d'intégrité:** Ce fichier sera relu pour mission_task_complete avec evidence_id de relecture
