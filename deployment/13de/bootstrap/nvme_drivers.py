"""Embed only NVMe PCI driver dependencies, authenticated by Debian's signed Release."""
import gzip,hashlib,io,lzma,pathlib,subprocess,tarfile,urllib.request

def add(assets, stage):
    # Keep the kernel pinned to the exact payload already authenticated by the builder.
    raw=gzip.decompress((assets/'initrd.gz').read_bytes());i=0;versions=set()
    while i+110<=len(raw):
        h=raw[i:i+110];v=[int(h[6+n*8:14+n*8],16) for n in range(13)];ns=v[11];size=v[6]
        name=raw[i+110:i+110+ns-1].decode();start=(i+110+ns+3)&~3;i=(start+size+3)&~3
        if name.startswith('usr/lib/modules/') and len(name.split('/'))>3:versions.add(name.split('/')[3])
        if name=='TRAILER!!!':break
    assert len(versions)==1,'ambiguous installer kernel'
    version=versions.pop();assert version=='6.12.107+deb13-amd64','review NVMe module dependency chain for new kernel'
    rel=(assets/'Release').read_text().split('SHA256:\n')[1].split('\nSHA512:')[0]
    checks={l.split()[2]:l.split()[0] for l in rel.splitlines() if len(l.split())==3}
    path='main/debian-installer/binary-amd64/Packages.xz'
    index=urllib.request.urlopen('https://deb.debian.org/debian/dists/trixie/'+path,timeout=30).read()
    assert hashlib.sha256(index).hexdigest()==checks[path],'installer index no longer matches pinned signed Release'
    packages=[]
    for paragraph in lzma.decompress(index).decode().split('\n\n'):
        d=dict(l.split(': ',1) for l in paragraph.splitlines() if ': ' in l and not l.startswith(' '))
        if d.get('Package')=='scsi-modules-'+version+'-di':packages.append(d)
    assert len(packages)==1,'matching kernel udeb required'
    package=packages[0];data=urllib.request.urlopen('https://deb.debian.org/debian/'+package['Filename'],timeout=30).read()
    assert hashlib.sha256(data).hexdigest()==package['SHA256'],'udeb hash'
    cache=stage.parent/'authenticated-drivers';cache.mkdir();(cache/'Packages.xz').write_bytes(index)
    source=cache/'scsi-modules.udeb';source.write_bytes(data)
    archive=subprocess.run(['dpkg-deb','--fsys-tarfile',str(source)],capture_output=True,check=True).stdout
    selected={}
    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:') as tar:
        for member in tar:
            name=pathlib.PurePosixPath(member.name).name
            if name in ('nvme-auth.ko.xz','nvme-core.ko.xz','nvme.ko.xz'):
                assert member.isfile();selected[name]=lzma.decompress(tar.extractfile(member).read())
    assert len(selected)==3,'NVMe dependency chain incomplete'
    drivers=stage/'jarvis-drivers';drivers.mkdir()
    for name,data in selected.items():
        p=drivers/name.removesuffix('.xz');p.write_bytes(data)
        dependencies=subprocess.check_output(['/usr/sbin/modinfo','-F','depends',str(p)],text=True).strip().replace('_','-')
        expected={'nvme-auth.ko':'','nvme-core.ko':'nvme-auth','nvme.ko':'nvme-core'}
        assert dependencies==expected[p.name],'unexpected NVMe module dependencies'
    print('NVMe PCI drivers authenticated and embedded for',version)
