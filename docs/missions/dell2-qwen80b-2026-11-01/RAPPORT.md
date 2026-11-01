# Dell 2 — vérification de Qwen3-Coder-Next 80B

Date : 1er novembre 2026. Publication des résultats sans détails d’infrastructure.

**✅ Présence et exécution réelle confirmées.** Une requête adressée directement au moteur de Dell 2 avec Qwen3-Coder-Next 80B a produit une réponse correcte. Cette conclusion repose sur une inférence exécutée, et non sur une liste de modèles copiés.

## Résultats observés

- Calcul demandé : 17 × 23 ; réponse obtenue : 391.
- Génération de code : formule de somme des carrés de 0 à n inclus ; résultat vérifié sur six valeurs (0, 1, 2, 10, 100 et 1000), six réussites.
- Contexte configuré et chargé lors du test : 32 768 tokens ; cela ne constitue pas un test avec 32 768 tokens d’entrée.
- Un second moteur d’inférence a répondu correctement à 6 × 7 : 42.
- Les services de calcul contrôlés et la supervision étaient fonctionnels.

Aucune réinstallation nécessaire. Aucun redémarrage de service, aucune modification de configuration et aucune intervention sur Dell 1 pendant cette vérification.

## Limites et conservation des preuves

La vérification ne réceptionne pas l’autonomie complète de JARVIS, les appels d’outils natifs, le parcours Launcher/WebUI, les charges longues ou le contexte maximal du modèle. Une réponse de code contenait des balises Markdown malgré la consigne de code seul.

Les preuves techniques détaillées et le compte rendu complet sont conservés hors du dépôt public. Cette version publique exclut les adresses, les accès, les chemins privés, les noms d’unités, les ports, les versions de services et les inventaires matériels. Les observations antérieures restent historiques ; aucun succès rétroactif n’est attribué aux missions 14/14A.

Archive additive sur une branche dédiée, sans remplacement de l’historique ni fusion automatique dans main.
