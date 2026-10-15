#!/bin/bash
set -e
export OLLAMA_HOST=127.0.0.1:11434
export OLLAMA_MODELS=/home/adminjarvis/JARVIS/ollama/models
export OLLAMA_CONTEXT_LENGTH=8192
export OLLAMA_NUM_PARALLEL=1
export CUDA_VISIBLE_DEVICES=GPU-ae5d487a-5a70-e915-879c-71e3cb60729d
exec /home/adminjarvis/JARVIS/ollama/bin/ollama serve
