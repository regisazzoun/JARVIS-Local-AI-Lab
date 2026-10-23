# Références et niveau de preuve

Aucun faisceau double n’est recommandé à l’achat ou reçu électriquement pour le montage présent. Les deux cartes identiques Dell OEM sont déclarées par le propriétaire ; leur DP/N exact et le câblage de leurs prises restent à relever.

| Référence | Ce qui a réellement été trouvé | Niveau et usage possible |
| --- | --- | --- |
| TV5X6 / VVFXD | Références évoquées par le propriétaire ; catalogues les présentent comme ensembles/cartes de distribution | Candidats d’identification PDB, pas une référence de faisceau double qualifié ; aucune correspondance broche à broche constructeur retrouvée |
| 76VYK /076VYK | Candidat de faisceau simple VGA1,8 vers6+2, présenté pour5820/7820 | Référence à confronter au faisceau présent ; aucune aptitude à alimenter deux prises350W démontrée |
| G3W07 | Autre candidat de faisceau simple proposé pour5820 | Longueur, révision, brochage et interchangeabilité non qualifiés ici |
| 8MC3R | Candidat de faisceau Precision souvent associé au7920 | L’association commerciale à une gamme ne suffit pas à qualifier le5820 présent ni un dédoublement |
| D92C9 | Candidat fréquemment associé au5810 et à des sorties6broches | Ne pas l’assimiler à un double6+2 adapté au5820 sans documentation exacte |
| Faisceau propriétaire vers deux6+2, sans DP/N | Type recherché pour remplacer les deux faisceaux, si chaque sortie est qualifiée pour cette charge | Non identifié de façon probante ; aucun pinout ni courant admissible obtenu |

Les [catalogues TV5X6/VVFXD](https://www.ascendtech.com/products/dell-t5820-distribution-board-tv5x6/tdwpdbdelltv5x6), [76VYK](https://www.eetgroup.com/en-gb/76vyk-dell-8-pin-to-6-pin-2-pin-power-cable-for-precision-workstations-wid-w124434148) et [autres câbles](https://www.gekko-computer.de/en/c/Parts/Cable-Adapter/GPU-Power-Cable) sont des pistes commerciales, **pas les preuves techniques retenues pour autoriser un raccordement**. Les recherches n’ont pas livré de schéma électrique constructeur associé au DP/N réellement installé. Les ressemblances de prises, mentions «compatible» et retours de forums ne sont pas utilisés comme qualification électrique.

## Liste conditionnelle de composants

- Réutiliser les deux cartes possédées et le socle actuel ; aucun nouveau GPU n’est demandé.
- Deux faisceaux GPU identifiés pour la PDB/révision et la charge cible, avec le nombre de sorties requis : référence et quantités définitives en attente du relevé physique.
- Retenues mécaniques et ventilation selon place réelle ; aucune référence inventée.
- Aucun adaptateur SATA/Molex, câble modulaire d’une autre alimentation ou dérivation sur une prise CPU/10broches inconnue proposé.
- Aucun remplacement de PSU déclaré compatible : une puissance plus élevée annoncée pour un autre Precision ne prouve pas l’interchangeabilité mécanique ou électrique avec ce5820.
