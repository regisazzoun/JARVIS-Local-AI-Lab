#!/usr/bin/env python3
"""Compare approved manifest with live discovery; no disk writes, no approval bypass."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import json, sys, uuid, re
from discover import discover

def validate(plan, actual):
    assert plan['vendor'] == actual['vendor'] == 'Dell Inc.', 'vendor'
    assert plan['product'] == actual['product'] == 'Precision 5820 Tower', 'product'
    assert str(uuid.UUID(plan['uuid'])) == plan['uuid'] == actual['uuid'], 'UUID'
    assert actual['uefi'] is True, 'UEFI required'
    disks = plan['disks']
    assert len(disks) == 2 and len({d['serial'] for d in disks}) == 2 and len({d['path'] for d in disks}) == 2, 'two distinct disks'
    live = {d['path']: d for d in actual['disks'] if d['type'] == 'disk'}
    assert set(live) == {d['path'] for d in disks}, 'unexpected/missing disk: unplug other disks/USB before install'
    for disk in disks:
        assert re.fullmatch(r'/dev/nvme[0-9]+n[0-9]+', disk['path']), 'whole NVMe required'
        assert disk['serial'] and disk['model'], 'identity missing'
        assert 1_900_000_000_000 <= disk['size'] <= 2_100_000_000_000, 'capacity'
        for field in ('path', 'serial', 'model', 'size'):
            assert disk[field] == live[disk['path']][field], field
        assert not live[disk['path']]['ro'], 'read-only disk'
    return True

if __name__ == '__main__':
    try:
        validate(json.load(open(sys.argv[1])), discover())
        print('IDENTITY MATCH ONLY — no destructive operation authorized')
    except (AssertionError, KeyError, OSError, ValueError) as exc:
        sys.exit('STOP: ' + str(exc))
