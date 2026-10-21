# JARVIS - Développement Skill config-repair (Mission25)

**Mission:** 4612213a05624836abec58385813439c  
**Tâche:** c_develop  
**Date:** 2026-10-21  
**Modèle utilisé:** qwen3.5:27b-q4_K_M

---

## Résumé Exécutif

Cette tâche a consisté à concevoir, développer et valider une compétence autonome `config-repair` capable de normaliser des configurations JSON en corrigeant les ports invalides vers 8091. Le skill a été créé via Skill Lab, testé avec succès, activé et exécuté réellement sur source-a.json.

---

## Sources Techniques Consultées

Deux sources Python officielles ont été consultées :

1. **Documentation json** - https://docs.python.org/3/library/json.html (evidence_id: `a6aa5dc6d1ef4b52806eaee898a480a3`)
   - Module json pour le parsing et la validation des fichiers JSON
   - Gestion des exceptions `json.JSONDecodeError` pour les JSON invalides

2. **Documentation pathlib** - https://docs.python.org/3/library/pathlib.html (evidence_id: `5cd83edbe75a4cb7826458317cb7ae8d`)
   - Classes Path pour la manipulation de chemins de fichiers
   - Méthodes `read_text()` et `write_text()` pour l'I/O

---

## Besoin et Solution

**Besoin:** Les fichiers source-a.json et source-b.json contiennent `"port": 0` (invalide). Le script doit:
- Corriger le port vers 8091 (entier)
- Conserver tous les autres champs
- Écrire de façon idempotente
- Rejeter proprement les JSON invalides (comme broken.json)

**Solution:** Script Python `/var/lib/jarvis/projects/mission25/config_repair.py` avec:
- Argumentaire CLI `argparse` (`--input`, `--output`)
- Validation JSON stricte via `json.load()` avec try/except
- Correction conditionnelle du port si != 8091
- Rapport JSON structuré en stdout

---

## Preuves d'Échec, Cause, Correction et Retest

### Échec Initial (skill_test)

**Evidence:** invocation_id `ce1d069d11a741f0b6cc489ca1fb1669`

**Erreur:** `"Parameter substitution must occupy the whole value; no shell interpolation"`

**Cause:** Le manifeste utilisait `${job_file}` dans une commande shell interpolée, ce qui est interdit. La substitution ne doit occuper qu'une valeur entière.

### Correction 1: Changement vers argv tableau

**Version:** v3.0.0 (evidence_id: `bbad9dbe4a0b46a8b71b0bbb613e613f`)

**Changement:** Remplacement de `command` par `argv` avec substitution entière:
```json
"arguments": {
  "argv": ["python3", "/var/lib/jarvis/projects/mission25/config_repair.py", "-i", "${input_file}", "-o", "${output_file}"]
}
```

### Retest Réussi

**Evidence:** `fd1683b8ac4a4319ab2e52d819733687` (skill_test)

**Résultat:** skill_test passé avec succès, stdout contient `"status": "ok"`.

---

## Vérifications Réelles

### 1. Exécution sur source-a.json

**Evidence:** `bdb3c6ab05124b029d313586a5747e95` (skill_run)

**Résultat stdout:**
```json
{
  "status": "ok",
  "message": "Port corrigé: 0 → 8091",
  "original_port": 0,
  "new_port": 8091
}
```

### 2. Vérification indépendante du fichier de sortie

**Evidence:** `7a7ba957a66f47a5af75a9ef957f598c`

**Contenu source-a-final.json:**
```json
{
  "port": 8091,
  "label": "first-operation",
  "preserve": {
    "enabled": true
  }
}
```

**Comparaison avec source-a.json original (evidence_id: `079a5bbb2e8e421ebbe5164381b7ccc9`):**
- ✅ Port corrigé: 0 → 8091
- ✅ Champ `label` conservé: "first-operation"
- ✅ Objet `preserve` conservé intact

### 3. Rejet propre de JSON invalide

**Evidence:** `c11db299579e45c89f9d7acc6b80781b` (host_exec sur broken.json)

**Résultat:**
- Code retour: 1 (erreur attendue)
- Message d'erreur structuré: `"JSON invalide: JSON invalide: Expecting value: line 1 column 10 (char 9)"`
- Pas de fichier de sortie corrompu créé

---

## Versions et Artefacts

**Skill version:** 6 (v3.0.0)  
**Sha256 manifest:** `409ca3b484ea4e5384b76dc7ec7d684653f0f2fbbbf5987577340ec16ceeb3a7`  
**Script:** `/var/lib/jarvis/projects/mission25/config_repair.py` (sha256: `53c2fc9c7385d144dde2ac06e975857cf0e2f46dda2f01f457310cc5e8be543c`)

**Artefacts créés:**
- `source-a-final.json`: résultat de skill_run
- `source-a-corrected.json`: correction initiale par host_exec
- Manifestes Skill Lab conservés dans l'historique

---

## Limites Observées

1. **Pas de traitement batch:** Le skill ne traite qu'un fichier à la fois (limitation acceptée pour cette mission)
2. **Port unique:** Seule la valeur 8091 est considérée comme valide ; autres ports non corrigés
3. **Pas de mode "dry-run":** L'exécution écrit systématiquement le fichier de sortie
4. **Validation syntaxique uniquement:** Le skill ne vérifie pas sémantiquement d'autres champs que `port`

---

## Conclusion

La compétence `config-repair` a été conçue, développée et validée avec succès. Elle normalise les configurations JSON en corrigeant les ports invalides, préserve tous les autres champs, et rejette proprement les fichiers JSON malformés. Le skill est activé et prêt à l'emploi dans le périmètre autorisé `/var/lib/jarvis/projects/mission25`.

**État:** ✅ TÂCHE COMPLÈTE - PRÊT POUR VALIDATION
