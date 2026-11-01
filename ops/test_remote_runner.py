import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('remote_runner',Path(__file__).with_name('remote_runner.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class RemoteStateTests(unittest.TestCase):
    def test_completed_write_racing_systemd_exit_is_not_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r.atomic(root/'state.json',{'status':'running','failures':0})
            def exited(unit):
                r.atomic(root/'state.json',{'status':'completed','failures':0,'returncode':0})
                return {'ActiveState':'inactive','MainPID':'0'}
            with patch.object(r,'unit_info',exited):s=r.status(root,'fixture.service')
            self.assertEqual(s['status'],'completed');self.assertEqual(s['failures'],0)
    def test_lost_supervisor_counts_once(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r.atomic(root/'state.json',{'status':'running','failures':1})
            with patch.object(r,'unit_info',lambda unit:{'ActiveState':'inactive','MainPID':'0'}):
                self.assertEqual(r.status(root,'fixture.service')['failures'],2)
                self.assertEqual(r.status(root,'fixture.service')['failures'],2)

if __name__=='__main__':unittest.main()
