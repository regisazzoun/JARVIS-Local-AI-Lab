# Inventaire exhaustif des erreurs enregistrées — mission23

**Arrêté au 2026-10-19T18:03:12+0200, événement 4281.** 130 retours d’outils en échec sur 695 intentions observées. Toutes les entrées sont conservées dans [le JSON détaillé](INVENTAIRE-ERREURS.json), avec opération/commande expurgée, message complet disponible, catégorie et référence de preuve.

Les refus avant exécution, erreurs Python, délais et refus de répétition sont distingués. Les événements internes de rejet de lots peuvent recouvrir un échec d’outil : ne pas les additionner comme incidents indépendants. Les intentions interrompues sans résultat restent indéterminées. Le journal privé canonique est la source intégrale ; aucun secret ou corps de fichier potentiellement privé publié.

| Catégorie | Retours concernés |
| --- | --- |
| HTTP ou référence absente | 20 |
| Système ou échec à contextualiser | 25 |
| Droits ou périmètre outil | 27 |
| Paramètres ou protocole d’outil | 8 |
| Code Python ou API SDK | 44 |
| Délai réseau ou processus | 3 |
| Répétition refusée par moteur | 3 |

Inférences du worker : 501 enregistrées ; motifs {'stop': 501}, 0 pannes de routage observées. Cela ne valide pas la justesse des réponses et ne confond pas les erreurs SDK applicatives avec celles du worker.

## Cas qui expliquent la stagnation

- Documentation officielle refusée, longues pages sans pagination et URL supposées404.
- Nombreuses incompatibilités SDK : imports, types, signatures STT/TTS/LLM, ChatContext et rôles.
- Compression du dernier lot supprimant les corps de code ; relectures sans exploitation.
- Processus de serveur éphémères entre appels du terminal.
- Tests applicatifs masquant les exceptions et imprimant quand même un succès ; ces versions sont refusées comme réception.
- Factory LLM visant Mac à froid ; délai SDK10s annule son chargement. JARVIS corrige le backend vers Dell puis réussit un vrai flux : [preuve](PROGRES-LLM-JARVIS.json).

Les dernières erreurs des adaptateurs et les prochains tests de la mission en cours peuvent être postérieurs à cet arrêté. Le rapport n’affirme pas couvrir des événements futurs. Corrections et contributions Codex : [détail](CORRECTIONS.md).
