# Mission 13E — architecture

Client navigateur → accès SSH localhost actuel / HTTPS privé futur → authentification passerelle → orchestrateur identité/mémoire/outils → Ollama existant. STT et TTS sont des workers CPU temporaires avec ressources 13A en lecture seule ; aucun service cloud. Piper Tom reste la voix sélectionnée. SQLite est la seule autorité mémoire, jamais une base séparée par moteur.

Schéma v2 : conversations, messages, memories, audit, documents, tool_audit, schema_version et index FTS5. Migration v1→v2 additive transactionnelle et testée sur fixtures ; les données existantes sont sauvegardées avant migration. Souvenirs : pending/approved/rejected, type persistent/project/temporary, active et expires. Obsolescence retire l’index actif. Déduplication normalise espaces/casse, proposition sérialisée en transaction ; correction refuse un contenu déjà actif identique. La suppression retire le souvenir et FTS, garde seulement trace d’opération/ID/date ; elle n’efface pas l’historique automatiquement.

Documents et résultats documentaires sont séparés des souvenirs personnels validés. Un document technique JARVIS est présent, sans fait personnel promu. Recherche lexicale avec projet, souvenirs globaux et limite de passages. Identité `identity/JARVIS-v1.md` versionnée, budget de contexte borné, historique glissant et passages tronqués. Trois modèles substituables : Qwen, Ministral, Llama.

Registre : system_status, disk_usage, jarvis_services, software_versions en lecture seule ; propose_memory autorisé uniquement pour créer une attente de validation. Schémas d’arguments fermés, noms allowlistés, commandes fixes sans shell, timeouts subprocess 8 s/HTTP 4–5 s/SQLite 10 s, journal outil minimal, risque read_only ou pending_write. Un outil inconnu ou de risque supérieur est refusé. Boucle LLM plafonnée à 2 tours d’outils et 4 appels par tour. Aucun shell root, Ansible, PXE, RAID ou action modificatrice système implémenté.

Authentification/CSRF/CSP protègent la passerelle locale ; APIs Ollama et vocales ne sont pas exposées au client distant. Sessions en RAM et expiration 8 h ; données persistantes indépendantes des connexions. Aucun raccordement aux conversations ou mémoire Open WebUI : seule cette passerelle possède l’autorité canonique JARVIS.

Sources techniques consultées : [Ollama Tool calling](https://docs.ollama.com/capabilities/tool-calling), [API chat](https://docs.ollama.com/api/chat). Le contrat message assistant/tool est utilisé avec les modèles réellement installés, sans changer le service Ollama.
