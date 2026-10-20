import unittest
from jarvis.durable_cycle import debugging_state
class DebuggingCheckpointTest(unittest.TestCase):
 def test_success_resolves_same_command_but_write_does_not(self):
  def obs(i,tool,args,ok,stdout=''):
   return {'id':str(i),'created':i,'tool':tool,'arguments':args,'result':{'ok':ok,'result':{'stdout':stdout,'returncode':0 if ok else 1}}}
  rows=[obs(1,'host_exec',{'command':'python check.py'},False,'TypeError'),obs(2,'host_write_file',{'path':'/work/code.py','content':'new'},True)]
  state=debugging_state(rows);self.assertEqual(len(state['unresolved_command_failures']),1);self.assertEqual(state['latest_file_writes'][0]['path'],'/work/code.py')
  rows.append(obs(3,'host_exec',{'command':'python check.py'},True,'PASS'))
  state=debugging_state(rows);self.assertEqual(state['unresolved_command_failures'],[]);self.assertEqual(state['latest_successful_commands'][0]['invocation'],'3')
