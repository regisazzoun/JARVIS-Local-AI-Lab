"""
title: Créer une mission JARVIS
version: 1.0.0
"""
import json,urllib.request
from pydantic import BaseModel
class Tools:
    class Valves(BaseModel):
        ADAPTER_URL: str = 'http://127.0.0.1:8092'
        ADAPTER_KEY: str = ''
    def __init__(self):self.valves=self.Valves()
    def create_jarvis_mission(self,goal:str)->str:
        """Créer une NOUVELLE mission dans le moteur canonique JARVIS, uniquement si l'utilisateur demande explicitement son lancement. Le reçu créé contient created=true, id et state. Un ID ne doit jamais être inventé. goal: objectif technique court."""
        req=urllib.request.Request(self.valves.ADAPTER_URL+'/tools/jarvis_task',data=json.dumps({'goal':goal}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+self.valves.ADAPTER_KEY})
        with urllib.request.urlopen(req,timeout=30) as r:return r.read().decode()
