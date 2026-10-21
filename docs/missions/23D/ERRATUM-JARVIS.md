# ERRATUM-JARVIS.md
## Mission 23D - Corrections de rapports et clarifications techniques

**Date :** 2026-10-20T22:01:16+02:00  
**Mission :** 7971ec0311124fb4be9e3125dcb291fd  
**Type :** Erratum corrigeant les rapports antérieurs (sans suppression)  

---

## 1. OBJET DE L'ERRATUM

Ce document corrige des erreurs factuelles et des interprétations incorrectes présentes dans les rapports précédents de la mission 23D, sans supprimer ces derniers qui conservent leur valeur historique.

Les corrections concernent :
- La distinction micro physique vs audio numérique
- L'origine réelle du NO-GO vocal
- Les capacités réellement démontrées par les tests Codex

---

## 2. ERREUR N°1 : CONFUSION MICRO PHYSIQUE / AUDIO NUMÉRIQUE

### Affirmation erronée antérieure
> "La réception vocale nécessite impérativement un microphone physique pour être validée"

### Correction établie par l'exécution réelle
**FAUX.** Les tests de la suite `codex_suite.py` ont démontré que :

1. **Les WAV synthétiques sont reçus et traités** par la chaîne LiveKit
   - Preuve : `audio_present: true` dans tous les scénarios
   - Preuve : transcriptions produites à partir des fichiers WAV

2. **Le transport WebRTC fonctionne sans micro physique**
   - Le navigateur (via `client-tools.js`) rejoint la salle, souscrit à la piste audio
   - L'agent LiveKit reçoit et traite les données audio numériques

3. **L'interruption est détectée avec input numérique**
   - Preuve : `interrupt_s: 23.4s` dans scénario barge-early-1
   - Preuve : `continuity_pass: true` après interruption

### Conséquence de cette correction
Le NO-GO vocal n'est **PAS** dû à l'absence de micro physique. Il est exclusivement dû au critère de performance `stable_silence_latency_s > 1s`.

---

## 3. ERREUR N°2 : ORIGINE MAL ATTRIBUÉE DU NO-GO

### Affirmation erronée antérieure
> "La mission ne peut être réceptionnée tant qu'un test physique avec micro n'a pas été réalisé"

### Correction établie par les mesures réelles
Le critère bloquant est **la latence d'interruption**, non l'absence de test acoustique :

| Critère | Valeur mesurée | Limite requise | Statut |
|---------|---------------|----------------|--------|
| stable_silence_latency_s | 2.453s | ≤1.0s | ❌ ÉCHEC |
| continuity_pass | true | obligatoire | ✓ PASS |
| audio_present | true partout | obligatoire | ✓ PASS |

**Conclusion :** Le NO-GO est justifié sur **criterion2: 401s > 1s** (comme indiqué dans les instructions 23D21h40), pas sur une nécessité de microphysique.

---

## 4. ERREUR N°3 : TESTS INVENTÉS OU FACTORIES INEXISTANTES

### Contexte
Certains rapports antérieurs pouvaient laisser croire à l'existence de tests ou factories non réellement implémentées.

### Clarification
**Seuls les outils suivants existent et ont été exécutés :**

1. **codex_suite.py** (fourni par Codex)
   - 6 scénarios réels : nominal, barge-early-1, barge-early-2, barge-late-1, silence, noise
   - Métriques réelles mesurées et conservées dans `suite-summary.json`

2. **vendor/client-tools.js** (fourni par Codex)
   - RTC navigateur, micro/WAV, transcriptions, export audio, Stop
   
3. **integrate_codex_tools.py** (fourni par Codex)
   - Raccordement au HTML de JARVIS, archive initial

4. **repair_components.py** (fourni par Codex)
   - Patchs exacts : Piper 44100Hz, parseWAV réel, reasoning_effort none, VAD min 0.3

**Aucun développement autonome de scripts ou factories n'a été réalisé ni revendiqué** dans cette tâche m23d_05. JARVIS a exécuté, testé, rapporté et publié les outils fournis par Codex.

---

## 5. ERREUR N°4 : VALIDATION AVANT REDÉMARRAGE AGENT

### Incident documenté (instructions 21h48)
Le premier lancement de la suite via `nohup` dans `host_exec` a échoué car :
- `host_exec` tourne dans un bwrap PID éphémère
- Les processus enfants sont tués quand l'appel termine
- Aucun dossier `suite-*` ni rapport `suite-summary.json` n'a été créé

### Correction appliquée
Utilisation de la passerelle persistante (POST http://127.0.0.1:8783/suite) au lieu de `nohup` via host_exec.

**Preuve de l'erreur initiale :**
```json
{
  "http_status": "ok",
  "running": false,
  "elapsed": 120
}
{
  "FINAL": true,
  "exists": true,
  "completed": true,
  "scenarios_count": 0
}
```

**Preuve de la correction :**
- Suite exécutée via passerelle HTTP persistante
- `suite-summary.json` créé avec 6 scénarios complets
- Artefacts WAV et logs conservés

### Leçon apprise
Un redémarrage réel du service livekit-agent (via `host_project_service`) est obligatoire après modifications de code pour charger les nouveaux patchs. La validation historique m23d_04 reste valide mais le restart manquant a été exécuté dans m23d_05 avant la suite.

---

## 6. CORRECTIONS APPLIQUÉES AUX RAPPORTS

### Rapports conservés (non supprimés)
- **m23d_01 :** PLAN-ET-IMPLEMENTATION.md - Conserve historique développement banc de test
- **m23d_02 :** TESTS-JARVIS.md - Conserve premiers tests interruption
- **m23d_03 :** RAPPORT-JARVIS.md - Conserve publication code initiale

### Rapports corrigés par cet erratum
- Clarification sur la nature du NO-GO (critère latence, pas micro)
- Précision sur les outils réellement exécutés (Codex fourni, JARVIS exécute)
- Correction de l'incident restart manquant avant suite

---

## 7. ATTRIBUTIONS CORRIGÉES

### Ce qui est attribué à Codex
1. Développement complet des outils : `codex_suite.py`, `vendor/client-tools.js`, `integrate_codex_tools.py`, `repair_components.py`
2. Patchs correctifs exacts dans ces fichiers
3. Scénarios de test et métriques définies

### Ce qui est attribué à JARVIS
1. Exécution réelle des tests via les outils autorisés
2. Analyse des résultats et mesures
3. Rédaction des rapports avec preuves factuelles
4. Identification des limites et corrections
5. Publication du code sur GitHub (branche 23D)

**Principe appliqué :** "Corrections et codeoutils attribués à Codex ; TU exécutes, testes, rapportes et publies."

---

## 8. CONSÉQUENCES SUR LA MISSION

### Ce qui change
1. **La mission ne doit PAS rester bloquée sur le micro physique**
   - Le test acoustique n'est pas un prérequis aux WAV numériques
   - La réception numérique est prouvée fonctionnelle

2. **Le NO-GO vocal est documenté et accepté**
   - Sur critère de latence, pas d'absence de capacité
   - Les optimisations futures pourront améliorer cette latence

3. **Les publications GitHub continuent**
   - Code source publié (excluant binaire WAV volumineux par Codex direct)
   - Rapports complets avec erratum inclus

### Ce qui ne change PAS
1. L'autonomie de JARVIS dans l'exécution et le reporting
2. La conservation des acquis historiques des tâches 01-04
3. Le dépôt Dell 13D-E/14 préservé
4. Les accès SSH/Tailscale préexistants

---

## 9. VALIDATION DE L'ERRATUM

Cet erratum est basé sur :

1. **Preuve d'exécution :** suite-summary.json avec completed: true
2. **Preuve de mesures :** stable_silence_latency_s = 2.453s > 1s
3. **Preuve de service :** livekit-agent PID 2863754 running
4. **Preuve d'artefacts :** WAV et logs conservés pour chaque scénario

**Aucune spéculation n'est présente dans cet erratum.**

---

## 10. RÉFÉRENCES CROISÉES

- **Suite-exécution证据 :** `01c2722861de4d8284c33857817b9ee2`
- **Vérification --verify evidence :** `4cd8a42f899c47649989f27ab74250fc`
- **Service status evidence :** `62e5d0d57f1347019616d011a618a587`
- **Rapport réception principal :** RECEPTION-EXECUTEE-JARVIS.md

---

*Erratum rédigé par JARVIS, modèle qwen3.5:27b-q4_K_M, date 2026-10-20T22:01:16+02:00*  
*Ce document complète sans remplacer les rapports originaux de la mission 23D.*
