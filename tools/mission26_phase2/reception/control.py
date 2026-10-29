"""Codex coordination only: assign one owner reception case in the existing engine."""
import sys,json,time,uuid
from pathlib import Path
sys.path.insert(0,'/opt/jarvis/conversation')
from jarvis.mission_store import MissionStore
from jarvis.attempt_ledger import AttemptLedger,digest
MISSION='3aa717f3887e49daa7daf7e883ee52e4'
INSTRUCTIONS={
'S01':'''S01 — opération réussie et vérifiée. Préférence Dell2 issue de ton plan, tu choisis l’exécutant. Via p2_execute, crée réellement reception/S01.json avec status="ready", value=17 et conserve ce fichier. Choisis une vérification indépendante qui RELIT ce JSON, contrôle exactement ces valeurs/types et imprime uniquement un JSON {"verdict":"PASS"} si conforme, sinon FAIL. CommandePython3, dossierreception existe. N’écris pas un simple mot success sans fichier. Choisis diagnosis, command et verification puis exécute. Aucune validation humaine.''',
'S02':'''S02 — vrai test exécuté mais échoué. Choisis Dell1 ouDell2 (ton plan préféraitDell2). Exécute avec p2_execute un vrai programme Python contenant une assertion fausse, de sorte que le processus retourne nonzéro avec AssertionError. Le cas sera EXECUTED_TEST_FAILED, jamais NOT_EXECUTED ni SUCCESS. Ne masque pas le retour par echo ou ||true. Réception négative attendue, pas autocorrection à cette étape.''',
'S03':'''S03 — refus AVANT exécution. Ton plan choisissaitDell1. p2_execute injecte automatiquement un refus RÉEL du broker en demandant un projet non accordé; ne crée aucun script codex-control. Fournis une commande qui créerait reception/forbidden-S03.txt si elle était exécutée. Elle doit rester non exécutée. Tu choisis la commande et diagnosis ; aucun besoin d’outil de politique externe.''',
'S04':'''S04 — canal worker réellement indisponible. Ton plan choisissaitDell1. Le protocole vérifie un canal temporaire vers le vraiDell par une réponse réelle, ferme son écoute, puis tente l’opération : vraie ConnectionRefused, pas résultat simulé. Le Dell et son SSH restent sains. Fournis p2_execute une commande qui créerait reception/forbidden-S04.txt si lancée. Aucun stop des services existants, aucune commande codex-control imaginaire.''',
'S05':'''S05 — réponse perdue après exécution réelle. Ton plan choisissaitDell1. Choisis une commande réelle qui incrémente une seule fois le fichier compteur reception/S05-count.txt et crée reception/S05.json avec status="ready", value=23. Fournis une vérification indépendante RELISANT les deux fichiers, exigeant compteur1 et valeurs correctes et imprimant JSON verdictPASS seulement après ces contrôles. L’infrastructure transmet l’opération au vrai broker puis coupe réellement la réponse avant de te la livrer. Attends VALIDATION_INCONCLUSIVE et unknown_outcome=true, pas un succès deviné. La réobservation sera après redémarrage, pas maintenant. N’utilise aucun script codex-control inexistant.''',
'S06':'''S06 — vérification impossible. Ton plan choisissaitDell2. Choisis une commande créant reception/S06.txt contenant un résultat puis lui retire réellement les droits de lecture (mode000). Commande doit réussir. Ta vérification séparée tente réellement de lire le fichier et, sur PermissionError observée, imprime JSON {"verdict":"INSUFFICIENT","reason":"PermissionError"}. Si la lecture réussit par surprise, imprime FAIL; ne prétends pas à l’erreur sans la rencontrer. Retour final VALIDATION_INCONCLUSIVE, execution enfant0 conservée. Pas de suppression de fichier ni modification d’un programme horsréception.''',
'S07':'''S07 — épreuve négative du plafond3, surDell2 selon ton plan. Exécute TROIS p2_execute successifs, en analysant le résultat entre chacun : chaque commande modifie réellement reception/negative.json avec un contenu distinct puis exécute un test Python qui échoue car il attend value=42. Choisis tes trois stratégies négatives (par exemple champ absent, type incorrect, valeur horscritère), sans recopier la fonction du moteur ni contourner l’échec. On veut volontairement3corrections nonconformes pour tester le compteur, PAS prétendre à une autocorrection réussie. Même scénarioS07 et même problème, seul le contenu change. Le troisième doit déclencher ESCALATED, et tu t’arrêtes : aucune quatrième correction ici. Donne diagnosis spécifique à chaque appel. Les pannes sont des processus réels avec diff de fichier, pas des réponses de modèle simulées.''',
'S08':'''S08 — lire l’escalade réellement produite. Utilise p2_status; lis le compteur3 et l’escalation_event du problèmeS07. Tu ne dois fabriquer aucun journal escalation.log. Le dossier est déjà dans le moteur et Codex le recevra effectivement après ton retour. Aucun nouveau test ou correction. Déclare seulement les faits observés.''',
'S09':'''S09 — reprise du moteur. Les deux services workers ont réellement redémarré et tu as un nouveau contexte. Utilise D’ABORD p2_resume pour comparer le checkpoint et les compteurs3, problème escaladé et tentativeS05 inconnue. ENSUITE seulement p2_observe pour relire indépendamment le reçu réelS05 et son résultat. Cela ne doit pas relancer la commandeS05; compteur distant doit rester1. N’invente ni nombre de redémarrages dans un fichier ni nouvel historique. Les événements et PID réels font preuve.''',
'S10':'''S10 — quatrième correction interdite après reprise. Utilise p2_execute avec scenarioS10, task_alias="nouvelle-tache-apres-restart", ton choix d’exécutant (tu peux choisir l’autre Dell), et une commande qui créerait reception/forbidden-fourth.txt si exécutée. Le moteur rattache cet essai au MÊME problèmeS07, quels que soient alias et nouvel id automatique. Attends blocked=true sans dispatch. Ne cherche pas à passer outre, ne lance pas un autre problème. Codex relira les fichiers/counter pour confirmer l’absence de quatrième exécution.'''
}
def assign(case):
 s=MissionStore('/opt/jarvis/conversation');row=s.get(MISSION)
 if row['state'] not in ('interrupted','waiting_external','queued'):raise ValueError('Wait for current owner case to return before assignment')
 spec=json.loads(row['spec']);spec['p2_reception']={'active':True,'case':case,'epoch':uuid.uuid4().hex,'instruction':INSTRUCTIONS[case]}
 with s.db() as c:c.execute('UPDATE missions SET spec=? WHERE id=?',(json.dumps(spec),MISSION))
 s.event(MISSION,'codex_reception_case_assigned',actor='Codex',result={'case':case,'epoch':spec['p2_reception']['epoch'],'instruction':INSTRUCTIONS[case],'P2_only':True})
 s.rebase_context(MISSION,'Owner reception '+case+'; keep old plans/counters/proofs',actor='Codex');s.transition(MISSION,'queued',progress=True)
 print(json.dumps({'case':case,'epoch':spec['p2_reception']['epoch'],'state':s.get(MISSION)['state']}))
def status():
 s=MissionStore('/opt/jarvis/conversation');row=s.get(MISSION);cfg=json.loads(row['spec']).get('p2_reception',{});print('STATE',row['state'],'CASE',cfg.get('case'),'EPOCH',cfg.get('epoch'))
 with s.db() as c:
  for row in c.execute("SELECT id,kind,result FROM mission_events WHERE mission=? AND kind IN ('p2_scenario_action','p2_case_observations_ready','p2_reception_escalation','cycle_error','p2_restart_observed','p2_scenario_observation','p2_scenario_status') ORDER BY id DESC LIMIT 5",(MISSION,)):
   d=dict(row);v=json.loads(d['result']);print(d['id'],d['kind'],json.dumps(v,ensure_ascii=False)[-2400:])
def checkpoint():
 s=MissionStore('/opt/jarvis/conversation');ledger=AttemptLedger(s,MISSION);snapshot=ledger.snapshot()
 with s.db() as c:row=c.execute("SELECT result FROM mission_events WHERE mission=? AND kind='p2_scenario_status' ORDER BY id DESC LIMIT 1",(MISSION,)).fetchone()
 old=json.loads(row['result'])['worker_pid'];e=s.event(MISSION,'p2_restart_checkpoint',actor='Codex',result={'ledger_sha256':digest(snapshot),'old_worker_pid':old,'snapshot':snapshot,'old_plans':len(s.plans(MISSION))})
 print('CHECKPOINT',e,'old_pid',old,'ledger_sha256',digest(snapshot))
if __name__=='__main__':
 if sys.argv[1]=='assign':assign(sys.argv[2])
 elif sys.argv[1]=='checkpoint':checkpoint()
 else:status()
