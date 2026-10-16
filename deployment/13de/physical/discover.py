#!/usr/bin/env python3
"""Read-only discovery. Run from Debian live on the Dell, never installs anything."""
import json, pathlib, subprocess

def discover():
    def dmi(name):
        return pathlib.Path('/sys/class/dmi/id', name).read_text().strip()
    data = json.loads(subprocess.check_output(['lsblk', '-bJd', '-o', 'PATH,TYPE,MODEL,SERIAL,SIZE,TRAN,RO']))
    return dict(vendor=dmi('sys_vendor'), product=dmi('product_name'), uuid=dmi('product_uuid'),
                uefi=pathlib.Path('/sys/firmware/efi').is_dir(), disks=data['blockdevices'])

if __name__ == '__main__':
    print(json.dumps(discover(), indent=2))
