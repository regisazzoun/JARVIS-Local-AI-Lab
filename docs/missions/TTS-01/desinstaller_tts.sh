#!/bin/bash
# Désinstallation TTS-01 : supprime SEULEMENT le venv
# Préserve generated/, cache/, références/
set -e
if [ "${1:-}" = "--execute" ]; then
    rm -rf /opt/jarvis-lab/tts-01/venv
    echo "Désinstallation terminée."
else
    echo "[dry-run] Supprimerait /opt/jarvis-lab/tts-01/venv"
fi
