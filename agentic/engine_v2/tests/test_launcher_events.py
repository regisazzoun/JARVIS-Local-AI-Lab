import tempfile,time,unittest
from pathlib import Path
from jarvis.mission_store import MissionStore
from jarvis.launcher_api import Launcher
class LauncherEvents(unittest.TestCase):
 def test_nullable_historical_event_does_not_break_later_pages(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);store=MissionStore(root);ident=store.create('test','local','conversation')
   for index in range(151):store.event(ident,'checkpoint',actor='JARVIS-engine')
   with store.db() as c:c.execute('INSERT INTO mission_events(mission,actor,kind,created) VALUES(?,?,?,?)',(ident,'Codex','legacy-import',time.time()))
   launcher=Launcher.__new__(Launcher);launcher.root=root
   first=launcher.events(ident);second=launcher.events(ident,first['cursor'])
   event=second['events'][-1]
   self.assertEqual(event['agent'],'Codex');self.assertIsNone(event['ok'])
   self.assertGreater(second['cursor'],first['cursor'])
