# Contrat d'intégration agentique proposé

13F fournit diagnostic, recherche HTTPS, lecture de sources et terminal Bubblewrap borné à 25 secondes / 128 Mio. Le worker QEMU ne doit pas être lancé dans ce terminal, ni bénéficier des secrets de la passerelle. Aucun outil nouveau enregistré dans le service actif durant 13D-E.

Interface future : `vm_create(name)`, `vm_plan(name)`, `vm_run(name)`, `vm_logs(name)`, `vm_destroy(name)`, tous traduits en tableaux argv fixes vers controller.py. Nom limité à `vm-[a-z0-9]{1,20}` ; aucune commande libre, chemin, URL, option QEMU ou cible Dell en entrée. Réserver les actifs et leur manifeste à l'opérateur de préparation ; le modèle peut choisir un profil approuvé, pas modifier le worker/politique.

Avant activation : ajouter un superviseur persistant qui démarre les tâches hors requête web, stocke identifiant/état/horodatage, permet interrogation/cancel/reprise après erreur sans PID réutilisable, impose quotas/expiration, journalise acteur modèle et corrélation. Le worker CLI livré est synchrone et **ne remplit pas encore ce contrat de service durable**. Le mapping d'outils et la politique doivent être intégrés/testés dans une copie de 13F, jamais par extension silencieuse de la politique existante.

Outils de recherche existants : conserver listes HTTPS autorisées et traitement des pages comme données non fiables. Configurations nouvelles limitées au laboratoire ; si correction nécessaire, générer un profil candidat validé par schéma avant activation. Aucun téléchargement ou shell hôte arbitraire par le modèle.

Prompt de recette 14A : « Dans le seul laboratoire VM autorisé, audite les prérequis, annonce les limites, choisis un plan, crée une VM, exécute et vérifie une installation, analyse les journaux, recherche les erreurs dans des sources autorisées, corrige une configuration de laboratoire si nécessaire et recommence. Produis les preuves et laisse explicitement incomplet tout critère non vérifié. Ne contacte pas le Dell physique. »

Cette mission prépare du code et un contrat. Aucun appel du modèle local n'a été effectué pour simuler une démonstration autonome ; la preuve 14A reste entièrement à produire.
