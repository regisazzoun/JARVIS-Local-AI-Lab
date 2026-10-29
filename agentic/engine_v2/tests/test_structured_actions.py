"""Software transport contracts, not proof of JARVIS autonomy."""
import json,unittest
from jarvis.structured_actions import request,response

class StructuredActionTests(unittest.TestCase):
 def payload(self):
  return {'model':'fixture','messages':[{'role':'system','content':'Full owner policy'},{'role':'user','content':'Full goal'}],'tools':[{'type':'function','function':{'name':'plan','description':'Model chooses a plan','parameters':{'type':'object','properties':{'observations':{'type':'array','items':{'type':'string'}}},'required':['observations'],'additionalProperties':False}}}]}
 def test_native_xml_tools_removed_but_complete_policy_goal_and_types_kept(self):
  source=self.payload();out,schema=request(source)
  self.assertNotIn('tools',out);self.assertIn('tools',source)
  self.assertEqual(out['messages'][1]['content'],'Full goal');self.assertTrue(out['messages'][0]['content'].startswith('Full owner policy'))
  selected=response({'content':json.dumps({'tool':'plan','arguments':{'observations':['model choice']}})},schema)
  self.assertEqual(selected['tool_calls'][0]['function']['arguments']['observations'],['model choice'])
 def test_bullet_string_is_rejected_without_silent_array_coercion(self):
  _,schema=request(self.payload())
  with self.assertRaisesRegex(ValueError,'does not match'):response({'content':json.dumps({'tool':'plan','arguments':{'observations':'- first\n- second'}})},schema)
 def test_unknown_tool_extra_argument_and_native_call_are_rejected(self):
  _,schema=request(self.payload())
  for value in [{'tool':'shell','arguments':{}},{'tool':'plan','arguments':{'observations':[],'unoffered':True}}]:
   with self.assertRaises(ValueError):response({'content':json.dumps(value)},schema)
  with self.assertRaises(ValueError):response({'tool_calls':[{'function':{'name':'plan','arguments':{}}}]},schema)
 def test_each_branch_keeps_its_own_argument_schema_and_local_refs(self):
  source=self.payload();source['tools'].append({'type':'function','function':{'name':'read','parameters':{'type':'object','$defs':{'path':{'type':'string','pattern':'^/allowed/'}},'properties':{'path':{'$ref':'#/$defs/path'}},'required':['path'],'additionalProperties':False}}})
  _,schema=request(source)
  result=response({'content':json.dumps({'tool':'read','arguments':{'path':'/allowed/file'}})},schema)
  self.assertEqual(result['tool_calls'][0]['function']['name'],'read')
  with self.assertRaises(ValueError):response({'content':json.dumps({'tool':'read','arguments':{'path':'/forbidden/file'}})},schema)
 def test_current_plan_token_is_constrained_without_choosing_plan_content(self):
  from jarvis.durable_cycle import plan_version_schemas
  from jsonschema import validate,ValidationError
  source=[{'type':'function','function':{'name':'mission_plan_report_step','parameters':{'type':'object','properties':{'expected_version':{'type':'integer'},'title':{'type':'string'}},'required':['expected_version','title']}}}]
  result=plan_version_schemas(source,2);props=result[0]['function']['parameters']['properties']
  validate({'expected_version':2,'title':'Model chooses content'},result[0]['function']['parameters'])
  with self.assertRaises(ValidationError):validate({'expected_version':3,'title':'Next version guessed'},result[0]['function']['parameters'])
  self.assertEqual(props['title'],{'type':'string'});self.assertNotIn('enum',source[0]['function']['parameters']['properties']['expected_version'])

 def test_malformed_or_multiple_actions_cannot_be_dispatched(self):
  _,schema=request(self.payload())
  for text in ['<function=plan><parameter>',json.dumps([{'tool':'plan','arguments':{'observations':[]}}])]:
   with self.assertRaises(ValueError):response({'content':text},schema)
