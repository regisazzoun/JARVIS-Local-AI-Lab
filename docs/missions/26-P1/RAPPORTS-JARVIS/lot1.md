Mission e26946bff84d4e06ad395b969ffcd72f — lot1 terminé (rapport impossible en écriture : système en lecture seule).

Corrections :
- normalize() dans `labtool/codec.py` (hash codec.py = 7c20488f...) respecte la validation stricte Q1 : lève ValueError si 'count' absent ou non entier ≥0.

Exécutions :
- Inspect Dell1 (ref 40146) : `normalize({'count': 5})` → {'count': 5}, returncode=0.
- Test Dell2 (ref 40117) : validation Q1 passée, sortie "OK: Q1 validation passed", returncode=0.
- Acceptation Dell2 (ref 40117 avec source_ref=39844) : accepted=true, manifeste identique, validation indépendante confirmée.

Fichiers synchronisés : `labtool/codec.py` (source Dell1 ref 39844 → Dell2, même manifeste complet incluant tests).

Conclusion :
lot1 validé, Q1 satisfait. Rapport impossible à écrire (systeme en lecture seule). Lot2 en attente (dépendance).
