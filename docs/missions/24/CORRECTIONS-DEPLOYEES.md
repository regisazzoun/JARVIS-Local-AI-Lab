# Corrections déployées — historique et réception24

**Lecture chronologique :** le premier état ci-dessous décrit la session initiale confinée. Les sections «Reprise hôte» et suivantes rendent compte du rétablissement réel ; voir [la réception actuelle](RAPPORT-FINAL.md).

Les neuf fichiers de référence23C comparés au commit distant `76f60c5bcc41acc55b8db7f829ab523ef0eebc44` sont identiques au contenu local (voir PREUVES-EXECUTION.json). Le HEAD Git local historique est `fffdb374f1efff4b2c30c51698470957cd7cdead` ; les corrections23C sont présentes comme modifications de travail, non comme ce HEAD. La nouvelle branche locale24 conserve ces modifications ; la branche distante24 est dérivée du véritable commit distant23C.

Les empreintes candidat/installé de host_client et host_bridge diffèrent. Le module installé capability_view.py est absent. Les correctifs de diagnostic, empreinte, catalogue et prévol restent donc non déployés. Les empreintes complètes sont dans le JSON. La politique persistante est illisible ; son empreinte et la version chargée par un processus actif ne sont pas connues.

Aucune modification du broker installé, service, politique, SSH, Tailscale, secret, mémoire ou modèle. Aucun redémarrage exécuté. Aucun composant23C reconstruit. Le blocage est le contexte d'exécution de l'opérateur, avant les habilitations JARVIS.

## Reprise hôte du20 octobre2026

Déploiement ciblé effectué : host_bridge.py, capability_view.py et jarvis/host_client.py seulement. Sauvegardes SQLite cohérentes et modules privés sous /var/backups/jarvis/mission24 ; détails et empreintes dans DEPLOIEMENT.json. Conservation des descriptions host_exec timeout et des paramètres GitHub plus précis déjà installés. Redémarrage broker/conversation réussi. La politique persistante reste identique octet pour octet. Le reste de install.py n’a pas été exécuté, évitant le remplacement inutile des autres modules/services. GitHub/local installé sont vérifiés par empreintes, état de processus et nouvelles réponses broker23C.1.

## Complément24 : visibilité des processus de service

L'appel ps de JARVIS dans host_exec a réellement échoué à voir LiveKit : cet outil possède son propre espace PID. Le statut systemd existant est enrichi par une lecture des processus du seul cgroup du service de projet déjà autorisé. Le broker renvoie PID/PPID, nom, UID et exécutable, sans arguments de commande ni environnement ; aucune permission globale ni nouveau profil. Les sorties signalent explicitement processus disparus et troncature. Le retest JARVIS sera effectué après redémarrage. Test de non-régression : processus Python réel dans un cgroup simulé, disparition concurrente, refus de remontée de chemin/d'un autre service et absence de lecture des secrets argv/environ. Suite77/77 réussie.

## Complément24 : diagnostic conservé jusqu'au modèle

L'inspection de Registry.execute montre que l'enveloppe BrokerError perdait error_code et diagnostic avant l'observation du modèle, malgré leur présence dans les reçus23C. Le registre conserve désormais catégorie, appelant et référence de preuve, y compris transport_denied sans reçu broker. Test de non-régression couvrant transport_denied/permission_denied et absence de preuve inventée ; suite78/78 réussie. Un résumé compact du catalogue expose également les nombres d'outils, capacités et demandes pour éviter l'interprétation erronée «stdout absent = registre vide» observée dans le premier rapport JARVIS, refusé et demandé en correction. Retest réel prévu après déploiement par JARVIS.
