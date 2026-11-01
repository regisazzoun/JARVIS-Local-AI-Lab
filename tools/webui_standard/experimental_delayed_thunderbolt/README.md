# Essai de démarrage Razer branché — candidat non installé

Préparation du 1 novembre 2026 à la demande du propriétaire. Aucun changement du profil fonctionnel par défaut, aucun service installé ou activé, aucun redémarrage programmé.

Le module Thunderbolt du noyau T2 actif est chargeable séparément. Un profil GRUB d’essai séparé, préparé en privé depuis l’entrée T2 reçue, conserve toutes les réserves mémoire et ajoute `modprobe.blacklist=thunderbolt`. Il ne remplace pas l’entrée fonctionnelle. Ne pas utiliser `module_blacklist=thunderbolt` : le blocage noyau empêcherait le chargement ultérieur recherché.

`jarvis-thunderbolt-ready.service` charge explicitement le module après le réseau et boltd, laisse les mécanismes natifs autoriser le Razer déjà connu et initialiser NVIDIA, puis vérifie le GPU. Le drop-in proposé fait attendre Ollama. SSH et le réseau ne dépendent pas de cette unité. Les autres services ne doivent recevoir cette dépendance que s’ils consomment effectivement le GPU ; l’interface de diagnostic doit rester accessible si le contrôle échoue.

La syntaxe du menu GRUB privé et de l’unité a été vérifiée avec les outils natifs, y compris vérification systemd privilégiée. Cela ne valide pas le prochain démarrage. Les fichiers de ce dossier sont des candidats, pas une installation active.

Limite essentielle : retarder Linux ne masque pas un boîtier physiquement connecté au firmware Apple/GRUB. Le rapport historique04W ne permettait pas d’attribuer le blocage à la période pré-Linux plutôt qu’au noyau. Le résultat doit donc être éprouvé par un unique démarrage surveillé, avec un profil de secours et une personne capable de débrancher le boîtier en cas de perte d’accès. Aucun nouveau paramètre EFI, écriture de registre PCIe ou désactivation permanente du contrôleur proposé.

Critères du futur essai : Razer laissé branché, nouveau boot sur le seul profil d’essai, accès SSH, module chargé au moment attendu, autorisation automatique, BAR valides, NVIDIA actif avant Ollama et inférence réelle27B surGPU. En cas d’échec, revenir au profil reçu et retirer les seuls fichiers d’essai ; aucune répétition aveugle. Les processus longs et la copie Dell1→Dell2 ne sont pas concernés par cette préparation.

Sources : manuel local modprobe/kmod ; documentation noyau Thunderbolt https://docs.kernel.org/admin-guide/thunderbolt.html ; rapport historique docs/missions/historique/04W/mission04W.md.
