#!/usr/bin/env python3
"""JARVIS idle worker. OFF by default; opt-in with --execute.

No shell, no automatic network changes, no GPU work. Jobs use argv arrays.
Job must be checkpoint-aware and safely resumable. Linux only.
"""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time

STOP = False

def stop(_sig, _frame):
    global STOP
    STOP = True

def cpu_idle():
    with open("/proc/stat", encoding="utf-8") as f:
        parts = list(map(int, f.readline().split()[1:]))
    return sum(parts), parts[3] + parts[4]

def mem_available_fraction():
    vals = {}
    with open("/proc/meminfo", encoding="utf-8") as f:
        for line in f:
            name, rest = line.split(":", 1)
            vals[name] = int(rest.strip().split()[0])
    return vals["MemAvailable"] / vals["MemTotal"]

def gpu_available(cfg):
    """Fail closed if NVIDIA telemetry is unavailable or GPU/VRAM is busy."""
    if not cfg.get("require_nvidia_gpu", True):
        return True
    try:
        p = subprocess.run(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5, check=True,
        )
        rows = [list(map(int, line.split(","))) for line in p.stdout.strip().splitlines()]
        if not rows:
            return False
        return all(util <= cfg["max_gpu_utilization_percent"] and
                   used / max(1, total) <= cfg["max_vram_used_fraction"]
                   for util, used, total in rows)
    except (OSError, subprocess.SubprocessError, ValueError, KeyError):
        return False


def eligible(cfg):
    a, idle_a = cpu_idle()
    time.sleep(cfg["sample_seconds"])
    b, idle_b = cpu_idle()
    idle = (idle_b - idle_a) / max(1, b - a)
    return idle >= cfg["min_cpu_idle_fraction"] and mem_available_fraction() >= cfg["min_mem_available_fraction"] and gpu_available(cfg)

def write_state(path, state):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(tmp, path)

def run(cfg, execute):
    state_path = Path(cfg["state_path"]).expanduser()
    if execute:
        state_path.parent.mkdir(parents=True, exist_ok=True)
    state = {"status": "disabled", "completed": [], "attempts": {}}
    if state_path.exists():
        state.update(json.loads(state_path.read_text(encoding="utf-8")))
    if not execute:
        print("DRY RUN ONLY: no job executed, no state changed.")
        print(json.dumps({"job_count": len(cfg["jobs"]), "state": state}, indent=2))
        return
    if not cfg.get("enabled", False):
        print("Disabled in configuration; no jobs run.")
        return
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    while not STOP:
        if not eligible(cfg):
            time.sleep(cfg["poll_seconds"])
            continue
        pending = next((j for j in cfg["jobs"] if j["id"] not in state["completed"] and state["attempts"].get(j["id"], 0) < 3), None)
        if not pending:
            break
        ident = pending["id"]
        state["status"] = "running"
        state["current"] = ident
        state["attempts"][ident] = state["attempts"].get(ident, 0) + 1
        write_state(state_path, state)
        # Jobs are single short units; a long job must support its own checkpoint.
        proc = subprocess.Popen(pending["argv"], start_new_session=True)
        started = time.monotonic()
        interrupted = False
        while proc.poll() is None:
            if STOP or time.monotonic() - started > cfg["max_job_seconds"] or not eligible(cfg):
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
                interrupted = True
                break
        if not interrupted and proc.returncode == 0:
            state["completed"].append(ident)
            state["status"] = "completed"
        elif interrupted:
            # Do not count preemption as a failed attempt.
            state["attempts"][ident] -= 1
            state["status"] = "paused"
        else:
            state["status"] = "failed"
        write_state(state_path, state)
        if STOP:
            break
        time.sleep(cfg["poll_seconds"])

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--execute", action="store_true", help="opt in to execution; config must also have enabled=true")
    args = p.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    run(cfg, args.execute)

if __name__ == "__main__":
    main()
