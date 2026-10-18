# 21.05 — Modification réelle du Dell par JARVIS
**Cible :** Dell n°1 seulement, profil `dell-observe` administrable de 11B.
**Action :** vérifier identité cible et SSH/Ansible ; créer ou actualiser sur Dell un petit fichier de configuration ou script de collecte non critique, utile à la supervision (dans un emplacement autorisé). Vérifier à distance par une seconde lecture et, avec Ansible, une seconde passe idempotente. Documenter le changement exact, l'accès utilisé, les preuves avant/après et le retour arrière réalisable.
**Résultat :** `RAPPORTS/05-ADMINISTRATION-DELL.md`.
**Réception :** une mutation réelle du Dell est prouvée ; SSH seul ne suffit pas. Ne toucher ni au RAID, au BIOS, aux disques, aux clés SSH ni aux services critiques. Puis tâche 06.
