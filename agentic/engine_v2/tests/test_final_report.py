import unittest
from jarvis.tools import validate_final_report

class FinalReportTest(unittest.TestCase):
 def test_stale_report_rejected_before_write_or_publication(self):
  spec={'final_report_contract':{'required':['7/7','Running','259200'],'forbidden':['6 tâches sur 7']}}
  with self.assertRaises(ValueError):validate_final_report('Rapport partiel : 6 tâches sur 7, NeedsLogin',spec)
  validate_final_report('7/7 reçues, Running, 259200 octets. Historique : NeedsLogin.',spec)
 def test_existing_missions_without_contract_still_supported(self):
  validate_final_report('Rapport existant',{})
