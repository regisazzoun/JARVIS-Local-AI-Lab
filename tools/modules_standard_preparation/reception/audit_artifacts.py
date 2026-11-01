"""Independent acceptance checks on fixture artifacts, never on production files."""
from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json,hashlib,subprocess,tempfile
from pypdf import PdfReader
from openpyxl import load_workbook
R=Path.home()/'JARVIS/qwen-code-projects/livraisons/reception-locale-20261101-a'
Q=R/'qa';Q.mkdir(exist_ok=True)
checks=[]
def add(name,ok,**detail):checks.append({'check':name,'passed':bool(ok),**detail})
def office_text(p):
 with zipfile.ZipFile(p) as z:
  return '\n'.join(''.join(E.fromstring(z.read(n)).itertext()) for n in z.namelist() if (n=='word/document.xml' or n.startswith('ppt/slides/slide') and n.endswith('.xml')))
def render(p,kind):
 out=Q/kind;out.mkdir(exist_ok=True)
 pdf=out/(p.stem+'.pdf')
 if not pdf.exists():
  with tempfile.TemporaryDirectory(prefix='jarvis-reception-lo-') as prof:
   r=subprocess.run(['soffice','-env:UserInstallation='+Path(prof).as_uri(),'--headless','--convert-to','pdf','--outdir',str(out),str(p)],capture_output=True,text=True,timeout=180)
  add(kind+'-libreoffice-open-render',r.returncode==0 and pdf.exists(),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
 else:add(kind+'-libreoffice-open-render',True,previous_render_reused=True)
 if pdf.exists():
  reader=PdfReader(pdf);add(kind+'-page-count',len(reader.pages)==(3 if kind=='powerpoint' else 1),pages=len(reader.pages))
  if not list(out.glob('*.png')):
   x=subprocess.run(['pdftoppm','-scale-to','1100','-png',str(pdf),str(out/'page')],capture_output=True,text=True,timeout=120)
   add(kind+'-rasterization',x.returncode==0)
  else:add(kind+'-rasterization',True,previous_render_reused=True)
 return pdf
p=R/'temoin-word.docx'
if p.exists():
 t=office_text(p);add('word-semantic-content',all(s in t for s in ['Contrôle local JARVIS','RECEPTION-WORD-20261101','Observer','Noter','Conclure','Cible','Mode','Mac','Local','Dell','Distant']))
 with zipfile.ZipFile(p) as z:
  ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};root=E.fromstring(z.read('word/document.xml'))
  tabs=root.findall('.//w:tbl',ns);add('word-table-structure',len(tabs)==1 and len(tabs[0].findall('w:tr',ns))==3)
  liststyles=[x.get('{'+ns['w']+'}val') for x in root.findall('.//w:pStyle',ns)];add('word-numbered-list-style',liststyles.count('ListNumber')==3,styles=liststyles)
 render(p,'word')
else:add('word-exists',False)
p=R/'temoin-excel-recalcule.xlsx'
if p.exists():
 f=load_workbook(p,data_only=False);v=load_workbook(p,data_only=True)
 add('excel-sheet','Suivi' in f.sheetnames,sheets=f.sheetnames)
 if 'Suivi' in f.sheetnames:
  ws=f['Suivi'];vv=v['Suivi'];add('excel-formula',ws['B4'].value=='=SUM(B2:B3)',formula=ws['B4'].value)
  add('excel-calculated-result',vv['B4'].value==5,cached_value=vv['B4'].value)
  add('excel-inputs',ws['B2'].value==2 and ws['B3'].value==3 and ws['A3'].value=='Écriture')
 render(p,'excel')
else:add('excel-exists',False)
p=R/'temoin-slides.pptx'
if p.exists():
 with zipfile.ZipFile(p) as z:names=[n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
 t=office_text(p);add('powerpoint-slide-count',len(names)==3,count=len(names));add('powerpoint-content',all(s in t for s in ['Objectif','Actions','Résultat','RECEPTION-PPTX-20261101']))
 render(p,'powerpoint')
else:add('powerpoint-exists',False)
p=R/'temoin-pdf.pdf'
if p.exists():
 reader=PdfReader(p);t='\n'.join(x.extract_text() or '' for x in reader.pages)
 add('pdf-page-count',len(reader.pages)==1,pages=len(reader.pages));add('pdf-content',all(x in t for x in ['Réception PDF','RECEPTION-PDF-20261101','Lecture','Écriture','Vérification']))
 out=Q/'pdf';out.mkdir(exist_ok=True)
 if not list(out.glob('*.png')):
  r=subprocess.run(['pdftoppm','-scale-to','1100','-png',str(p),str(out/'page')],capture_output=True,text=True,timeout=120);add('pdf-rasterization',r.returncode==0)
 else:add('pdf-rasterization',True,previous_render_reused=True)
else:add('pdf-exists',False)
p=R/'temoin-reseau.drawio'
if p.exists():
 root=E.parse(p).getroot();cells=root.findall('.//mxCell');nodes=[x for x in cells if x.get('vertex')=='1'];edges=[x for x in cells if x.get('edge')=='1']
 labels=[x.get('value') for x in nodes];add('drawio-editable-xml',root.tag=='mxfile' and len(nodes)==3 and len(edges)==2,nodes=len(nodes),edges=len(edges),labels=labels)
 add('drawio-labels',all(x in labels for x in ['Mac mini','Routeur','Dell']))
else:add('drawio-exists',False)
p=R/'word-extrait.md'
if p.exists():add('markitdown-docx-text','RECEPTION-WORD-20261101' in p.read_text())
else:add('markitdown-output-exists',False)
p=R/'conversion-pandoc.docx'
if p.exists():add('pandoc-docx-content',all(s in office_text(p) for s in ['Conversion témoin','RECEPTION-CONVERSION-20261101','Écriture']))
else:add('pandoc-output-exists',False)
files=[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in R.iterdir() if p.is_file()]
result={'checks':checks,'files':files,'all_passed':all(x['passed'] for x in checks),'author':'Independent Codex verification of JARVIS WebUI-produced fixtures'}
(Q/'artifact-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False,indent=2))
