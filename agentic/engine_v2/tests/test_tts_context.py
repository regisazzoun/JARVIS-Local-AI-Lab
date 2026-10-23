import json
import unittest
from jarvis.mission_assurance import plan_view,plan_evolution_view


class LongPlanningHistory(unittest.TestCase):
    def test_long_history_keeps_current_definitions_and_originals(self):
        rows=[{'version':i+1,'reason':'historical rationale '*1000,'author':'JARVIS','sha256':str(i),'plan':{'tasks':[{'id':'task','title':'test','artifacts':['/result.json']}]}} for i in range(40)]
        class Store:
            def plans(self,ident):return rows
        store=Store();before=json.dumps(rows)
        view=plan_view(store,'mission');evolution=plan_evolution_view(store,'mission')
        self.assertEqual(len(view),40)
        self.assertEqual([row['version'] for row in view],list(range(1,41)))
        self.assertEqual(view[-1]['plan'],rows[-1]['plan'])
        self.assertTrue(all(len(row.get('reason',''))<=200 for row in view))
        self.assertEqual([row['version'] for row in evolution if 'tasks' in row],[1,39,40])
        self.assertEqual(json.dumps(rows),before)
