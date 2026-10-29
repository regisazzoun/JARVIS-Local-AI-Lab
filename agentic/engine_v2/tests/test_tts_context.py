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
        self.assertEqual([row['version'] for row in evolution if 'tasks_same_as' in row],[1,39,40])
        self.assertEqual(json.dumps(rows),before)

    def test_changed_history_is_preserved_and_exact_duplicates_are_referenced(self):
        from types import SimpleNamespace
        def row(version,title):
            return {'version':version,'author':'JARVIS','sha256':str(version),
                    'plan':{'tasks':[{'id':'t','title':title,'artifacts':['/x']}]}}
        rows=[row(1,'Original'),row(2,'Original'),row(3,'Changed')]
        view=plan_evolution_view(SimpleNamespace(plans=lambda _:rows),'fixture')
        self.assertEqual(view[0]['tasks'],rows[0]['plan']['tasks'])
        self.assertEqual(view[1]['tasks_same_as'],'plan_evolution version 1.tasks')
        self.assertIn('plan.tasks',view[2]['tasks_same_as'])
        self.assertEqual([r['sha256'] for r in view],['1','2','3'])

    def test_artifact_change_is_not_deduplicated_as_current(self):
        from types import SimpleNamespace
        rows=[{'version':i,'author':'JARVIS','sha256':str(i),
               'plan':{'tasks':[{'id':'t','title':'Same','artifacts':[path]}]}}
              for i,path in [(1,'/old'),(2,'/new')]]
        view=plan_evolution_view(SimpleNamespace(plans=lambda _:rows),'fixture')
        self.assertEqual(view[0]['tasks'][0]['artifacts'],['/old'])
        self.assertIn('tasks_same_as',view[1])
