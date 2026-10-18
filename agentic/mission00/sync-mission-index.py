#!/usr/bin/env python3
"""Check or update README's mission catalogue from registry IDs and SUIVI rows."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / 'docs/missions/00-Mission-Pilotage-point-26-10-17'
START = '<!-- BEGIN MISSION CATALOGUE -->'
END = '<!-- END MISSION CATALOGUE -->'
EXCLUDED = {'09 à 11', 'Documentation'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Update the README catalogue')
    args = parser.parse_args()
    current = ROOT / 'docs/missions/REGISTRE-MISSIONS.json'
    registry = json.loads((current if current.exists() else REPORTS / 'REGISTRE-MISSIONS.json').read_text())
    identifiers = [r['identifiant'] for r in registry]
    if len(set(identifiers)) != len(identifiers):
        raise SystemExit('Duplicate identifier in registry')
    suivi = (ROOT / 'SUIVI.md').read_text()
    overview = suivi.split('## Vue d\'ensemble — toutes les missions\n', 1)[1].split('\n## ', 1)[0]
    rows = {}
    for line in overview.splitlines():
        if not line.startswith('| **'):
            continue
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line)[1:-1]]
        identifier = cells[0].strip('* ')
        if identifier in rows:
            raise SystemExit('Duplicate SUIVI row: ' + identifier)
        if len(cells) != 5:
            raise SystemExit('Unexpected SUIVI table columns: ' + identifier)
        rows[identifier] = cells
    missing = sorted(set(identifiers) - rows.keys())
    extra = sorted(rows.keys() - set(identifiers) - EXCLUDED)
    if missing or extra:
        raise SystemExit(json.dumps({'missing_in_suivi': missing, 'unregistered_rows': extra}))
    count = len(identifiers)
    lines = [START, f'## Catalogue des missions — {count} identifiants', '',
             f'**{count} missions et sous-missions recensées**, dont dix incréments 15A/15B prévus, non exécutés. '
             'Cette liste reprend exactement les identifiants, intitulés et états du tableau courant de [SUIVI.md](SUIVI.md). '
             'Les lignes « 09 à 11 » (regroupement historique) et « Documentation » (activité transversale) '
             'ne sont pas des missions supplémentaires et ne sont pas comptées.', '',
             '| Mission | Objet / étapes | État |', '| --- | --- | --- |']
    lines.extend('| ' + ' | '.join(rows[i][:3]) + ' |' for i in identifiers)
    lines += ['', 'Catalogue synchronisé avec `python3 agentic/mission00/sync-mission-index.py --write`. '
              'Sans option, la commande vérifie la concordance ligne par ligne.', END]
    block = '\n'.join(lines)
    path = ROOT / 'README.md'
    readme = path.read_text()
    if (START in readme) != (END in readme):
        raise SystemExit('Incomplete README catalogue markers')
    if START in readme:
        old = readme[readme.index(START):readme.index(END) + len(END)]
        expected = readme.replace(old, block, 1)
    else:
        if not args.write or '## Accéder aux résultats' not in readme:
            raise SystemExit('README mission catalogue is missing')
        expected = readme.replace('## Accéder aux résultats', block + '\n\n## Accéder aux résultats', 1)
    if args.write:
        path.write_text(expected)
    elif readme != expected:
        raise SystemExit('README catalogue differs; run with --write after reviewing SUIVI')
    print(json.dumps({'registry': count, 'readme': count, 'suivi_counted': count,
                      'suivi_table_rows': len(rows), 'excluded_group_rows': sorted(EXCLUDED),
                      'identifiers_names_states_equal': True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
