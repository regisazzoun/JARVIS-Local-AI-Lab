import argparse,csv,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('destination');p.add_argument('--delimiter',default=',');a=p.parse_args()
with open(a.source,newline='') as f: rows=list(csv.DictReader(f,delimiter=a.delimiter))
result={'count':len(rows),'sum':sum(int(r['valeur']) for r in rows)}
Path(a.destination).write_text(json.dumps(result,sort_keys=True)+'\n')
print(json.dumps({'produced':a.destination,'result':result}))
