import json,sys
from pathlib import Path
value=json.loads(Path(sys.argv[1]).read_text())
port=value['port']
if type(port) is not int or not 1<=port<=65535:
    raise ValueError('port must be integer in 1..65535; actual='+repr(port))
print(json.dumps({'functional':True,'port':port,'label':value['label']},ensure_ascii=False))
