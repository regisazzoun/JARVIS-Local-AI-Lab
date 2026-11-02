"""Independent validation of an integrity checkpoint; input order is irrelevant."""
import argparse
import hashlib
import json
from pathlib import Path

def validate(expected, checkpoint, events, report):
    reference={item['path']:item['sha256'] for item in expected['files']}
    if len(reference)!=len(expected['files']):raise ValueError('Duplicate reference paths')
    if set(checkpoint['done'])!=set(reference):raise ValueError('Missing or extra checkpoint entries')
    if any(checkpoint['done'][name]['sha256']!=value or not checkpoint['done'][name]['match'] for name,value in reference.items()):raise ValueError('Source integrity mismatch')
    if len(events)!=len(reference) or len({e['path'] for e in events})!=len(reference):raise ValueError('Missing or duplicated commits')
    if set(e['path'] for e in events)!=set(reference):raise ValueError('Unexpected trace paths')
    if any(not e['match'] for e in events):raise ValueError('Failed trace entry')
    canonical=hashlib.sha256(json.dumps(sorted(expected['files'],key=lambda x:x['path']),sort_keys=True).encode()).hexdigest()
    if report['actual_root_sha256']!=canonical or report['mismatches'] or report['file_count']!=len(reference):raise ValueError('Invalid aggregate report')
    return {'files':len(reference),'mismatches':0,'duplicate_commits':0,'canonical_root_sha256':canonical}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('expected');p.add_argument('checkpoint');p.add_argument('trace');p.add_argument('report');a=p.parse_args()
    print(json.dumps(validate(json.loads(Path(a.expected).read_text()),json.loads(Path(a.checkpoint).read_text()),[json.loads(x) for x in Path(a.trace).read_text().splitlines()],json.loads(Path(a.report).read_text())),indent=2))
