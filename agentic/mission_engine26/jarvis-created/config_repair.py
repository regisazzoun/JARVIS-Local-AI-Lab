#!/usr/bin/env python3
"""
config_repair.py - Normalise une configuration JSON en corrigeant le port invalide.

Fonctionnalités:
- Lit un fichier JSON spécifié
- Corrige le champ 'port' si invalide (0 ou non-entier) vers 8091
- Préserve tous les autres champs
- Rejette proprement les fichiers JSON invalides
- Écriture idempotente

Usage: python3 config_repair.py --input <chemin> [--output <chemin>]
Si --output omis, écrase le fichier d'entrée.
"""

import argparse
import json
import sys
from pathlib import Path


def is_valid_port(value) -> bool:
    """Vérifie si la valeur est un port valide (entier 1-65535)."""
    if not isinstance(value, int):
        return False
    if isinstance(value, bool):  # bool est sous-type de int en Python
        return False
    return 1 <= value <= 65535


def repair_config(input_path: Path, output_path: Path) -> dict:
    """
    Lit un fichier JSON, corrige le port si nécessaire, écrit le résultat.
    
    Args:
        input_path: Chemin vers le fichier JSON d'entrée
        output_path: Chemin vers le fichier de sortie (peut être identique)
    
    Returns:
        dict avec les clés 'status', 'message', 'original_port', 'new_port'
    
    Raises:
        json.JSONDecodeError: Si le fichier n'est pas un JSON valide
        FileNotFoundError: Si le fichier d'entrée n'existe pas
    """
    # Lecture du fichier
    try:
        content = input_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier non trouvé: {input_path}")
    
    # Parsing JSON - rejette proprement les erreurs de syntaxe
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"JSON invalide: {e.msg}",
            e.doc,
            e.pos
        )
    
    # Vérifie que c'est un dictionnaire (objet JSON)
    if not isinstance(data, dict):
        raise ValueError("Le fichier doit contenir un objet JSON (dictionnaire)")
    
    result = {
        'status': 'ok',
        'message': '',
        'original_port': None,
        'new_port': None
    }
    
    # Vérifie et corrige le port si présent
    if 'port' in data:
        original_port = data['port']
        result['original_port'] = original_port
        
        if not is_valid_port(original_port):
            data['port'] = 8091
            result['new_port'] = 8091
            result['message'] = f"Port corrigé: {original_port} → 8091"
        else:
            result['message'] = f"Port valide conservé: {original_port}"
    else:
        result['message'] = "Aucun champ 'port' trouvé, fichier inchangé"
    
    # Écriture idempotente (même format JSON)
    output_content = json.dumps(data, ensure_ascii=False, indent=2)
    output_path.write_text(output_content + '\n', encoding='utf-8')
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Normalise une configuration JSON en corrigeant le port invalide"
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        default=None,
        help="Chemin vers le fichier JSON d'entrée"
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=None,
        help="Chemin vers le fichier de sortie (défaut: écrase l'entrée)"
    )
    parser.add_argument(
        '--job', '-j',
        type=Path,
        default=None,
        help="Chemin vers un fichier job JSON contenant input_file et output_file"
    )
    
    args = parser.parse_args()
    
    # Si --job est fourni, lire les chemins depuis le fichier job
    if args.job:
        try:
            job_data = json.loads(args.job.read_text(encoding='utf-8'))
            input_path = Path(job_data['input_file'])
            output_path = Path(job_data['output_file'])
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(json.dumps({'status': 'error', 'message': f'Erreur lecture job file: {e}', 'original_port': None, 'new_port': None}, indent=2))
            sys.exit(1)
    elif args.input and args.output:
        input_path = args.input
        output_path = args.output
    elif args.input:
        input_path = args.input
        output_path = input_path  # écrase en place
    else:
        print(json.dumps({'status': 'error', 'message': 'Doit fournir --input ou --job', 'original_port': None, 'new_port': None}, indent=2))
        sys.exit(1)
    
    try:
        result = repair_config(input_path, output_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0)
    except json.JSONDecodeError as e:
        error_result = {
            'status': 'error',
            'message': f"JSON invalide: {e}",
            'original_port': None,
            'new_port': None
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
        sys.exit(1)
    except FileNotFoundError as e:
        error_result = {
            'status': 'error',
            'message': str(e),
            'original_port': None,
            'new_port': None
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        error_result = {
            'status': 'error',
            'message': f"Erreur inattendue: {e}",
            'original_port': None,
            'new_port': None
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
