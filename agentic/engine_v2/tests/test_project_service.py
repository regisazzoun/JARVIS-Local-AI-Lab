import importlib.util,unittest,tempfile
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'broker/project_service.py';s=importlib.util.spec_from_file_location('project_service',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class ProjectServiceTest(unittest.TestCase):
 def test_same_sandbox_identity_and_no_unit_injection(self):
  with tempfile.TemporaryDirectory() as t:
   cfg={'user':'adminjarvis','write_roots':[t],'project_services':{'mission23':t}}
   a={'project':'mission23','name':'probe','action':'install','argv':['/usr/bin/python3','-c','print("$HOME %x")']}
   unit,body=m.definition(a,cfg,lambda command,cfg:['/usr/bin/bwrap','--clearenv','--',command])
   self.assertEqual(unit,'jarvis-mission23-probe.service');self.assertIn('User=adminjarvis',body);self.assertIn('/usr/bin/bwrap',body);self.assertIn('$$HOME %%x',body)
   with self.assertRaises(ValueError):m.definition({**a,'name':'bad\nUser=root'},cfg,lambda *a:[])
   with self.assertRaises(PermissionError):m.definition({**a,'project':'other'},cfg,lambda *a:[])
   with self.assertRaises(PermissionError):m.definition({**a,'argv':['/usr/bin/sudo']},cfg,lambda *a:[])
 def test_readonly_repository_policy_does_not_grant_write(self):
  source=p.parent/'host_bridge.py';spec=importlib.util.spec_from_file_location('bridge_test',source);bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
  cfg={'repositories':['owner/project'],'read_repositories':['livekit/agents'],'user':'adminjarvis'}
  seen=[]
  bridge.run=lambda *args,**kw:seen.append(args) or {'returncode':0,'stdout':'{}'}
  result=bridge.execute('host_github',{'repository':'livekit/agents','action':'file','path':'README.md'},cfg)
  self.assertEqual(result['returncode'],0);self.assertEqual(len(seen),1)
  with self.assertRaises(PermissionError):bridge.execute('host_github',{'repository':'livekit/agents','action':'push'},cfg)
  self.assertEqual(len(seen),1)
