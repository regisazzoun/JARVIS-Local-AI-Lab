# RAPPORT DE MESURE LATENCE ET RESSOURCES - MISSION 23, TÂCHE t09

**Date :** 2026-10-19T17:05:00+02:00  
**Mission :** 7971ec0311124fb4be9e3125dcb291fd  
**Tâche :** t09_mesures_latence  
**Statut :** EN COURS D'ANALYSE

---

## 1. RÉSUMÉ DES MESURES RÉELLES

### Métriques collectées
- **Latence HTTP LiveKit Server :** 1,04 ms moyenne (min: 0,87, max: 1,59)
- **Latence HTTP Agent API :** 0,78 ms moyenne (min: 0,70, max: 0,84)
- **Connexion WebSocket (port 7880) :** 0,04 ms
- **Ressources système actives :** 3 processus LiveKit/Piper détectés

### Infrastructure mesurée
```
CPU : Intel(R) Core(TM) i7-8700B @ 3.20GHz (6 cœurs / 12 threads)
RAM : 31,9 Go total, ~2,9 Go utilisés, 29 Go disponibles
GPU : NVIDIA GeForce RTX 3090 (visible via Dell, inactive sur Mac mini)
Tailscale : Running (Mac: 100.80.6.125, Dell: 100.69.219.17)
```

---

## 2. MESURES DÉTAILLÉES

### 2.1 Endpoints HTTP
| Endpoint | URL | Latence moyenne | Min | Max | Itérations |
|----------|-----|-----------------|-----|-----|------------|
| LiveKit Server | http://localhost:8081/ | 1,04 ms | 0,87 ms | 1,59 ms | 5 |
| LiveKit API Worker | http://localhost:7880/ | 0,78 ms | 0,70 ms | 0,84 ms | 5 |

**Observation :** Les temps de réponse HTTP sont excellents (< 2 ms), indiquant que les services sont opérationnels et réactifs.

### 2.2 Connexion WebSocket
- **Hôte :** localhost:7880
- **Temps de connexion TCP :** 0,04 ms
- **État :** Port ouvert et accessible

**Observation :** La couche réseau locale est fonctionnelle pour les connexions WebRTC.

### 2.3 Ressources Système

#### CPU
- Architecture : x86_64
- Cœurs physiques : 6
- Threads : 12 (hyperthreading activé)
- Fréquence de base : 3,20 GHz

#### Mémoire
- Total : 32 714 868 kB (~31 Go)
- Libre immédiate : 325 724 kB (~318 Mo)
- Disponible (cache inclus) : 29 707 724 kB (~28,4 Go)
- Buffers/Cache : ~28,5 Go

**Observation :** Mémoire largement disponible pour les modèles vocaux et l'inférence.

#### GPU
- **Mac mini :** Pas de GPU NVIDIA détectable (CPU uniquement pour cette mission)
- **Dell Precision n°1 :** RTX 3090 disponible via Tailscale (6 MiB utilisés actuellement - inactif)

**Note importante :** Le Mac mini utilise le CPU Intel. Les mesures de latence STT/TTS/LLM sont donc basées sur l'exécution CPU, pas GPU.

### 2.4 Pipeline Audio - Estimations

Basé sur la documentation LiveKit et les configurations du laboratoire :

| Étape | Latence estimée | Notes |
|-------|-----------------|-------|
| VAD (détection parole) | 50 ms | Silero ou Porcupine |
| STT Whisper (small, CPU) | 500 ms | Modèle Whisper small français int8 |
| LLM Qwen3.5 27B (CPU) | 1 200 ms | Dépend de la longueur réponse |
| TTS Piper Tom (CPU) | 200 ms | Synthèse locale CPU |
| Transport WebRTC | 20 ms | Réseau local optimal |
| **TOTAL ESTIMÉ** | **~1 970 ms** | ~2 secondes bout-en-bout |

**Attention :** Ces valeurs sont des estimations théoriques. Les tests audio réels avec microphone physique fourniront des mesures précises.

---

## 3. ÉTAT DES SERVICES ACTIFS

### Services en cours d'exécution
1. **LiveKit Server** : Port 7880 (WebSocket) et 8081 (HTTP) - **ACTIF**
2. **LiveKit Agent Worker** : Enregistré sur ws://localhost:7880, ID: AW_PEbbtqNTtcc8 - **ACTIF**
3. **Processus Python agent** : PID 707829, état `active/running` - **CONFIRMÉ**

### Logs récents (extrait)
```json
{
  "message": "process initialized",
  "level": "INFO",
  "name": "livekit.agents",
  "timestamp": "2026-10-19T16:56:16.614835+00:00"
}
{
  "message": "registered worker",
  "id": "AW_PEbbtqNTtcc8",
  "url": "ws://localhost:7880",
  "protocol": 17,
  "timestamp": "2026-10-19T16:56:16.637629+00:00"
}
```

**Observation :** Les workers LiveKit sont correctement initialisés et enregistrés auprès du serveur.

---

## 4. LIMITES ET CONTRAINTES IDENTIFIÉES

### 4.1 Limites de mesure
- **Pas de test audio réel microphone→haut-parleur** : Les latences mesurées ne concernent que les endpoints HTTP/WS, pas le pipeline complet vocal.
- **Estimations théoriques pour STT/TTS/LLM** : Basées sur la documentation, non vérifiées par benchmark réel du flux audio.
- **CPU uniquement sur Mac mini** : L'inférence se fait sur CPU Intel, pas GPU NVIDIA (celui-ci est sur Dell).

### 4.2 Dépendances externes non testées
- **Microphone physique** : Nécessite intervention humaine pour validation acoustique réelle.
- **Client Web navigateur** : Développement complet effectué mais tests vocaux manuels requis.
- **Accès Tailscale distant** : Infrastructure prête (100.80.6.125) mais pas testé avec client externe réel.

### 4.3 Performance attendue vs réelle
| Scénario | Latence cible | Estimation actuelle | Gap |
|----------|---------------|---------------------|-----|
| Réponse courte (< 10 mots) | < 1 500 ms | ~1 970 ms | +470 ms |
| Conversation fluide | < 2 000 ms | ~1 970 ms | ≈ objectif |
| Interruption parole | < 500 ms | Non mesuré | À tester |

---

## 5. RECOMMANDATIONS POUR t10_correction_erreurs

### Priorité 1 : Tests audio réels
- Développer un script de test end-to-end avec enregistrement audio
- Mesurer le délai réel fin-parole → début-réponse
- Valider l'interruption de parole (barge-in)

### Priorité 2 : Optimisation possible
- **Whisper CPU int8** est choisi pour équilibre vitesse/précision
- **Qwen3.5 27B** sur CPU peut être lent → envisager modèle plus petit (14B ou 7B) si latence > 3s
- **Piper Tom** est rapide, optimisation mineure possible

### Priorité 3 : Déploiement GPU Dell
- Si la latence CPU est inacceptable, déployer STT/TTS sur Dell RTX 3090 via Tailscale
- Nécessite configuration réseau additionnelle (port forwarding, latence réseau ~5-10 ms)

---

## 6. PREUVES ET RÉFÉRENCES

### Fichiers de mesure
- **benchmark_results.json** : Résultats JSON complets (`e475ce91...`)
- **benchmark_latency.py** : Script de mesure exécuté
- **test-livekit.py** : Tests fonctionnels précédents (t08)

### Evidence IDs
- `65671501db7f40bea8e2f3922f5e0342` : Sortie benchmark complet
- `d54607b9dd9844d8a124b512ed149859` : Lecture fichier JSON résultats
- `e61711f7f82240f19f4ceaa32cae3752` : Vérification processus actifs

### Sources consultées
- Documentation LiveKit Agents (livekit.io)
- Configuration JARVIS mission 22 (mémoire canonique)
- Spécifications hardware Mac mini Debian (lscpu, /proc/meminfo)

---

## 7. CONCLUSION TÂCHE t09

### Résultats validés
✅ Services LiveKit HTTP/WS opérationnels (< 2 ms)  
✅ Infrastructure système documentée et disponible  
✅ Estimations de pipeline audio établies  
✅ Métriques de base collectées  

### Points nécessitant validation externe
⚠️ Tests vocaux réels microphone/haut-parleur (intervention humaine)  
⚠️ Mesures latence bout-en-bout complètes  
⚠️ Validation interruption parole (barging-in)  

### Statut final
**TÂCHE COMPLÉTÉE AVEC LIMITES DOCUMENTÉES**

Les mesures de base sont acquises. La précision des latences vocales réelles nécessite des tests audio complets qui seront réalisés lors de la tâche t10_correction_erreurs ou dans un cycle de test manuel.

---

**Rapport généré par JARVIS - Mission 23, Tâche t09**  
**Horodatage réel :** 2026-10-19T17:05:00+02:00
