"""Opt-in typed model action transport; decisions still belong to the model.

No tool is executed here. Registry, permissions, semantic gates and durable
attempt limits remain the authority after a validated model selection.
"""
import copy
import json
from jsonschema import Draft202012Validator

CONTRACT='jarvis.action.v1'


def explicit_variants(params):
    """Express finite discriminator contracts without conditional grammar rules.

    Only the known lossless subset is expanded. Unsupported contracts retain
    their original schema and backend validation; no requirements are dropped.
    """
    clauses=params.get('allOf',[])
    if not clauses:return params
    discriminator=None
    for clause in clauses:
        if set(clause)!={'if','then'}:return params
        condition=clause['if'];props=condition.get('properties',{})
        if len(props)!=1 or set(condition)-{'properties','required'}:return params
        key=next(iter(props));rule=props[key]
        if key not in params.get('required',[]) or set(rule) not in ({'const'},{'enum'}):return params
        if condition.get('required',[]) not in ([],[key]):return params
        if discriminator is not None and discriminator!=key:return params
        discriminator=key
        if set(clause['then'])-{'required','properties'}:return params
        for field,constraints in clause['then'].get('properties',{}).items():
            base=params.get('properties',{}).get(field,{})
            if any(k in base and base[k]!=v for k,v in constraints.items()):return params
    values=params.get('properties',{}).get(discriminator,{}).get('enum')
    if not values:return params
    base=copy.deepcopy(params);base.pop('allOf');definitions=base.pop('$defs',{})
    field_key='_f'
    if field_key in definitions:return params
    definitions[field_key]={'type':'object','properties':copy.deepcopy(base['properties'])};variants=[]
    groups={}
    for value in values:
        matches=tuple(i for i,clause in enumerate(clauses) if value in clause['if']['properties'][discriminator].get('enum',[clause['if']['properties'][discriminator].get('const')]))
        groups.setdefault(matches,[]).append(value)
    for matches,group in groups.items():
        variant=copy.deepcopy(base);variant['properties'][discriminator]['enum']=group
        for index in matches:
            clause=clauses[index]
            for field in clause['then'].get('required',[]):
                if field not in variant['required']:variant['required'].append(field)
            for field,constraints in clause['then'].get('properties',{}).items():
                variant['properties'].setdefault(field,{}).update(constraints)
        for field,definition in list(variant['properties'].items()):
            if definition==definitions[field_key]['properties'].get(field):
                escaped=field.replace('~','~0').replace('/','~1')
                variant['properties'][field]={'$ref':'#/$defs/'+field_key+'/properties/'+escaped}
        variants.append(variant)
    return {'$defs':definitions,'oneOf':variants,'type':'object'}


def request(payload,select_only=False):
    schemas=payload.get('tools',[])
    if not schemas:raise ValueError('Structured action requires actual offered tools')
    branches=[]
    for index,tool in enumerate(schemas):
        if select_only:
            fn=tool['function']
            branches.append({'type':'object','properties':{'tool':{'type':'string','enum':[fn['name']],'description':fn.get('description','')}},'required':['tool'],'additionalProperties':False})
            continue
        fn=tool['function'];params=explicit_variants(copy.deepcopy(fn['parameters']))
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
    if select_only:
        result['messages'][0]['content']+='\nTransport '+CONTRACT+' : choisis toi-même le prochain outil parmi le catalogue complet proposé. Réponds seulement par un objet JSON tool. Ce choix ne déclenche aucune opération ; son schéma complet sera fourni au tour suivant pour que tu choisisses les paramètres.'
    else:
        result['messages'][0]['content']+='\nTransport '+CONTRACT+' : choisis toi-même une seule action parmi les noms du schéma. Réponds par un objet JSON tool/arguments conforme au schéma, sans XML ni appel natif. Les tableaux restent des tableaux et les objets des objets. Les permissions et contrôles backend restent inchangés ; une sélection n’est pas une exécution.'
    return result,schema


def response(message,schema,select_only=False):
    if not isinstance(message,dict) or message.get('tool_calls'):raise ValueError('Expected one schema-constrained JSON action, not native tool calls')
    try:value=json.loads(message.get('content',''))
    except (ValueError,TypeError) as exc:raise ValueError('Invalid structured action JSON') from exc
    errors=list(Draft202012Validator(schema).iter_errors(value))
    if errors:
        def leaves(error):
            if error.context:
                for child in error.context:yield from leaves(child)
            else:yield error
        details=[leaf for error in errors for leaf in leaves(error)]
        # Show the closest matching branch's concrete constraints, rather than
        # truncating the entire generated action before the failing field.
        branches={}
        for error in details:
            path=list(error.absolute_schema_path)
            choices=[i for i,item in enumerate(path) if item in ('oneOf','anyOf')]
            key=tuple(path[:choices[-1]+2]) if choices else ()
            branches.setdefault(key,[]).append(error)
        closest=min(branches.values(),key=len)
        diagnostic='; '.join('/'.join(map(str,e.absolute_path))+': '+e.validator+' '+e.message for e in closest)
        raise ValueError('Structured action does not match offered tool schema: '+diagnostic[:600])
    if select_only:return value['tool']
    return {'role':'assistant','content':'','tool_calls':[{'function':{'name':value['tool'],'arguments':value['arguments']}}]}
