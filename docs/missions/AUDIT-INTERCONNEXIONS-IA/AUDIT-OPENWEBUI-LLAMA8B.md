# Pourquoi Llama8B et pourquoi du JSON ask_user ?

## Cause démontrée du choix de modèle

Le compose existant impose `DEFAULT_MODELS=llama3.1:8b` et `ENABLE_PERSISTENT_CONFIG=false`. Le profil DB d'identifiant `llama3.1:8b`, `base_model_id=null`, renomme le modèle en **JARVIS — Qualité (Llama3.1 8B)** et ajoute un système,8192contexte, température0,1, top_p0,9 et2048sortie. Ce n'est ni une redirection vers27B, ni une copie de poids, ni une sélection automatique du Mission Engine.

Un navigateur neuf authentifié choisit effectivement ce profil. Le compte n'a pas de préférence de modèle serveur explicite observée ;son champUI ne contient qu'une version. Les conversations enregistrent leur modèle et peuvent donc rester sur8B après un changement du défaut. Avant les essais,9conversations utilisent8B, une le profilCode et une27B. Les choix propres à Safari/iPhone ou à un stockage local de navigateur non accessible ne sont pas supposés connus.

La décision28A affecte **JARVIS canonique** à27B/Mac ;elle n'a pas migré le défaut d'Open WebUI issu de mission07. La récente intégration a conservé ce défaut tout en ajoutant le profilCode. Voilà l'incohérence de configuration, sans téléchargement récent de Llama8B. E08, compose actuel, README d'installation historique et rapports28A/Qwen-WebUI.

## Serveur réellement choisi

Les fournisseurs actifs sont Mac11434 etDell1-missions11435. Le catalogue fusionné indique `urls=[0,1]` pour8B,27B et14B, contre `[1]` pour80B. Le source installé `ollama-router.py:1110–1124` applique **random.choice** aux backends d'un identifiant dupliqué. Pendant le seul scénario de clarification,8B est réellement chargé surMac etDell1. On ne peut pas attribuer chaque requête historique à une machine unique sans son reçu réseau ;la fusion de catalogue ne conserve pas cette information dans le simple nom du modèle.

Ce mécanisme est indépendant de l'ordonnanceur hybride JARVIS. Ainsi une conversationWebUI27B peut aller surDell1 malgré le rôle conversationnel prévu pourMac. Le profilCode80B n'a qu'un backend mais ses inférences directes contournent l'admission de priorité canonique.

## Défaut ask_user reproduit et limites du diagnostic

Sept messages assistant d'une conversation existante contiennent un objet JSON textuel `name=ask_user`, `parameters=...`. Leur sortie persistante est de type **message**, sans vrai appel d'outil. Une ouverture de cette même conversation enChromium reproduit l'affichage du JSON brut. Aucune ancienne conversation n'est modifiée. Les textes originaux restent privés ;E08 publie seulement le constat structurel.

L'outil **existe** dans Open WebUI0.12.0 :`tools-backend.py` ajoute le builtinask_user si user_input est autorisé, et le middleware traite les vrais tool_calls pour produire l'interaction. Le système du profil8B ne contient pasask_user. Lors d'une nouvelle clarification synthétique sur le même profil, le navigateur affiche réellement deux choix et les boutons de réponse. L'outil et le transport ne sont donc pas globalement absents ou cassés.

**Cause immédiate prouvée :** l'objet a été produit/conservé comme texte de réponse, au lieu d'un appel structuré reconnu. Le front ne doit pas exécuter un texte arbitraire ressemblant à duJSON. **Origine exacte non établie :** template/parseur du modèle8B, influence de l'historique et mode de function calling de ces tours historiques. Les captures brutes des réponses Ollama historiques ne sont pas disponibles ;aucune preuve ne permet d'attribuer exclusivement la faute au connecteur ou au prompt. La génération neuve n'a pas reproduit le défaut ;c'est la restitution du message historique qui est reproduite.

## Corrections proposées, non appliquées dans cet instantané

1. Aligner le défautWebUI sur27B et documenter que les conversations anciennes gardent leur choix.
2. Filtrer les modèles par fournisseur pour garantir Mac→conversation etDell1→80B, sans sélection aléatoire pour ces identifiants.
3. Utiliser le mode natif d'appels d'outils sur le profil retenu ;retour en texte français clair si le modèle ne produit pas d'appel valide.
4. Garder un test positif de formulaire et un test négatif de JSON brut. Ne pas transformer par regex tout contenuJSON en outil exécutable.

L'autorisation propriétaire ultérieure permet de traiter ces corrections après gel du bilan ;leurs résultats seront des preuves distinctes, jamais une réécriture du constat initial.
