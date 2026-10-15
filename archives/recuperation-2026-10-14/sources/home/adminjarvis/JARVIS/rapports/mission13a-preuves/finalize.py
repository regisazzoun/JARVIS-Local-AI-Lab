from pathlib import Path
import json,hashlib,datetime,shutil,subprocess
P=Path('/home/adminjarvis/JARVIS/rapports/mission13a-preuves');R=Path('/opt/jarvis/voice');before=json.loads((P/'before.json').read_text());after=json.loads((P/'after.json').read_text())
gpu=json.loads((P/'gpu-during-tests.json').read_text());integ=json.loads((P/'installation-integrity.json').read_text());models=json.loads((P/'installed-models.json').read_text());inputs=json.loads((P/'verified-inputs.json').read_text())
checks={'existing_config_hashes_unchanged':before['configs']==after['configs'],'29_ollama_model_files_sha256_unchanged':before['ollama_models']==after['ollama_models'],'ollama_tags_unchanged':before['ollama_tags']==after['ollama_tags'],'services_active_before_after':before['services']['stdout']==after['services']['stdout']=='active\nactive\n','system_packages_inventory_unchanged':before['dpkg']==after['dpkg'],'kernel_unchanged':before['kernel']==after['kernel'],'ollama_ps_empty_before_after':before['ollama_ps']==after['ollama_ps']=={'models':[]},'no_gpu_compute_processes_during_sampled_tests':bool(gpu) and all(s['exit_code']==0 and not s['processes'].strip() for s in gpu),'no_remaining_voice_process':not integ['voice_processes'],'models_are_real_files_without_tmp_symlinks':not any(m['symlink'] for m in models),'network_kernel_isolation_verified':json.loads((P/'offline-namespace.json').read_text())['connection_blocked'],'systemd_templates_not_installed':not list(Path('/etc/systemd/system').glob('jarvis-voice*')),'offline_tests_four_successful_runs':True}
# Compare listening sockets independent of volatile process labels.
def listeners(snapshot):
 return sorted(tuple(line.split()[:6]) for line in snapshot['listeners']['stdout'].splitlines()[1:])
checks['listening_sockets_unchanged']=listeners(before)==listeners(after)
results={};guards={}
for name in ['A-tts','A-stt','D-tts','D-stt']:
 results[name]=json.loads((P/(name+'.result.json')).read_text());guards[name]=json.loads((P/(name+'.guard.json')).read_text())
checks['offline_tests_four_successful_runs']=all(g['exit_code']==0 and not g['stop_reason'] and not g['loaded_gpu_libraries'] for g in guards.values())
for m in models:
 expected=next(e for e in inputs['models'] if e['name'].removeprefix('tom-').removeprefix('whisper-small-')==Path(m['path']).name)
 assert m['sha256']==expected['sha256']
assert all(checks.values()),checks
(P/'acceptance-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(P/'measurements-summary.json').write_text(json.dumps({'results':results,'guards':guards,'disk':integ['directory_sizes'],'gpu_samples':len(gpu)},ensure_ascii=False,indent=2)+'\n')
rows='\n'.join(f"| {name} | {r['model_load_s']:.3f} | {r.get('synthesis_s',r.get('transcription_s')):.3f} | {guards[name]['peak_rss_mib']:.1f} | {r['cpu_average_percent_one_core']:.1f} % | {r['rtf']:.3f} |" for name,r in results.items())
end=datetime.datetime.now(datetime.timezone.utc);date=end.astimezone(datetime.timezone(datetime.timedelta(hours=2))).isoformat()
report=f'''# JARVIS — Mission 13A : installation durable et isolée du socle vocal

13 octobre 2026 — Mac mini 2018, Debian 13 T2Linux. Finalisation : {date}, heure de Paris.

## 1. Bilan et réception

**RÉUSSI : les sept critères de réception sont satisfaits dans le périmètre des tests fichiers.** Whisper small et Piper Tom sont installés et réellement exécutés depuis `/opt/jarvis/voice`, sur disque permanent. Deux cycles synthèse/transcription ont réussi avec quatre processus moteurs distincts, sans accès réseau et sans chargement Ollama. Les quatre processus se sont terminés. Aucun moteur permanent ni démarrage automatique activé. Mission 13B non commencée.

| Critère | Résultat et preuve |
|---|---|
| 1. Moteurs dans un répertoire permanent | **RÉUSSI**, `/opt/jarvis/voice`, modèles copies réelles et venv propre sans liens vers `/tmp` |
| 2. Arrêt et relancement | **RÉUSSI**, nouveaux PID pour D-tts et D-stt après terminaison des processus A |
| 3. WAV et transcription | **RÉUSSI**, deux WAV mono PCM16, 44 100 Hz, non silencieux, décodés et transcrits |
| 4. Aucun téléchargement pendant les essais | **RÉUSSI**, namespace réseau sans route, fichiers explicites, mode offline et hook Python connect/bind |
| 5. Installation JARVIS préservée | **RÉUSSI**, hashes configurations, 29 fichiers modèles Ollama, tags, inventaire dpkg et noyau identiques avant/après |
| 6. GPU réservé à Ollama | **RÉUSSI**, CPUExecutionProvider et CPU/int8 explicites ; zéro processus GPU aux {len(gpu)} relevés ; RTX 3090 à 6 Mio avant/après |
| 7. Preuves et procédures | **RÉUSSI**, dossier de preuves, scripts, mesures, WAV, sauvegardes privées, procédures et propositions systemd |

## 2. Audit préalable, sauvegardes et décisions

Lecture des rapports Missions 11 et 12, de leurs index/notes techniques, du worker de test, des manifests de modèles et wheels et du lock testé. Les versions réellement exécutées en Mission 12 priment sur les anciennes dépendances du projet Jarvis Voice inspecté en Mission 11. PyAV 19.0.1 et le vocabulaire .json étaient des incidents déjà corrigés : seul PyAV 15.1.0 et `vocabulary.txt` ont été repris.

L’audit actuel concorde avec les références : SHA des deux unités existantes et du Compose égaux aux preuves Mission 12 ; Python 3.13.5, noyau `{before['kernel']['stdout'].strip()}` ; Ollama et Open WebUI actifs ; aucun modèle Ollama chargé au début ni à la fin. Environ 26 Gio RAM disponibles, 355 Go disque libres, swap initial inutilisé. Les chemins `/opt/jarvis` et `/opt/jarvis/voice` n’existaient pas ; `/opt` existe sur le disque racine. Ce chemin a donc été retenu sans écraser d’installation existante ni rencontrer de contradiction nécessitant confirmation.

Sauvegardes réalisées avant installation : les deux unités systemd JARVIS, `compose.yaml` et `.env` Open WebUI, dans `mission13a-preuves/backup-configs/` avec permissions privées. `.env` n’est pas affiché dans les preuves lisibles ; ses secrets ne sont pas inclus dans le rapport. Ne pas partager cette sauvegarde privée. Les empreintes seules sont dans before/after. Aucun accès ni copie de la base WebUI active ; aucune restauration nécessaire. Les unités et éventuels drop-ins ont été examinés sans mutation.

Toutes les 29 entrées fichiers de `/home/adminjarvis/JARVIS/ollama/models` ont été hachées intégralement avant et après, y compris les poids totalisant environ 30 Go. Aucun modèle Ollama supprimé, remplacé, téléchargé ou forcé en mémoire. Le noyau, les paquets système et les sockets en écoute sont identiques entre relevés.

## 3. Installation et versions

Répertoire racine mode 0750, propriétaire adminjarvis ; parent `/opt/jarvis` mode 0755, root. Sudo limité à la création de ces nouveaux répertoires et aux namespaces réseau des essais ; installation Python et moteurs en UID1000, jamais pip système. Le venv est neuf, créé avec `--without-pip`, bootstrap depuis le wheel pip vérifié, puis pip installé uniquement dans ce venv. `include-system-site-packages=false`.

Organisation : `venv/`, `models/stt/whisper-small/`, `models/tts/`, `scripts/`, `config/`, `logs/`, `docs/`, `docs/systemd/`, `wheels/`.

Versions effectives : **Python 3.13.5, faster-whisper 1.2.1, CTranslate2 4.8.2, Piper 1.8.0, PyAV 15.1.0, ONNX Runtime CPU 1.31.0, NumPy 2.5.4**, pip local 26.2.1. Les 25 distributions nécessaires aux deux moteurs sont sélectionnées par fermeture transitive des dépendances de base, sans extras, à partir des METADATA des distributions testées. Leur lock exact est un sous-ensemble du `requirements-tested-cp313-linux.txt` Mission 12 ; pip est figé séparément. Résolution et installation avec `--no-index`, `--require-hashes`, wheels binaires locales uniquement. `pip check` passe. Aucun Kokoro, Siwis, F5-TTS, PyTorch, onnxruntime-gpu ni package CUDA installé dans ce venv.

Les fichiers temporaires de Mission 12 étaient présents. Réutilisation par copie, avec vérification SHA-256 avant et après copie ; **zéro téléchargement nécessaire pour cette installation**. Ni le venv temporaire ni ses symlinks de modèles n’ont été déplacés/cop iés comme installation. Les seuls liens du nouveau venv pointent vers son propre lib et l’interpréteur `/usr/bin/python3.13`.

STT : `/opt/jarvis/voice/models/stt/whisper-small`, quatre fichiers `config.json`, `model.bin`, `tokenizer.json`, `vocabulary.txt`, révision Systran `536b0662742c02347bc0e980a01041f333bce120`.

TTS : `/opt/jarvis/voice/models/tts/fr_FR-tom-medium.onnx`, configuration `.onnx.json` associée et `MODEL_CARD`, révision rhasspy/piper-voices `c10ece1aade47bb51c153c893d14e5bf8e5b7117`. SHA modèle Tom : `bf65074ccdeeeeaa832e75edb1c0a513c01c9a972bdf085ff8a6e71ea234fd41`. SHA small model.bin : `3e305921506d8872816023e4c273e75d2419fb89b24da97b4fe7bce14170d671`. Les sept empreintes, références URL et tailles sont conservées dans verified-inputs et installed-models.

## 4. Tests A à E, transcription et incident

**A — RÉUSSI :** versions effectives, modèles permanents vérifiés, absence de dépendances système modifiées ; hashes inputs et packages figés. **B — RÉUSSI :** deux synthèses de « Bonjour, je suis JARVIS. Les modules vocaux sont installés et opérationnels. », WAV valides et non silencieux. **C — RÉUSSI :** transcription réelle avec langue fr forcée, small, CPU, compute_type demandé int8, deux threads, beam_size=1 sans VAD externe, local_files_only=True. **D — RÉUSSI :** nouveaux processus après arrêt, même installation et absence de réseau. **E — RÉUSSI :** configurations et poids existants inchangés, services actifs, CPU exclusif.

Premier texte reconnu :

> Bonjour, je suis Jarvis. Les modules vocaux sont installés et opérationnels.

Second texte reconnu après relancement :

> Bonjour, je suis Jarvis. Les modules vocaux sont installés et opérationnelles.

La casse de JARVIS devient Jarvis dans les deux essais. Le deuxième présente une substitution lexicale réelle `opérationnels` → `opérationnelles`, préservée dans D-stt.result.json. Aucune correction du texte reconnu appliquée. Piper comporte de l’aléatoire de synthèse, les deux WAV ne sont pas supposés identiques. Aucun résultat n’est présenté comme une reconnaissance parfaite générale.

**CORRIGÉ — assertion de contrôle trop stricte :** le premier essai A-stt a chargé le modèle mais a été arrêté par une assertion qui exigeait que l’attribut compute_type effectif soit exactement `int8`. CTranslate2 rapporte `int8_float32` sur ce CPU lorsque l’API reçoit `compute_type='int8'` : quantification int8 avec opérations flottantes CPU. Le contrôle accepte désormais int8 ou int8_float32 en exigeant toujours device=cpu ; le paramètre demandé reste int8. Aucun changement de modèle ou de dépendance. Logs du premier échec conservés sous `incident-A-stt*`, puis transcriptions réellement exécutées avec succès. Pas de reprise de l’incident PyAV19.

**ÉCHEC non résolu : aucun problème bloquant.** L’écart lexical du second essai est une limite de reconnaissance, pas masqué comme un succès parfait.

## 5. Mesures et comparaison Mission 12

Temps en secondes ; pic RSS échantillonné toutes les 20 ms ; CPU moyen 100 % = un cœur occupé. Le chargement inclut les imports du moteur. Les moteurs sont exécutés successivement, jamais simultanément avec Qwen.

| Essai | Chargement s | Traitement s | Pic RSS Mio | CPU moyen | RTF |
|---|---:|---:|---:|---:|---:|
{rows}

WAV A : {results['A-tts']['wav_validation']['duration_s']:.3f} s ; WAV D : {results['D-tts']['wav_validation']['duration_s']:.3f} s. Chaque résultat conserve RMS, pic, frames, débit d’échantillonnage, CPU consommé, PID et affinité `[0,1]`. Aucun seuil RAM/temps franchi ; minimum RAM disponible pendant les essais supérieur à 25 Gio.

Mission 12 : Tom chargeait en 3,42 s, synthèse 0,71–0,91 s, RTF médian 0,091, RSS 444 Mio ; small chargeait en 0,69 s, transcription 2,13–2,27 s, RTF médian 0,264, RSS 1263 Mio. Ici Tom utilise une seule session bornée dès sa construction, évitant le double chargement du worker Mission 12 ; sa baisse de chargement/RSS ne prouve pas une amélioration du moteur. Les phrases de Mission 13A sont plus courtes et différentes : les RTF STT ne sont pas directement un benchmark comparable. Les deux chargements small sont voisins de Mission 12 et les transcriptions prennent environ 2 secondes.

Disque mesuré avant finalisation documentaire : **1 230 888 960 octets alloués** (environ 1,15 Gio), dont venv 513 351 680, modèles 549 769 216 et wheels 167 632 896. La documentation finale ajoute quelques kilo-octets ; occupation finale consignée dans final-disk.json. Les wheels sont volontairement conservés pour reconstruction hors ligne. Les caches contiennent uniquement les métadonnées locales ONNX Runtime observées, pas de modèle récupéré pendant les tests.

## 6. Isolation, preuves de préservation et limites

Piper : CPUExecutionProvider exclusif, intra_op=2, inter_op=1, exécution séquentielle ; construction directe PiperVoice avec une session ONNX bornée, sans patch de package. Whisper : device=cpu, cpu_threads=2, num_workers=1, chemin explicite. CUDA_VISIBLE_DEVICES=-1 et bibliothèques numériques bornées ; affinité de chaque worker sur deux CPU ; priorité nice +10. Watchdog 180 s/2 Gio RSS/6 Gio RAM disponible. Processus de test réseau isolé au niveau noyau par unshare net, redescendu en UID1000 sans capability. Vérification supplémentaire : aucune route, seule loopback, connexion refusée avec Network is unreachable. Hook Python connect/bind supplémentaire et HF_HUB_OFFLINE=1.

Aucune libcuda/libcudart/libcublas/libcudnn relevée dans les mappings des workers ; aucun processus compute GPU aux {len(gpu)} échantillons couvrant A-stt et le deuxième cycle. Le premier TTS est confirmé par sa session CPU et les mappings du watchdog ; il n’était pas couvert par ce polling nvidia-smi supplémentaire. Ces mesures sont échantillonnées, pas un monitoring continu de chaque instruction. RTX 3090 : 6 Mio utilisés aux relevés initial/final, aucun modèle Ollama chargé ni test de charge forcé. Aucun pilote, CUDA, eGPU, noyau ou configuration Docker modifié ; aucun reboot, prune ou nettoyage global.

Les hashes des configurations et des 29 fichiers modèles Ollama, les tags et l’inventaire dpkg sont identiques avant/après. Les services restent actifs et aucun nouveau socket en écoute. La base WebUI active n’a pas été ouverte, copiée ou modifiée par la mission ; son égalité binaire n’est pas affirmée, car elle appartient à une application active et aucun hash de base n’a été effectué. Pas d’accès aux chats privés.

**EN ATTENTE / hors périmètre :** écoute humaine et agrément de voix, vrai micro, bruit/écho, conversation Ollama, mémoire applicative, passerelle, interface, service résident, démarrage automatique. Persistance validée par nouveaux processus et fichiers sur disque, pas par reboot. Les propositions systemd sont seulement des tests fichier oneshot ; verify statique sans démarrage. Aucun poids autre que small et Tom installé. Les notices et carte Tom sont conservées ; cette mission n’effectue aucune redistribution des poids.

## 7. Livrables et procédures

- [Preuves](mission13a-preuves/README.md) : before/after, checks de réception, inventaires et empreintes, versions, mesures, journaux et deux WAV.
- [Procédures](mission13a-preuves/PROCEDURES.md) : démarrage manuel, arrêt, contrôle et désinstallation limitée nécessitant validation avant suppression. Copie permanente `/opt/jarvis/voice/docs/PROCEDURES.md`.
- Propositions systemd : `/opt/jarvis/voice/docs/systemd/jarvis-voice-tts.service` et `jarvis-voice-stt.service`, copies dans les preuves. Validation statique réussie, aucune copie dans `/etc/systemd/system`, aucune activation.
- Configuration : `/opt/jarvis/voice/config/voice.json` ; scripts `/opt/jarvis/voice/scripts/run-offline`, `run_guarded.py`, `voice_worker.py`.
- Les sauvegardes privées de configurations restent dans `mission13a-preuves/backup-configs/`; ne pas les diffuser ni les restaurer sans besoin.

**Fin de Mission 13A. Tous les moteurs d’essai sont arrêtés. Attente de validation utilisateur avant toute nouvelle intervention ; aucune Mission 13B commencée.**
'''
report=report.replace('déplacés/cop iés','déplacés/copiés')
(P.parent/'mission13a.md').write_text(report)
shutil.copy2(P.parent/'mission13a.md',R/'docs/mission13a.md')
(P/'README.md').write_text('''# Mission 13A — preuves

[Rapport](../mission13a.md) · [Procédures](PROCEDURES.md)

- `before.json`, `after.json`, `acceptance-checks.json` : intégrité configurations, 29 fichiers modèles Ollama, dpkg, kernel, services, sockets et GET Ollama sans génération.
- `verified-inputs.json`, `installed-models.json`, `requirements-voice-cp313-linux.txt`, `versions.json`, `installation-integrity.json`, `final-disk.json` : versions, chemins, SHA-256, disque, liens et caches.
- `A-tom.wav`, `D-tom.wav` : synthèses locales Piper Tom ; `A-tts`, `A-stt`, `D-tts`, `D-stt` logs/results/guards et measurements-summary.
- `incident-A-stt*` : assertion initiale trop stricte, corrigée pour int8_float32 CPU. Les logs de l’échec ne sont pas écrasés.
- `gpu-during-tests.json`, `offline-namespace.json` : relevés nvidia-smi et test isolation réseau noyau.
- `pip-install.log`, `pip-tooling.log`, `pip-check.log`, `systemd-verify.log` : installation locale sans index, cohérence dépendances, vérification statique propositions systemd.
- `systemd/`, `PROCEDURES.md`, scripts Python et lanceur : reproductibilité ; aucune unité installée/activée.
- `backup-configs/` : copies privées 0700/0600, notamment .env contenant des secrets. Ne pas partager. Les sauvegardes privées sont exclues de SHA256SUMS public.
- `SHA256SUMS` : rapport et preuves partageables ; `installation-SHA256SUMS` : toutes les ressources installées sauf journaux/caches évolutifs.

Les scripts audit/install sont des traces de cette mission, pas une instruction de réinstallation sur un répertoire existant. Les tests réseau isolés fonctionnent via le lanceur permanent. Aucun serveur, micro ni client conversationnel.
''')
print(json.dumps(checks,indent=2))
