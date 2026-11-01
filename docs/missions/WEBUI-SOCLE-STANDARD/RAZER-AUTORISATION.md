> Étape initiale avant redémarrage. **Rétablissement GPU reçu ensuite** : voir [réception finale ciblée](RAZER-RECEPTION-GPU.md) et ses preuves. Les constats ci-dessous restent historiques.

# Razer Core — autorisation persistante et blocage GPU après redémarrage

Demande propriétaire du 1 novembre 2026 : corriger l’autorisation du boîtier pour qu’elle persiste, vérifier le 27B sur NVIDIA, sans perturber la copie Dell1 → Dell2.

## Correction appliquée

Le Razer Core connecté était reconnu par Thunderbolt mais non autorisé (`authorized=0`, `stored: no`). Une ancienne entrée Razer existait avec politique `auto`, mais son identité ne correspondait pas au périphérique actuellement connecté. Les autres entrées sont conservées.

Après contrôle du nom et du fabricant et sauvegarde privée de la base boltd, inscription par le mécanisme natif `boltctl enroll --policy auto` pour ce seul boîtier. Relecture indépendante : `authorized=1`, entrée persistante correspondant à son identité, politique `auto`, autorisation globale boltd activée. Aucune règle autorisant tous les périphériques, aucune suppression d’entrée existante.

La RTX3090 apparaît désormais sur PCIe. Ce résultat ne signifie pas encore qu’Ollama l’utilise.

## Second blocage observé

Le pilote déjà installé n’initialise pas la carte : `NVRM: BAR1 is 0M @ 0x0`. Le chargement du module existant a échoué avec `No such device`. Les fenêtres mémoire PCIe nécessaires ne sont pas attribuées ; aucune nouvelle tentative identique ni écriture manuelle dans les registres PCIe n’est effectuée.

Le noyau courant est Debian `6.12.111+deb13-amd64`. Le bilan du31octobre atteste le noyau AppleT2 `6.18.54-1-t2-trixie` avec RTX3090 et un processus GPU. Plus précisément, la source `preuves/mac.json` montre Qwen3.5 27B chargé à16384, `size=17456756161` et `size_vram=17456756161` : le 27B était bien entièrement sur GPU. Cela ne fournit pas une surveillance continue de deux semaines, mais réfute l’hypothèse d’une absence totale d’utilisation GPU sur toute cette période.

L’entrée déjà installée `jarvis-t2-egpu-np32-pref512` contient le noyau T2 et les réglages de réserve mémoire du protocole historique. Les images et le module NVIDIA595.91.07 correspondants existent toujours. Le fichier principal GRUB indique0, mais la surcharge `/etc/default/grub.d/99-jarvis-t2.cfg` force explicitement Debian6.12.111 ; le GRUB généré le confirme. Une simple lecture du fichier principal ne décrit donc pas le choix effectif.

## Préparation, sans redémarrage

Copie privée du réglage effectif et candidat où seul `GRUB_DEFAULT` cible l’entrée T2 existante. Syntaxe du candidat et du GRUB actuel vérifiées. Ce candidat n’est pas installé ; aucune prochaine entrée programmée et aucun redémarrage déclenché. Aucun paquet, pilote, noyau ou initramfs installé ou remplacé. Aucune commande sur les Dell, aucune modification du transfert.

La procédure historique préparait un démarrage sans boîtier puis un branchement surveillé ; le rapport05C ne qualifiait pas le démarrage boîtier connecté. La disponibilité physique du propriétaire est donc demandée après la copie, sans réinventer une validation logicielle de chaque étape. Ne pas modifier silencieusement le protocole par une réallocation PCIe improvisée pendant le transfert.

## Réception restant à faire

Après retour contrôlé sur le profil T2 : vérifier noyau et paramètres réellement chargés, autorisation automatique du boîtier, BAR attribués, pilote lié, NVIDIA fonctionnel, puis une inférence27B à32768 et la présence effective du modèle en VRAM. La persistance est configurée, mais son comportement après un nouveau démarrage n’a pas encore été reçu. **Le 27B sur GPU n’est pas encore reçu dans l’état actuel.**

Preuves expurgées : `RAZER-AUTORISATION.json`. Identités matérielles, sauvegardes boltd et sorties originales conservées dans `razer-gpu-private`, non publiées.
