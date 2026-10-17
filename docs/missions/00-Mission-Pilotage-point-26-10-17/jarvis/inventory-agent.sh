python3 << 'PYTHON_SCRIPT'
import json
import hashlib
import re
import os
from pathlib import Path

# Configuration
SOURCE_FILE = "/var/lib/jarvis/projects/mission00/SOURCES-A-EXPLORER.json"
OUTPUT_DIR = "/var/lib/jarvis/projects/mission00"
JSON_OUTPUT = os.path.join(OUTPUT_DIR, "INVENTAIRE-LOCAL-JARVIS.json")
MD_OUTPUT = os.path.join(OUTPUT_DIR, "INVENTAIRE-LOCAL-JARVIS.md")

# Exclusions strictes
EXCLUDE_PATTERNS = ["/private/", "/.git/", "/docs/missions/00-Mission-Pilotage-point-26-10-17"]

def is_excluded(path):
    path_str = str(path)
    return any(pattern in path_str for pattern in EXCLUDE_PATTERNS)

def extract_metadata(content, filepath):
    """Extrait titre, mission, date, type depuis le contenu Markdown."""
    # Initialisation de filename dès le début pour éviter les erreurs d'accès
    filename = os.path.basename(filepath)
    
    lines = content.split('\n')
    title = None
    mission = None
    date = "À confirmer"
    
    # Recherche Titre en H1
    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            break
    
    # Si pas de H1, on utilise le nom du fichier sans extension
    if not title:
        title = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ")
    
    # Recherche Mission (dans un champ spécifique ou déduit du titre/nom)
    # On cherche une ligne "^Mission:" ou "# Mission"
    mission_pattern = re.compile(r'^(?:#|##)\s*Mission[:\s]+(.+)$', re.IGNORECASE | re.MULTILINE)
    mission_match = mission_pattern.search(content)
    if mission_match:
        mission = mission_match.group(1).strip()
    else:
        # Fallback : déduire du nom de fichier si contient "Mission" ou chiffre
        filename_lower = filename.lower()
        if "mission" in filename_lower or re.search(r"\d{2}-\d{2}", filename):
            mission = title # On suppose que le titre est la mission
    
    # Recherche Date (format YYYY-MM-DD ou textuel en haut de page)
    date_pattern = re.compile(r'^(?:Date|Dernière modification|Créé)[:\s]+([^\n]+)$', re.IGNORECASE | re.MULTILINE)
    date_match = date_pattern.search(content)
    if date_match:
        date = date_match.group(1).strip()
    
    # Type d'après nom/titre
    filetype = "Document"
    filename_lower = filename.lower()
    if "rapport" in filename_lower or "rapport" in (title or "").lower():
        filetype = "Rapport"
    elif "procédure" in filename_lower or "procédure" in (title or "").lower():
        filetype = "Procédure"
    elif "note" in filename_lower or "note" in (title or "").lower():
        filetype = "Note"
    
    return {
        "titre": title,
        "mission": mission if mission else "Non spécifiée",
        "date": date,
        "type": filetype
    }

def discover_files(base_path):
    """Découvre les fichiers .md récursivement dans un répertoire."""
    files = []
    if os.path.isdir(base_path):
        for root, _, filenames in os.walk(base_path):
            # Exclusion au niveau du répertoire parent
            if is_excluded(root):
                continue
            for fname in filenames:
                if fname.endswith(".md"):
                    filepath = os.path.join(root, fname)
                    if not is_excluded(filepath):
                        files.append(filepath)
    else:
        # Si c'est un fichier direct
        if base_path.endswith(".md") and not is_excluded(base_path):
            files.append(base_path)
    return files

# Chargement de la source
try:
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        sources_data = json.load(f)
except Exception as e:
    print(f"Erreur lecture SOURCE: {e}")
    exit(1)

# Normalisation des chemins (la source peut contenir des fichiers ou dossiers)
sources_list = []
for item in sources_data:
    if isinstance(item, str):
        sources_list.append(item)
    elif isinstance(item, dict) and "path" in item:
        sources_list.append(item["path"])

all_files = set()
for src in sources_list:
    files = discover_files(src)
    all_files.update(files)

# Déduplication et tri
unique_files = sorted(list(all_files))

print(f"Fichiers uniques à traiter : {len(unique_files)}")

# Traitement
inventory_json = {"meta": {"generé_par": "JARVIS-00-01", "script_date": None}, "documents": []}
md_lines = ["# Inventaire Local JARVIS - Mission 00", "", "**Statut :** Chargement machine intégral, interprétation non exhaustive.", ""]

errors_count = 0

for filepath in unique_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calcul SHA256
        sha256_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        # Extraction métadonnées
        meta = extract_metadata(content, filepath)
        
        doc_entry = {
            "chemin_absolu": filepath,
            "sha256": sha256_hash,
            "contenu": meta
        }
        inventory_json["documents"].append(doc_entry)
        
        # Ligne MD
        md_lines.append(f"## {meta['titre']}")
        md_lines.append(f"- **Chemin :** `{filepath}`")
        md_lines.append(f"- **Mission :** {meta['mission']}")
        md_lines.append(f"- **Date :** {meta['date']}")
        md_lines.append(f"- **Type :** {meta['type']}")
        md_lines.append(f"- **Intégrité (SHA256) :** `{sha256_hash[:16]}...`")
        md_lines.append("")
        
    except Exception as e:
        print(f"Erreur lecture {filepath}: {e}")
        errors_count += 1
        continue

# Mise à jour de la date avec l'heure réelle du script (pas d'invention)
import datetime
inventory_json["meta"]["script_date"] = datetime.datetime.now().isoformat() + "Z"

# Écriture JSON
try:
    with open(JSON_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(inventory_json, f, ensure_ascii=False, indent=2)
    print(f"JSON écrit : {JSON_OUTPUT}")
except Exception as e:
    print(f"Erreur écriture JSON: {e}")

# Écriture MD
try:
    with open(MD_OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    print(f"MD écrit : {MD_OUTPUT}")
except Exception as e:
    print(f"Erreur écriture MD: {e}")

print(f"\nTraitement terminé.")
print(f"Fichiers traités avec succès : {len(inventory_json['documents'])}")
print(f"Erreurs rencontrées : {errors_count}")
PYTHON_SCRIPT
