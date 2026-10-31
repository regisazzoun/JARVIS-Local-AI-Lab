# Modèles, moteurs et consommateurs

| Machine | Port | Version | Modèles au catalogue | Chargé au relevé |
|---|---|---|---|---|
| Mac mini | 11434 | 0.40.3 | 3 | Qwen 3.5 27B |
| Dell 1 | 11435 | 0.40.3 | 6 | Qwen3-Coder-Next 80B |
| Dell 1 | 11434 | 0.40.3 | 6 | aucun |
| Dell 2 | aucun observé | non applicable | aucun observé | aucun processus d’inférence observé |

[Inventaire par modèle](modeles.csv) · [configuration et empreintes](preuves/configurations.json).

Les deux services Dell 1 utilisent `/var/lib/ollama/models` et exposent les mêmes digests. Les douze lignes de catalogue représentent six modèles dans un stockage partagé, pas douze copies. Les trois modèles historiques du Mac existent également sur Dell 1, avec les mêmes digests : cette duplication entre machines est réelle, mais sa suppression demanderait une analyse des usages et du secours. Aucun poids n’a été déplacé, téléchargé ou supprimé.

Le 27B du Mac représente 17,48 Go de poids et un contexte chargé de 16 384 tokens. Le 80B sur Dell 1 représente 51,74 Go de poids, un contexte chargé de 32 768 tokens et `size_vram` de 47,70 Go. Le même processus de calcul apparaît sur les deux GPU. Cela ne signifie pas que deux cartes constituent une mémoire monolithique. Le mappage RAM est documenté historiquement ; aucun nouvel offload de couches CPU n’est déduit de ces seules valeurs.

Les contextes théoriques des modèles, les valeurs par défaut des services et les contextes chargés sont trois informations distinctes. Le service peut afficher un défaut de 8 192 alors que le modèle est chargé à 32 768 par une requête explicite.

La configuration active place la conversation sur le Mac et les missions sur Dell 1:11435. Qwen Code appelle le relais local8091 ; il ne contacte pas directement le service Dell depuis son lanceur. Le profil Dell 2 reste désactivé comme nœud d’inférence. Les modèles 32B/70B sont présents mais non chargés à cet instant ; leur utilisation historique n’est pas niée.

Open WebUI possède encore un profil nommé « JARVIS — Qualité (Llama 3.1 8B) », mais `DEFAULT_MODELS` vaut le27B. Les profils outils/missions utilisent le27B et le profil de programmation le80B. La présence du nom Llama ne prouve plus sa sélection par défaut.

**Distribution des commandes et distribution des inférences restent distinctes.** Dell 2 peut exécuter du code sans héberger Ollama. Aucun nouveau benchmark, test de repli ou déploiement d’inférence Dell 2 dans ce bilan.
