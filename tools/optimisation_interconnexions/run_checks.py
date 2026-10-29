"""Targeted regressions, separate from live model/worker receipts."""
import sys,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'agentic/engine_v2'));sys.path.insert(0,str(Path(__file__).parent))
loader=unittest.TestLoader();suite=unittest.TestSuite()
for pattern in ['test_conversation_tools_api.py','test_chat_promotion.py','test_task_context28a.py']:
 suite.addTests(loader.discover(str(root/'agentic/engine_v2/tests'),pattern=pattern))
import test_gateway
suite.addTests(loader.loadTestsFromModule(test_gateway))
r=unittest.TextTestRunner(verbosity=2).run(suite);sys.exit(not r.wasSuccessful())
