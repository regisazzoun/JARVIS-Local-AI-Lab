# Razer et 27B — réception du rétablissement GPU

## Résultat reçu le 1 novembre 2026

- Razer autorisé automatiquement après le redémarrage contrôlé et le rebranchement physique, sans nouvel appel d’autorisation. Politique native boltd `auto` et inscription persistante relues ; autres entrées conservées.
- Noyau effectivement chargé : `6.18.54-1-t2-trixie`. Paramètres de réserve/reconstruction PCIe existants présents. Réserves contrôlées avant branchement : NP32M et PREF512M ; registres de pont relus.
- RTX3090 reconnue, pilote NVIDIA595.91.07 lié. BAR1 de256M à0x4000000000 et BAR3 de32M à0x4010000000 réellement attribués. Aucun pilote ou noyau installé/remplacé.
- Ollama local relancé à vide pour la redécouverte GPU. Inférence du27B : réponseOK, deux tokens générés, `done=true`. Modèle à32768 avec `size=18547275201` et `size_vram=18547275201`, donc entièrement en VRAM. Processus llama-server présent dans les applications de calcul NVIDIA.
- Lecture depuis le profil27B dans WebUI/Open Terminal : `uname -s`, réponseLinux. Chat et journal de processus natif contrôlés séparément, fin0 ; empreintes dans `RAZER-RECEPTION-GPU.json`. Ce résultat n’est pas une simple déclaration du modèle.

## Persistance de démarrage

Le démarrage de réception a été lancé une fois sur l’entrée T2 existante, boîtier débranché par le propriétaire puis rebranché après contrôle des réserves. L’identifiant du boot a changé ; aucune prochaine entrée temporaire ne reste programmée.

Après réception GPU, la surcharge `/etc/default/grub.d/99-jarvis-t2.cfg` a été modifiée pour que le défaut soit `jarvis-t2-egpu-np32-pref512`, puis GRUB a été régénéré et sa syntaxe vérifiée. L’entrée sélectionnée est strictement celle reçue lors de ce démarrage. Les noyaux de secours Debian6.12.111 et6.12.107 ainsi que les autres entrées restent présents. Réglage source précédent sauvegardé et empreinte de l’ancien GRUB conservée en privé.

L’autorisation persistante et la sélection du profil sont configurées et contrôlées. **Le scénario reçu reste démarrage boîtier débranché, puis rebranchement. Un démarrage à froid avec le boîtier déjà connecté n’a pas été essayé dans cette correction.** Aucune nouvelle expérience matérielle improvisée.

## Persistance WebUI réellement vérifiée

Le redémarrage du Mac a révélé une régression de configuration : la source Compose historique imposait `ENABLE_PERSISTENT_CONFIG=false`. Les réglages API de connexions étaient donc perdus lors du redémarrage, malgré la persistance des profils en base. Le premier contrôle navigateur après boot n’a pas trouvé le terminal : aucun appel modèle attribué à ce contrôle échoué.

Correction par l’option native `ENABLE_PERSISTENT_CONFIG=true` dans la source de déploiement, et connexion Ollama native dans cette même source. Même image OpenWebUI0.12.0 et même volume de données ; aucune réinstallation, aucun effacement de session ni jetonGoogle. Connexions MCP/OpenTerminal, profils32768, filtre propriétaire désactivé et compaction native réappliqués par les API standard.

Le conteneur WebUI a ensuite été redémarré une fois pour tester cette persistance : égalité des réglages critiques avant/après, terminal et MCP présents, profils conservés, relais maison toujours contourné. Aucun script de démarrage, filtre ou moteur de réparation ajouté. Surcharge Compose sans secret fournie dans `tools/webui_standard/compose.override.example.yaml`.

## Limites et préservation

Un redémarrage du Mac, avec disponibilité physique du propriétaire. Aucun redémarrage Dell, aucune commande sur ces machines ni modification de leur copie. Le contrôle fonctionnel GPU ne constitue pas un benchmark comparatif sous transfert réseau, une réception de stabilité prolongée ou une validation de toutes les conclusions Qwen. M26-P4/MANUAL-HOLD, historiques et accès conservés. Aucune fusion automatique main.

La preuve historique du31octobre montre déjà le27B entièrement en VRAM sur le Mac avec T2 ; le changement vers27B n’est donc pas la cause démontrée du repli CPU. Les constats CPU/BAR manquants avant correction restent conservés dans `RAZER-AUTORISATION.md/json`.
