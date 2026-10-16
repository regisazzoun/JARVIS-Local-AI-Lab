#!/usr/bin/env python3
"""Build reviewed installation candidate; old fail-closed builder remains unchanged.
Only an explicit, hash-bound local approval enables partman confirmations.
"""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import argparse,copy,datetime,gzip,hashlib,json,os,pathlib,subprocess,sys,tempfile,secrets
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'physical'))
from validate import validate

def digest(data):return hashlib.sha256(data).hexdigest()
def check_approval(approval, manifest, recipe, base_hash):
    assert approval['installation_authorized'] is True,'explicit installation authorization absent'
    assert approval['manifest_sha256']==digest(manifest),'manifest approval mismatch'
    assert approval['recipe_sha256']==digest(recipe),'recipe approval mismatch'
    assert approval['base_initrd_sha256']==base_hash,'base initrd mismatch'
    plan=json.loads(manifest)
    assert sorted(approval['serials'])==sorted(d['serial'] for d in plan['disks']),'approved serials'
    assert approval['raid_efi_qualified'] is True,'RAID/dual ESP recipe unqualified'
    assert approval['lan_exposure_reviewed'] is True,'bootstrap capability/hash LAN exposure not reviewed'
    for name in ('install-bootstrap.sh','finalize-efi.sh','sync-esp.sh','verify-storage.py'):
        assert approval['payload_sha256'][name]==digest((ROOT/'bootstrap'/name).read_bytes()), 'payload approval mismatch'
    assert approval['payload_sha256']['guard-physical.sh']==digest((ROOT/'debian/guard-physical.sh').read_bytes()), 'guard approval mismatch'
    assert int(approval['expires_at'])>int(datetime.datetime.now(datetime.timezone.utc).timestamp()),'approval expired'

def main():
    p=argparse.ArgumentParser();p.add_argument('manifest',type=pathlib.Path);p.add_argument('secret_directory',type=pathlib.Path);p.add_argument('discovery_session',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);p.add_argument('--approval',type=pathlib.Path);a=p.parse_args()
    os.umask(0o077)
    raw=a.manifest.read_bytes();manifest=json.loads(raw);live=copy.deepcopy(manifest);live['uefi']=True
    for disk in live['disks']:disk.update(type='disk',ro=False)
    validate(manifest,live)
    for disk in manifest['disks']:
        for field in ('path','model','serial'):assert not any(c in disk[field] for c in '\r\n\t'),'manifest delimiter'
        assert disk['size']%512==0
    base=a.discovery_session/'initrd.gz' # Verified discovery base; contains no disk-write path by itself.
    # Obtain the original VERIFIED Debian initrd, not the discovery archive (whose early_command blocks).
    settings=json.loads((a.discovery_session/'receiver.json').read_text())
    assets=ROOT/'private/debian-verified'
    subprocess.run(['gpgv','--keyring','/usr/share/keyrings/debian-archive-keyring.gpg',str(assets/'Release.gpg'),str(assets/'Release')],check=True)
    sums=(assets/'SHA256SUMS').read_bytes();release=(assets/'Release').read_text().split('SHA256:\n')[1].split('\nSHA512:')[0]
    assert any(l.split()[-1:]==['main/installer-amd64/current/images/SHA256SUMS'] and l.split()[0]==digest(sums) for l in release.splitlines())
    entries={l.split(maxsplit=1)[1].lstrip('*./'):l.split()[0] for l in sums.decode().splitlines()}
    for name in ('linux','initrd.gz'):assert digest((assets/name).read_bytes())==entries['netboot/debian-installer/amd64/'+name]
    base_bytes=(assets/'initrd.gz').read_bytes()
    recipe=(ROOT/'debian/preseed-bootstrap.candidate.cfg').read_bytes()
    approval=json.loads(a.approval.read_text()) if a.approval else None
    if approval:check_approval(approval,raw,recipe,digest(base_bytes))
    hashed=(a.secret_directory/'password.sha512').read_text().strip()
    assert hashed.startswith('$6$') and not any(c in hashed for c in '\r\n\t '),'SHA512 password hash'
    cfg=recipe.decode().replace('@PASSWORD_HASH@',hashed).replace('@DISK_A@',manifest['disks'][0]['path']).replace('@DISK_B@',manifest['disks'][1]['path'])
    with tempfile.TemporaryDirectory() as temp:
        stage=pathlib.Path(temp)/'stage';stage.mkdir()
        from nvme_drivers import add
        add(assets,stage)
        (stage/'load-nvme.sh').write_text('set -eu\nfor n in nvme-auth nvme-core nvme; do\n module=$(printf %s "$n" | tr "-" "_")\n test -d "/sys/module/$module" || insmod /jarvis-drivers/$n.ko\ndone\nudevadm settle\n/bin/sh /guard-physical.sh || { echo STOP-JARVIS-identity-or-approval; while :; do sleep 3600; done; }\n')
        cfg+='\nd-i preseed/early_command string /bin/sh /load-nvme.sh\n'
        (stage/'preseed.cfg').write_text(cfg)
        (stage/'approved.json').write_bytes(raw)
        rows=['uuid\t'+manifest['uuid'],'product\t'+manifest['product']]
        for d in manifest['disks']:rows.append('\t'.join(['disk',pathlib.Path(d['path']).name,d['serial'],d['model'],str(d['size']//512)]))
        for media in manifest.get('excluded_empty_media',[]):rows.append('\t'.join(['empty-media',pathlib.Path(media['path']).name,media['model'],'0']))
        tsv='\n'.join(rows)+'\n';(stage/'approved.tsv').write_text(tsv)
        for n in ('install-bootstrap.sh','finalize-efi.sh','sync-esp.sh','verify-storage.py'):(stage/n).write_bytes((ROOT/'bootstrap'/n).read_bytes())
        (stage/'guard-physical.sh').write_bytes((ROOT/'debian/guard-physical.sh').read_bytes())
        callback_key=secrets.token_hex(24)
        collector=(ROOT/'discovery/collect.sh').read_text()
        for k,v in dict(BASE='http://192.168.1.99:8090',KEY=callback_key,HOST='192.168.1.99',PORT='8090').items():collector=collector.replace('@'+k+'@',v)
        (stage/'jarvis-collect.sh').write_text(collector)
        event='#!/bin/sh\n# Progress only, no passwords. Failure must not block an otherwise safe install.\nwget --no-proxy -q -T 5 -t 1 -O /tmp/jarvis-event-ack --post-data="$1" http://192.168.1.99:8090/'+callback_key+'/event >/dev/null 2>&1 || :\n'
        (stage/'jarvis-event.sh').write_text(event)
        expiry=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=24)
        (stage/'bootstrap-expires').write_text(expiry.strftime('%Y-%m-%d %H:%M:%S UTC')+'\n')
        if approval:
            (stage/'approved-erase.sha256').write_text(digest(tsv.encode())+'\n')
            with (stage/'preseed.cfg').open('a') as f:
                f.write('\nd-i partman-md/confirm boolean true\nd-i partman-md/confirm_nooverwrite boolean true\nd-i partman-md/device_remove_md boolean true\nd-i partman-lvm/device_remove_lvm boolean true\nd-i partman/confirm_write_new_label boolean true\nd-i partman/choose_partition select finish\nd-i partman/confirm boolean true\nd-i partman/confirm_nooverwrite boolean true\n')
            if approval.get('reboot_authorized') is True:(stage/'approved-reboot').write_text(digest(raw)+'\n')
        names='\n'.join(sorted(str(p.relative_to(stage)) for p in stage.rglob('*')))+'\n'
        archive=subprocess.run(['cpio','-o','-H','newc','--reproducible'],cwd=stage,input=names.encode(),capture_output=True,check=True).stdout
        with a.output.open('xb') as f:f.write(base_bytes);f.write(gzip.compress(archive,mtime=0))
    callback=dict(lifetime=28800,bind='192.168.1.99',port=8090,source='192.168.1.0/24',key=callback_key,script=str(a.output.resolve())+'.collect.sh',output=str(a.output.resolve())+'.firstboot-report.txt')
    with pathlib.Path(str(a.output)+'.collect.sh').open('x') as f:f.write(collector)
    with pathlib.Path(str(a.output)+'.receiver.json').open('x') as f:json.dump(callback,f,indent=2);f.write('\n')
    print('Install artifact:',a.output,'explicit erase enabled:',bool(approval),'reboot enabled:',bool(approval and approval.get('reboot_authorized')))

if __name__=='__main__':main()
