> **Trace de production, avec limites de réception.** Ce fichier conserve une sortie ou un assemblage de la mission 00 ; il ne remplace pas le registre consolidé. Voir les corrections Codex et le bilan agentique dans le dossier parent de mission. Les textes historiques ou propositions du modèle ne créent aucune nouvelle autorisation ou obligation de validation.

# Fiches historiques — Lot 08 (Mission00)
## Données extraites des rapports du 12 octobre 2026

---

### Fiche 05C : Premier test Quadro RTX 5000
**Titre/Fonction** : Test fonctionnel initial GPU.  
**Objectif** : Vérifier l’apparition et le pilotage de la Quadro RTX 5000 après branchement à chaud.  
**Matériel/Composants** : Quadro RTX 5000, noyau 6.18.54-1-t2-trixie, modules NVIDIA 10 empreintes conformes.  
**Actions/Résultats** : Branchement confirmé ; GPU détecté par PCIe et Xorg en ~1 min 48. Premier succès fonctionnel court (fenêtre 10 min non tenue). Inhibition veille testée puis levée.  
**Réserves/Preuves manquantes** : Stabilité prolongée et sous charge non démontrées. Retrait à chaud et démarrage avec Core non qualifiés.  
**Dépendances** : Pilotage NVIDIA actif, noyau T2.  
**Exécutant** : À confirmer (rapport daté 12/10/2026).  
**Chemin preuve** : `/home/adminjarvis/JARVIS/rapports/mission05C.md`.

---

### Fiche 05D : Calcul CUDA réel et première inférence GPU
**Titre/Fonction** : Validation calcul CUDA et inférence Ollama.  
**Objectif** : Exécuter un kernel PTX et une première requête LLM locale sur la Quadro.  
**Matériel/Composants** : Quadro RTX 5000, UUID [IDENTIFIANT GPU EXPURGÉ], NVIDIA 595.91.07, Python ctypes, libcuda.so.1.  
**Actions/Résultats** : Kernel PTX JIT (3*i+7) vérifié. Première réponse Llama 3.1 8B obtenue via Ollama. Incident réversible sur version PTX corrigé à 6.4.  
**Réserves/Preuves manquantes** : Stabilité sous charge prolongée non qualifiée. Configuration durable non finalisée.  
**Dépendances** : Pilotes NVIDIA, environnement Python, Ollama installé.  
**Exécutant** : À confirmer (rapport 12/10/2026).  
**Chemin preuve** : `/home/adminjarvis/JARVIS/rapports/mission05D.md` et dossier `mission05D-preuves/`.

---

### Fiche 06 : Open WebUI et utilisation quotidienne
**Titre/Fonction** : Déploiement interface web authentifiée pour LLM.  
**Objectif** : Rendre accessible Llama 3.1 8B via navigateur LAN avec persistance.  
**Matériel/Composants** : Serveur local, port 3000, Open WebUI, Quadro RTX 5000 pour inférence.  
**Actions/Résultats** : Interface authentifiée `admin@jarvis.local` fonctionnelle. 3 conversations testées conservées. Démarrage automatique configuré. Inférence GPU démontrée.  
**Réserves/Preuves manquantes** : Veille et retrait à chaud non qualifiés. Mot de passe initial à changer par l’administrateur.  
**Dépendances** : Open WebUI, Docker/container, accès LAN.  
**Exécutant** : À confirmer (rapport 12/10/2026).  
**Chemin preuve** : `/home/adminjarvis/JARVIS/rapports/mission06.md` et dossier `mission06-preuves/`.

---

### Fiche 07 : Compréhension, raisonnement et contexte
**Titre/Fonction** : Évaluation des capacités de raisonnement du modèle.  
**Objectif** : Tester fidélité documentaire, logique et gestion de contexte long sans changer les poids.  
**Matériel/Composants** : Même environnement que 06 (Open WebUI, Llama 3.1 8B, Quadro).  
**Actions/Résultats** : Surcouche paramètres créée (nom « JARVIS — Qualité »). Tests d’évaluation montrant amélioration mais limites persistantes de raisonnement. Aucun nouveau modèle installé.  
**Réserves/Preuves manquantes** : Capacités complexes non garanties ; résultats évalués sur jeu spécifique, pas généralisable sans nouvelle mission.  
**Dépendances** : Open WebUI configuré, paramètres ajustables.  
**Exécutant** : À confirmer (rapport 12/10/2026).  
**Chemin preuve** : `/home/adminjarvis/JARVIS/rapports/mission07.md` et dossier `mission07-preuves/`.

---

*Note : Ces fiches reprennent strictement les données des rapports historiques du 12 octobre 2026. Aucun état actuel n’est affirmé. Les identifiants matériels et logiciels cités sont ceux attestés dans les preuves associées.*
