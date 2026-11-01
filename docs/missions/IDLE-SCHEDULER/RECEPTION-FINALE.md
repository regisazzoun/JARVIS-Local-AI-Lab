# Réception finale de l’ordonnanceur de fond

**1 novembre 2026 — ✅ Ordonnanceur central activé ; exécution distante à checkpoints qualifiée sur Dell2 par Tailscale.** La discussion est limitée à l’ordonnanceur. JM-01 reste suspendue individuellement : son développement n’est pas poursuivi ici.

## Résultat vérifié

- Service `jarvis-idle-scheduler` activé au démarrage, actif et en attente après les unités reçues. Un déploiement versionné et son redémarrage contrôlé sont enregistrés dans `REDEPLOIEMENT.json`.
- Télémétrie existante des trois machines et cinq GPU réutilisée ; aucun collecteur supplémentaire. Les noms logiques et les profils du broker restent canoniques.
- Contrôle distant par les alias SSH existants, désormais résolus vers Tailscale. Les quatre endpoints Ollama des deux Dell ont répondu via des routes `tailscale0`. Les services distants ne sont pas redéployés par cette mission.
- Essai réel de l’ordonnanceur sur Dell2 : démarrage, priorité accordée à une connexion extérieure d’inférence passant par le relais Tailscale, arrêt du groupe, checkpoint **6 resté à 6** pendant la pause, puis reprise à **12**. Le redémarrage du contrôleur n’a pas rejoué l’unité terminée.
- **21 tests ciblés PASS** sur l’hôte réel. Les réceptions précédentes de bail expiré, crash du superviseur, monoinstance, plafond de trois erreurs et manifest immuable restent acquises ; elles ne sont pas additionnées aux tests actuels.
- Services conversation, broker, MCPO, collecteur, Ollama et deux workers centraux actifs ; WebUI HTTPS200 au contrôle. Aucune commande de travail ou de redémarrage envoyée à Dell1 par cette reprise.

## Pause par mission

`enabled: false` sur une entrée de `jobs` suspend son admission, sans bloquer les autres unités et sans modifier ses compteurs ou checkpoints. Par défaut, les entrées historiques restent actives. La configuration est chargée au démarrage du contrôleur ; son rechargement redémarre uniquement ce service, avec arrêt supervisé d’une éventuelle unité active.

Cette séparation a été testée : une entrée suspendue ne s’exécute pas, tandis qu’une autre unité termine. Le marqueur global PAUSE utilisé auparavant a été retiré pour réactiver l’ordonnanceur ; JM-01 porte maintenant `enabled:false` et son unité distante reste inactive, MainPID0. Son état natif est strictement identique avant/après la qualification. Aucun nouveau livrable mobile n’est revendiqué.

## Corrections conservées

Le superviseur traite un SIGTERM reçu pendant une observation `ss` comme une pause demandée, sans ajouter un faux échec. Il signale d’abord le superviseur principal, attend la fin du groupe, puis utilise l’arrêt systemd comme repli borné. L’état completed est relu avant de classer une disparition de processus en résultat inconnu.

Une escalade de l’application est propagée au contrôleur et interdit ses relances automatiques. Une correction vérifiée peut ouvrir un nouveau segment d’essais avec référence de résolution ; les totaux historiques restent conservés. Les tests couvrent la conservation des erreurs, l’archivage du contexte et le refus d’une résolution incohérente. La correction du contexte Qwen effectuée avant la pause est sauvegardée ; elle ne constitue pas une réception de l’audit mobile.

Pendant une propre inférence GPU, l’activité CPU/GPU du modèle n’est pas assimilée à une demande extérieure. CPU libre requis au lancement, réserve RAM, fraîcheur, file canonique et connexions extérieures restent contrôlés. Le seuil de connexion persistante est 6s pour éviter de traiter les sondes de santé courtes comme des sessions interactives.

## Limites du contrat

Une unité distante doit être explicitement checkpoint-safe et idempotente entre checkpoints. Ce mécanisme n’annule pas automatiquement une mutation externe et ne garantit pas toutes les applications arbitraires. Le bail arrête le processus distant si le contrôleur disparaît ; reprise après reboot matériel ou déplacement intersite non qualifiée. Le serveur Ollama reste hors du groupe du client ; il est préservé.

La détection de priorité par connexions n’identifie pas parfaitement plusieurs clients locaux. L’environnement de fichiers séparé n’est pas un confinement hermétique. Les sources et identités détaillées restent privées ; les preuves publiques sont expurgées. Les futurs livrables applicatifs ne sont pas exportés automatiquement : seuls les contenus réellement relus sont publiés.

## Sources et périmètre

AGENTS.md et charte relus, rapports PR39/41, état26/PR29 et rapports précédents PR47 conservés. L’ordre courant autorise la reprise et le redéploiement de l’ordonnanceur en utilisant les chemins Tailscale existants. La clarification du propriétaire limite cette discussion à l’ordonnanceur. M26-P4/MANUAL-HOLD, checkpoints, modèles, accès et configurations réseau déployées sont préservés ; aucune fusion main et aucune demande d’approbation intermédiaire.

Les états antérieurs «non actif», «longues unités non qualifiées» ou «JM-01 en cours» restent des instantanés historiques. Ce rapport et ses preuves donnent l’état actuel. Il ne clôture pas les projets applicatifs ni les réserves d’autonomie de JARVIS.
