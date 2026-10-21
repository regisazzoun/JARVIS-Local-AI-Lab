#!/usr/bin/env python3
"""JARVIS entry point using the Codex RTC measurement tool; old draft archived."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).parent/'codex_capture.py'),run_name='__main__')
