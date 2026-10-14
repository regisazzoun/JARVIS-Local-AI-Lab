#!/bin/sh
# Lecture seule. Ne charge/decharge aucun module et ne change aucun reglage.
set -eu
python3 - <<'PY'
from pathlib import Path
import os
args=Path('/proc/cmdline').read_text().split()
expected={'intel_iommu=on','iommu=pt','pm_async=off','module_blacklist=nouveau'}
checks={
 'noyau T2 attendu':os.uname().release=='6.18.54-1-t2-trixie',
 'arguments diagnostic presents':expected.issubset(args),
 'argument de blacklist unique':sum(a.startswith('module_blacklist=') for a in args)==1,
 'Nouveau absent de sysfs':not Path('/sys/module/nouveau').exists(),
 'i915 charge':Path('/sys/module/i915').exists(),
 'GPU Intel lie a i915':Path('/sys/bus/pci/devices/0000:00:02.0/driver').resolve().name=='i915',
 'Intel boot_vga':Path('/sys/bus/pci/devices/0000:00:02.0/boot_vga').read_text().strip()=='1',
}
print('Noyau:',os.uname().release)
print('Boot ID:',Path('/proc/sys/kernel/random/boot_id').read_text().strip())
print('Cmdline:',' '.join(args))
for name,ok in checks.items():print(('OK' if ok else 'ECHEC')+': '+name)
if not all(checks.values()):raise SystemExit(2)
print('Controles locaux conformes. SSH depuis le Mac et reactivite du bureau restent a confirmer.')
PY
