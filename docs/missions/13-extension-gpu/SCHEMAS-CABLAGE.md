# Schémas fonctionnels — pas un brochage de raccordement

Les symboles A/B servent à repérer les deux sorties GPU signalées par le propriétaire. Ils ne sont ni des numéros de connecteurs Dell vérifiés ni une affectation de broches. La PDB réelle et ses références restent à observer.

## Distribution connue par déclaration

```mermaid
flowchart LR
  PSU[PSU Dell annoncé950W — plaque à relever] --> PDB[Carte de distribution — DP/N inconnu]
  PDB --> A[Sortie GPU A signalée]
  PDB --> B[Sortie GPU B signalée]
  PDB --> SYS[Autres liaisons système — détails à relever]
```

## Faisceaux existants

```mermaid
flowchart LR
  A[Sortie A] -. chemin à inventorier .-> H1[Faisceau actuel — DP/N et branches inconnus]
  B[Sortie B] -. chemin à inventorier .-> H2[Faisceau actuel — DP/N et branches inconnus]
  H1 -. affectation inconnue .-> G0[RTX3090 Dell0 reconnue]
  H2 -. affectation inconnue .-> G1[RTX3090 Dell1 reconnue]
```

Ce dessin **ne prétend pas** que les cartes sont réellement raccordées chacune à une seule sortie. Leur reconnaissance est observée ; leur chemin électrique n’est pas encore décrit par le propriétaire.

## Cible fonctionnelle conditionnelle

```mermaid
flowchart LR
  PDB[PDB/PSU qualifiés pour budget retenu] --> A[Départ GPU A qualifié]
  PDB --> B[Départ GPU B qualifié]
  A -. faisceau double uniquement si qualifié .-> C0[Deux prises GPU0 — nombre à confirmer physiquement]
  B -. faisceau double uniquement si qualifié .-> C1[Deux prises GPU1 — nombre à confirmer physiquement]
  C0 --> G0[RTX3090 Dell0]
  C1 --> G1[RTX3090 Dell1]
```

Il s’agit du besoin fonctionnel étudié, **pas d’une instruction de branchement autorisée sur le matériel non identifié**. Le tableau constructeur distingue deux/quatre6+2 selon châssis ; il ne qualifie pas deux3090350W ni chaque départ PDB.

## Matrice électrique à renseigner sur preuve

| Départ / cavité vue face contacts et verrou défini | Destination / cavité |12V/masse/sense/NC | Preuve constructeur ou mesure hors tension | Courant admissible démontré |
| --- | --- | --- | --- | --- |
| A — non relevé | Non relevée | Inconnu | Absente | Inconnu |
| B — non relevé | Non relevée | Inconnu | Absente | Inconnu |

Aucune numérotation ou polarité n’est inventée. Une carte fonctionnelle en lecture NVIDIA ne remplit pas ce tableau.
