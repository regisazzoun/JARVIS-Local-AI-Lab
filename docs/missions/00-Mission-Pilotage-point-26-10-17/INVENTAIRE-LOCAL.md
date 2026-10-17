# Inventaire local — exécution réelle de JARVIS

JARVIS a généré son inventaire en exécutant ses propres programmes Python via les outils hôte de la passerelle canonique. Le résultat final contient **671 chemins Markdown distincts**. Le contrôle indépendant Codex retrouve les **637 fichiers** de son inventaire initial, plus **34 documents** des références de mission accessibles lors de l’exécution. Au contrôle, les **671 empreintes SHA256 correspondent aux fichiers réels**, sans chemin manquant ni erreur enregistrée dans le résultat final. Voir [réception chiffrée](RECEPTION-INVENTAIRE.json).

- [Inventaire original JARVIS en Markdown](jarvis/INVENTAIRE-LOCAL-JARVIS.md).
- [Inventaire original JARVIS structuré](jarvis/INVENTAIRE-LOCAL-JARVIS.json).
- [Programme écrit puis réparé par JARVIS](jarvis/inventory-agent.sh).
- [Complément initial Codex](INVENTAIRE-LOCAL-COMPLEMENT-CODEX.json).
- [Archives inspectées par Codex](INVENTAIRE-ARCHIVES.json) : 94 archives, 323 membres Markdown, aucun contenu documentaire nouveau.
- [Instructions, outils et chronologie de délégation](PREUVES-AGENTIQUES.json), à lire avec le [bilan agentique](BILAN-AGENTIQUE-JARVIS.md).

## Ce qui a été lu et ce qui reste interprétatif

Le programme de JARVIS ouvre réellement les fichiers, calcule leur empreinte et extrait titre, numéro apparent, date et type. Il s’agit d’un **chargement machine intégral avec interprétation non exhaustive**, distinction conservée dans son résultat. Les numéros/types/dates extraits automatiquement peuvent rester approximatifs : ils ne deviennent pas les verdicts de mission. Le registre consolidé confronte ces métadonnées aux rapports et décisions récents. La fonction détaillée par document est complétée par les fiches de mission et les types, sans inventer une fonction là où le titre ne la démontre pas.

Les dossiers binaires, environnements Python, .git, runtime, secrets et répertoires private sont exclus. Les archives ont été cataloguées en lecture seule, leurs membres Markdown chargés pour dédoublonnage ; les binaires et journaux bruts ne sont pas publiés. L’absence d’un chemin privé dans cet inventaire ne prouve pas son inexistence.

## Corrections et provenance

La première passe JARVIS ne traitait que 63 fichiers explicitement listés et classait parfois une mission selon une référence citée. Elle est conservée comme résultat rejeté. Une seconde tentative a bouclé sur le manifeste. Le script suivant a découvert 218 fichiers mais échoué sur une variable `filename` non initialisée, ne produisant initialement que 141 fiches. Codex a identifié ce défaut et extrait sans modifier le programme réellement envoyé par Qwen ; **JARVIS a écrit la correction, exécuté le script et obtenu les 218 entrées**. Des relectures répétées ont ensuite épuisé la boucle sans clôture formelle, même si l’effet fichier était acquis.

Codex a alors élargi les seuls droits de lecture aux fichiers Markdown retrouvés, sans nouveau droit d’écriture, sans accès aux clés/mots de passe et sans redémarrage. **JARVIS a relancé son propre programme sur le manifeste enrichi et produit les 671 entrées**. La réception repose sur les fichiers, empreintes et traces d’outils ; la réponse conversationnelle tronquée du modèle ne constitue pas la preuve. Les horodatages d’autorité sont ceux des appels et journaux ; une date rédigée librement dans une première métadonnée n’est pas utilisée comme preuve temporelle.

## Rapprochement par document

Le [JSON consolidé](INVENTAIRE-LOCAL-CONSOLIDE.json) et le [CSV](INVENTAIRE-LOCAL-CONSOLIDE.csv) ajoutent la fonction et les rattachements vérifiés par Codex. Les fonctions non établies restent « À confirmer » ; les métadonnées originales JARVIS sont conservées séparément. La découverte complémentaire a aussi inspecté structurellement [31 fichiers TXT/JSON](AUTRES-FORMATS-CODEX.json) ; les six rapports de compétences du projet tiers JarvisVoice ne constituent pas des exécutions JARVIS.
