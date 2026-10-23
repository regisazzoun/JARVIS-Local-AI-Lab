# Étude d’alimentation — conclusion partielle

**🟡 Non qualifiée électriquement.** Les deux RTX3090 sont maintenant reconnues, mais le chemin d’alimentation de la seconde, les références des faisceaux et les limites par sortie de distribution ne sont pas établis. La détection ne démontre ni le brochage ni la tenue sous charge. Aucune proposition de branchement sur une prise Dell inconnue n’est reçue.

## Ce que les sources établissent

La [fiche Dell5820](https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/Precision-5820-Tower-Spec-Sheet.pdf), page4, annonce600W graphiques au total et deux cartes de300W ; elle ne fournit pas le brochage des sorties. Le [guide Dell7920, tableau transversal page24, copie du document constructeur](https://www.pcdeal.no/file/standardmappe-uni/precision_7920_tower_technical_guidebook.pdf) distingue le5820 standard à deux prises6+2 des châssis RTX à câblage mis à jour pouvant en avoir quatre. Il indique aucune plateforme double GeForce3080/3090 prise en charge. Sa ligne commune320W ne remplace pas la puissance réelle du VBIOS3090 : les deux cartes du laboratoire annoncent350W chacune.

Cette configuration est donc expérimentale, hors qualification double3090 documentée par Dell. Un faisceau double ne crée ni puissance supplémentaire ni nouvelle capacité thermique. Les limites600W et300W concernent les cartes complètes, et ne signifient pas300W fournis par le seul connecteur PCIe de la carte mère.

## Budget de dimensionnement, pas mesure de consommation système

| Hypothèse de charge | GPU seuls | CPU de référence | Sous-total avant carte mère/RAM/disques/ventilateurs/pertes VRM | Reste arithmétique sur950W |
| --- | ---: | ---: | ---: | ---: |
| Deux cartes aux limites annoncées350W | 700W | 165W | 865W | 85W |
| Deux cartes plafonnées à300W, hypothèse non appliquée | 600W | 165W | 765W | 185W |
| Deux cartes plafonnées à250W, hypothèse non appliquée | 500W | 165W | 665W | 285W |

Le165W est le TDP [Intel du10980XE](https://www.intel.com/content/www/us/en/products/sku/198017/intel-core-i910980xe-extreme-edition-processor-24-75m-cache-3-00-ghz/specifications.html), pas un maximum système mesuré ni une borne garantie en turbo. Le950W est déclaré par le propriétaire ; SMBIOS ne fournit pas sa plaque. Les autres charges et les transitoires ne sont pas mesurés. Le premier scénario dépasse déjà l’enveloppe graphique Dell et ne démontre aucune marge correcte. Les deux autres sont des pistes de dimensionnement, sans qualification des faisceaux ni garantie sur les pointes/phase de démarrage ; aucune limite de puissance n’a été changée.

Le rendement ne doit pas être soustrait arbitrairement à la puissance DC nominale du bloc. La puissance à la prise diffère de la puissance GPU lue par NVIDIA. Les relevés de quelques dizaines de watts au repos ne remplacent pas ce budget.

## Contraintes par ligne

Pour chaque sortie PDB : intensité admissible, protection/OCP, brochage, section/contacts et éventuel partage avec une autre sortie restent inconnus. Même à250W par carte, aucun raccordement propriétaire n’est réputé sûr sans ces renseignements. Le calcul I=P/12 donne uniquement une intensité équivalente, pas une certification :350W représentent29,2A sur12V pour la carte complète ; sa répartition effective entre slot et prises auxiliaires n’est pas observée.

## Qualification à compléter

1. Relever hors tension DP/N/révision de PSU/PDB/faisceaux, marquages des sorties, prises des deux cartes et section des conducteurs. Documenter le montage effectivement utilisé, pas un dessin supposé.
2. Obtenir une correspondance constructeur pour cette révision et ces faisceaux, avec limites de courant. À défaut, faire établir par une personne compétente la continuité broche à broche du faisceau débranché et la qualification des sorties ; ne jamais mesurer une résistance sur circuit alimenté ni ouvrir le bloc secteur.
3. Numéroter les cavités depuis une vue et un verrouillage explicitement définis. Reporter12V, masse, sense et NC seulement après preuve. Le tableau reste vide dans SCHEMAS-CABLAGE.md tant que cette preuve manque.
4. Vérifier logement, refroidissement et espace entre cartes. Le BIOS ne mesure ni la température des contacts ni leur intensité.
5. Définir une enveloppe de puissance compatible avec l’ensemble qualifié, puis recevoir les essais ciblés. Un power limit logiciel ne répare pas un brochage inconnu.

Le propriétaire réalise les manipulations physiques. Aucune nouvelle approbation générale de mission n’est demandée ; les renseignements manquants sont une dépendance technique réelle.
