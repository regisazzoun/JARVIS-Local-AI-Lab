"""Lossless coverage transport, independently expanded before comparison."""
import copy
import unittest
from jarvis.mission_assurance import coverage_review_view


def expand(document):
 if 'review_values' not in document:return document
 pool=document['review_values'];values=[]
 def value(item):
  if isinstance(item,dict):
   if set(item)=={'$review_ref'}:return copy.deepcopy(values[item['$review_ref']])
   return {k:value(v) for k,v in item.items()}
  if isinstance(item,list):return [value(v) for v in item]
  return item
 for item in pool:values.append(value(item))
 return value(document['review_data'])

class CoverageTransportTests(unittest.TestCase):
 def test_nested_duplicates_distinct_values_and_array_order(self):
  common={'window':{'text':'é'*600,'limit':27648},'path':'/tmp/report-'+'x'*150}
  data={'tasks':[dict(common,id=str(i),depends=['same','same','other']) for i in range(8)],'changed':dict(common,window={'text':'different','limit':27648})}
  before=copy.deepcopy(data);wire=coverage_review_view(data)
  self.assertLess(len(str(wire)),len(str(data)));self.assertEqual(expand(wire),before);self.assertEqual(data,before)
 def test_small_document_retains_existing_layout(self):
  data={'plan':{'id':'one'},'requirements':[1,2]}
  self.assertIs(coverage_review_view(data),data)
 def test_reserved_marker_cannot_be_misinterpreted(self):
  with self.assertRaises(ValueError):coverage_review_view({'literal':{'$review_ref':0}})
