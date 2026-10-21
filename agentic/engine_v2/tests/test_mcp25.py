"""Real official-SDK stdio roundtrip against installed adapter, no mocks."""
import asyncio
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from jarvis.mcp_gateway import client

class MCP(unittest.TestCase):
    def test_real_discovery_and_parameter_error(self):
        listed=asyncio.run(client('list',None,{}))
        self.assertEqual(listed['transport'],'stdio')
        names={t['name'] for t in listed['tools']}
        self.assertIn('skill_run',names);self.assertIn('host_service',names)
        self.assertNotIn('mcp_tools',names)
        response=asyncio.run(client('call','host_service',{'service':42}))
        self.assertTrue(response['isError']);self.assertEqual(response['returncode'],1)
        self.assertTrue(response['responses'])


class Promotion(unittest.TestCase):
    def test_mcp_and_skill_mutations_are_deferred_before_effect(self):
        import json,tempfile
        from unittest.mock import Mock
        from jarvis.core import Core,ROOT
        from jarvis.memory import Memory
        from jarvis.missions import Missions
        cases=[('skill_run',{'name':'sample','parameters':'{}'}),('mcp_tools',{'action':'call','name':'host_remote','arguments':'{"action":"write_file","host":"dell-observe","path":"/tmp/test","content":"x"}'})]
        for tool,args in cases:
            with self.subTest(tool=tool),tempfile.TemporaryDirectory() as temp:
                root=Path(temp);memory=Memory(root/'runtime/memory.sqlite');config=json.loads((ROOT/'config/example.json').read_text());config['voice_summary']=False
                responses=iter([{'role':'assistant','content':'','tool_calls':[{'function':{'name':tool,'arguments':args}}]}])
                core=Core(config,memory,lambda p:next(responses));missions=Missions(core,root,start_worker=False)
                forbidden=Mock(side_effect=AssertionError('Effect must be deferred'))
                old=core.tools.specs[tool];core.tools.specs[tool]=(*old[:4],forbidden)
                result=core.chat('Execute the authorized test',config['default_model'])
                self.assertTrue(result['mission_id']);forbidden.assert_not_called()

if __name__=='__main__':unittest.main()
