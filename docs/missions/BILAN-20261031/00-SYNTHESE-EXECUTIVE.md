# BILAN-20261031 — photographie du laboratoire

**✅🟡 Audit réalisé avec réserves de couverture. Aucune transformation déployée.**

Les trois machines ont été observées directement. Le Mac mini assure coordination, interfaces, mémoire et conversation27B sur une RTX3090 externe. Dell1 dispose de256GiB de RAM et de deux3090 : son80B est chargé sur Ollama11435. Dell2 possède128GiB, une3090 et une 3080 : il sert d’exécuteur SSH/CUDA, sans inférence Ollama observée.

Les cinq GPU sont donc **quatre RTX3090 et une RTX3080**, pas cinq3090. Les liens Ethernet actifs négocient à1Gb/s. Les miroirs RAID1 des Dell sont sains[UU]. Le BIOS diffère :2.8.0 sur Dell1,2.24.0 sur Dell2.

Le bilan recense24 groupes applicatifs,4935 entrées logiciels APT/Python/npm,144 composants ou contrats et16 domaines de développement. Douze familles amont à licence libre identifiée sont distinguées dans une sélection de15 familles externes. Ces nombres ne représentent pas autant d’applications indépendantes et n’incluent pas une attribution de toutes les dépendances transitives. Trois domaines de recouvrement sont analysés. [Comptages](STATISTIQUES.json).

Les différences Dell correspondent largement aux rôles : inférence/TTS/bureau sur Dell1, exécuteur minimal sur Dell2. Git et npm absents des deux Dell peuvent limiter certains projets ; les installer partout sans besoin serait une autre forme d’accumulation. Deux services Ollama Dell1 partagent les mêmes poids. Open WebUI conserve un profil Llama 8B historique, mais son défaut est le27B.

Deux lectures MCP distantes ont réussi sous Qwen Code guidé. Son résumé invente des disques : **accès reçu, restitution rejetée**. Un premier essai s’était arrêté sur une erreur de contexte. Les originaux et rectifications sont conservés. Six modules installés diffèrent de la base Git ; leur provenance doit être réconciliée avant toute mise à jour par remplacement.

Google Éducation fonctionne désormais en lecture Drive/Calendar/Gmail. Les comptes restent isolés. Les écritures et parcours WebUI/Qwen Code Éducation ne sont pas encore réceptionnés. Aucun projet Cloud ou fournisseur commercial plafonné ajouté.

Priorités proposées : budgets de contexte cohérents, manifestes de déploiement, rapports fondés sur les faits, profils Ansible par rôle et métriques standardisées. Pas de remplacement global du moteur ou de JL03 recommandé sans comparaison de contrats. P4 reste en pause ; aucune clôture14A, aucun lancement24-Old ou P7.

[Matériel Dell](02-COMPARATIF-DELL1-DELL2-MATERIEL.md) · [Applications Dell](04-COMPARATIF-DELL1-DELL2-APPLICATIONS.md) · [Plan proposé](12-PLAN-DE-RATIONALISATION.md) · [Réserves](13-REGISTRE-PREUVES-ET-RESERVES.md).
