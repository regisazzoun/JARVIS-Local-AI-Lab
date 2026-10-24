# Erratum prioritaire — rapport libre de démonstrationJARVIS

L'original reste inchangé dans DEMO-JARVIS-ORIGINAL.md et le journal. Contrôle indépendantCodex,24octobre2026.

- « Rapport binaire » : le fichier est un rapportMarkdownUTF-8, pas un format binaire.
- « Réécriture JSON redondante » : aucune deuxième écritureJSON n'est observée. Les deux host_write_file ont créé respectivementpreuve.json et RAPPORT-JARVIS.md.
- « Lecture rapport tronquée (profilDell1) » : les lectures broker sont complètes (stdout_truncated:false). Le dépassement de contexte concerne mission_report_review, pas une lecture tronquée du fichier ni une preuve deRAMinsuffisante.
- « Publications distantes non réalisables sans accès supplémentaire » : aucune publication n'était demandée dans cette recette et aucune n'a été tentée ; les accèsGitHubexistent et cette incapacité n'est pas démontrée.
- « Souscription à mission autonome » : le plan est fourni parCodex et spec.autonomous=false. Ce test n'évalue pas une planification autonome.
- mission_task_complete a effectivement validé la tâche (événement33321). Son refus ultérieur correspond à une répétition dans une phase déjà close, pas une permission d'administration manquante.
- L'état moteur final estcompleted ; le JSON contient son champstatus=verified. Ce champ ne doit pas être confondu avec l'étatvalidated de la tâche.

Le contrôle porte sur les reçus originaux, les événements33313/33321 et les appels d'écriture/lecture. Aucun texte corrigé n'est faussement attribué àJARVIS. Les réserves de restitution héritées de26Brestent ouvertes.
