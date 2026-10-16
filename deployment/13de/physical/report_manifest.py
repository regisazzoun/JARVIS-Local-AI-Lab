"""Parse read-only installer reports into UNAPPROVED manifests; no disk operations."""
if not __debug__:
    raise RuntimeError('STOP: optimized Python disables safety assertions')
import json, re, uuid

def parse(text):
    if text.count('JARVIS_IDENTITY_BEGIN\n') != 1 or text.count('JARVIS_IDENTITY_END\n') != 1:
        raise ValueError('missing/duplicate identity section')
    block = text.split('JARVIS_IDENTITY_BEGIN\n')[1].split('JARVIS_IDENTITY_END\n')[0]
    result = {'disks': []}
    for line in block.splitlines():
        parts = line.split('\t')
        if any(any(ord(c) < 32 for c in p) for p in parts): raise ValueError('control characters')
        if parts[0] == 'disk':
            if len(parts) != 6: raise ValueError('disk fields')
            _, path, serial, model, sectors, ro = parts
            if not re.fullmatch(r'/dev/nvme[0-9]+n[0-9]+', path):
                if path=='/dev/sda' and model=='SD/MMC CRW' and int(sectors)==0:
                    if result.get('excluded_empty_media'):raise ValueError('duplicate empty reader')
                    result['excluded_empty_media']=[dict(path=path,model=model,size=0)]
                    continue
                raise ValueError('unexpected non-NVMe disk')
            result['disks'].append(dict(path=path, serial=serial, model=model, size=int(sectors)*512, type='disk', ro=ro!='0'))
        else:
            if len(parts)!=2 or parts[0] not in ('vendor','product','uuid','uefi') or parts[0] in result:
                raise ValueError('identity fields')
            result[parts[0]]=parts[1]
    result['uuid']=str(uuid.UUID(result['uuid']))
    result['uefi']=result['uefi']=='true'
    from validate import validate
    validate(result,result)
    return result

if __name__ == '__main__':
    import sys, pathlib
    manifest=parse(pathlib.Path(sys.argv[1]).read_text())
    with pathlib.Path(sys.argv[2]).open('x') as f: json.dump(manifest,f,indent=2);f.write('\n')
    print('Unapproved manifest only; explicit erase authorization still required.')
