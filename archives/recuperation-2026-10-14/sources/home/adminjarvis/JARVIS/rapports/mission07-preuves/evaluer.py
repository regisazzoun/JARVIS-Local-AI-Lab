import pathlib,json,re,ast,subprocess,sys
P=pathlib.Path(__file__).parent
RUBRIC={'document':15,'durees':15,'autocorrection':15,'memoire':20,'document_present_absent':10,'ambiguite':10,'programmation':10,'journal':5}
def numbers(s):return [float(x.replace(',','.')) for x in re.findall(r'\d+(?:[.,]\d+)?',s)]
def codeok(s,negative=False):
 blocks=re.findall(r'```(?:python)?\s*([\s\S]*?)```',s);code=blocks[0] if blocks else s
 try:
  tree=ast.parse(code); tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)]; code=ast.unparse(tree)
  forbidden=(ast.Import,ast.ImportFrom,ast.Attribute,ast.While,ast.ClassDef,ast.With,ast.AsyncFunctionDef)
  if any(isinstance(n,forbidden) or (isinstance(n,ast.Name) and '__' in n.id) for n in ast.walk(tree)):return False
  test="env={'__builtins__':{'range':range,'sum':sum,'ValueError':ValueError,'int':int,'isinstance':isinstance}};exec("+repr(code)+",env);f=env['total_pairs'];assert [f(x) for x in [0,1,2,4,5]]==[0,0,2,6,6]\n"
  if negative:test+="try:\n f(-1)\n raise AssertionError('negative not rejected')\nexcept ValueError:pass\n"
  r=subprocess.run([sys.executable,'-I','-c',test],capture_output=True,timeout=2);return r.returncode==0
 except:return False

def score(rows):
 d={r['test']:r for r in rows};txt=lambda k:d[k]['text'].lower();sc={};ev={}
 t=txt('1_document');facts=sum(bool(re.search(p,t)) for p in ['5172|5[,.]2','99','70[.,]|70 token|33.?33','0[.,]12[.,]0','trois conversation|3 conversation']);docfacts=min(5,facts*2)
 # Documentary limitations and next-step correctness require manual review; provisional flags are explicitly heuristic.
 limits=int('pas' in t or 'non' in t or 'limite' in t)*2;nextstep=int(any(s in t for s in ['suivant','prochaine','recommand','poursuiv','tester','vérifier']))*3
 sc['document']=docfacts+limits+nextstep;ev['document']='Provisional lexical score out of 10; manual correction to 15-point semantic rubric required.'
 u=txt('2_duree_inconnue');m=txt('2_duree_mesuree');nums=numbers(m);metric=d['1_document']['metrics'];expected=[metric.get('prompt_eval_duration',0)/1e9,metric.get('eval_duration',0)/1e9];sc['durees']=5*int(any(x in u for x in ['pas accès','inconn','pas de','ne peux','indispon','non disponible','aucune information']))+5*int(all(any(abs(n-e)<=.02 for n in nums) for e in expected))+5*int(any(x in m for x in ['inconn','pas connu','non instrument','indispon','pas disponible']))
 t=txt('3_autocorrection');sc['autocorrection']=5*int(any(x in t for x in ['demand','question']))+5*int(any(x in t for x in ['erreur','incorrect','ne répond','pas répondu','hors sujet','inappropri','pas appropri']))+5*int(any(abs(n-1.392528)<.002 for n in numbers(t)))
 t=txt('4_memoire_final');checks={'alias':'noeud-cerise' in t,'budget':730 in numbers(t),'duree':42 in numbers(t),'interdiction':bool(re.search(r'(redémarr|redemarr).*(interdit|prohib|non autoris)|interdit.*(redémarr|redemarr)|aucun redémarrage|pas de redémarrage',t)),'code':'zebre17' in t};sc['memoire']=sum(checks.values())*4;ev['memoire']=checks
 a=txt('5_document_absent');b=txt('5_document_present');sc['document_present_absent']=5*int(bool(re.search(r'pas|inconn|impossible|indispon|ne peux',a)) and not re.search(r'gpu-[0-9a-f]{8}',a))+2.5*int('0.12.0' in b)+2.5*int('70.53' in b or '70,53' in b)
 if '6_ambiguite' in d:
  t=txt('6_ambiguite');sc['ambiguite']=5*int('?' in t)+5*int(not numbers(t))
  sc['programmation']=5*int(codeok(d['7_code_initial']['text']))+5*int(codeok(d['7_code_modifie']['text'],True))
  t=txt('8_journal');sc['journal']=5*int(any(w in t for w in ['fonctionn','chargé','chargement','réussi','succès','actif']) and not re.search(r'activer secure boot|activez secure boot|activer.*bios|réinstallez|réinstaller|redémarrez',t))
 return {'scores':sc,'total_provisoire':sum(sc.values()),'criteria':ev}
if __name__=='__main__':
 rows=json.loads((P/'batterie-resultats.json').read_text());out={}
 for c in sorted(set(r['config'] for r in rows)):
  rr=[r for r in rows if r['config']==c]
  if any(r['test']=='8_journal' for r in rr):out[c]=score(rr)
 (P/'scores-provisoires.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
