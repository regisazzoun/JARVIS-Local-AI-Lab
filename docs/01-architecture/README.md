# Architecture et plateformes

JARVIS est un laboratoire d'IA locale expérimental articulé autour d'une plateforme Mac mini et d'une seconde plateforme Dell Precision 5820 envisagée. Les validations sur une machine **ne valent pas validation sur l'autre**.

## Références

- [Description générale du projet](../../README.md)
- [Plateforme Mac mini](../../platforms/mac-mini/README.md)
- [Plateforme Dell Precision 5820](../../platforms/dell-precision-5820/README.md)
- [Décisions techniques tracées](../../indexes/DECISIONS.md)
- [Feuille de route originale](../../ROADMAP.md)
- [Méthodologie expérimentale](../methodologie.md)

## Frontières de validation

Sur Mac mini, les archives documentent les phases Debian/T2, eGPU, pilote NVIDIA, CUDA, inférences Ollama, services et composants de JARVIS. Pour le Dell, les intentions RAID NVMe, PXE, GPU et automatisation restent à confirmer par essais dédiés.

Ne pas modifier de partitions, RAID, firmware, réseau ou services à partir de cette synthèse : elle sert de navigation, non de procédure de déploiement.
