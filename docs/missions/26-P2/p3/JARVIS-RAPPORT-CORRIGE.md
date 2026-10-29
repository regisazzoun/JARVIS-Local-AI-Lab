P3-02-run validé avec validation croisée indépendante Codex55251.  
Test55057 (Dell1) : fichier lu via `cat`, stdout = 219000 octets, SHA vérifié.  
Test55210 (Dell2) : fichier = 859999 octets, stdout = 283 octets, SHA256 = f49035ce... inchangé.  
Checkpoint54911/redémarrage54915/reprise54930 : PID70821→71255, compteurs conservés.  
Core.ollama n’est pas l’exécutable invoqué ; original inexistant, lectures stériles arrêtées après 3.  
Un seul artefact Dell2 observé, pas d’idempotence universelle.  
P3 complète : tests volumineux réussis, reprise opérationnelle confirmée, rapport canonical généré (SHA256 5ad719f6...).  
P4 non déclenchée, limites respectées.