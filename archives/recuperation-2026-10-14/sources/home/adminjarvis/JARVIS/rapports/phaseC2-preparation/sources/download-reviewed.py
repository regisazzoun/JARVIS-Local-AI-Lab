import importlib.util, json, pathlib, urllib.parse, hashlib
base=pathlib.Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location("reviewed",base/"sources/fetch-macOS-v2.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
original=m.run_query
def secure_query(url,headers,post=None,raw=False):
 u=urllib.parse.urlsplit(url)
 if not (u.hostname=="apple.com" or u.hostname.endswith(".apple.com")):
  raise RuntimeError("Non-Apple host rejected")
 scheme="http" if u.hostname=="oscdn.apple.com" else "https"
 url=urllib.parse.urlunsplit((scheme,u.netloc,u.path,u.query,u.fragment))
 return original(url,headers,post,raw)
m.run_query=secure_query
args=m.gdata(verbose=False)
session=m.get_session(args)
info=m.get_image_info(session,bid="Mac-827FAC58A8FDFA22",mlb=m.MLB_ZERO,os_type="default")
(base/"recovery").mkdir(exist_ok=True)
(base/"recovery/provenance.json").write_text(json.dumps({k:v for k,v in info.items() if k not in ["AT","CT"]},indent=2))
cnk=m.save_image(info[m.INFO_SIGN_LINK],info[m.INFO_SIGN_SESS],"BaseSystem.chunklist",str(base/"recovery"))
dmg=m.save_image(info[m.INFO_IMAGE_LINK],info[m.INFO_IMAGE_SESS],"BaseSystem.dmg",str(base/"recovery"))
with open(dmg,"rb") as f:
 for size,digest in m.verify_chunklist(cnk):
  if hashlib.sha256(f.read(size)).digest()!=digest: raise RuntimeError("Chunk hash mismatch")
 if f.read(1):raise RuntimeError("Unexpected trailing image data")
(base/"recovery/verification.txt").write_text("All chunk SHA256 hashes and Apple RSA chunklist signature verified with reviewed helper.\n")
print("Image and signed chunklist verified")
