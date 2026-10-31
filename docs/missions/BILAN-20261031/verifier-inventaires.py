"""Contrôles structurels reproductibles sans accès aux machines ou aux données privées."""
from pathlib import Path
import csv,json
root=Path(__file__).resolve().parent
stats=json.loads((root/'STATISTIQUES.json').read_text())
for name,key in [('logiciels.csv','software_rows'),('composants-enfichables.csv','pluggable_components'),('applications-dell.csv','application_groups'),('developpements.csv','development_groups')]:
    rows=list(csv.DictReader((root/name).open()))
    assert len(rows)==stats[key],name
    assert len({row['id'] for row in rows})==len(rows),name
for host in ['mac','dell1','dell2']:
    data=json.loads((root/'preuves'/str(host+'.json')).read_text())
    assert data['hardware']['id']==host
    assert data['packages']
assert stats['rtx3090']==4 and stats['rtx3080']==1
assert json.loads((root/'preuves/local.json').read_text())['manual_hold'] is True
print('Inventaires cohérents ; ceci ne reçoit pas les fonctions agentiques.')
