#!/usr/bin/env python3
"""
JARVIS Mission 23D — Lanceur de la passerelle temporaire Codex

Ce fichier ne fait qu'importer et exécuter codex_gateway.py qui fournit :
- HTTP loopback sur port 8783
- GET /health pour vérifier LiveKit Server
- GET /token pour générer des jetons signés TTL court terme
- POST /stop pour nettoyer la salle unique
- Service de fichiers fixtures via whitelist
- POST /test pour lancer codex_capture.py avec scénarios
- GET /test/<id> pour récupérer résultats et audio

La passerelle est un outil opérationnel fourni par Codex, pas une réimplémentation JARVIS.
Elle lit les credentials LiveKit depuis l'env privé du projet (jamais exposés).

Usage:
    python server.py --root /var/lib/jarvis/projects/mission23/mission23d --env /var/lib/jarvis/projects/mission23/livekit-agent/.env [--port 8783]

Pour exécution directe de la passerelle :
    python codex_gateway.py --root <dossier> --env <fichier-env> --port 8783
"""

import sys
from pathlib import Path

# Point d'entrée unique : importer et lancer codex_gateway
if __name__ == '__main__':
    # Construire les arguments par défaut si non fournis
    if len(sys.argv) == 1:
        # Arguments implicites pour le projet mission23d
        sys.argv = [
            'server.py',
            '--root', str(Path(__file__).parent.resolve()),
            '--env', str(Path(__file__).parent.parent / 'livekit-agent' / '.env'),
            '--port', '8783'
        ]
    
    # Importer la fonction main de codex_gateway et l'exécuter
    # Cela évite de dupliquer le code et garde une source unique de vérité
    import importlib.util
    gateway_path = Path(__file__).parent / 'codex_gateway.py'
    
    if not gateway_path.exists():
        print(f"ERREUR: Fichier passerelle manquant: {gateway_path}", file=sys.stderr)
        print("La passerelle temporaire Codex est requise pour les endpoints token/test/fixtures.", file=sys.stderr)
        sys.exit(1)
    
    spec = importlib.util.spec_from_file_location("codex_gateway", gateway_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Exécuter main() qui parse sys.argv et lance le serveur HTTP
        print("=" * 60)
        print("JARVIS Mission 23D — Passerelle temporaire Codex (via server.py)")
        print(f"Serveur: {gateway_path}")
        print(f"Root: {sys.argv[sys.argv.index('--root') + 1] if '--root' in sys.argv else 'défaut'}")
        print("=" * 60)
        module.main()
    else:
        print(f"ERREUR: Impossible de charger codex_gateway", file=sys.stderr)
        sys.exit(1)
