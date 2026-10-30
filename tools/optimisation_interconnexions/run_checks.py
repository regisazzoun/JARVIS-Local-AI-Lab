"""Targeted regressions, separate from live model/worker receipts."""
import sys,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'agentic/engine_v2'));sys.path.insert(0,str(Path(__file__).parent))
loader=unittest.TestLoader();suite=unittest.TestSuite()
for pattern in ['test_conversation_tools_api.py','test_chat_promotion.py','test_task_context28a.py','test_operational_policy.py','test_report_plan_step.py','test_mission_context_budget.py','test_planning_recovery.py','test_attempt_ledger.py','test_legacy_attempts.py','test_worker_recovery.py','test_report_claims.py']:
 suite.addTests(loader.discover(str(root/'agentic/engine_v2/tests'),pattern=pattern))
sys.path.insert(0,str(root/'agentic/engine_v2/tests'))
for name in ['test_editorial_failure_survives_technical_pass_and_store_reopen','test_independent_findings_survive_later_different_editorial_failure']:
 suite.addTests(loader.loadTestsFromName('test_mission_engine26b.AssuranceTests.'+name))
import importlib.util
for filename in ['test_gateway.py','test_protocol.py']:
 spec=importlib.util.spec_from_file_location('gateway_checks_'+filename[:-3],Path(__file__).parent/filename)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 suite.addTests(loader.loadTestsFromModule(module))
r=unittest.TextTestRunner(verbosity=2).run(suite);sys.exit(not r.wasSuccessful())
