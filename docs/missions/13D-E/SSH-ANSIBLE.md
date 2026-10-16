# Bootstrap SSH et Ansible

Aucune clé créée ou modifiée. Sélection future : clé publique existante de JARVIS, signataire disponible côté worker/agent SSH, utilisateur propriétaire identifié. Les clés autorisant l'accès au Mac mini ne prouvent pas l'existence de leur clé privée sur JARVIS. Ne jamais exporter une clé privée, l'agent socket ou un secret dans initrd/Git.

L'initrd privé doit contenir `preseed.cfg`, `install-ssh.sh`, `authorized_key` (une seule clé publique, commentaire expurgé). Le late_command installe OpenSSH pendant le bootstrap, crée `.ssh` en 0700 et `authorized_keys` en 0600, fixe le propriétaire et active SSH. Le compte dédié `jarvisadmin` utilise la clé ; sudo sans mot de passe est limité à la future cible laboratoire, nécessaire à Ansible et à réévaluer avant le Dell. Aucun fichier SSH du Mac mini modifié.

Après installation : récupérer **depuis la console VM de confiance** l'empreinte de la clé hôte et comparer avec le fichier `known_hosts` dédié. `ssh-keyscan` seul n'authentifie pas la cible. Ne pas désactiver `StrictHostKeyChecking`. La configuration SLIRP actuelle n'offre pas SSH à l'hôte : transport invité/worker à ajouter uniquement sur loopback ou via canal virtio dédié, après test. L'inventaire contient des adresses de documentation ; aucun contact physique possible.

Depuis `deployment/13de/ansible` :

```
umask 077
ansible-playbook --syntax-check site.yml
ansible-playbook -i inventory/lab.yml site.yml --check --diff --limit jarvis-lab
ansible-playbook -i inventory/lab.yml site.yml --limit jarvis-lab
ansible-playbook -i inventory/lab.yml site.yml --limit jarvis-lab
```

Renseigner l'adresse du transport VM validé, `ansible_ssh_private_key_file` via configuration privée ou agent existant et `UserKnownHostsFile` dédié. Ne pas placer de clé dans l'inventaire. Première exécution : convergence ; seconde : zéro changement attendu. `--check` ne prouve pas une installation réussie. Reprise : playbook complet idempotent après correction du prérequis, traces privées `ansible-private.log`. Aucune journalisation publique des variables privées.

Neuf rôles distincts livrés ; Debian et répertoire JARVIS gèrent l'état, comptes/réseau/stockage/supervision contrôlent sans reconfiguration sensible. NVIDIA/CUDA/Ollama sont des jalons explicites différés, sans installation ni téléchargement implicites : versions, compatibilité RTX 3090/Debian, signature Secure Boot et provenance doivent être validées sur cible. L'inventaire Dell est désactivé et le playbook ne sélectionne que `lab` avec assertions de virtualisation et Debian 13.
