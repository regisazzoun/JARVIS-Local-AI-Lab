# Mission 12 — preuves et échantillons

Début : 2026-10-12 22:18:28 UTC (13 octobre 00:18:28 Paris). Finalisation : 2026-10-12T22:35:33.161473+00:00. Recherche et essais terminés en moins d’une heure ; plafond 4 h + 1 h respecté, aucune prolongation artificielle.

- [Rapport](../mission12.md)
- [Lecteur local](ecoute.html) et `audio/` : neuf WAV synthétisés, trois voix, trois textes identiques.
- [Corpus](corpus.json), [validation WAV](audio-validation.json), `silence-fixture.wav` : fixture technique, pas voix candidate.
- [Synthèse des mesures](measurements-summary.json), `*-results.json`, `*-guard.json`, `*-run.log` : succès et traces reproductibles.
- [Mémoire 16/16](memory-results.json), [source démo](memory_demo.py), bases `*-fictive.sqlite` / `*-fictif.sqlite` : données fictives exclusivement.
- [Notes techniques](notes-techniques.md), [revue statique](static-review.json), `sources/`, `wheel-review/` : code/documentation publique examinés, licences préservées dans sources disponibles.
- [Manifest sources](source-manifest.json), [manifest modèles](download-manifest.json), [manifest wheels](wheel-manifest.json), `metadata/` : snapshots, SHA-256, dates/versions.
- [Lock temporaire testé](requirements-tested-cp313-linux.txt), `installed-temporary-packages.json` : 32 distributions, venv uniquement.
- `stt-first-attempt-*`, `stt-second-attempt-*`, `av-pin-*` : échecs puis correction du vocabulaire/PyAV, conservés.
- `before.json`, `after.json` : services, Ollama ps en GET et SHA de quatre fichiers ; pas de secrets/config en clair ni base WebUI copiée.
- `SHA256SUMS` : intégrité des livrables et de toutes les preuves.

Les modèles binaires/wheels/venv restent seulement dans `/tmp/jarvis-m12-EC3FOY`; leur disponibilité après reboot n’est pas présumée. Les sons et preuves dans JARVIS sont durables sur disque. Aucun script de preuve ne doit être lancé depuis ce répertoire en croyant qu’il est un service déployé : les scripts visent l’environnement temporaire et le scénario SQLite suppose une base neuve.

Échantillons sans données personnelles : phrases originales/fictives ; aucune capture de micro. Copies publiques comportant attributions d’auteur et notices de licence, aucun secret de JARVIS. Le modèle de langage n’a reçu aucun outil ni accès au serveur.

Contrôles finaux : 10 rubriques requises ; neuf WAV non silencieux ; 16 tests mémoire passés ; workers CPU retournés zéro après correction ; liens relatifs validés ; quatre hashes et deux états de services identiques, ps vide début/fin. Pas de qualification audio subjective, de chatbot réel, de réseau/auth/effacement physique ou de reboot.
