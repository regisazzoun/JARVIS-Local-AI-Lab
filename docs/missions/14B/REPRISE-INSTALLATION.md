# Mission 14B — reprise réelle et suivi physique

🟡 **En cours, sans réception finale.** État du 24 octobre 2026, vers 23 h 20 sur le contrôleur. La mission reste `a1becab1a8244e2295463bd5be833784` ; aucun nouveau moteur n'est créé.

Le propriétaire a allumé le Dell2, fourni sa MAC et demandé de reprendre les procédures de14 pour éviter les interventions répétées. Les deux premiers démarrages étaient des découvertes en RAM : « aucun partitionnement autorisé » était leur arrêt attendu, pas une nouvelle demande de consentement. Codex a trop fractionné la préparation ; cette erreur de coordination est explicitement reconnue. Le troisième environnement a établi un SSH temporaire épinglé ; aucune nouvelle manipulation physique n'est actuellement nécessaire.

## État démontré

| Étape | État | Observation |
|---|---|---|
| Identification Dell2 | ✅ | MAC propriétaire, UUID distinct deDell1, garde exacte et SSH épinglé |
| Stockage | ✅ identifié | Deux NVMe2To : KIOXIA et Samsung ; lecteur de cartes vide exclu |
| GPT / deux ESP / RAID1 | ✅ exécuté | Deux membres `[UU]`, nouvelles partitions sur les seuls disques identifiés |
| Synchronisation initiale | 🔄 | Environ28% à ce point ; aucune réception « RAID propre » avant `idle` |
| Debian13 | ✅ installé sous `/target` | Paquets/noyau/comptes/SSH ; pas encore une preuve de boot installé |
| Finalisation EFI | ✅ exécutée | Copies signées cohérentes et deux entrées EFI ; redondance physique non testée |
| NVIDIA/CUDA | 🔄 | Préparation réellement déclenchée parJARVIS, téléchargement de paquets observé |
| Reboot / réception installée | ⏳ | Continuation cible bornée6h active ; attend paquets et miroir synchronisé, démonte/arrête proprement, sans `reboot -f` |
| Affichage physique | ✅ installé | Tableau `/dev/tty1`, actualisation5s, progression réelle ; suivi tty8 préparé aprèsboot |
| Ansible et calcul CUDA | ⏳ | Connexion et calcul numérique sur chaque GPU à observer aprèsboot |

Deux périphériques graphiques NVIDIA sont observés sur PCI. La base locale des identifiants indique3090 et3080LHR pour leurs deux identifiants différents ; cela reste à confirmer par le pilote. **DeuxRTX3090 ne sont pas déclarées reçues.** Aucune tenue électrique sous forte charge n'est déduite de l'énumération PCI.

## Incidents, causes et corrections

1. Découverte01 : aucun disque utilisable ; seul le lecteur de cartes vide apparaît. Le contrôleurPCI de stockage n'est pas pris en charge par l'image issue du Dell1. Codex ajoute à une nouvelle image en RAM les modules SATA/VMD et leurs dépendances, vérifiés par la chaîne Release signée/index/SHA256 Debian. Découverte02 réelle : les deux NVMe apparaissent. Les deux rapports originaux restent privés et conservés.
2. Le candidat de plan JARVIS comporte des contrats invalides et des confusions de cible/périmètre. Codex fournit une aide substantielle aux schémas et à la procédure ; le plan assisté est versionné. Ce n'est pas une preuve de planification initiale autonome réussie.
3. L'installation réellement déclenchée parJARVIS installe Debian, puis échoue sur `cp: can't stat '/jarvis/progress-viewer.sh'`. La cause est une omission de paquetage **Codex**. Codex ajoute les deux fichiers validés et une reprise au checkpoint de finalisation. JARVIS déclenche cette reprise ; Debian/EFI sont finalisés sans réinstaller, recréer les comptes ni reformater.
4. Une rédaction JARVIS annonce `gpu_prepare` exécuté sans reçu. Le rapport est conservé et rectifié dans le journal. Une nouvelle continuation atomique appelle réellement l'outil ; marqueur et téléchargement sont observés. La prose seule n'est pas reçue.
5. Pour lancer la continuation après synchronisation, JARVIS invente trois actions distantes (`host_policy`, `autonomous_status`, `capability_status`) au lieu de l'action fournie. Trois refus comparables : arrêt effectif par le garde. Aucun alias opportuniste ni quatrième essai. Codex documente le diagnostic et lance ponctuellement le contrôleur fixe parSSH épinglé ; **ce lancement est attribué àCodex**. La main est préparée pourJARVIS sur la réception installée dans un contexte minimal.
6. Un chevauchement antérieur de workers a été provoqué par une reprise trop précoce deCodex. Les appels engagés ont été laissés terminer avant nouvelle continuation ; aucun service existant n'a été arrêté. L'incident est conservé dans les événements.

Les horodatages bruts du Dell installateur sont conservés sans les réécrire. Son horloge n'était pas qualifiée ; pour l'ordre entre machines, utiliser les reçus du contrôleur. Le synchronisme NTP fait partie de la lecture aprèsboot.

## Continuation et limites

Le contrôleur de la cible attend les paquets et un RAID non dégradé/synchronisé, vérifie stockage/EFI/SSH, conserve les logs sur le système installé, démonte les volumes, arrête le miroir et demande un reboot normal. Arrêt documenté en cas d'échec de paquets, dégradation, absence de progression20min ou échéance6h. Il ne relance jamais l'installation.

Un observateur borné côtéMac conserve `assist/CONTINUATION-STATUS.json` dans le projet privé14B. Après un boot réel, il vérifie SSH par clé/sudo et l'UUID, prépare uniquement le profil administratif d'observationDell2, réalise un pingAnsible et rend les lectures de réception àJARVIS. Une indisponibilité ou un échec reste un blocage documenté, pas un GO implicite. La réception finale et la consolidation des preuves restent à effectuer.

Le tableau physique demandé par le propriétaire est alimenté par les vrais fichiers d'étape, `/proc/mdstat` et les résultats de contrôle. Il n'affiche pas une réussite GPU avant le test effectif. Le suivi postboot est préparé sur la console dédiée déjà utilisée par la procédure14.

## Attribution et invariants

- **JARVIS** : candidat de plan ; préparation locale partielle ; appels broker de prévol/démarrage installation, reprise finalisation et préparationGPU, avec reçus. Rapports erronés et appels refusés conservés.
- **Codex** : qualification indépendante, assistance substantielle aux contrats, adaptation du déploiement validé14 au nouveau matériel, drivers de découverte, script d'installation, correction du paquetage, outils fixes, lancement ponctuel de la continuation après blocage, tableau physique, contrôles et documentation.
- **Propriétaire** : allumage, informationMAC et choixPXE physiques déjà réalisés. Aucune nouvelle validation de partitionnement ajoutée.

Le profil temporaire ajouté au broker ne concerne que le Dell2 identifié et ses commandes fixes. Les anciens profils, tous les autres champs de politique, la configuration conversationnelle, le code de routage et l'unitéOllama sont inchangés selon les empreintes contrôlées. Aucun Ollama/modèle/répartition de charges n'est installé ou modifié par14B. Aucun playbookIA historique ni aucune mission14A/24-Old n'est lancé. Les identités, clés et mots de passe restent horsGit.
