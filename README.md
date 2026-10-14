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

## Pilotage — 14 octobre 2026

- Mission 13F : GO AVEC RÉSERVES.
- Mission 14 : déploiement Dell Precision, indépendant des applications.
- Mission 15A : application native macOS (Mac mini et MacBook).
- Mission 15B : application native iOS (iPhone et éventuellement iPad).
- Missions 15A et 15B réalisables en parallèle, avec API JARVIS commune.
- Installation iOS : Xcode pour les tests, Ad Hoc ou TestFlight à évaluer pour la diffusion privée ; PWA en solution alternative.

Les détails et les critères de validation sont décrits dans [ROADMAP.md](ROADMAP.md).
