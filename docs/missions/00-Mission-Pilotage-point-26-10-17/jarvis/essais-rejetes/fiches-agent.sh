python3 << 'PYTHON_SCRIPT'
import os
import glob
import re
import json
from pathlib import Path

def extract_mission_info(filepath, file_type):
    """Extrait les informations pertinentes d'un fichier de mission."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = {
            'filepath': str(filepath),
            'file_size': os.path.getsize(filepath),
            'file_type': file_type,
            'title': '',
            'objective': '',
            'components': [],
            'results': [],
            'reserves': [],
            'dependencies': [],
            'content_excerpt': ''
        }
        
        # Extraction basique du titre (premier H1 ou ligne avec "Mission")
        lines = content.split('\n')
        for line in lines[:20]:  # Premier 20 lignes pour le titre
            if line.startswith('#') or 'mission' in line.lower():
                info['title'] = line.strip().lstrip('#').strip()
                break
        
        # Extraction de sections pertinentes
        sections = {
            'composants': ['matériel', 'composant', 'hardware', 'pièces'],
            'résultats': ['résultat', 'succès', 'échec', 'output', 'production'],
            'réserves': ['réserve', 'limite', 'problème', 'warning', 'note'],
            'dépendances': ['dépendance', 'prérequis', 'nécessaire', 'depends']
        }
        
        for section, keywords in sections.items():
            for line in lines:
                line_lower = line.lower()
                if any(kw in line_lower for kw in keywords):
                    extracted_line = line.strip().lstrip('-').strip()
                    if extracted_line and len(extracted_line) < 200:
                        info[section].append(extracted_line)
        
        # Extrait court du contenu
        if content:
            words = content.split()[:50]
            info['content_excerpt'] = ' '.join(words) + '...'
        
        return info
    
    except Exception as e:
        return {'error': str(e), 'filepath': str(filepath)}

def generate_fiches_missions():
    """Génère les fiches missions à partir des fichiers disponibles."""
    
    # Chemins de recherche
    mission_md_patterns = [
        '/home/adminjarvis/JARVIS/rapports/mission*.md',
        '/home/adminjarvis/JARVIS-Doc*/missions/mission-*/README.md'
    ]
    
    all_missions = {}
    
    # Recherche des fichiers
    for pattern in mission_md_patterns:
        files = glob.glob(pattern)
        print(f"Pattern {pattern}: {len(files)} fichiers trouvés")
        
        for filepath in files:
            try:
                info = extract_mission_info(filepath, 'markdown')
                
                # Extraction de l'identifiant de mission
                filename = os.path.basename(filepath)
                # Recherche de pattern "missionXX" ou "mission-XX"
                match = re.search(r'mission[-_]?(\d+)', filename, re.IGNORECASE)
                if match:
                    mission_id = f"mission{match.group(1).zfill(2)}"
                    
                    if mission_id not in all_missions:
                        all_missions[mission_id] = {
                            'files': [],
                            'titles': set(),
                            'objectives': set(),
                            'components': set(),
                            'results': set(),
                            'reserves': set(),
                            'dependencies': set()
                        }
                    
                    all_missions[mission_id]['files'].append(info)
                    if info.get('title'):
                        all_missions[mission_id]['titles'].add(info['title'])
                    for comp in info.get('composants', []):
                        all_missions[mission_id]['components'].add(comp)
                    for res in info.get('résultats', []):
                        all_missions[mission_id]['results'].add(res)
                    for res in info.get('réserves', []):
                        all_missions[mission_id]['reserves'].add(res)
                    for dep in info.get('dépendances', []):
                        all_missions[mission_id]['dependencies'].add(dep)
                        
            except Exception as e:
                print(f"Erreur avec {filepath}: {e}")
    
    return all_missions

def create_fiches_documentation(missions_data):
    """Crée le fichier de documentation des fiches missions."""
    
    output_dir = Path('/var/lib/jarvis/projects/mission00')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'FICHES-MISSIONS-JARVIS.md'
    json_file = output_dir / 'MISSIONS_INDEX.json'
    
    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write("# FICHES MISSIONS JARVIS\n")
        md_file.write(f"*Généré automatiquement - {len(missions_data)} missions identifiées*\n\n")
        
        mission_count = 0
        for mission_id, data in sorted(missions_data.items()):
            mission_count += 1
            md_file.write(f"## {mission_id.upper()}\n\n")
            
            # Chemins des fichiers sources
            md_file.write("**Fichiers sources:**\n")
            for file_info in data['files']:
                md_file.write(f"- `{file_info['filepath']}` ({file_info['file_size']} octets)\n")
            md_file.write("\n")
            
            # Titre et objectif
            if data['titles']:
                md_file.write("**Titres/Objectifs:**\n")
                for title in data['titles']:
                    md_file.write(f"- {title}\n")
                md_file.write("\n")
            
            # Composants/Matériel
            if data['components']:
                md_file.write("**Matériel/Composants identifiés:**\n")
                for comp in list(data['components'])[:10]:  # Limité à 10
                    md_file.write(f"- {comp}\n")
                md_file.write("\n")
            
            # Résultats pertinents
            if data['results']:
                md_file.write("**Extraits résultats:**\n")
                for res in list(data['results'])[:5]:
                    md_file.write(f"- {res}\n")
                md_file.write("\n")
            
            # Réserves/Limites
            if data['reserves']:
                md_file.write("**Réserves/Dépendances:**\n")
                for res in list(data['reserves'])[:5]:
                    md_file.write(f"- {res}\n")
                md_file.write("\n")
            
            # Niveau de lecture (estimé basé sur la complexité)
            complexity = "élémentaire"
            if len(str(data)) > 5000:
                complexity = "avancé"
            elif len(str(data)) > 2000:
                complexity = "intermédiaire"
            
            md_file.write(f"**Niveau de lecture:** {complexity}\n")
            md_file.write("---\n\n")
    
    # Création du fichier JSON d'index
    json_data = {
        'mission_count': len(missions_data),
        'generated_for': 'mission00',
        'missions': {
            mid: {
                'file_count': len(data['files']),
                'has_title': bool(data['titles']),
                'component_count': len(data['components']),
                'result_count': len(data['results'])
            }
            for mid, data in missions_data.items()
        }
    }
    
    with open(json_file, 'w', encoding='utf-8') as jf:
        json.dump(json_data, jf, indent=2, ensure_ascii=False)
    
    return mission_count, output_file, json_file

# Exécution principale
if __name__ == "__main__":
    print("=== DÉBUT EXPLORATION MISSIONS JARVIS ===")
    
    # Extraction des missions
    missions_data = generate_fiches_missions()
    
    if not missions_data:
        print("Aucune mission trouvée - vérification des chemins...")
        # Vérification manuelle des répertoires
        check_dirs = [
            '/home/adminjarvis/JARVIS/rapports/',
            '/home/adminjarvis/JARVIS-Doc/',
            '/home/adminjarvis/JARVIS-Docs/'
        ]
        for dir_path in check_dirs:
            if os.path.exists(dir_path):
                print(f"Répertoire {dir_path} existe")
                files = os.listdir(dir_path)
                print(f"  Contient {len(files)} éléments")
                if files:
                    print(f"  Échantillon: {files[:5]}")
            else:
                print(f"Répertoire {dir_path} inexistant")
        
        # Écriture d'un fichier vide avec message si rien trouvé
        output_dir = Path('/var/lib/jarvis/projects/mission00')
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / 'FICHES-MISSIONS-JARVIS.md', 'w') as f:
            f.write("# FICHES MISSIONS JARVIS\n\n")
            f.write("Aucune mission trouvée dans les chemins standards.\n")
            f.write("Vérifiez la structure du répertoire JARVIS.\n")
        print("Fichier vide créé - aucune mission identifiée")
    else:
        # Création de la documentation
        count, md_path, json_path = create_fiches_documentation(missions_data)
        
        print(f"\n=== RÉSULTATS ===")
        print(f"Missions identifiées: {count}")
        print(f"Fichier fiches créé: {md_path}")
        print(f"Fichier index JSON créé: {json_path}")
        print(f"Taille fichier MD: {os.path.getsize(md_path)} octets")
        
        # Affichage résumé par mission
        for mission_id, data in sorted(missions_data.items())[:5]:  # Top 5
            print(f"\n{mission_id}: {len(data['files'])} fichier(s), {len(data['titles'])} titre(s)")

PYTHON_SCRIPT