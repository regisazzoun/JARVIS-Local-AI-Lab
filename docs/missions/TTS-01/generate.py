#!/opt/jarvis-lab/tts-01/venv/bin/python3
# -*- coding: utf-8 -*-
"""
Script de génération TTS avec Qwen3-TTS-12Hz-1.7B-CustomVoice
Production: accueil.wav, diagnostic.wav, conversation.wav + MESURES_PERFORMANCES.json
Corrections: pynvml pour GPU util, mesures avant/apres correctes, valeurs brutes sans round
"""

import os
import json
import time
import torch
import soundfile as sf
import pynvml

os.environ['HOME'] = '/opt/jarvis-lab/tts-01'
os.environ['HF_HOME'] = '/opt/jarvis-lab/tts-01/.cache/huggingface'

from qwen_tts import Qwen3TTSModel

GENERATED_DIR = "/opt/jarvis-lab/tts-01/generated"
MESURES_PATH = os.path.join(GENERATED_DIR, "MESURES_PERFORMANCES.json")
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
SPEAKER = "Uncle_Fu"

# Création répertoire generated si inexistant
os.makedirs(GENERATED_DIR, exist_ok=True)

# Textes exacts (apostrophes ASCII)
PHRASES = [
    "Bonsoir monsieur. Tous les systèmes sont opérationnels. Je suis prêt à recevoir vos instructions.",
    "L'analyse du serveur est terminée. Le processeur graphique fonctionne normalement et les services de communication sont disponibles.",
    "J'ai examiné votre demande. Plusieurs solutions sont envisageables. Souhaitez-vous que je vous présente celle qui me paraît la plus efficace ?"
]

FICHIERS = ["accueil.wav", "diagnostic.wav", "conversation.wav"]

def init_nvml():
    """Initialise pynvml"""
    try:
        pynvml.nvmlInit()
        return True
    except Exception as e:
        print(f"Erreur NVML: {e}", flush=True)
        return False

def shutdown_nvml():
    """Ferme pynvml"""
    try:
        pynvml.nvmlShutdown()
    except:
        pass

def measure_gpu():
    """Mesure GPU via pynvml (utilisé MB, total MB, util_pct)"""
    if not torch.cuda.is_available():
        return {"used_MB": None, "total_MB": None, "util_pct": None}
    
    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        
        mem_used_MB = info.used / 1024 / 1024
        total_MB = info.total / 1024 / 1024
        
        # Utilisation GPU en % (compute)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        util_pct = util.gpu  # Pourcentage d'utilisation GPU
        
        return {"used_MB": mem_used_MB, "total_MB": total_MB, "util_pct": util_pct}
    except Exception as e:
        print(f"Erreur mesure GPU: {e}", flush=True)
        return {"used_MB": None, "total_MB": None, "util_pct": None}

def measure_ram():
    """Mesure RAM via /proc/meminfo"""
    try:
        with open("/proc/meminfo", "r") as f:
            data = {}
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0].rstrip(":")
                    val_kb = int(parts[1])
                    data[key] = val_kb
            
            total_kb = data.get("MemTotal", 0)
            avail_kb = data.get("MemAvailable", 0)
            used_kb = total_kb - avail_kb
            
            return {
                "used_MB": used_kb / 1024,
                "total_MB": total_kb / 1024,
                "util_pct": (100 * used_kb / total_kb) if total_kb else None
            }
    except Exception as e:
        print(f"Erreur mesure RAM: {e}", flush=True)
        return {"used_MB": None, "total_MB": None, "util_pct": None}

def main():
    # Initialisation NVML
    if not init_nvml():
        print("NVML non disponible, mesures GPU limitées", flush=True)
    
    print("Initialisation du modèle...", flush=True)
    
    load_start = time.time()
    model = Qwen3TTSModel.from_pretrained(
        MODEL_ID,
        device_map="cuda:0",
        dtype=torch.bfloat16,
        attn_implementation="eager"
    )
    torch.cuda.synchronize()  # Sync avant chrono fin
    load_time = time.time() - load_start
    
    print(f"Chargement du modèle: {load_time}s (brut)", flush=True)

    # Version du paquet
    try:
        import importlib.metadata
        ENGINE_VERSION = importlib.metadata.version("qwen-tts")
    except Exception:
        ENGINE_VERSION = "unknown"

    samples = []
    success = True

    for i, (phrase, fichier) in enumerate(zip(PHRASES, FICHIERS)):
        print(f"\nGénération {i+1}/3: {fichier}", flush=True)
        path_wav = os.path.join(GENERATED_DIR, fichier)
        
        # MESURES AVANT (brutes, sans round)
        gpu_before = measure_gpu()
        ram_before = measure_ram()
        
        t_start = time.time()

        # Appel GPU
        audio_arrays, rate_hz = model.generate_custom_voice(
            text=phrase,
            language="French",
            speaker=SPEAKER,
            instruct="Calm, mature, professional delivery."
        )
        
        torch.cuda.synchronize()  # Sync après génération
        
        # Écriture WAV
        sf.write(path_wav, audio_arrays[0], rate_hz)

        t_gen = time.time() - t_start

        # MESURES APRÈS (brutes, sans round)
        gpu_after = measure_gpu()
        ram_after = measure_ram()

        # Durée audio brute
        duree_audio_s = len(audio_arrays[0]) / rate_hz

        # RTF brut
        rtf = t_gen / duree_audio_s if duree_audio_s > 0 else None

        sample = {
            "text": phrase,
            "file": fichier,
            "speaker": SPEAKER,
            "model_id": MODEL_ID,
            "engine_version": ENGINE_VERSION,
            "t_gen_s": t_gen,           # BRUT sans round
            "load_time_s": load_time,   # BRUT sans round
            "duree_audio_s": duree_audio_s,  # BRUT sans round
            "rtf": rtf,                 # BRUT sans round
            "gpu_before": gpu_before,
            "gpu_after": gpu_after,
            "ram_before": ram_before,
            "ram_after": ram_after
        }
        samples.append(sample)
        
        print(f"  Généré: {path_wav} (t_gen={t_gen}s, RTF={rtf}, duree={duree_audio_s}s)", flush=True)

    # Arrêt NVML
    shutdown_nvml()

    # Écriture mesures (objet {samples:[...]}, PAS tableau racine)
    # VALEURS BRUTES SANS ROUND
    mesures = {"samples": samples}
    
    with open(MESURES_PATH, "w", encoding="utf-8") as f:
        json.dump(mesures, f, indent=2, ensure_ascii=False)

    print(f"\nRapport mesures: {MESURES_PATH}", flush=True)
    print(f"Success: {success}", flush=True)

if __name__ == "__main__":
    main()