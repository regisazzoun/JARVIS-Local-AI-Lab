from pathlib import Path
import hashlib,json,datetime
R=Path.home()/'JARVIS/modules-standard-20261101'
backup=Path.home()/'JARVIS/modules-standard-20261101-private/reception-skill-instructions-before'
backup.mkdir(parents=True,exist_ok=True)
for name in ['microsoft-office','pdf']:
 p=R/'native-skills'/name/'SKILL.md';old=p.read_text();(backup/(name+'.md')).write_text(old)
 a=old.index('## Prerequisites');b=old.index('## How to Run',a)
 replacement=f'''## Prerequisites — environnement JARVIS déjà installé

Utiliser exclusivement l’interpréteur existant `{R}/venvs/documents/bin/python` pour les scripts de ce Skill. Ne pas créer de second environnement et ne pas lancer le bootstrap Hermes : les dépendances sont déjà installées.

Pour une commande shell, utiliser ce chemin absolu ou commencer la même commande par `. {R}/documents.env` puis utiliser `"$PY"`. Les variables d’une commande terminal ne persistent pas nécessairement dans la suivante.

Les ressources `references/` et `scripts/` sont sur le terminal dans `{R}/native-skills/{name}`. Sur WebUI, `read_skill_file` pour un Skill terminal ne lit que SKILL.md : lire les références avec le `read_file` du terminal et leur chemin absolu. LibreOffice et Poppler sont présents pour les rendus. Les options OCR externes marker/nano-pdf restent hors réception.

Avant un script de création : lire son schéma d’entrée documenté (pour pdf_create.py, la documentation en tête du script), écrire la spécification JSON, attendre le succès de cette écriture, puis seulement lancer la création. Ne pas lancer ces étapes dépendantes simultanément. pdf_create.py attend `elements` à la racine ; la clé `pages` ne définit pas son contenu.

Après la création, une lecture qui établit les critères demandés suffit : PDF page_count/contenu ; Excel --formulas fournit à la fois la formule et cached ; PowerPoint --outline fournit le plan. Ne pas dérouler toutes les commandes d’exemple ou recommencer un recalcul déjà réussi. Si une copie est demandée, employer --out et ne pas recalculer aussi l’original. Après satisfaction des critères, répondre immédiatement.

Rapporter un code de processus uniquement quand run_command/get_process_status fournit exit_code. Pour write_file/read_file, rapporter le succès ou l’erreur JSON, jamais un code0 inventé. Un exit_code0 n’est pas une preuve suffisante de contenu : un PDF de zéro page ou un résultat vide est un échec sémantique.

'''
 new=old[:a]+replacement+old[b:]
 new=new.replace('lire les références/fichiers avec les outils natifs exposés ou le terminal','lire les références/fichiers avec read_file du terminal et leurs chemins absolus')
 p.write_text(new)
 print(name,hashlib.sha256(new.encode()).hexdigest())
(R/'reception-instruction-adjustments.json').write_text(json.dumps({'reason':'First real WebUI run attempted an upstream duplicate environment bootstrap and a supporting reference through the SKILL-only endpoint. Native Markdown clarified; original skills and scripts unchanged.','skills':['microsoft-office','pdf'],'new_agent_engine':False},indent=2))
