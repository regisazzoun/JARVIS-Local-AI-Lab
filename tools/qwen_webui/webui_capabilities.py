"""
title: Capacités canoniques JARVIS
version: 1.0.0
"""
import asyncio,json,urllib.request
from pydantic import BaseModel,Field
class Tools:
    class Valves(BaseModel):
        ADAPTER_URL:str='http://127.0.0.1:8092'
        ADAPTER_KEY:str=Field(default='',description='Private local adapter key')
    def __init__(self):self.valves=self.Valves()
    def _request(self,operation,data):
        request=urllib.request.Request(self.valves.ADAPTER_URL+'/tools/capabilities/'+operation,data=json.dumps(data).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+self.valves.ADAPTER_KEY})
        with urllib.request.urlopen(request,timeout=600) as response:return response.read().decode()
    async def _call(self,*args):
        return await asyncio.to_thread(self._request,*args)
    async def jarvis_catalog(self,query:str='',offset:int=0)->str:
        """Découvrir les outils réellement raccordés à JARVIS, par pages de douze. query : filtre du nom ou de la description. offset : page suivante indiquée par next_offset. Vérifier le schéma avant appel."""
        return await self._call('catalog',{'query':query,'offset':offset})
    async def jarvis_schema(self,name:str)->str:
        """Obtenir les paramètres exacts d’un outil du catalogue. name : nom réel de l’outil."""
        return await self._call('schema',{'name':name})
    async def jarvis_remote_project(self,host:str,project:str,command:str)->str:
        """Exécuter réellement une commande dans un projet distant autorisé. host : dell-observe ou dell2, obligatoire. project : projet accordé. command : commande choisie par JARVIS. Aucun repli local ne vaut résultat distant."""
        if host not in ('dell-observe','dell2'):raise ValueError('Unknown Dell profile')
        return await self._call('call',{'name':'host_remote','arguments':{'host':host,'action':'project_exec','project':project,'command':command}})
    async def jarvis_call(self,name:str,arguments:dict,request_id:str='')->str:
        """Exécuter un outil réel du catalogue, selon son schéma. arguments : objet JSON structuré conforme au schéma, sans encodage en texte. request_id : identifiant stable facultatif évitant une double exécution. Un reçu n’est pas une vérification indépendante."""
        parameters=json.loads(arguments) if isinstance(arguments,str) else arguments
        if not isinstance(parameters,dict):return json.dumps({'ok':False,'status':'NOT_EXECUTED','error':'arguments must be a JSON object conforming to jarvis_schema; never a quoted command'})
        data={'name':name,'arguments':parameters}
        if request_id:data['request_id']=request_id
        return await self._call('call',data)
    async def jarvis_receipt(self,id:int,offset:int=0)->str:
        """Relire un reçu persistant. id : audit_id retourné par jarvis_call. offset : position en octets pour les longs reçus."""
        return await self._call('receipt',{'id':id,'offset':offset,'limit':3000})
    async def jarvis_missions(self,action:str='list',id:str='',goal:str='',after:int=0,profile:str='standard')->str:
        """Consulter list/read les missions canoniques. create crée une nouvelle mission uniquement sur demande explicite. id : mission pour read ; goal : objectif pour create ; after : pagination. profile standard utilise les interfaces plates et rapports factuels existants ; service_observation sélectionne le profil reçu d'observation systemd en lecture seule, seulement pour cet usage."""
        return await self._call('missions',{'action':action,'id':id,'goal':goal,'after':after,'profile':profile})

    async def google_personal(self,action:str='list',name:str='',arguments:str='{}',query:str='',offset:int=0)->str:
        """Google PERSONNEL uniquement : list découvre les méthodes, schema décrit name, call exécute name avec arguments JSON. Drive/Docs/Sheets/Calendar/Gmail. Aucun changement implicite de compte."""
        return await self._call('call',{'name':'google_personal','arguments':{'action':action,'arguments':json.loads(arguments),'offset':offset,**({'name':name} if name else {}),**({'query':query} if query else {})}})
    async def google_education(self,action:str='list',name:str='',arguments:str='{}',query:str='',offset:int=0)->str:
        """Google ÉDUCATION uniquement : list découvre les méthodes, schema décrit name, call exécute name avec arguments JSON. Drive/Docs/Sheets/Calendar/Gmail. Identité distincte du compte personnel."""
        return await self._call('call',{'name':'google_education','arguments':{'action':action,'arguments':json.loads(arguments),'offset':offset,**({'name':name} if name else {}),**({'query':query} if query else {})}})
    async def jarvis_skill_run(self,name:str,parameters:dict,run_id:str='')->str:
        """Exécuter un Skill existant avec paramètres structurés JSON. Découvre son manifeste actif et encode uniquement les conteneurs requis par les anciens champs texte JSON. Ne recrée ni n'active de Skill."""
        listing=json.loads(await self._call('call',{'name':'skill_list','arguments':{'name':name}}))
        if not listing.get('ok'):return json.dumps(listing,ensure_ascii=False)
        skills=listing.get('result',{}).get('skills',[])
        active=next((s for s in skills if s.get('name')==name and s.get('version')==s.get('active_version')),None)
        if not active:raise ValueError('No active existing Skill with this name')
        props=active.get('parameters',{}).get('properties',{})
        values={k:json.dumps(v,ensure_ascii=False) if props.get(k,{}).get('type')=='string' and isinstance(v,(dict,list)) else v for k,v in parameters.items()}
        args={'name':name,'parameters':json.dumps(values,ensure_ascii=False)}
        if run_id:args['run_id']=run_id
        return await self._call('call',{'name':'skill_run','arguments':args})
    async def jarvis_github(self,repository:str,action:str,parameters:dict)->str:
        """GitHub réel via le broker JARVIS existant. repository : owner/repo. action : opération du schéma host_github. parameters : champs structurés (branch,file,path,query,files,...). Ne passe jamais par les outils SSH pour une lecture GitHub."""
        if set(parameters)&{'repository','action'}:raise ValueError('Repository and action must use their explicit fields')
        schema=json.loads(await self._call('schema',{'name':'host_github'}))['schema']
        props=schema.get('properties',{})
        values={k:json.dumps(v,ensure_ascii=False) if props.get(k,{}).get('type')=='string' and isinstance(v,(dict,list)) else v for k,v in parameters.items()}
        return await self._call('call',{'name':'host_github','arguments':{'repository':repository,'action':action,**values}})
