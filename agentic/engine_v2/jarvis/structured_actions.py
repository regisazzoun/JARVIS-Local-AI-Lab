"""Opt-in typed model action transport; decisions still belong to the model.

No tool is executed here. Registry, permissions, semantic gates and durable
attempt limits remain the authority after a validated model selection.
"""
import copy
import json
from jsonschema import Draft202012Validator

CONTRACT='jarvis.action.v1'


def request(payload):
    schemas=payload.get('tools',[])
    if not schemas:raise ValueError('Structured action requires actual offered tools')
    branches=[]
    for index,tool in enumerate(schemas):
        fn=tool['function'];params=copy.deepcopy(fn['parameters'])
        def relocate(value):
            if isinstance(value,list):return [relocate(item) for item in value]
            if not isinstance(value,dict):return value
            return {key:('#/oneOf/'+str(index)+'/properties/arguments'+item[1:] if key=='$ref' and isinstance(item,str) and item.startswith('#/') else relocate(item)) for key,item in value.items()}
        params=relocate(params)
        branches.append({'type':'object','properties':{'tool':{'type':'string','enum':[fn['name']],'description':fn.get('description','')},'arguments':params},'required':['tool','arguments'],'additionalProperties':False})
    schema={'type':'object','oneOf':branches}
    Draft202012Validator.check_schema(schema)
    result=copy.deepcopy(payload);result.pop('tools',None);result['format']=schema
    result['_jarvis_action_contract']=CONTRACT
    result['messages'][0]['content']+='\nTransport '+CONTRACT+' : choisis toi-même une seule action parmi les noms du schéma. Réponds par un objet JSON tool/arguments conforme au schéma, sans XML ni appel natif. Les tableaux restent des tableaux et les objets des objets. Les permissions et contrôles backend restent inchangés ; une sélection n’est pas une exécution.'
    return result,schema


def response(message,schema):
    if not isinstance(message,dict) or message.get('tool_calls'):raise ValueError('Expected one schema-constrained JSON action, not native tool calls')
    try:value=json.loads(message.get('content',''))
    except (ValueError,TypeError) as exc:raise ValueError('Invalid structured action JSON') from exc
    errors=list(Draft202012Validator(schema).iter_errors(value))
    if errors:
        error=min(errors,key=lambda item:len(item.absolute_path))
        raise ValueError('Structured action does not match offered tool schema: '+str(error.message)[:600])
    return {'role':'assistant','content':'','tool_calls':[{'function':{'name':value['tool'],'arguments':value['arguments']}}]}
