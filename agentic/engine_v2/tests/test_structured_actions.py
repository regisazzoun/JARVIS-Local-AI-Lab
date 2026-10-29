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

 def test_conditional_execution_fields_are_explicit_in_each_grammar_variant(self):
  from jarvis.structured_actions import explicit_variants
  from jsonschema import Draft202012Validator
  original={'type':'object','properties':{'kind':{'type':'string','enum':['inspect','correct','test','analyze','accept']},'executor':{'type':'string','enum':['Dell1','Dell2']},'command':{'type':'string'},'reference':{'type':'integer'},'source_reference':{'type':'integer'}},'required':['kind'],'additionalProperties':False,'allOf':[{'if':{'properties':{'kind':{'const':'accept'}},'required':['kind']},'then':{'required':['reference','source_reference']}},{'if':{'properties':{'kind':{'enum':['inspect','correct','test']}},'required':['kind']},'then':{'required':['executor','command'],'properties':{'command':{'minLength':1}}}}]}
  variants=explicit_variants(original)
  self.assertNotIn('allOf',variants)
  self.assertEqual(len(variants['oneOf']),3)  # identical execution contracts share one branch
  for item in variants['oneOf']:
   mode=item['properties']['kind']['enum'][0]
   if mode in ('inspect','correct','test'):
    self.assertIn('executor',item['required']);self.assertIn('command',item['required'])
    self.assertEqual(item['properties']['command']['minLength'],1)
   if mode=='accept':self.assertTrue({'reference','source_reference'}<=set(item['required']))
  source=self.payload();source['tools'][0]['function']['parameters']=original
  _,schema=request(source)
  for kind in original['properties']['kind']['enum']:
   for fields in ({},{'executor':'Dell2'},{'executor':'Dell1','command':''},{'executor':'Dell2','command':'python3 -V'},{'reference':1,'source_reference':2}):
    args={'kind':kind,**fields}
    expected=Draft202012Validator(original).is_valid(args)
    self.assertEqual(Draft202012Validator(variants).is_valid(args),expected)
    self.assertEqual(Draft202012Validator(schema).is_valid({'tool':'plan','arguments':args}),expected)
 def test_unknown_conditional_contract_is_preserved_without_weakening(self):
  from jarvis.structured_actions import explicit_variants
  schema={'type':'object','allOf':[{'if':{'required':['x']},'then':{'anyOf':[{'required':['y']},{'required':['z']}]}}]}
  self.assertEqual(explicit_variants(schema),schema)
 def test_two_stage_choice_preserves_catalogue_and_does_not_produce_calls(self):
  source=self.payload();source['tools'].append({'type':'function','function':{'name':'test','description':'Independent validation','parameters':{'type':'object','properties':{'command':{'type':'string'}},'required':['command'],'additionalProperties':False}}})
  offered,schema=request(source,select_only=True)
  self.assertEqual([b['properties']['tool']['enum'][0] for b in schema['oneOf']],['plan','test'])
  self.assertNotIn('arguments',schema['oneOf'][0]['properties'])
  choice=response({'content':json.dumps({'tool':'test'})},schema,select_only=True)
  self.assertEqual(choice,'test');self.assertEqual(len(source['tools']),2)
  narrowed={**source,'tools':[x for x in source['tools'] if x['function']['name']==choice]}
  _,arguments_schema=request(narrowed)
  with self.assertRaises(ValueError):response({'content':json.dumps({'tool':'test','arguments':{}})},arguments_schema)
  selected=response({'content':json.dumps({'tool':'test','arguments':{'command':'model-chosen test'}})},arguments_schema)
  self.assertEqual(selected['tool_calls'][0]['function']['arguments']['command'],'model-chosen test')
 def test_two_stage_choice_rejects_unknown_tool_and_premature_arguments(self):
  _,schema=request(self.payload(),select_only=True)
  for value in ({'tool':'unknown'},{'tool':'plan','arguments':{'observations':[]}}):
   with self.assertRaises(ValueError):response({'content':json.dumps(value)},schema,select_only=True)
 def test_malformed_or_multiple_actions_cannot_be_dispatched(self):
  _,schema=request(self.payload())
  for text in ['<function=plan><parameter>',json.dumps([{'tool':'plan','arguments':{'observations':[]}}])]:
   with self.assertRaises(ValueError):response({'content':text},schema)
