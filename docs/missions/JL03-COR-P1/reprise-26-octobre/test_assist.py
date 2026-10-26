import importlib.util,unittest
from pathlib import Path
p=str(Path(__file__).with_name('jl03_assist.py'));sp=importlib.util.spec_from_file_location('assist',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Store:
 def get(self,ident):return {"state":"running"}
 def tasks(self,ident):return [{'id':'D03','state':'running'}]
 def contract_status(self,*args):return {'all_satisfied':False}
class R:
 context={'mission_id':'16087a18f86d42b7b79296bc93b3a754','task_id':'D03'}
 mission_store=Store()
 def __init__(self):self.specs={}
class Checks(unittest.TestCase):
 def test_wrong_mission_rejected(self):
  r=R();r.context={'mission_id':'other','task_id':'D03'}
  with self.assertRaises(ValueError):m.scope(r)
 def test_other_d04_validated_task_not_writable(self):
  r=R();r.context={'mission_id':'4b96e63671e1458ba93300a0e7980e2f','task_id':'D04'}
  with self.assertRaises(ValueError):m.scope(r)
 def test_finish_is_not_force(self):self.assertEqual(m.finish(R())['returncode'],1)
 def test_tools_have_no_arguments(self):
  r=R();m.register(r);self.assertEqual(len(r.specs),6)
  for spec in r.specs.values():self.assertEqual(spec[1],{});self.assertEqual(spec[2],[])
 def test_repair_forbidden_outside_d17(self):
  with self.assertRaises(ValueError):m.repair(R())
 def test_interrupted_scope_blocks_next_action(self):
  r=R();r.mission_store=Store();r.mission_store.get=lambda ident:{'state':'interrupted'}
  with self.assertRaises(ValueError):m.scope(r)
 def test_protocol_stops_at_first_failure(self):
  previous=m.native;called=[]
  try:
   def fake(reg,name,args):
    called.append(name);return {'invocation':'observed','result':{'ok':False}}
   m.native=fake;result=m.protocol(R())
   self.assertEqual(result['returncode'],1);self.assertEqual(called,['jl03_candidate_check'])
  finally:m.native=previous
 def test_protocol_preserves_order_of_verification_and_finish(self):
  previous=m.native;called=[]
  try:
   def fake(reg,name,args):
    called.append(name);return {'invocation':'observed','result':{'ok':True}}
   m.native=fake;self.assertEqual(m.protocol(R())['returncode'],0)
   self.assertEqual(called,['jl03_candidate_check','jl03_write_fact_report','jl03_verify_report','jl03_finish_checked_task'])
  finally:m.native=previous
if __name__=='__main__':unittest.main()
