# TESTS JARVIS - MISSION 23D
## Exécution des scénarios d'interruption et validation de la chaîne vocale

**Date :** 2026-10-20T17:02:43+02:00  
**Mission :** 7971ec0311124fb4be9e3125dcb291fd  
**Tâche :** m23d_02 - Exécuter les scénarios et corriger interruption  
**Statut :** EN COURS  

---

## 1. PRÉREQUIS ET ENVIRONNEMENT

### 1.1 Services vérifiés
- ✅ LiveKit Server : opérationnel sur localhost:7880
- ✅ Passerelle Codex (codex_gateway.py) : écoutant sur 127.0.0.1:8783
- ✅ Agent Python LiveKit : configuré dans /var/lib/jarvis/projects/mission23/livekit-agent/
- ✅ Page Web temporaire (index.html) : accessible via la passerelle
- ✅ Bundle LiveKit client : vendor/livekit-client.umd.js (350410 octets)

### 1.2 Configuration des seuils annoncés (Mission 23D)
| Critère | Seuil requis | Statut |
|---------|-------------|--------|
| Audio sortant actif avant injection | ≤200ms | À mesurer |
| Délai coupure stable après interruption | ≤1000ms | À mesurer |
| RMS PCM ≤20 pendant ≥500ms (coupure) | Oui | À mesurer |
| Transcription finale exacte (dimanche/dix/vingt) | ≤20s | À mesurer |
| Réponse audio reprise après transcription | ≤90s | À mesuer |
| Stop UI coupe son local | ≤250ms | À mesurer |
| Silence/bruit ne déclenche pas réponse | Non | À mesurer |

---

## 2. TEST SMOKE INITIAL

### 2.1 Commande exécutée
```bash
cd /var/lib/jarvis/projects/mission23 && \
/var/lib/jarvis/projects/mission23/livekit-agent/venv/bin/python \
/var/lib/jarvis/projects/mission23/mission23d/codex_smoke.py
```

### 2.2 Résultat
```json
{
  "actor": "Codex-test-run-by-JARVIS",
  "utc": "2026-10-20T15:07:32Z",
  "checks": {
    "page_http": true,
    "real_fixture_http": true,
    "signed_short_lived_room_token": true,
    "real_named_dispatch": true,
    "rtc_connected_real_agent_audio_track": true,
    "own_room_cleanup": true
  },
  "room": "m23d-web-8f59c66797ec",
  "ok": true
}
```

### 2.3 Analyse
✅ **TOUS LES TESTS SMOCK PASSENT**  
La chaîne complète fonctionne :
- Page HTTP accessible via la passerelle Codex
- Fixtures WAV accessibles par whitelist
- Génération de token JWT signé valide avec TTL court (600s)
- Dispatch nommé réel vers l'agent `jarvis-agent`
- Connexion RTC et réception de piste audio réelle de l'agent
- Nettoyage propre de la salle après test

**Évidence :** invocation_id `913d233080df4737a2392dbd5afb6b62`, returncode 0

---

## 3. ÉTAT DES COMPOSANTS EXISTANTS

### 3.1 Fichiers du projet mission23d
| Fichier | Taille | Description |
|---------|--------|-------------|
| codex_gateway.py | 6214 octets | Passerelle HTTP Codex (token, fixtures, test scenarios) |
| codex_capture.py | 12092 octets | Script de capture audio retour et tests barge-in |
| codex_smoke.py | 3001 octets | Test smoke validant toute la chaîne |
| index.html | 14689 octets | Page Web temporaire avec interface micro/test |
| test_interruption_23d.py | 13395 octets | Banc de test avec critères stricts Mission 23D |
| server.py | 2655 octets | Lanceur/import de codex_gateway |
| vendor/livekit-client.umd.js | 350410 octets | Bundle LiveKit client v2.4 |

### 3.2 Fichiers de l'agent livekit-agent
| Fichier | Taille | Dernière modif |
|---------|--------|----------------|
| agent.py | ? | Oct 19 15:54 |
| config.py | 2319 octets | Oct 19 14:16 |
| factories.py | 3605 octets | Oct 20 09:34 |
| llm_adapter.py | 7451 octets | Oct 19 15:33 |
| stt_adapter.py | 13435 octets | Oct 20 00:57 |
| tts_adapter.py | 6066 octets | Oct 20 09:30 |

---

## 4. ÉCARTS ET CORRECTIONS IDENTIFIÉES

### 4.1 Problème de référence CDN résolu
**Problème initial :** L'ancien index.html référençait `/dist/livekit-client.js` qui renvoyait HTTP 404.  
**Correction appliquée :** Référence mise à jour vers `/vendor/livekit-client.umd.js` avec namespace `LivekitClient`.  
**Statut :** ✅ Résolu, bundle local présent et accessible.

### 4.2 Erreur d'import livekit.agents.pipeline
**Problème détecté :**  
```
ModuleNotFoundError: No module named 'livekit.agents.pipeline'
```
**Diagnostic :** L'API LiveKit agents a évolué. Le module `pipeline` n'existe plus dans la version installée.  
**Modules disponibles (vérifiés par host_exec) :**
```python
['voice', 'vad', 'stt', 'tts', 'llm', 'job', 'cli', 'worker', ...]
```
**Action requise :** Mettre à jour `test_interruption_23d.py` et autres scripts pour utiliser l'API actuelle (`livekit.agents.voice.VoiceAssistant` au lieu de `pipeline.VoiceAssistant`).  
**Statut :** ⚠️ À corriger avant exécution des scénarios complets.

---

## 5. PROCHAINE ACTION

### 5.1 Correction immédiate
Corriger l'import dans `test_interruption_23d.py` :
- Remplacer `from livekit.agents.pipeline import VoiceAssistant` 
- Par `from livekit.agents.voice import VoiceAssistant` (ou équivalent réel)

### 5.2 Exécution des scénarios
Une fois la syntaxe corrigée, exécuter les scénarios via `codex_capture.py` ou l'interface Web :
1. **nominal** - Conversation complète sans interruption
2. **barge-early** - Interruption à 0.6s après début audio non silencieux
3. **barge-late** - Interruption tardive pendant réponse active
4. **silence** - Vérification qu'un silence ne déclenche pas d'interruption
5. **noise** - Vérification qu'un bruit synthétique sans mots ne déclenche pas

### 5.3 Mesures à capturer
- Horodatages UTC ISO8601 et temps relatif `performance.now()` 
- WAV d'entrée injecté (empreinte SHA256)
- WAV réellement reçu par le client (empreinte SHA256, durée, fréquence)
- Logs VAD, STT, états agent, interruption demandée/effective
- Comparaison attendu/réel pour chaque critère

---

## 6. LIMITES ET RÉSERVES

### 6.1 Limites techniques documentées
- ❌ Aucun micro physique testé (contexte Mac sécurisé via tunnel SSH localhost)
- ⚠️ Validation acoustique réelle impossible sans intervention humaine
- ✅ Tests automatisés avec WAV synthétiques Piper français valident la chaîne technique

### 6.2 Périmètre préservé
- ✅ Pas de modification du déploiement Dell 13D-E/14
- ✅ Pas de reset mémoire canonique
- ✅ Pas de secret Git ou identifiant privé exposé
- ✅ Autorisations 11/11B/23/24 maintenues sans validation intermédiaire

---

## 7. RÉFÉRENCES ET PREUVES

### 7.1 Évidences d'exécution
| ID Invocation | Outil | Résultat | Date UTC |
|---------------|-------|----------|----------|
| 913d233080df4737a2392dbd5afb6b62 | host_exec (smoke) | ✅ ok: true | 2026-10-20T15:07:32Z |
| ed64fcbbfd304c05968676d94fb18ac4 | host_exec (ls vendor) | ✅ bundle présent | 2026-10-20T17:02:XXZ |

### 7.2 Sources consultées
- `/var/lib/jarvis/projects/mission23/mission23d/codex_gateway.py` - Passerelle Codex
- `/var/lib/jarvis/projects/mission23/mission23d/index.html` - Page Web temporaire  
- `/var/lib/jarvis/projects/mission23/livekit-agent/agent.py` - Agent LiveKit
- `/var/lib/jarvis/projects/mission23/livekit-agent/factories.py` - Factories STT/TTS/LLM

### 7.3 Documentation de la mission
- `docs/missions/23D/INSTRUCTION-JARVIS.md` - Instructions complètes Mission 23D
- `docs/missions/23D/PLAN-ET-IMPLEMENTATION.md` - Plan validé tâche m23d_01

---

## 8. CONCLUSION INTERMÉDAIRE

**État :** La chaîne technique LiveKit est **opérationnelle et validée par smoke test**.  
**Blocage syntaxe :** L'erreur d'import `livekit.agents.pipeline` doit être corrigée avant l'exécution des scénarios complets.  
**Prochaine étape :** Correction de l'API dans les scripts de test, puis exécution réelle avec capture audio et mesures de latence.

**Verdict partiel :** ✅ Infrastructure prête, ⚠️ Scripts à corriger, 🔄 Tests en cours.

---

*Rapport généré par JARVIS - Mission 23D - Tâche m23d_02*  
*Modèle : qwen3.5:27b-q4_K_M | Date serveur : 2026-10-20T17:02:43.642188+02:00*
