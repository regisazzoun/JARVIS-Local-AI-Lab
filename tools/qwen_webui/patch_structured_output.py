"""Pinned Qwen Code 0.26.4 local endpoint compatibility patch; reversible.

The upstream driver gates response_format on api.openai.com. Our existing local
relay now implements that contract via Ollama format. Enable it only for the
exact loopback URL, preserving upstream behavior for every other endpoint.
"""
import hashlib,json,sys
from pathlib import Path

OLD='buildResponseFormat(request){if(!isOfficialOpenAIEndpoint(this.contentGeneratorConfig))return{};'
NEW='buildResponseFormat(request){if(!isOfficialOpenAIEndpoint(this.contentGeneratorConfig)&&this.contentGeneratorConfig.baseUrl!=="http://127.0.0.1:8091/v1")return{};'

def apply(package,backup):
    package=Path(package);backup=Path(backup)
    version=json.loads((package/'package.json').read_text())['version']
    if version!='0.26.4':raise ValueError('Review compatibility patch against installed version before applying')
    path=package/'chunks/chunk-G7EIVPEW.js';source=path.read_text()
    if NEW in source:return {'version':version,'already_applied':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if source.count(OLD)!=1:raise ValueError('Unexpected driver source; nothing changed')
    backup.mkdir(parents=True,exist_ok=True);destination=backup/path.name
    if destination.exists():raise ValueError('Backup exists for a different unpatched source; inspect before overwrite')
    destination.write_text(source);destination.chmod(0o600)
    path.write_text(source.replace(OLD,NEW,1))
    return {'version':version,'already_applied':False,'before_sha256':hashlib.sha256(source.encode()).hexdigest(),'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'scope':'responseMimeType application/json only, exact loopback relay URL only'}
if __name__=='__main__':print(json.dumps(apply(sys.argv[1],sys.argv[2]),indent=2))
