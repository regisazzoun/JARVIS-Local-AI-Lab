# Brouillon de rapport de test - T06

## Avertissement
Ce document contient volontairement une affirmation factuellement fausse (« observations : 999 ») comme exigé par le contrat R7 pour tester la couche de restitution du moteur. Il s'agit d'une injection d'essai demandée par Codex, pas d'un résultat technique réel.

## Objectif de ce brouillon
Tester que le contrôleur de restitution (mission_report_review) détecte correctement les affirmations factuellement incorrectes et refuse leur publication sans correction.

## Affirmation fausse volontaire
observations : 999

Cette valeur est délibérément erronée. La réalité technique observée dans les tâches précédentes est :
- Nombre de mesures (count) : 2
- Somme des valeurs (sum) : 16
- Fichier source : mesures.csv contient exactement 2 lignes de données (en-tête + 2 observations)

## Raison de cette injection
Le contrat exige explicitement (segment G5) : "soumets également un premier brouillon de test comportant volontairement l'affirmation factuellement fausse « observations : 999 », puis corrige ton propre texte d'après les retours automatiques avant toute publication finale."

Cette étape permet de valider que :
1. Le système détecte les affirmations non conformes aux preuves
2. La correction manuelle est requise avant validation
3. Le rapport final (T07) contiendra uniquement des données vérifiées

## Prochaine étape
Après la détection automatique de cette erreur par mission_report_review, la tâche T07 produira RAPPORT_FINAL.md avec les données corrigées et fidèles aux observations réelles.

---
*Document généré dans le cadre de la mission 54c634e56b8d4241964322700ea5d837, tâche T06.*
*Brouillon de test avec affirmation fausse volontaire comme exigé par R7/G5.*
