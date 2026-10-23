# Sortie originale JARVIS — erreurs conservées

Ce texte brut peut contenir des erreurs. L’erratum et les preuves de réception prévalent. Adresses privées masquées uniquement ; aucune correction silencieuse.

**Mission 28A - Étape 1 terminée.**

Les deux modèles candidats sont installés et vérifiés sur Dell-1 (port 11435) :
- **Qwen3.5:27b-q4_K_M** (16.28 Go, SHA256 `64ae5b...`) — substitut optimal à `qwen3:32b` inexistant.
- **Llama3.3:70b-instruct-q4_K_M** (39.60 Go, SHA256 `a6eb47...`).

Correction appliquée : passage de GET à POST sur l'API Ollama pour résoudre l'erreur 405 initiale. Aucune inférence lancée, services partagés préservés. Logs complets persistants en `/opt/jarvis-lab/mission28a/logs/`. Rapport d'intervention enregistré. Prêt pour les tests de comparaison qualitative suivant les directives Codex.
