"""Actual registry contract regression: no inference or remote execution claim."""
import json,tempfile,unittest
from pathlib import Path
from jsonschema import Draft202012Validator
from jarvis.core import Core,ROOT
from jarvis.memory import Memory
from jarvis.mission_store import MissionStore

class ExecutionContractTests(unittest.TestCase):
 def setUp(self):
  self.folder=tempfile.TemporaryDirectory();self.addCleanup(self.folder.cleanup)
  root=Path(self.folder.name);self.store=MissionStore(root)
  self.m=self.store.create('bounded audit','model','conv',spec={'distributed_authority':True,'authority_requirements':['AUDIT'],'authority_readonly_validation':True})
  config=json.loads((ROOT/'config/example.json').read_text());self.reg=Core(config,Memory(root/'memory.sqlite')).tools
  self.reg.mission_store=self.store;self.reg.context={'mission_id':self.m,'task_id':'audit'}
 def errors(self,args):return list(Draft202012Validator(self.reg.active_schema('authority_work')).iter_errors(args))
 def test_execution_without_executor_or_command_is_invalid_in_advertised_schema(self):
  args={'issue':'AUDIT','kind':'inspect','summary':'Actual observed missing fields','operation_id':'first'}
  self.assertTrue(self.errors(args));args['executor']='Dell1';self.assertTrue(self.errors(args));args['command']='';self.assertTrue(self.errors(args))
  args['command']='python3 -V';self.assertFalse(self.errors(args))
 def test_accept_still_requires_references_without_requiring_a_command(self):
  args={'issue':'AUDIT','kind':'accept','summary':'provenance','operation_id':'accept','reference':1,'source_reference':2}
  self.assertFalse(self.errors(args));args.pop('reference');self.assertTrue(self.errors(args))
 def test_owner_execution_phase_exposes_only_concrete_execution_modes(self):
  with self.store.db() as c:
   spec=json.loads(self.store.get(self.m)['spec']);spec['authority_execution_only']=True
   c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),self.m))
  args={'issue':'AUDIT','kind':'test','summary':'bounded test','operation_id':'run','executor':'Dell2','command':'python3 -V'}
  self.assertFalse(self.errors(args));args['kind']='accept';self.assertTrue(self.errors(args))
