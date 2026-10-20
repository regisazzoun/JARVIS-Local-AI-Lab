# Diagnostic 23C

## Faits exécutés par Codex

- Le socket du broker existe dans la vue de fichiers.
- La connexion Unix depuis le client installé échoue avec PermissionError errno1 « Operation not permitted ».
- Une création de socket TCP locale échoue avec la même erreur ; aucun service n'a répondu.
- systemctl échoue avant interrogation : « Failed to connect to system scope bus via local transport: Operation not permitted ».
- La politique `/etc/jarvis/host-policy.json` et la base privée du broker ne sont pas lisibles. L'ouverture en lecture seule de missions.sqlite échoue aussi dans cette session.
- Le code installé et le code publié relisent un chemin de politique unique à chaque appel ; aucun sélecteur de mission n'a été trouvé dans le chemin client/Handler/execute.
- Description systemd « mission 11 » et ancienne attribution SQL `mission='11'` : libellés historiques, sans effet d'autorisation dans le code examiné.

Ces observations établissent une limitation de transport de **cette session**, avant application des permissions. Elles n'établissent pas la cause exacte de l'incident historique signalé par le propriétaire.

## Questions encore ouvertes

| Question demandée | Résultat actuel |
| --- | --- |
| Pourquoi la session précédente présentait mission11 ? | Libellés historiques démontrés ; réponse réelle de cette session historique non récupérée |
| Mauvais processus, configuration périmée ou rechargement ? | Non déterminé ; PID, commande vivante, politique et événements privés requis |
| Quelles opérations23 ont été refusées par politique ? | Non déterminé ; les essais actuels n'ont pas atteint le broker |
| Droits23 encore dans la politique persistante ? | Non vérifié, fichier inaccessible |
| Plusieurs instances incohérentes ? | Non vérifié ; présence d'un socket ne dénombre pas les processus |
| Changement après reboot/session ? | Non testé ; aucun redémarrage exécuté |

JARVIS n'a pas reçu le diagnostic : API locale inaccessible. Aucun texte de Codex n'est attribué à JARVIS. Ne pas remplacer une cause inconnue par l'hypothèse « droits révoqués » ni par l'hypothèse « problème réparé ».
