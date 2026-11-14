# Essai 3 après correctifs — sortie observée

**14 novembre 2026, copie privée. Cette réponse reste soumise à la revue critique. Expurgation de publication seulement ; aucun filtre ajouté au modèle.**

Je vais rechercher les documents relatifs au déploiement de la téléphonie IP dans la salle 407 sur le Drive Éducation du lycée.
Voici l’état d’avancement du déploiement téléphonie IP de la salle 407, tel que documenté dans le fichier **Salle-407-Documentation-deploiement.md** (mis à jour le 13 novembre 2026) [source id="1"].

### 📡 Réseau
*   **VLAN et adressage :** Les téléphones sont sur le sous-réseau `[ADRESSE EXPURGÉE]` (ex: `[ADRESSE EXPURGÉE]`, `.54`, `.65`, `.60`).
*   **Connectivité serveur ↔ VLAN :** Des problèmes de routage ont été observés (SYN reçus mais pas d’établissement de connexion). Des routes statiques temporaires `/32` via la passerelle `[ADRESSE EXPURGÉE]` ont été ajoutées sur le serveur pour les hôtes problématiques (`[ADRESSE EXPURGÉE]`, `[ADRESSE EXPURGÉE]`) et conservées dans NetworkManager (`pbx-lycee`).
*   **État :** La route générale du VLAN reste à examiner ; aucun changement global n’a été effectué sur le réseau [source id="1"].

[PASSAGE D’AUTHENTIFICATION EXPURGÉ — valeur et règle non publiées]

### 📱 Téléphones (État par modèle)
| Extension | Modèle | État d'inscription | IP observée | Détails |
| :--- | :--- | :--- | :--- | :--- |
| **[EXTENSION EXPURGÉE]** | Cisco SPA504G | ✅ Déployé | [ADRESSE EXPURGÉE] | MAC `[MAC EXPURGÉE]`, firmware 7.4.8a. Profil et dictionnaire FR reçus (HTTP 200). |
| **[EXTENSION EXPURGÉE]-[EXTENSION EXPURGÉE]** | Cisco SPA504G | ✅ Reachable | - | Dictionnaires FR téléchargés, langue French, NTP fr.pool.ntp.org. |
| **[EXTENSION EXPURGÉE]** | Poly VVX 450 | ✅ Reachable | [ADRESSE EXPURGÉE] | Route statique ajoutée. Boot Server Static configuré. Dictionnaire FR reçu. |
| **[EXTENSION EXPURGÉE]** | Aastra 480i | ✅ Reachable | - | Profil téléchargé, NTP activé (fr.pool.ntp.org). |
| **[EXTENSION EXPURGÉE]** | Grandstream GXP1620 | ✅ Reachable | [ADRESSE EXPURGÉE] | Route statique ajoutée. DHCP option 42 désactivée pour conserver fuseau Paris. |
| **[EXTENSION EXPURGÉE]** | Cisco SPA525G | ✅ Reachable | - | Profils FR et NTP configurés. |
| **[EXTENSION EXPURGÉE]** | Poly SoundStation IP 7000 | ✅ Reachable | [ADRESSE EXPURGÉE] | Route temporaire retirée. Dictionnaire FR reçu (116 ko). |

*   **Configuration commune :** Langue française, NTP `fr.pool.ntp.org`, fuseau Paris (UTC+1 avec heure d’été), format 24h [source id="1"].

### 📟 SIP et Provisioning
*   **Provisioning HTTP :** Les profils XML/CFG sont servis via `/provision-s407/`. Les fichiers valides retournent HTTP 200, les absents retournent 404 (pas de redirection vers la page de login).
*   **Dictionnaires :** Dictionnaires français publiés pour Cisco et Polycom. Sources : archives Cisco et paquets Poly conservés localement (les URLs officielles renvoyant 403) [source id="1"].

### 📞 Appels testés
*   **Validé :** Appel bidirectionnel avec audio confirmé uniquement entre les extensions **[EXTENSION EXPURGÉE]** et **[EXTENSION EXPURGÉE]**.
*   **À tester :**
    *   Ouverture du répertoire sur l’écran physique (service XML configuré vers annuaire central de 11 contacts).
    *   Appel avec audio depuis/vers le poste **[EXTENSION EXPURGÉE]** (dans les deux sens).
    *   Appels avec audio pour les postes Polycom (**[EXTENSION EXPURGÉE]**, **[EXTENSION EXPURGÉE]**) bien que l’utilisateur confirme qu’ils "fonctionnent", la validation audio formelle reste à documenter [source id="1"].

### ⏳ Reste à faire / Points en attente
1.  **Tests utilisateurs :** Valider l’affichage physique français et la synchronisation heure sur chaque écran (à confirmer sur place).
2.  **Tests d’appels :** Compléter les tests audio pour le Grandstream ([EXTENSION EXPURGÉE]) et les Polycom ([EXTENSION EXPURGÉE], [EXTENSION EXPURGÉE]).
3.  **Réseau :** Examiner la route générale du VLAN `[ADRESSE EXPURGÉE]` pour supprimer les routes statiques `/32` temporaires si possible.
4.  **NTP Serveur :** Le serveur `[ADRESSE EXPURGÉE]` présentait un décalage de ~410 secondes ; son rôle officiel n’a pas été vérifié ni modifié [source id="1"].

**Source unique utilisée :**
*   [id="1"] *Salle-407-Documentation-deploiement.md* (Drive Éducation, mis à jour le 2026-11-13).
