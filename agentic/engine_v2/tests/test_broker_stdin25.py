import importlib.util
import os
from pathlib import Path
import sys
import unittest

broker=Path(__file__).resolve().parents[1]/'broker'
sys.path.insert(0,str(broker))
spec=importlib.util.spec_from_file_location('bridge25',broker/'host_bridge.py');bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)

class Stdin(unittest.TestCase):
    def test_nonblocking_parent_stdin_does_not_leak_to_commands(self):
        saved=os.dup(0)
        r,w=os.pipe()
        try:
            os.set_blocking(r,False);os.dup2(r,0)
            result=bridge.run([sys.executable,'-c','import os; print(os.get_blocking(0)); print(len(input()) if False else len(os.read(0,1)))'])
            self.assertEqual(result['returncode'],0)
            self.assertEqual(result['stdout'].splitlines(),['True','0'])
            self.assertFalse(os.get_blocking(0))
        finally:os.dup2(saved,0);os.close(saved);os.close(r);os.close(w)

if __name__=='__main__':unittest.main()
