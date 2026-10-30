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
    async def jarvis_call(self,name:str,arguments:str,request_id:str='')->str:
        """Exécuter un outil réel du catalogue, selon son schéma. arguments : objet JSON encodé en texte. request_id : identifiant stable facultatif évitant une double exécution. Un reçu n’est pas une vérification indépendante."""
        data={'name':name,'arguments':json.loads(arguments)}
        if request_id:data['request_id']=request_id
        return await self._call('call',data)
    async def jarvis_receipt(self,id:int,offset:int=0)->str:
        """Relire un reçu persistant. id : audit_id retourné par jarvis_call. offset : position en octets pour les longs reçus."""
        return await self._call('receipt',{'id':id,'offset':offset,'limit':3000})
    async def jarvis_missions(self,action:str='list',id:str='',goal:str='',after:int=0)->str:
        """Consulter list/read les missions canoniques. create crée une nouvelle mission uniquement sur demande explicite du propriétaire. id : mission pour read ; goal : objectif pour create ; after : pagination des événements."""
        return await self._call('missions',{'action':action,'id':id,'goal':goal,'after':after})
