"""Software schema fixtures only; no claim of real P2 scenario coverage."""
import json, unittest
from types import SimpleNamespace
from jsonschema import Draft202012Validator
from jarvis.tools import Registry
from jarvis.distributed_authority import register

P2='3aa717f3887e49daa7daf7e883ee52e4'
class AcceptSchemaTests(unittest.TestCase):
 def schema(self,mission=P2):
  reg=Registry.__new__(Registry);reg.specs={};reg.context={'mission_id':mission}
  reg.mission_store=SimpleNamespace(get=lambda _: {'spec':json.dumps({'authority_requirements':['P2']})})
  register(reg)
  return reg.active_schema('authority_work')
 def test_accept_requires_both_distinct_fields(self):
  validate=Draft202012Validator(self.schema())
  base={'issue':'P2','kind':'accept','operation_id':'fixture','summary':'fixture'}
  for missing in ({},{'reference':43535},{'source_reference':43535}):
   self.assertTrue(list(validate.iter_errors(base|missing)))
  self.assertFalse(list(validate.iter_errors(base|{'reference':43535,'source_reference':43353})))
 def test_execution_does_not_require_acceptance_fields(self):
  args={'issue':'P2','kind':'test','operation_id':'fixture','summary':'fixture','executor':'Dell2','command':'true'}
  self.assertFalse(list(Draft202012Validator(self.schema()).iter_errors(args)))
 def test_other_missions_unchanged(self):
  self.assertNotIn('allOf',self.schema('unrelated-software-fixture'))
if __name__=='__main__':unittest.main()
