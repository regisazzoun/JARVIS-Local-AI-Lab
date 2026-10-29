import unittest
from prices import total_cents
class Prices(unittest.TestCase):
    def test_empty(self): self.assertEqual(total_cents([]),0)
    def test_sum(self): self.assertEqual(total_cents([125,275]),400)
    def test_input_unchanged(self):
        p=[125,275];total_cents(p);self.assertEqual(p,[125,275])
if __name__=='__main__':unittest.main()
