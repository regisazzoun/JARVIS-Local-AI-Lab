# Accès opérationnel aux outils depuis Open WebUI

🟡 En cours — correctifs préparés, non déployés, réception de bout en bout non effectuée.

## Mission et sources consultées

Ordre propriétaire : accès opérationnel depuis Open WebUI à Google personnel et Éducation, GitHub, SSH/Ansible/Skills/MCP et missions JARVIS. Réutiliser les composants et autorisations existants, préserver services/accès/mémoire, sans fusion automatique main. Aucun nouvel inventaire général ni campagne de standardisation.

Sources lues : AGENTS.md et docs/CHARTE_DIRECTIVES_JARVIS.md de codex/bilan-20261031 ; descriptions et discussions PR35/37/38 ; rapports finaux INTEGRATION-AGENTIQUE-WEBUI-CODE, GOOGLE-MCP-OAUTH et BILAN-20261031 ; cahiers des deux missions de raccordement, état SUIVI courant, installation/utilisation et sources actives. Base exacte : 9e059cf208a86e87b8673cddc38fc0a39dbfeb72. Les anciens états Éducation bloquée sont historiques : le bilan plus récent documente des lectures réussies. M26-P4/MANUAL-HOLD ne sont pas repris.

## État avant et diagnostic

- Services conversation, adaptateur WebUI, broker et deux workers : actifs. Aucune mission running/queued parmi les vingt missions récentes exposées par le client ; ce contrôle borné ne constitue pas un inventaire intégral de la base.
- Les deux profils Google sont configurés dans des répertoires distincts ; leurs caches déclarent Drive, Documents, Calendar, gmail.modify et spreadsheets.readonly. Cela ne prouve pas les permissions effectives sur chaque ressource. Le cache personnel est expiré avec mécanisme de renouvellement existant ; aucun nouveau besoin OAuth interactif démontré.
- `Capabilities.schema` refuse tout nom absent de EXPOSED avec « Tool is outside the exposed client catalog ». Des méthodes imbriquées comme `drive.search` ne sont pas des noms du registre JARVIS : elles doivent passer par google_mcp avec profile/action/name/arguments. La présence de ce garde est démontrée ; l'appel précis ayant causé l'erreur utilisateur n'est pas encore identifié dans sa conversation.
- Façade Google commune à paramètre profile, filtrage ALLOWED et WORKSPACE_FEATURE_OVERRIDES désactivant notamment envoi, invitations/réponses et corbeille. Le registre MCP possède encore sa propre projection de neuf capacités. Aucun composant manquant ne justifie réinstallation.

## Correctifs préparés

Deux outils liés à un compte, google_personal et google_education, réutilisent strictement perform(profile=...) existant ; le schéma ne permet pas de changer profile. Deux méthodes natives WebUI offrent list/schema/call et pagination. L'ancienne interface reste compatible.

Exposition des méthodes amont des familles Drive/Docs/Sheets/Calendar/Gmail/time ; l'amont épinglé reste responsable de l'existence et du schéma de chaque méthode. Les opérations d'authentification ne sont pas exposées au modèle. Suppression des désactivations artificielles envoi/invitations/corbeille dans la préparation. Les confinements des téléchargements et pièces jointes sont conservés ; les secrets ne transitent pas dans les prompts.

Les deux identités sont raccordées au registre/MCP et classées comme écritures selon l'opération. Skill define/test/activate devient découvrable depuis le client, en plus de list/run. L'erreur de catalogue donne désormais la route pour une méthode Google imbriquée.

Le fichier tools.py préparé conserve une différence runtime préexistante (description des artefacts de plan) ; cette ligne n'est pas un développement de la présente mission. Aucun écrasement global du runtime n'a été effectué.

## Tests et limites

28 tests ciblés PASS sur la branche : 17 Google MCP/OAuth/identité, 11 capacités client. Identités liées vérifiées par test ; anciennes restrictions de mission remplacées dans les assertions concernées. Les tests logiciels ne reçoivent ni accès distant, ni OAuth effectif, ni comportement agentique.

Aucun déploiement, rechargement, écriture Google/GitHub par WebUI, commande Dell, Skill ou nouvelle mission de cette campagne n'est déclaré reçu. Les réceptions PR35/37 et lectures Éducation du bilan restent historiques, sans être réattribuées à cette intervention.

Le contrôle automatique d'approbation a rejeté le déploiement préparé combinant remplacement du code actif, mise à jour WebUI, rechargement des services et exposition de méthodes Google sensibles. Motif : autorisation jugée insuffisamment précise pour ce changement combiné. Une confirmation précise a été demandée ; aucun contournement effectué.

## Suite nécessaire

Après levée du blocage : sauvegarde privée des quatre modules actifs et de l'outil WebUI/valves ; déploiement ciblé ; contrôle des tâches/connexions puis rechargement des seuls services concernés. Réaliser depuis WebUI sur chaque identité Drive recherche/lecture, Docs création/relecture exacte, Sheets création/écriture/relecture, Calendar événement de test/relecture et Gmail brouillon/relecture. Aucun message à un tiers nécessaire aux essais. Vérifier indépendamment les objets et leurs comptes.

Depuis la même interface : lecture et publication GitHub sur branche de test, commandes réellement distantes sur chacun des deux Dell dans le projet autorisé existant, exécution d'un Skill existant et mission canonique dédiée avec reçus consultables. Archiver sorties originales, audit_id, IDs privés hors Git, résultats et contrôles indépendants ; distinguer modèle, outil et vérificateur. Documenter erreurs et effets inconnus avant tout rejeu d'écriture.

Retour arrière prévu : restaurer uniquement les fichiers et l'outil sauvegardés, recharger les mêmes services ; conserver bases, missions, preuves, comptes et jetons. PR empilée sur PR38, aucune fusion main.
