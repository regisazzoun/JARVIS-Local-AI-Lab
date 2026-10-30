"""
title: JARVIS et Qwen Code local
version: 1.0.0
"""
import asyncio,json, urllib.request
from pydantic import BaseModel, Field
class Tools:
    class Valves(BaseModel):
        ADAPTER_URL: str = 'http://127.0.0.1:8092'
        ADAPTER_KEY: str = Field(default='',description='Private adapter bearer key')
    def __init__(self):self.valves=self.Valves()
    def _request(self,path,data):
        req=urllib.request.Request(self.valves.ADAPTER_URL+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+self.valves.ADAPTER_KEY})
        with urllib.request.urlopen(req,timeout=650) as r:return r.read().decode()
    async def _call(self,*args):
        return await asyncio.to_thread(self._request,*args)
    async def jarvis_missions(self)->str:
        """Consulter les missions existantes de JARVIS, sans les relancer."""
        return await self._call('/tools/missions',{})
    async def jarvis_task(self,goal:str)->str:
        """Créer une mission dans le moteur canonique existant, sur demande explicite. goal: objectif court (2000 caractères maximum)."""
        return await self._call('/tools/jarvis_task',{'goal':goal})
    async def qwen_code(self,task:str,project:str='acceptance')->str:
        """Confier un travail de programmation au Qwen80B existant via Qwen Code. Projet dédié existant uniquement; résultat à vérifier indépendamment. task: consigne courte. project: identifiant de projet."""
        return await self._call('/tools/qwen_code',{'task':task,'project':project})
