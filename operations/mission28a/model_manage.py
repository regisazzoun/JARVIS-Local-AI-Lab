#!/usr/bin/env python3
"""Bounded Ollama pull with exact-tag readback; invoked by the owner-policy broker."""
import argparse
import fcntl
import json
import shlex
import subprocess
import time
import urllib.request
from pathlib import Path


def service_url():
    raw = subprocess.check_output(['systemctl', 'show', 'jarvis-ollama-missions',
                                   '-p', 'Environment', '--value'], text=True)
    env = dict(x.split('=', 1) for x in shlex.split(raw) if '=' in x)
    base = env['OLLAMA_HOST']
    return base if base.startswith('http://') else 'http://' + base


def catalogue(base, opener=urllib.request.urlopen):
    with opener(base + '/api/tags', timeout=15) as response:
        return json.load(response)['models']


def pull(base, model, observe=lambda value: None, opener=urllib.request.urlopen,
         clock=time.monotonic, deadline_s=535):
    started = clock()
    result = {'model': model, 'verified': False, 'status': 'incomplete'}
    try:
        current = next((m for m in catalogue(base, opener) if m.get('name') == model), None)
        if current:
            result.update(status='already_present', verified=True, observed=current)
        else:
            request = urllib.request.Request(base + '/api/pull', method='POST',
                data=json.dumps({'model': model, 'stream': True}).encode(),
                headers={'Content-Type': 'application/json'})
            completed = False
            with opener(request, timeout=20) as response:
                for raw in response:
                    if clock() - started > deadline_s:
                        raise TimeoutError('Bounded pull expired; retry the same model to resume its cache')
                    event = json.loads(raw)
                    result['last_progress'] = event
                    observe(dict(result))
                    if event.get('error'):
                        raise RuntimeError(event['error'])
                    completed = event.get('status') == 'success'
            actual = next((m for m in catalogue(base, opener) if m.get('name') == model), None)
            result.update(status='success' if completed and actual else 'incomplete',
                          verified=bool(completed and actual), observed=actual)
            if not result['verified']:
                result['error'] = 'No terminal success and exact installed tag confirmed together'
    except Exception as error:
        result.update(status='incomplete', error=type(error).__name__ + ': ' + str(error))
    result['elapsed_s'] = round(clock() - started, 3)
    observe(dict(result))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True)
    args = parser.parse_args()
    # These are experiment candidates, not an arbitrary model/URL command surface.
    allowed = {'qwen3:32b-q4_K_M', 'llama3.3:70b-instruct-q4_K_M'}
    if args.model not in allowed:
        parser.error('Model outside the installed experiment contract')
    root = Path('/opt/jarvis-lab/mission28a/model-management')
    root.mkdir(mode=0o750, exist_ok=True)
    with (root / 'pull.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print(json.dumps({'verified': False, 'status': 'busy', 'model': args.model}))
            return 2
        log = root / ('pull-' + str(time.time_ns()) + '.json')
        last_write = [0]
        def observe(value):
            if time.monotonic() - last_write[0] < 1 and 'elapsed_s' not in value:
                return
            last_write[0] = time.monotonic()
            temporary = log.with_suffix('.tmp')
            temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
            temporary.replace(log)
        result = pull(service_url(), args.model, observe)
        result['progress_file'] = str(log)
        observe(result)
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result['verified'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
