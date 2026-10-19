# Vérifications du correctif23

-49 tests V2 réussis, dont maintien du résultat d’un test échoué malgré une écriture, résolution après retest réussi, refus d’une unité/projet/exécutable hors politique, échappement des paramètres systemd, accès en lecture à un dépôt tiers sans permettre push, pagination documentaire et résumé d’erreur avec stderr redirigé et refus d’un test code0 contenant une panne fonctionnelle explicite, conservation du dernier lot structuré pendant la compression du contexte.
- Compilation des modules broker réussie.
- Deux lectures HTTPS réelles des documents LiveKit auparavant refusés réussissent ; le modèle effectue ensuite ses propres lectures officielles avec succès.
- Sonde de service réelle installée/démarrée via le broker, puis observée active dans une requête indépendante ; elle conserve le même confinement que host_exec. Sonde arrêtée et unité retirée. Ce test est Codex, pas JARVIS et pas une validation LiveKit.
- Les quatre réceptions initiales doivent rester exactement identiques ; comparaison des empreintes et sauvegarde privée des fichiers à l’appui.
- L’acceptation du correctif demande une évolution utile du code ou des tests par JARVIS. Des lectures ou des cycles supplémentaires seuls ne la démontrent pas.

Les tests unitaires utilisent des doubles ciblés pour vérifier les frontières et erreurs ; ils ne remplacent pas les opérations réelles de JARVIS ni une réception vocale au microphone.


La correction finale conserve aussi le dernier échange assistant/outils dans son protocole natif, plutôt que de le remplacer uniquement par du texte de checkpoint. Le préambule de débogage est recentré sur les erreurs les plus récentes (ordre chronologique corrigé) et leurs références ; le journal intégral reste accessible. La vérification ajoute un test de conservation des liens et contenus natifs, sans modifier le reçu original.

Collecte reproductible en lecture seule : `sudo python3 docs/missions/23/collect-observation.py --output /chemin/observation.json`. Les marqueurs sont seulement signalés : leur présence doit être confrontée aux assertions du test réellement écrit par JARVIS.


Le vérificateur indépendant est compilé et testé négativement dans le véritable confinement : un manifeste manquant produit un échec code1, sans faux marqueur de validation. Il n’implémente pas l’application. Les commandes de recette exactes sont inscrites au contrat05 ; les scripts permissifs de JARVIS ne peuvent pas les remplacer.
