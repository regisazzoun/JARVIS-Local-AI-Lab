"""Apply local relay resource policy even when Qwen Code uses --bare.

Only explicit qwen-local environment variables on the exact loopback provider
activate this patch. No context, prompts, decisions or task outcomes are injected.
"""
import hashlib,json,sys
from pathlib import Path

def apply(package,backup):
    package=Path(package);backup=Path(backup)
    if json.loads((package/'package.json').read_text())['version']!='0.26.4':raise ValueError('Pinned patch requires reviewed Qwen Code0.26.4')
    path=package/'chunks/chunk-JKF3N3Y2.js';source=path.read_text();before=source
    local='argv.openaiBaseUrl==="http://127.0.0.1:8091/v1"&&process.env.JARVIS_QWEN_CONTEXT_WINDOW'
    pairs=[('generationConfig:resolvedCliConfig.generationConfig,','generationConfig:{...resolvedCliConfig.generationConfig,...('+local+'?{contextWindowSize:Math.min(32768,Math.max(1,Number(process.env.JARVIS_QWEN_CONTEXT_WINDOW)||32768)),enableCacheControl:false}:{})},'),('autoCompactThreshold:settings.context?.autoCompactThreshold,','autoCompactThreshold:('+local+'?Math.min(1,Math.max(.01,Number(process.env.JARVIS_QWEN_COMPACT_THRESHOLD)||.18)):settings.context?.autoCompactThreshold),')]
    for old,new in pairs:
        if new in source:continue
        if source.count(old)!=1:
            previous=new.replace(',enableCacheControl:false','')
            if source.count(previous)==1:source=source.replace(previous,new,1);continue
            raise ValueError('Unexpected constructor source; no file written')
        source=source.replace(old,new,1)
    if source==before:return {'already_applied':True}
    backup.mkdir(parents=True,exist_ok=True);saved=backup/path.name
    if not saved.exists():saved.write_text(before);saved.chmod(0o600)
    path.write_text(source)
    return {'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(source.encode()).hexdigest(),'scope':'Exact loopback provider with explicit qwen-local budget environment'}
if __name__=='__main__':print(json.dumps(apply(sys.argv[1],sys.argv[2]),indent=2))
