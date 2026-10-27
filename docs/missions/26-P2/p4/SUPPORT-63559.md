# Support borné après l’escalade 63559

🟡 Candidat non terminé, P4 non validée. Mission persistante
`d8fe752876db480cbe5f22cd5525e2dd`, plan 3, tâche P4-ATTEST-01.

Directives relues : AGENTS, charte fondamentale, supervision, paquet
LANCEMENT-ATTESTATION, PLAN-REPRISE-INSTRUMENTATION, INTERFACES-PERENNES et
CORRECTION-FAUX-MATCH. Autorisation de toute la suite P4 conservée ; candidat
sans déploiement avant revue indépendante, puis continuation autorisée.

Après le correctif 63429, JARVIS a effectivement choisi une inspection physique
de worker.py sur Dell1 : exécution 63528, commande cat, rc 0. Il a ensuite
redemandé l’ancienne référence 63265 déjà épuisée ; le troisième refus comparable
a produit l’escalade 63559. Le garde a donc fonctionné. Aucun nouveau défaut
d’infrastructure n’est démontré par cet arrêt.

Contrôle indépendant Codex 63562 : reçu complet vérifié par SHA-256
`46ad6c3e90eeaab9583c396e2ff2e5f0ee30dacdf145f18bf1211ab6ab3fab6d`,
44 lignes, source analysable par ast, fonctions worker_locks/run/main présentes.
Le contenu figure déjà dans la projection compacte de l’inférence 63550.
L’instrumentation attendue reste absente de cette source ; ce contrôle n’est
pas un test du candidat.

Changement concret de reprise : instruction 63563 désignant la véritable
observation 63528, archivage natif du dialogue de travail périmé via MissionStore,
puis action Codex-periodic 63565 et transition queued. Les états d’autorité,
problèmes et refus d’interface sont comparés avant/après et strictement identiques.
Plan 3 conservé ; absence de lease vérifiée avant reprise.

Aucun programme écrit à la place de Qwen, aucun reload, modification de service,
script de supervision, modèle, routage ou compteur. Aucun rejeu des tests reçus.
Le registre de revue reste inchangé : technical_review_recorded n’est pas marqué.
JARVIS conserve le choix de son instrumentation et de ses tests sur les deux Dell.
