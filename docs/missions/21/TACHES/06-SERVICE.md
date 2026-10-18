# 21.06 — Installation de service de supervision
**Cible :** Dell n°1.
**Action :** vérifier ce qui existe ; installer seulement si nécessaire un service léger de collecte/supervision système compatible avec Debian 13, en réutilisant les outils autorisés. Préférer réemployer le script de 05 avec unité systemd/temporisateur plutôt qu'une lourde pile. Contrôler état, journaux, résultat concret et relance du service. Ne pas remplacer Ollama/SSH/SDDM ni modifier le boot.
**Résultat :** `RAPPORTS/06-INSTALLATION-SERVICE.md` avec composants, versions, commandes, tests et réserves.
**Réception :** service réellement présent, actif ou déclenchable et résultat observable ; paquet simplement installé ≠ réussite. Puis tâche 07.
