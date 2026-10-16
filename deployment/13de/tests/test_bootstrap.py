import base64,copy,hashlib,importlib.util,json,os,pathlib,runpy,subprocess,sys,tempfile,time,unittest
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'physical'))
from report_manifest import parse
spec=importlib.util.spec_from_file_location('build_install',ROOT/'bootstrap/build-install.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class Bootstrap(unittest.TestCase):
 def report(self):
  return 'JARVIS_IDENTITY_BEGIN\nvendor\tDell Inc.\nproduct\tPrecision 5820 Tower\nuuid\t12345678-1234-1234-1234-123456789abc\nuefi\ttrue\ndisk\t/dev/nvme0n1\tA\tNVMe\t3906250000\t0\ndisk\t/dev/nvme1n1\tB\tNVMe\t3906250000\t0\nJARVIS_IDENTITY_END\n'
 def test_manifest_real_fields(self):
  self.assertEqual(parse(self.report())['disks'][0]['size'],2000000000000)
 def test_manifest_refuses_duplicates_extra_disk_legacy_and_unknown_product(self):
  for old,new in [('\tB\t','\tA\t'),('/dev/nvme1n1','/dev/nvme0n1'),('uefi\ttrue','uefi\tfalse'),('Precision 5820 Tower','Other Dell'),('/dev/nvme1n1','/dev/sda')]:
   with self.subTest(new=new), self.assertRaises((ValueError,AssertionError)):parse(self.report().replace(old,new))
 def test_erase_approval_is_bound_and_expiring(self):
  raw=json.dumps(parse(self.report())).encode();recipe=b'recipe';h=builder.digest
  payload={n:h((ROOT/'bootstrap'/n).read_bytes()) for n in ('install-bootstrap.sh','finalize-efi.sh','sync-esp.sh','verify-storage.py')}
  payload['guard-physical.sh']=h((ROOT/'debian/guard-physical.sh').read_bytes())
  a=dict(installation_authorized=True,manifest_sha256=h(raw),recipe_sha256=h(recipe),base_initrd_sha256='base',serials=['A','B'],raid_efi_qualified=True,lan_exposure_reviewed=True,expires_at=int(time.time())+60,payload_sha256=payload)
  builder.check_approval(a,raw,recipe,'base')
  for field,value in [('installation_authorized',False),('raid_efi_qualified',False),('lan_exposure_reviewed',False),('serials',['A','C']),('manifest_sha256','bad'),('expires_at',0)]:
   with self.subTest(field=field),self.assertRaises(AssertionError):builder.check_approval(dict(a,**{field:value}),raw,recipe,'base')
  with self.assertRaises(AssertionError):builder.check_approval(a,raw,b'changed recipe','base')
 def takeover(self,fail_new_key=False,authorized=True):
  with tempfile.TemporaryDirectory() as temp:
   b=pathlib.Path(temp);manifest=parse(self.report());(b/'manifest').write_text(json.dumps(manifest));(b/'id').write_text('fixture');(b/'password').write_text('fixture-secret');(b/'password').chmod(0o600)
   pub='ssh-ed25519 '+base64.b64encode(b'fixture-public-key').decode()
   settings=dict(host='192.0.2.2',approved_addresses=['192.0.2.2'],manifest=str(b/'manifest'),identity_file=str(b/'id'),password_file=str(b/'password'),host_public_key=pub,authorized_public_key_sha256=hashlib.sha256(b'fixture-public-key').hexdigest(),host_key_origin='reviewed-authenticated-installation-report',administration_authorized=authorized)
   (b/'settings').write_text(json.dumps(settings));calls=[];installed=False
   def remote(cmd,**kw):
    nonlocal installed
    calls.append(cmd);user=cmd[-2];action=cmd[-1]
    if 'jarvisadmin@' in user and (not installed or fail_new_key):raise subprocess.CalledProcessError(255,cmd)
    if 'base64 -d | sudo' in action:installed=True
    if 'passwd -S' in action:out='jarvis-bootstrap L x\npasswordauthentication no\n'
    elif 'product_uuid' in action:out=json.dumps(dict(sys_vendor=manifest['vendor'],product_name=manifest['product'],product_uuid=manifest['uuid']))
    else:out=''
    return subprocess.CompletedProcess(cmd,0,out,'')
   with patch.object(sys,'argv',['takeover',str(b/'settings')]),patch('subprocess.check_output',return_value=pub),patch('subprocess.run',side_effect=remote):
    if fail_new_key or not authorized:
     with self.assertRaises((subprocess.CalledProcessError,AssertionError)):runpy.run_path(str(ROOT/'bootstrap/takeover.py'),run_name='__main__')
     self.assertTrue((b/'password').exists());self.assertFalse(any('jarvis-revoke-bootstrap' in c[-1] for c in calls))
    else:
     runpy.run_path(str(ROOT/'bootstrap/takeover.py'),run_name='__main__')
     revoke=next(i for i,c in enumerate(calls) if 'jarvis-revoke-bootstrap' in c[-1])
     self.assertIn('PreferredAuthentications=publickey',calls[revoke-1]);self.assertIn('ControlMaster=no',calls[revoke-1]);self.assertFalse((b/'password').exists())
     self.assertTrue((b/'takeover-complete.json').exists())
 def test_no_revocation_before_independent_key_success(self):self.takeover(fail_new_key=True)
 def test_takeover_and_secret_cleanup(self):self.takeover()
 def test_administration_authorization_required(self):self.takeover(authorized=False)
