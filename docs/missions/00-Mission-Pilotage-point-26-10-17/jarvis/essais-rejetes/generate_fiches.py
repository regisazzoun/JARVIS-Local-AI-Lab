#!/usr/bin/env python3
"""
Script d'extraction des fiches de mission pour JARVIS-00.
Lit les rapports mission*.md et les README missions, produit FICHES-MISSIONS-JARVIS.md.
"""

import os
import re
import json
from pathlib import Path

# Chemins de base
RAPPORT_DIR = "/home/adminjarvis/JARVIS/rapports"
DOC_BASE = "/home/adminjarvis/JARVIS-Doc*/missions"
OUTPUT_FILE = "/var/lib/jarvis/projects/mission00/FICHES-MISSIONS-JARVIS.md"
OUTPUT_JSON = "/var/lib/jarvis/projects/mission00/fiches_missions.json"

def read_file_safe(path):
    """Lit un fichier en gérant les erreurs"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[Erreur lecture] {path}: {e}")
        return None

def extract_mission_info(content, filepath):
    """Extrait les informations d'une mission depuis son contenu"""
    info = {
        'chemin': filepath,
        'titre': '',
        'objectif': '',
        'materiel': [],
        'resultats': [],
        'reserves': [],
        'dependances': [],
        'niveau_lecture': 'basique'
    }
    
    if not content:
        return info
    
    lines = content.split('\n')
    
    # Détection du titre (premier titre H1 ou H2)
    for line in lines[:50]:
        if line.startswith('#'):
            title_match = re.sub(r'^#+\s*', '', line.strip())
            if title_match:
                info['titre'] = title_match
                break
    
    # Extraction par sections
    current_section = None
    for line in lines:
        # Détection des sections
        section_match = re.match(r'^(#\s*|\*\s*|===)\s*(matériel|composants|resultat|résultat|objectif|but|materiel|analyse|reserves|réserves|dependances|dépendances|conclusion|lecture|niveau)', line, re.IGNORECASE)
        
        if section_match:
            current_section = section_match.group(2).lower()
            continue
        
        # Attribution du contenu selon la section active
        if current_section:
            if 'materiel' in current_section or 'composants' in current_section:
                info['materiel'].append(line.strip())
            elif 'resultat' in current_section or 'analyse' in current_section:
                info['resultats'].append(line.strip())
            elif 'reserve' in current_section:
                info['reserves'].append(line.strip())
            elif 'dependance' in current_section:
                info['dependances'].append(line.strip())
            elif 'objectif' in current_section and not info['objectif']:
                info['objectif'] = line.strip()
    
    # Détermination du niveau de lecture
    if any(k in content.lower() for k in ['expert', 'avancé', 'technique']):
        info['niveau_lecture'] = 'avancé'
    elif any(k in content.lower() for k in ['débutant', 'basique', 'simple']):
        info['niveau_lecture'] = 'basique'
    
    return info

def glob_readme_paths():
    """Trouve tous les chemins de type JARVIS-Doc*/missions/mission-*/README.md"""
    base_path = Path("/home/adminjarvis/")
    paths = []
    
    # Recherche des dossiers JARVIS-Doc*
    for item in base_path.iterdir():
        if item.is_dir() and 'JARVIS-Doc' in item.name:
            missions_dir = item / "missions"
            if missions_dir.exists():
                # Recherche des sous-dossiers mission-*
                for mission_item in missions_dir.iterdir():
                    if mission_item.is_dir() and mission_item.name.startswith('mission-'):
                        readme = mission_item / "README.md"
                        if readme.exists():
                            paths.append(str(readme))
    
    return paths

def main():
    print("[START] Génération des fiches de mission JARVIS")
    
    all_missions = {}
    processed_files = []
    
    # 1. Lecture des rapports mission*.md
    if os.path.isdir(RAPPORT_DIR):
        for filename in sorted(os.listdir(RAPPORT_DIR)):
            if filename.startswith('mission') and filename.endswith('.md'):
                filepath = os.path.join(RAPPORT_DIR, filename)
                content = read_file_safe(filepath)
                
                if content:
                    # Extraction de l'ID de mission du nom du fichier
                    # Formats attendus: mission04A.md, mission05B.md, etc.
                    id_match = re.search(r'mission([0-9]+[A-Z]*)\.md', filename)
                    if id_match:
                        mission_id = f"{id_match.group(1)}"
                        
                        info = extract_mission_info(content, filepath)
                        
                        # Regrouper par ID de mission (sans les lettres non attestées)
                        base_id = re.match(r'([0-9]+)', mission_id).group(1) if re.match(r'([0-9]+)', mission_id) else mission_id
                        
                        if base_id not in all_missions:
                            all_missions[base_id] = {
                                'versions': [],
                                'info': info
                            }
                        
                        # Ajouter cette version comme une sous-mission spécifique
                        all_missions[base_id]['versions'].append({
                            'id_complet': mission_id,
                            'chemin': filepath,
                            'content_info': info
                        })
                        
                        processed_files.append(filepath)
                    else:
                        print(f"[WARN] Pas d'ID extrait de {filename}")
    
    # 2. Lecture des README missions
    readme_paths = glob_readme_paths()
    for filepath in readme_paths:
        content = read_file_safe(filepath)
        
        if content:
            # Extraire l'ID du chemin
            path_parts = filepath.split('/')
            mission_folder = None
            for part in path_parts:
                if part.startswith('mission-'):
                    mission_folder = part
                    break
            
            if mission_folder:
                id_match = re.search(r'mission-(\d+[A-Z]*)', mission_folder)
                if id_match:
                    mission_id = f"{id_match.group(1)}"
                    base_id = re.match(r'(\d+)', mission_id).group(1) if re.match(r'(\d+)', mission_id) else mission_id
                    
                    info = extract_mission_info(content, filepath)
                    
                    if base_id not in all_missions:
                        all_missions[base_id] = {
                            'versions': [],
                            'info': info
                        }
                    
                    all_missions[base_id]['versions'].append({
                        'id_complet': mission_id,
                        'chemin': filepath,
                        'content_info': info
                    })
                    
                    processed_files.append(filepath)
    
    print(f"[INFO] {len(all_missions)} missions de base identifiées")
    print(f"[INFO] {len(processed_files)} fichiers traités")
    
    # 3. Génération du fichier markdown
    output_lines = []
    output_lines.append("# FICHES DE MISSIONS JARVIS - EXTRACTION AUTOMATIQUE")
    output_lines.append("## Généré par script d'extraction locale\n")
    
    fiche_counter = 0
    
    for base_id in sorted(all_missions.keys(), key=lambda x: int(x) if x.isdigit() else (len(x), x)):
        mission_data = all_missions[base_id]
        
        # Si pas de versions, utiliser l'info par défaut
        if not mission_data['versions']:
            info = mission_data['info']
            output_lines.append(f"## Fiche Mission {base_id}")
            output_lines.append("")
            
            if info['titre']:
                output_lines.append(f"**Titre:** {info['titre']}")
                output_lines.append("")
            
            if info['objectif']:
                output_lines.append(f"**Objectif:** {info['objectif']}")
                output_lines.append("")
            
            output_lines.append("**Chemin:** " + info['chemin'])
            output_lines.append("")
            
            if info['materiel']:
                output_lines.append("**Matériel/Composants:**")
                for item in info['materiel'][:10]:  # Limiter à 10 items
                    output_lines.append(f"  - {item}")
                output_lines.append("")
            
            if info['resultats']:
                output_lines.append("**Résultats/Extraits:**")
                for item in info['resultats'][:5]:
                    output_lines.append(f"  - {item}")
                output_lines.append("")
            
            if info['reserves']:
                output_lines.append("⚠️ **Réserves:**")
                for item in info['reserves']:
                    output_lines.append(f"  - {item}")
                output_lines.append("")
            
            if info['dependances']:
                output_lines.append("📋 **Dépendances:**")
                for item in info['dependances']:
                    output_lines.append(f"  - {item}")
                output_lines.append("")
            
            output_lines.append(f"**Niveau de lecture:** {info['niveau_lecture']}")
            output_lines.append("")
            output_lines.append("---\n")
            fiche_counter += 1
        
        # Pour les versions multiples (lettres A, B, C, etc.)
        else:
            for version in mission_data['versions']:
                info = version['content_info']
                fiche_counter += 1
                
                output_lines.append(f"## Fiche Mission {version['id_complet']}")
                output_lines.append("")
                
                if info['titre']:
                    output_lines.append(f"**Titre:** {info['titre']}")
                    output_lines.append("")
                
                if info['objectif']:
                    output_lines.append(f"**Objectif:** {info['objectif']}")
                    output_lines.append("")
                
                output_lines.append("**Chemin:** " + info['chemin'])
                output_lines.append("")
                
                if info['materiel']:
                    output_lines.append("**Matériel/Composants:**")
                    for item in info['materiel'][:10]:
                        output_lines.append(f"  - {item}")
                    output_lines.append("")
                
                if info['resultats']:
                    output_lines.append("**Résultats/Extraits:**")
                    for item in info['resultats'][:5]:
                        output_lines.append(f"  - {item}")
                    output_lines.append("")
                
                if info['reserves']:
                    output_lines.append("⚠️ **Réserves:**")
                    for item in info['reserves']:
                        output_lines.append(f"  - {item}")
                    output_lines.append("")
                
                if info['dependances']:
                    output_lines.append("📋 **Dépendances:**")
                    for item in info['dependances']:
                        output_lines.append(f"  - {item}")
                    output_lines.append("")
                
                output_lines.append(f"**Niveau de lecture:** {info['niveau_lecture']}")
                output_lines.append("")
                output_lines.append("---\n")
    
    # Écriture du fichier markdown
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"[SUCCES] Fichier créé: {OUTPUT_FILE}")
    print(f"[INFO] Nombre de fiches générées: {fiche_counter}")
    
    # 4. Génération du JSON si utile
    json_data = []
    for base_id, data in all_missions.items():
        if data['versions']:
            for ver in data['versions']:
                json_data.append({
                    'id_complet': ver['id_complet'],
                    'chemin': ver['content_info']['chemin'],
                    'titre': ver['content_info']['titre'],
                    'materiel_count': len(ver['content_info']['materiel']),
                    'resultats_count': len(ver['content_info']['resultats'])
                })
        else:
            json_data.append({
                'id_complet': base_id,
                'chemin': data['info']['chemin'],
                'titre': data['info']['titre'],
                'materiel_count': len(data['info']['materiel']),
                'resultats_count': len(data['info']['resultats'])
            })
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"[SUCCES] Fichier JSON créé: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
