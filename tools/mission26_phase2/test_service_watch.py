"""Software monitor checks; simulated states are not production crash evidence."""
import importlib.util
from pathlib import Path
import subprocess,tempfile,json,unittest
from unittest.mock import Mock
spec=importlib.util.spec_from_file_location('service_watch',Path(__file__).with_name('service_watch.py'))
w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
class ServiceWatchTests(unittest.TestCase):
 def test_actual_systemd_shape_parsed_without_control_commands(self):
  runner=Mock(return_value=Mock(stdout='Id=jarvis-worker.service\nLoadState=loaded\nActiveState=active\nSubState=running\nNRestarts=1\n',returncode=0))
  row=w.poll_services(['jarvis-worker.service'],runner)['jarvis-worker.service']
  self.assertEqual(row['status'],'OK');self.assertEqual(runner.call_args.args[0][1],'show')
 def test_down_service_alerts_without_waiting_for_mission_stagnation(self):
  result=w.evaluate({'jarvis-worker.service':{'status':'DOWN','NRestarts':'0'}},{},100)
  self.assertEqual(result['unavailable_units'],['jarvis-worker.service'])
 def test_native_auto_restart_gets_grace_before_escalation(self):
  row={'jarvis-worker.service':{'status':'RECOVERING','NRestarts':'1'}}
  first=w.evaluate(row,{},100);self.assertEqual(first['unavailable_units'],[])
  self.assertEqual(w.evaluate(row,first,161)['unavailable_units'],['jarvis-worker.service'])
 def test_recovery_is_distinguished_from_observed_crash_increment(self):
  first=w.evaluate({'jarvis-worker.service':{'status':'OK','NRestarts':'0'}},{},100)
  second=w.evaluate({'jarvis-worker.service':{'status':'OK','NRestarts':'1'}},first,160)
  self.assertEqual(second['status'],'OK');self.assertEqual(second['services']['jarvis-worker.service']['observed_restart_increments'],1)
  third=w.evaluate({'jarvis-worker.service':{'status':'OK','NRestarts':'0'}},second,220)
  self.assertEqual(third['services']['jarvis-worker.service']['observed_restart_increments'],1)
 def test_failed_observation_is_unknown_not_a_confirmed_crash(self):
  rows=w.poll_services(['jarvis-worker.service'],Mock(side_effect=subprocess.TimeoutExpired('systemctl',8)))
  self.assertEqual(rows['jarvis-worker.service']['status'],'UNKNOWN')
  first=w.evaluate(rows,{},100);self.assertEqual(first['unavailable_units'],[])
  self.assertEqual(w.evaluate(rows,first,161)['status'],'ATTENTION')
 def test_healthy_state_clears_old_down_period(self):
  first=w.evaluate({'jarvis-worker.service':{'status':'DOWN'}},{},100)
  second=w.evaluate({'jarvis-worker.service':{'status':'OK'}},first,160)
  self.assertIsNone(second['services']['jarvis-worker.service']['unhealthy_since']);self.assertEqual(second['unavailable_units'],[])
 def test_stale_or_absent_health_is_not_reported_healthy(self):
  with tempfile.TemporaryDirectory() as folder:
   self.assertTrue(w.read_health(folder,now=100)['monitor_stale'])
   Path(folder,'HEALTH.json').write_text(json.dumps({'checked_at':100,'status':'OK'}))
   self.assertFalse(w.read_health(folder,now=110)['monitor_stale'])
   self.assertTrue(w.read_health(folder,now=281)['monitor_stale'])
 def test_unrelated_or_shell_units_are_refused(self):
  runner=Mock()
  for name in ['ssh.service','jarvis-worker.service;reboot','jarvis-worker']:
   with self.assertRaises(ValueError):w.poll_services([name],runner)
  runner.assert_not_called()
 def main_fixture(self,root):
  from jarvis.mission_store import MissionStore
  root=Path(root);private=root/'private';private.mkdir();store=MissionStore(root/'engine');m=store.create('health software fixture','model','conv')
  registry=root/'register.json';registry.write_text(json.dumps({'tasks':[{'id':'P4','mission_id':m}]}))
  config=root/'config.json';config.write_text(json.dumps({'private':str(private),'register':str(registry),'allowed_tasks':['P4'],'allowed_mission_ids':[m],'monitor_units':['jarvis-worker.service'],'coordinator_service':'jarvis-test-coordinator.service'}))
  return private,store,m,config
 def test_health_is_persisted_before_requesting_existing_coordinator(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as root:
   private,store,m,config=self.main_fixture(root)
   def trigger(command,**kwargs):
    health=json.loads((private/'HEALTH.json').read_text());self.assertEqual(health['unavailable_units'],['jarvis-worker.service'])
    self.assertEqual(command,['sudo','-n','systemctl','start','--no-block','jarvis-test-coordinator.service'])
    return Mock(returncode=0)
   with patch.dict(w.os.environ,{'JARVIS_COORDINATOR_CONFIG':str(config)}),patch('jarvis.mission_store.MissionStore',return_value=store),patch.object(w,'poll_services',return_value={'jarvis-worker.service':{'status':'DOWN'}}),patch.object(w.subprocess,'run',side_effect=trigger) as run:
    w.main();w.main();self.assertEqual(run.call_count,1)
   self.assertTrue(any(e['kind']=='mission_service_health_observed' for e in store.events(m)))
   self.assertEqual(store.get(m)['state'],'queued')
 def test_manual_coordinator_hold_does_not_spawn_another_coordinator(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as root:
   private,store,m,config=self.main_fixture(root);(private/'MANUAL-HOLD').write_text('Software fixture')
   with patch.dict(w.os.environ,{'JARVIS_COORDINATOR_CONFIG':str(config)}),patch('jarvis.mission_store.MissionStore',return_value=store),patch.object(w,'poll_services',return_value={'jarvis-worker.service':{'status':'DOWN'}}),patch.object(w.subprocess,'run') as run:
    w.main();run.assert_not_called()
   self.assertEqual(json.loads((private/'HEALTH.json').read_text())['coordinator_trigger'],'MANUAL_COORDINATOR_ACTIVE')
 def test_idle_successful_oneshot_is_healthy_and_failed_oneshot_is_not(self):
  for active,result,expected in [('inactive','success','OK'),('activating','success','OK'),('failed','exit-code','DOWN')]:
   runner=Mock(return_value=Mock(stdout='Id=jarvis-coordinator.service\nType=oneshot\nLoadState=loaded\nActiveState='+active+'\nResult='+result+'\n',returncode=0))
   self.assertEqual(w.poll_services(['jarvis-coordinator.service'],runner)['jarvis-coordinator.service']['status'],expected)
 def test_three_failed_coordinator_starts_survive_monitor_restarts(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as root:
   private,store,m,config=self.main_fixture(root)
   with patch.dict(w.os.environ,{'JARVIS_COORDINATOR_CONFIG':str(config)}),patch('jarvis.mission_store.MissionStore',return_value=store),patch.object(w,'poll_services',return_value={'jarvis-worker.service':{'status':'DOWN'}}),patch.object(w.subprocess,'run',return_value=Mock(returncode=1)) as run:
    for i in range(4):
     w.main()
     health=json.loads((private/'HEALTH.json').read_text());health['last_trigger_at']=0;(private/'HEALTH.json').write_text(json.dumps(health))
    self.assertEqual(run.call_count,3)
   self.assertEqual(health['coordinator_trigger'],'ESCALATION_EXHAUSTED')
   self.assertTrue(any(e['kind']=='mission_health_escalation' for e in store.events(m)))
