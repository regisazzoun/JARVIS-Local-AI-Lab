# Réception de la mission21 par le moteur22

**19 octobre2026 : sept tâches sur sept validées. Verdict GO AVEC RÉSERVES sur l’autonomie démontrée.** Même exécution `e370b0bef74f4deaa390b5c46bfdc299`, reprise depuis `waiting_external`, sans nouvelle mission ni réexécution des six tâches reçues. [État et preuves](PREUVES-MISSION21.json), [rapports du modèle](../21/RAPPORTS/), [manifestes GitHub](MANIFESTE-RAPPORTS-MISSION21.json).

| Tâche | Résultat réellement reçu |
| --- | --- |
| 01 Santé | Lectures Mac/Dell et rapport vérifié |
| 02 Journaux | Journaux autorisés et réserves conservées |
| 03 Synthèse | Rapports01/02 relus et synthèse enregistrée |
| 04 Concordance | Sources GitHub consultées, accès manquants signalés |
| 05 Administration | SSH/Ansible gardés, copie réelle et seconde passe sans changement |
| 06 Service | Collecteur/timer installé par JARVIS, nouveau résultat vérifié |
| 07 Bureau | KDE/VNC ; authentification et image reçue via tunnels SSH LAN et directement Tailscale |

## Réception de07 : deux sources distinctes

**Propriétaire :** confirme l’enrôlement de `jarvis-dell` et l’utilisation réelle de KDE/VNC depuis son Mac via tunnel SSH sur le tailnet. C’est un test utilisateur déclaré, pas une observation physique de Codex : [confirmation](CONFIRMATION-UTILISATEUR-TAILSCALE.json).

**JARVIS/Qwen :** nouvel appel `tailscale_status`, reçu `43c1d569d0684ea0aa56227fb2523acd`, confirme service actif, `Running`, en ligne, adresse tailnet présente. Appel `desktop_network_test`, reçu `5e5b4dbea3504540a74ce37c898bc216`, confirme deux clients RFB réels, tunnel SSH et identité épinglée, authentification réussie et **259200 octets d’image reçus par transport**, géométrie annoncée1440×900. `coverage.mode=direct` : le trajet Tailscale ne passe pas par la passerelle de bureau Mac. Le client technique est exécuté sur le Mac mini Debian ; il ne remplace pas le test physique du propriétaire. Aucune capture d’écran privée publiée.

Les six empreintes initiales sont inchangées. JARVIS a appelé lui-même `mission_task_complete` pour07 ; le moteur a relu le rapport et validé le contrat, puis vérifié son contenu publié sur GitHub. La synthèse finale est produite par le modèle, avec vérification distante : [rapport21](../21/RAPPORT-FINAL.md).

## Corrections et limites conservées

Le18oct, Tailscale était installé par JARVIS mais non enrôlé. L’omission du déploiement13D-E reste documentée ; son état courant est corrigé. Aucune identité Tailscale Mac copiée sur Dell.

Le19oct, le premier test RFB a échoué : le contrôleur lisait un ancien secret de déploiement. Codex a corrigé le client privilégié pour lire le fichier de mot de passe réellement utilisé par TigerVNC, sans exposer le secret au modèle et sans modifier le mot de passe ni les services Dell fonctionnels. JARVIS a ensuite exécuté le test réussi. Une tentative du modèle de déposer un script de réinitialisation a été refusée pour droits insuffisants ; elle n’a pas changé le mot de passe.

La reprise réutilisait aussi une ancienne dépendance non résolue et des notes périmées. Codex a corrigé le filtrage temporel des observations, archivé le contexte de travail, épinglé les preuves récentes et fourni un objectif de reprise ciblé. Les preuves et checkpoints originaux restent conservés. La première synthèse finale répétait faussement6/7 et l’ancien blocage ; Codex l’a refusée et a fait reprendre uniquement sa rédaction par JARVIS. Un contrat de synthèse explicite empêche cette version contradictoire d’être reçue à nouveau.

Cela démontre une exécution réelle persistante, des outils, des preuves et des publications ; **cela ne démontre pas une autonomie longue sans correction ni guidage Codex**. Répétitions, erreurs sémantiques et attribution imprécise dans certains rapports bruts restent des réserves. La réception14A globale et le déploiement Dell2 ne sont pas déduits de cette mission. Les anciens rapports sont conservés dans l’historique Git et les archives privées ; aucune réécriture silencieuse par Codex des productions du modèle.


La synthèse définitive distingue désormais explicitement le test utilisateur et les contrôles JARVIS. Réserves de formulation conservées : l’expression « intervention physique sur son Mac » est celle du modèle ; le propriétaire n’a pas détaillé sa méthode d’enrôlement. Les noms d’outils résumés et références raccourcies ne remplacent pas le journal complet. Le résultat technique reçu et la déclaration utilisateur font autorité, sans déduire de clé fournie ni de manipulation précise.
