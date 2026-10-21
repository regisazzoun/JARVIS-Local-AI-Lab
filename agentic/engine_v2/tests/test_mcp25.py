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

if __name__=='__main__':unittest.main()
