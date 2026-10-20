"""Read-only attachment test. Execute on the host; no fallback authority or credentials."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jarvis.host_client import request, BrokerError


def main():
    try:
        response = request('capability_status', {})
        print(json.dumps({'actor': 'Codex-preflight', 'ok': True,
                          'policy_identity': response['result'].get('policy_identity'),
                          'evidence_id': response.get('evidence_id'),
                          'caller': response.get('caller')}, ensure_ascii=False))
        return 0
    except BrokerError as exc:
        print(json.dumps({'actor': 'Codex-preflight', **exc.response}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
