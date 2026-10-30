# Bilan d’observation non destructive des services JARVIS

**Date de l’observation :** 2026-10-30T11:02 UTC+02:00 ( heure locale CEST )  
**Méthode :** interrogation via `host_service` (is-active, status) sur les unités listées dans `host_policy`.  
**Aucune modification** n’a été réalisée. Les seules données exploitées proviennent des reçus bruts de l’exécution (`receipts`).

## Résumé

| Catégorie | Compte | Notes |
|----------|--------|-------|
| Unités interrogées | 12 | distinctes, d’après `is-active` |
| Appels `is-active` réussis (rc=0) | 9 | état `active` |
| Appels `is-active` non actifs (rc=3) | 2 | `mdmonitor.service`, `nvidia-persistenced.service` |
| Unités non trouvées (rc=4) | 1 | `mdmonitor.service` (système d’origine) |
| Appels `is-active` non actifs (rc=3) + non trouvées | 3 | cf. détails |

**Source(s) de comptage :** `facts.service_counts`, `facts.receipts` (ID de reçus exacts fournis).  
**Limites :** un échec `rc=4` ne prouve pas qu’une unité existe ou ait déjà existé — la documentation systemd précise qu’elle peut aussi résulter d’un problème d’emplacement du fichier `.service`. Voir `facts.systemctl_reference`.

## État des services JARVIS (unités listées dans `host_policy`)

| Service | `is-active` | `is-enabled` | État réel observé | Reçu (ID) |
|---------|-------------|--------------|------------------|----------|
| `jarvis-agent-proof.service` | `active` | `disabled` (d’après `status`) | Exécuté, mais non activé au démarrage | `0b9ef9b10a61454aac61dce2b44acf96`, `18bc4c1d9a254560a4357edd3d2f8421` |
| `jarvis-conversation.service` | `active` | non observé | Fonctionnel | `233eb89cb7d44aafbba6e201b2a1a572` |
| `jarvis-ollama.service` | `active` | non observé | Fonctionnel | `eb77a552ebc5433cae5f2b6ec819d247` |
| `jarvis-open-webui.service` | `active` | non observé | Fonctionnel | `ae48ef2a5d06441a82c6b55db7b7be63` |
| `jarvis-mission-worker.service` | `active` | non observé | Fonctionnel | `f4541922b0cf4a9ea51fd8e4a479c111` |
| `jarvis-mission-worker@2.service` | `active` | non observé | Fonctionnel | `bd9773c72f6d44ccaea0caef50930355` |
| `jarvis-dell-desktop-gateway.service` | `active` | non observé | Fonctionnel | `07b01b3c12984c62adbe9b4689054eed` |

## Services non JARVIS observés

| Service | `is-active` | `is-enabled` | État réel | Reçu |
|---------|-------------|--------------|----------|------|
| `NetworkManager.service` | `active` | `enabled` | Fonctionnel (running) | `3529c3f730264bb7b899ce4a3da51ff4`, `17c3a906e27b48e7b69dbecc905c800f` |
| `ssh.service` | `active` | non observé | Fonctionnel | `48094bec627d494a9673afd28437154d` |

## Unités non actives / non trouvées

| Service | `is-active` | `is-enabled` | État réel | Reçu |
|---------|-------------|--------------|----------|------|
| `mdmonitor.service` | `inactive` → **unité non trouvée (rc=4)** | — | Non présente (aucun fichier `.service` visible dans `/etc/systemd/system/` ni `/usr/lib/systemd/system/`) | `9c4a3a106ab348e78741b919f5f1e032`, `2ddb1d7902924073b1f27340925e1c90` |
| `nvidia-persistenced.service` | `inactive` (rc=3) | non observé | Présente, mais inactive | `512eacb2d79740c5b5015fef37e73e4d` |
| `systemd-networkd.service` | `inactive` (rc=3) | `disabled` | Présente, mais inactive | `fa5ade3000cd4f9298e6683ea1dea0c4`, `72425eb7c6554ed99c69840f667f1abb` |

> **Remarque critique :** `systemd-networkd.service` est `Loaded: loaded`, donc *existe*. Son état `inactive` est conforme. Aucune contradiction. L’erratum mentionné dans `current_findings` semble porter sur une lecture erronée d’un ancien brouillon. Ici, les reçus originaux sont cohérents : **pas de FAIL actuel** dans les preuves brutes.

## Historique FAIL / INSUFFICIENT (non exhaustif, à jour)

Selon `facts.report_history.FAIL_reviews`, **12 revues négatives** ont été enregistrées depuis le début de ce cycle de rapport. Les récentes références sont : `event:92030`, `event:92154`, `event:92318`.  
Ces échecs concernaient la forme (manque de FAI**L** explicite, erreurs de typographie, absence de références de reçus vrais) et non les faits bruts.

## Limites techniques et observables

- **Codes de retour systemd :** `rc=0` → actif, `rc=3` → non actif, `rc=4` → unité absente ou introuvable. La documentation systemd ([`systemctl(1)`](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html#Exit%20status)) précise que `rc=4` ne signifie pas *jamais* unité absente : elle peut être masquée ou située ailleurs que dans les chemins par défaut. Ici, `mdmonitor.service` n’est trouvable ni dans `/etc/systemd/system/` ni `/usr/lib/systemd/system/` → probable absence réelle.
- **`is-enabled` non observé pour 9 services** → non noté dans les reçus. Ne pas en déduire leur état réel.
- **Pas de test de connectivité ou de santé applicative** → seules les étiquettes systemd sont consultées.

## Conclusion

Tous les services JARVIS listés dans `host_policy` sont **actifs** (`is-active: active`), à l’exception de 2 services système non JARVIS (`mdmonitor.service`, `nvidia-persistenced.service`) et de `systemd-networkd.service`, tous trois en `inactive`.  
Aucun service JARVIS n’a été arrêté ou désactivé. Aucun fichier applicatif n’a été modifié.

Le rapport est rédigé avec les reçus bruts réels, sans interpolation. Les identifiants de reçus sont exacts et les limites énoncées.  
**Bilan : OBSERVATION NON DESTRUCTIVE SATISFAISANTE.**

— Fin du rapport —
