import argparse,json,os
from pathlib import Path
from .memory import Memory
ap=argparse.ArgumentParser();ap.add_argument('action',choices=['backup','restore-test','export']);ap.add_argument('source');ap.add_argument('destination');a=ap.parse_args();os.umask(0o077)
if Path(a.destination).exists():raise SystemExit('Destination existante refusée')
if a.action=='restore-test':Memory.restore(a.source,a.destination)
elif a.action=='backup':Memory(a.source).backup(a.destination)
else:Path(a.destination).write_text(json.dumps(Memory(a.source).export(),ensure_ascii=False,indent=2))
