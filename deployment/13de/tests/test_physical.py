import copy, importlib.util, pathlib, sys, unittest
sys.path.insert(0,str(pathlib.Path(__file__).parents[1]/'physical'))
from validate import validate
class Physical(unittest.TestCase):
 def setUp(self):
  self.plan=dict(vendor='Dell Inc.',product='Precision 5820 Tower',uuid='12345678-1234-1234-1234-123456789abc',disks=[dict(path='/dev/nvme0n1',serial='a',model='NVMe',size=2000000000000),dict(path='/dev/nvme1n1',serial='b',model='NVMe',size=2000000000000)])
  self.live=copy.deepcopy(self.plan); self.live['uefi']=True
  for d in self.live['disks']:d.update(type='disk',ro=False)
 def test_valid(self):self.assertTrue(validate(self.plan,self.live))
 def test_wrong_host(self):
  self.live['vendor']='Apple Inc.'
  with self.assertRaises(AssertionError):validate(self.plan,self.live)
 def test_disk_changes(self):
  for field,value in [('serial','other'),('size',1999999999999),('model','other'),('path','/dev/nvme2n1')]:
   with self.subTest(field=field):
    live=copy.deepcopy(self.live);live['disks'][0][field]=value
    with self.assertRaises(AssertionError):validate(self.plan,live)
 def test_extra_disk(self):
  self.live['disks'].append(dict(path='/dev/sda',type='disk'))
  with self.assertRaises(AssertionError):validate(self.plan,self.live)
 def test_missing_disk(self):
  self.live['disks'].pop()
  with self.assertRaises(AssertionError):validate(self.plan,self.live)
 def test_legacy(self):
  self.live['uefi']=False
  with self.assertRaises(AssertionError):validate(self.plan,self.live)
 def test_readonly(self):
  self.live['disks'][0]['ro']=True
  with self.assertRaises(AssertionError):validate(self.plan,self.live)
 def test_duplicate(self):
  self.plan['disks'][1]['serial']='a'
  with self.assertRaises(AssertionError):validate(self.plan,self.live)

 def test_uuid_mismatch(self):
  self.live['uuid']='87654321-1234-1234-1234-123456789abc'
  with self.assertRaises(AssertionError):validate(self.plan,self.live)
 def test_partition_rejected(self):
  self.plan['disks'][0]['path']='/dev/nvme0n1p1'
  self.live['disks'][0]['path']='/dev/nvme0n1p1'
  with self.assertRaises(AssertionError):validate(self.plan,self.live)

 def test_observed_xseries_product_is_still_exact(self):
  self.plan['product']=self.live['product']='Precision 5820 Tower X-Series'
  self.assertTrue(validate(self.plan,self.live))
  self.live['product']='Other Dell'
  with self.assertRaises(AssertionError):validate(self.plan,self.live)
 def test_empty_reader_exception_never_accepts_inserted_media(self):
  self.plan['excluded_empty_media']=[dict(path='/dev/sda',model='SD/MMC CRW',size=0)]
  self.live['disks'].append(dict(path='/dev/sda',type='disk',model='SD/MMC CRW',size=0,ro=False))
  self.assertTrue(validate(self.plan,self.live))
  for size in (512,1000000):
   self.live['disks'][-1]['size']=size
   with self.assertRaises(AssertionError):validate(self.plan,self.live)
 def test_empty_reader_exception_cannot_be_generalized(self):
  self.plan['excluded_empty_media']=[dict(path='/dev/sdb',model='anything',size=0)]
  with self.assertRaises(AssertionError):validate(self.plan,self.live)
