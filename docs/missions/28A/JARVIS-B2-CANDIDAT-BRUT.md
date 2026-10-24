# Sortie originale JARVIS — erreurs conservées

Voir ERRATA.md et les reçus techniques ; aucune correction silencieuse du texte ci-dessous.

# Rapport Tâche B2_candidate — Installation du candidat Qwen3-Coder-Next 80B

## Contexte et objectif

Cette tâche vise à installer le modèle `qwen3-coder-next:q4_K_M` (~52 Gio) sur Dell Precision 5820 pour évaluation comparative comme candidat agentique renforcé. L'installation doit être vérifiée par catalogue hybride avant validation.

## Exécution réelle effectuée

### Installation initiée
- **Commande** : `host_remote host=dell-observe action=model_pull model=qwen3-coder-next:q4_K_M`
- **Statut initial** : L'appel a terminé avec statut INCOMPLETE durant le téléchargement SHA256 (timeout pendant vérification des blobs)
- **Résultat effectif** : Le serveur Ollama sur Dell a poursuivi et finalisé l'installation indépendamment après le timeout

### Vérification indépendante
Plusieurs lectures de catalogue hybride ont confirmé la présence effective du modèle malgré le statut INCOMPLETE initial du pull :
- 6 modèles confirmés dans le catalogue dont `qwen3-coder-next:q4_K_M` (digest: `ca06e9e4087c714d44355bf954099187890e63084b4a632b8e9956c4b9492074`, taille: 51 741 611 823 octets)
- Aucun redownload nécessaire : le modèle était entièrement présent dans le cache serveur

## Vérification du contrat

**Contrat validé** avec `mission_verify` :
```json
{
  "expected": {"/installed/qwen3-coder-next:q4_K_M": true},
  "kind": "json",
  "source": {"tool": "host_remote", "arguments": {"action": "hybrid_catalogue", "host": "dell-observe"}}
}
```

**Résultat** : ✅ PASS
- **Invocation ID** : `c1f9e5d221a1409a815271feea3ad3bb`
- **Observation** : Le modèle est bien installé et accessible dans le catalogue hybride de dell-observe

## État actuel

✅ Modèle 80B candidat installé et vérifié  
⏳ En attente de tâche B3_comparative pour évaluation qualitative contre qwen3:32b et autres candidats  

## Limites

- Le timeout durant la phase de pull n'a pas affecté l'installation finale (comportement normal d'Ollama avec reprise)
- Aucune mesure de qualité conversationnelle ou latence effectuée à ce stade (réservée à B3_comparative)
- Le modèle est candidat, non encore sélectionné comme supérieur

## Sources

- https://ollama.com/library/qwen3-coder-next:q4_K_M
- https://huggingface.co/Qwen/Qwen3-Coder-Next
- Catalogue hybride dell-observe (reçu horodaté 1792783870.7835639)

---
*Rapport généré par JARVIS — Tâche B2_candidate — Mission 28A*
