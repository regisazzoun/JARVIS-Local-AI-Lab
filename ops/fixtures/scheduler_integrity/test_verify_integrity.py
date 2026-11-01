import copy,hashlib,json,unittest
from verify_integrity import validate
class AuditOracleTests(unittest.TestCase):
    def setUp(self):
        self.files=[{'path':'a/z','sha256':'one'},{'path':'a-x','sha256':'two'}]
        self.expected={'files':self.files};self.checkpoint={'done':{f['path']:{'sha256':f['sha256'],'match':True} for f in self.files}}
        self.trace=[{'path':f['path'],'match':True} for f in self.files]
        self.report={'actual_root_sha256':hashlib.sha256(json.dumps(sorted(self.files,key=lambda x:x['path']),sort_keys=True).encode()).hexdigest(),'mismatches':[],'file_count':2}
    def test_different_path_sort_orders_do_not_create_false_failure(self):
        self.assertEqual(validate(self.expected,self.checkpoint,self.trace,self.report)['files'],2)
    def test_duplicate_commit_is_rejected(self):
        with self.assertRaises(ValueError):validate(self.expected,self.checkpoint,[self.trace[0],self.trace[0]],self.report)
    def test_missing_checkpoint_is_rejected(self):
        self.checkpoint['done'].pop('a/z')
        with self.assertRaises(ValueError):validate(self.expected,self.checkpoint,self.trace,self.report)
    def test_content_mismatch_is_rejected(self):
        self.checkpoint['done']['a/z']['sha256']='changed'
        with self.assertRaises(ValueError):validate(self.expected,self.checkpoint,self.trace,self.report)
if __name__=='__main__':unittest.main()
