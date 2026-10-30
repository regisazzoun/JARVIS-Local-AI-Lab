import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from jarvis.client_capabilities import Capabilities

class FakeRegistry:
    context={}
    def execute(self,name,args):return {'ok':True,'tool':name,'result':args}

class ClientTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.api=Capabilities(Path(self.tmp.name),config={'test':True})
        self.schema=patch.object(Capabilities,'schema',return_value={});self.schema.start();self.addCleanup(self.schema.stop)
        self.registry=patch.object(Capabilities,'registry',return_value=FakeRegistry());self.registry.start();self.addCleanup(self.registry.stop)
    def test_idempotency_survives_new_client(self):
        first=self.api.call('host_exec',{'command':'fixture'},'same')
        other=Capabilities(self.api.root,config={'test':True})
        with patch.object(FakeRegistry,'execute',side_effect=AssertionError('duplicate dispatch')):
            cached=other.call('host_exec',{'command':'fixture'},'same')
        self.assertEqual(first['result'],cached['result']);self.assertTrue(cached['client_receipt']['cached'])
        with self.assertRaises(ValueError):other.call('host_exec',{'command':'different'},'same')
    def test_unknown_dispatch_never_repeated(self):
        with patch.object(FakeRegistry,'execute',side_effect=RuntimeError('lost result')):
            with self.assertRaises(RuntimeError):self.api.call('host_exec',{},'unknown')
        other=Capabilities(self.api.root,config={'test':True})
        self.assertEqual(other.call('host_exec',{},'unknown')['client_receipt']['state'],'UNKNOWN')
        with self.assertRaises(ValueError):other.call('host_exec',{'changed':True},'unknown')
    def test_large_result_original_archived_and_pageable(self):
        result=self.api.call('host_exec',{'large':'é'*9000},'large')
        self.assertIn('explicit_excerpt',result['result'])
        ident=result['client_receipt']['audit_id'];offset=0;raw=b''
        # ASCII-only encoded envelope is not assumed; byte windows have explicit sizes.
        with self.api.memory.connect() as c:
            original=json.loads(c.execute('SELECT target FROM audit WHERE id=?',(ident,)).fetchone()[0])
        self.assertEqual(original['result']['result']['large'],'é'*9000)
        self.assertIsNotNone(self.api.receipt(ident,0,100)['next_offset_bytes'])
    def test_parent_paused_blocks_before_dispatch(self):
        mission=self.api.store.create('fixture','model','conv');self.api.mission=mission
        with patch.object(FakeRegistry,'execute',side_effect=AssertionError('must not run')):
            with self.assertRaisesRegex(ValueError,'not running'):self.api.call('host_exec',{})
    def test_negative_result_retains_failure(self):
        with patch.object(FakeRegistry,'execute',return_value={'ok':False,'result':{'returncode':2}}):
            result=self.api.call('host_exec',{})
        self.assertFalse(result['ok']);self.assertFalse(result['client_receipt']['call_completed'])
    def test_non_json_arguments_rejected(self):
        with self.assertRaises(ValueError):self.api.call('host_exec',[])
    def test_receipt_missing_rejected(self):
        with self.assertRaises(ValueError):self.api.receipt(999999)

if __name__=='__main__':unittest.main()

class MissionReceiptTests(unittest.TestCase):
 def test_invalid_creation_receipt_stays_unknown(self):
  with tempfile.TemporaryDirectory() as tmp:
   api=Capabilities(Path(tmp),config={'test':True})
   with patch('jarvis.client_capabilities.CanonicalAPI.request',return_value={'message':'model claims created'}):
    result=api.missions('create',goal='Explicit fixture goal')
   self.assertIsNone(result['created']);self.assertEqual(result['state'],'UNKNOWN')
 def test_catalog_is_bounded_and_searchable(self):
  class Catalog:
   def schemas(self,*args):return [{'function':{'name':n,'description':'fixture '*100,'parameters':{}}} for n in ['host_exec','host_remote','host_read_file','host_write_file','host_service','host_logs','host_resources','host_policy','host_ansible','host_github','disk_usage','system_status','qwen_code_run']]
  with tempfile.TemporaryDirectory() as tmp:
   api=Capabilities(Path(tmp),config={'test':True})
   with patch.object(api,'registry',return_value=Catalog()):
    first=api.catalog();last=api.catalog(offset=first['next_offset']);found=api.catalog(query='qwen')
  self.assertEqual(len(first['tools']),12);self.assertEqual(len(last['tools']),1);self.assertEqual(found['tools'][0]['name'],'qwen_code_run')
