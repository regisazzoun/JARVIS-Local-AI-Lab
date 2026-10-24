# RAPPORT D'EXÉCUTION TTS-01 — ÉTAPE DE LIVRAISON

**Date/Heure :** 2026-10-24T11:56:18+02:00  
**Mission :** tâche unique liée à la mission 7971ec03… (non clôturée)  
**Exécutant :** JARVIS (Codex orchestre, JARVIS exécute)  
**Système :** Debian 13 (trixie) + Dell 13D-E/14 (probe distante)

---

## FAITS PROUVÉS

### Génération GPU réussie (reçu `2d7ca821218b4bf1b62cc5a66f11488b`)
- Modèle : `qwen1.7B CustomVoice Uncle_Fu French` (chargement partagé 4,788 s)
- 3 fichiers WAV générés à 24 kHz, mono, à la suite :
  - `accueil.wav` → 6,16 s, t_gen = 11,266 s, RTF = 1,8289
  - `diagnostic.wav` → 8,24 s, t_gen = 14,391 s, RTF = 1,7464
  - `conversation.wav` → 7,60 s, t_gen = 13,388 s, RTF = 1,7616
- RTF moyen = 1,7793

### Contrôles indépendants (probe `tts_samples`, `archive_inventory`)
- Probe `tts_samples` : 3 WAV validés, aucun défaut de format
- Probe `archive_inventory` :
  - Archive ZIP valide (SHA256 `624ad5a0…`)
  - 14 fichiers WAV, 88,71175 s totales, 8 517 672 octets
  - Sample rate 48 kHz, mono, 16 bit, débit 768 kbps
  - 3 fichiers contiennent des échantillons en plein-échelle (risque de clippings mineurs)

### Transferts binaires (SHA256 validés)
| Fichier | SHA256 (vérifié) | Taille |
|--------|------------------|--------|
| accueil.wav | `322cce3a…` | 295 724 |
| diagnostic.wav | `e85f3e5a…` | 395 564 |
| conversation.wav | `544f0dc9…` | 364 844 |
| MESURES_PERFORMANCES.json | `7207cb3d…` | 2 857 |
| generate.py | `017234e1…` | 6 394 |

### Vérifications de syntaxe
- `lancer_tts.sh` et `desinstaller_tts.sh` : syntaxe bash valide (`bash -n` → 0)

### Contrôle HTTP (Chrome)
- GET `/api/launcher/artifact?path=%2Fopt%2Fjarvis-lab%2Ftts-01%2Fgenerated%2F…` → HTTP 200, MIME `audio/wav`
- Lecture Chromium terminée (ended) pour les 3 fichiers

### Erreurs observées (historique, non corrigibles ici)
- Mauvais interpréteur Python lors de premiers appels
- Mauvaise API NVIDIA initialisée (CUDA non disponible)
- Dépendance `nvidia-ml-py` absente → installée et vérifiée
- Erreur OOM après appel hors réservation (80B)

---

## LIMITES DE CE RAPPORT
- Aucune écoute physique ni jugement esthétique (contrôle automatique seulement)
- Aucune modification système n’a été apportée à cette étape (scripts validés seulement)
- Aucune installation ni génération supplémentaire (commande déjà exécutée)

---

**Source :** host_remote (evidence_id : `7041bcee…`, `a110a2e2…`)  
**Auteur :** JARVIS (exécution uniquement, Codex orchestre)
