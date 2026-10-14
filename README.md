# JARVIS — Local AI Lab

Laboratoire expérimental d'IA locale sur **Mac mini + eGPU NVIDIA**, avec une seconde plateforme prévue sur **Dell Precision 5820 (2 × RTX 3090)**.

## Objectif

Documenter les tests reproductibles, les échecs, les contournements et les limites sans confondre hypothèses et résultats validés. L'objectif est d'avancer vers la faisabilité, pas de résoudre chaque anomalie secondaire avant de continuer.

## État documenté — 12 octobre 2026

| Composant | Mac mini | Dell Precision 5820 |
| --- | --- | --- |
| Debian et SSH | Documentés (mission 03) | Prévus |
| Pilote NVIDIA / eGPU | Missions 04–05 | Prévus |
| Calcul CUDA réel | Validé (mission 05D) | Non testé |
| Ollama / Llama 3.1 8B | Inférence GPU validée (05D) | Non testé |
| Open WebUI | Fonctionnel sur LAN (06) | Non testé |
| Optimisations conversation / RAG | Tests documentés (07) | Non testé |

**Attention :** les résultats Mac mini ne constituent pas des validations sur Dell.

## Documentation

- [Chronologie des missions](docs/chronologie.md)
- [Méthodologie expérimentale](docs/methodologie.md)
- [Mac mini](platforms/mac-mini/README.md)
- [Dell Precision 5820](platforms/dell-precision-5820/README.md)
- [Feuille de route](ROADMAP.md)
- [Précautions de publication](SECURITY-PUBLICATION.md)

## Sources et confidentialité

Synthèse initiale des rapports de mission Codex reçus. Les preuves brutes, logs et données privées ne sont pas importés dans le dépôt. Chaque résultat reste à confronter au rapport source avant de publier un guide reproductible.

## Centre documentaire consolidé — 14 octobre 2026

La synthèse historique ci-dessus est conservée telle qu'elle a été rédigée au 12 octobre ; elle ne constitue pas un état actuel du serveur. Pour consulter les preuves collectées jusqu'au 14 octobre :

- **[Entrée par thèmes et navigation complète](docs/README.md)**
- [Inventaire des missions 01 à 13 et sous-missions](indexes/INVENTAIRE.md)
- [Chronologie détaillée](indexes/CHRONOLOGIE.md)
- [État technique démontré et limites](indexes/ETAT_TECHNIQUE.md)
- [Rapport de consolidation et exclusions](indexes/RAPPORT_FINAL.md)
- [Travaux restant à documenter, dont 13F](docs/04-suivi/README.md)

La réorganisation est **non destructive** : archives, rapports et chemins historiques demeurent accessibles. La branche documentaire ne contient pas de modifications d'installation ni de déploiement du serveur.
