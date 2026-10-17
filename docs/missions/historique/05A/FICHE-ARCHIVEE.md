> **Reprise documentaire par Codex — mission 00, 17 octobre 2026.** Source locale JARVIS : `/home/adminjarvis/JARVIS-Documentation/missions/mission-05a/README.md`. Texte historique expurgé ; les restrictions et états anciens sont datés. Le [registre courant](../../00-Mission-Pilotage-point-26-10-17/REGISTRE-MISSIONS.md) prévaut pour la consolidation. Les liens vers des preuves privées non publiées restent des références historiques ; leur contenu n’est pas prétendument récupéré.

# Mission 05A

- Identifiant : 05A.
- Date ou période : 12 octobre 2026
- Objectif initial : JARVIS — Mission 05A : sélection du pilote NVIDIA pour le serveur IA
- Matériel mentionné : Macmini8,1 / Quadro RTX 5000
- Logiciels mentionnés : Debian / T2Linux / CUDA / NVIDIA / Ollama / Open WebUI
- État final documentaire : **NON VÉRIFIÉ**. Documents retrouvés ; réception finale non établie dans cette première passe.

## Actions et résultats confirmés

Documents retrouvés ; réception finale non établie dans cette première passe.

Les extraits sourcés ci-dessous conservent le périmètre et les réserves des auteurs. Ils ne constituent pas un nouvel audit du système.

## Problèmes résolus et corrections

Voir les sections de résultats et correctifs des rapports associés ; aucune correction système appliquée pendant la consolidation. Les informations absentes ne sont pas complétées par supposition.

## Problèmes ouverts

Documents retrouvés ; réception finale non établie dans cette première passe.

La réception doit être limitée au périmètre des preuves archivées. Les éventuelles validations ultérieures doivent être consultées séparément.

## Documents et preuves

- README.alternatives (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/README.alternatives`
- README.source (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/README.source`
- bug-control.mk (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/bug-control.mk`
- bug-script (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/bug-script`
- build-module-packages.sh.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/build-module-packages.sh.in`
- changelog (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/changelog`
- control (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/control`
- control.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/control.in`
- control.kmod (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/control.kmod`
- control.md5sum (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/control.md5sum`
- control.models (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/control.models`
- copyright (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/copyright`
- nvidia-detect.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-detect.in`
- nvidia-legacy-173xx.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-legacy-173xx.ids`
- nvidia-legacy-304xx.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-legacy-304xx.ids`
- nvidia-legacy-340xx.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-legacy-340xx.ids`
- nvidia-legacy-390xx-amd64.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-legacy-390xx-amd64.ids`
- nvidia-legacy-390xx.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-legacy-390xx.ids`
- nvidia-legacy-71xx.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-legacy-71xx.ids`
- nvidia-legacy-96xx.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-legacy-96xx.ids`
- nvidia-tesla-418.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-tesla-418.ids`
- nvidia-tesla-440.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-tesla-440.ids`
- nvidia-tesla-450.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-tesla-450.ids`
- nvidia-tesla-460.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-tesla-460.ids`
- nvidia-tesla-470.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-tesla-470.ids`
- nvidia-tesla-535.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/detect/nvidia-tesla-535.ids`
- end-of-life-390.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/end-of-life-390.ids`
- end-of-life-390.list (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/end-of-life-390.list`
- end-of-life-470.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/end-of-life-470.ids`
- end-of-life-470.list (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/end-of-life-470.list`
- firmware-nvidia-gsp.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/firmware-nvidia-gsp.install.in`
- firmware-nvidia-gsp.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/firmware-nvidia-gsp.lintian-overrides.in`
- gbp.conf (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/gbp.conf`
- gen-control.pl (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/gen-control.pl`
- libcuda1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcuda1.install.in`
- libcuda1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcuda1.links.in`
- libcuda1.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcuda1.lintian-overrides.in`
- libcuda1.postinst.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcuda1.postinst.in`
- libcuda1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcuda1.symbols`
- libcudadebugger1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcudadebugger1.install.in`
- libcudadebugger1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcudadebugger1.links.in`
- libcudadebugger1.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcudadebugger1.lintian-overrides.in`
- libcudadebugger1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libcudadebugger1.symbols`
- libegl-nvidia0.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libegl-nvidia0.install.in`
- libegl-nvidia0.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libegl-nvidia0.links.in`
- libegl-nvidia0.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libegl-nvidia0.lintian-overrides.in`
- libegl-nvidia0.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libegl-nvidia0.symbols`
- libegl1-glvnd-nvidia.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libegl1-glvnd-nvidia.install.in`
- libegl1-glvnd-nvidia.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libegl1-glvnd-nvidia.links.in`
- libegl1-glvnd-nvidia.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libegl1-glvnd-nvidia.lintian-overrides.in`
- libegl1-glvnd-nvidia.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libegl1-glvnd-nvidia.symbols`
- libgl1-glvnd-nvidia-glx.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgl1-glvnd-nvidia-glx.install.in`
- libgl1-glvnd-nvidia-glx.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgl1-glvnd-nvidia-glx.links.in`
- libgl1-glvnd-nvidia-glx.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgl1-glvnd-nvidia-glx.lintian-overrides.in`
- libgl1-glvnd-nvidia-glx.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgl1-glvnd-nvidia-glx.symbols`
- libgl1-nvidia-glvnd-glx.docs (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgl1-nvidia-glvnd-glx.docs`
- libgles-nvidia1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles-nvidia1.install.in`
- libgles-nvidia1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles-nvidia1.links.in`
- libgles-nvidia1.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles-nvidia1.lintian-overrides.in`
- libgles-nvidia1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles-nvidia1.symbols`
- libgles-nvidia2.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles-nvidia2.install.in`
- libgles-nvidia2.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles-nvidia2.links.in`
- libgles-nvidia2.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles-nvidia2.symbols`
- libgles1-glvnd-nvidia.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles1-glvnd-nvidia.install.in`
- libgles1-glvnd-nvidia.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles1-glvnd-nvidia.links.in`
- libgles1-glvnd-nvidia.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles1-glvnd-nvidia.lintian-overrides.in`
- libgles1-glvnd-nvidia.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles1-glvnd-nvidia.symbols`
- libgles2-glvnd-nvidia.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles2-glvnd-nvidia.install.in`
- libgles2-glvnd-nvidia.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles2-glvnd-nvidia.links.in`
- libgles2-glvnd-nvidia.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles2-glvnd-nvidia.lintian-overrides.in`
- libgles2-glvnd-nvidia.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libgles2-glvnd-nvidia.symbols`
- libglvnd0-nvidia.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglvnd0-nvidia.install.in`
- libglvnd0-nvidia.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglvnd0-nvidia.lintian-overrides.in`
- libglvnd0-nvidia.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglvnd0-nvidia.symbols`
- libglx-nvidia0.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglx-nvidia0.install.in`
- libglx-nvidia0.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglx-nvidia0.links.in`
- libglx-nvidia0.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglx-nvidia0.lintian-overrides.in`
- libglx-nvidia0.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglx-nvidia0.symbols`
- libglx0-glvnd-nvidia.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglx0-glvnd-nvidia.install.in`
- libglx0-glvnd-nvidia.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglx0-glvnd-nvidia.lintian-overrides.in`
- libglx0-glvnd-nvidia.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libglx0-glvnd-nvidia.symbols`
- libnvcuvid1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvcuvid1.install.in`
- libnvcuvid1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvcuvid1.links.in`
- libnvcuvid1.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvcuvid1.lintian-overrides`
- libnvcuvid1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvcuvid1.symbols`
- libnvidia-allocator1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-allocator1.install.in`
- libnvidia-allocator1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-allocator1.links.in`
- libnvidia-allocator1.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-allocator1.lintian-overrides`
- libnvidia-allocator1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-allocator1.symbols`
- libnvidia-api1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-api1.install.in`
- libnvidia-api1.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-api1.lintian-overrides.in`
- libnvidia-api1.symbols.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-api1.symbols.in`
- libnvidia-cfg1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-cfg1.install.in`
- libnvidia-cfg1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-cfg1.links.in`
- libnvidia-cfg1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-cfg1.symbols`
- libnvidia-eglcore.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-eglcore.install.in`
- libnvidia-eglcore.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-eglcore.lintian-overrides.in`
- libnvidia-eglcore.symbols.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-eglcore.symbols.in`
- libnvidia-encode1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-encode1.install.in`
- libnvidia-encode1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-encode1.links.in`
- libnvidia-encode1.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-encode1.lintian-overrides`
- libnvidia-encode1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-encode1.symbols`
- libnvidia-fbc1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-fbc1.install.in`
- libnvidia-fbc1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-fbc1.links.in`
- libnvidia-fbc1.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-fbc1.lintian-overrides`
- libnvidia-fbc1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-fbc1.symbols`
- libnvidia-glcore.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-glcore.install.in`
- libnvidia-glcore.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-glcore.lintian-overrides.in`
- libnvidia-glcore.symbols.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-glcore.symbols.in`
- libnvidia-glvkspirv.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-glvkspirv.install.in`
- libnvidia-glvkspirv.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-glvkspirv.lintian-overrides.in`
- libnvidia-glvkspirv.symbols.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-glvkspirv.symbols.in`
- libnvidia-gpucomp.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-gpucomp.install.in`
- libnvidia-gpucomp.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-gpucomp.lintian-overrides.in`
- libnvidia-gpucomp.symbols.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-gpucomp.symbols.in`
- libnvidia-ml1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ml1.install.in`
- libnvidia-ml1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ml1.links.in`
- libnvidia-ml1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ml1.symbols`
- libnvidia-ngx1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ngx1.install.in`
- libnvidia-ngx1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ngx1.links.in`
- libnvidia-ngx1.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ngx1.lintian-overrides.in`
- libnvidia-ngx1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ngx1.symbols`
- libnvidia-nvvm4.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-nvvm4.install.in`
- libnvidia-nvvm4.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-nvvm4.links.in`
- libnvidia-nvvm4.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-nvvm4.lintian-overrides`
- libnvidia-nvvm4.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-nvvm4.symbols`
- libnvidia-opticalflow1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-opticalflow1.install.in`
- libnvidia-opticalflow1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-opticalflow1.links.in`
- libnvidia-opticalflow1.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-opticalflow1.lintian-overrides`
- libnvidia-opticalflow1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-opticalflow1.symbols`
- libnvidia-pkcs11-openssl3.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-pkcs11-openssl3.install.in`
- libnvidia-pkcs11-openssl3.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-pkcs11-openssl3.lintian-overrides.in`
- libnvidia-pkcs11-openssl3.symbols.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-pkcs11-openssl3.symbols.in`
- libnvidia-ptxjitcompiler1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ptxjitcompiler1.install.in`
- libnvidia-ptxjitcompiler1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ptxjitcompiler1.links.in`
- libnvidia-ptxjitcompiler1.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ptxjitcompiler1.lintian-overrides.in`
- libnvidia-ptxjitcompiler1.symbols.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-ptxjitcompiler1.symbols.in`
- libnvidia-rtcore.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-rtcore.install.in`
- libnvidia-rtcore.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-rtcore.lintian-overrides.in`
- libnvidia-rtcore.symbols.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvidia-rtcore.symbols.in`
- libnvoptix1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvoptix1.install.in`
- libnvoptix1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvoptix1.links.in`
- libnvoptix1.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvoptix1.lintian-overrides`
- libnvoptix1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libnvoptix1.symbols`
- libopengl0-glvnd-nvidia.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libopengl0-glvnd-nvidia.install.in`
- libopengl0-glvnd-nvidia.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libopengl0-glvnd-nvidia.lintian-overrides.in`
- libopengl0-glvnd-nvidia.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/libopengl0-glvnd-nvidia.symbols`
- control.modules.in.binary.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/module/debian/control.modules.in.binary.in`
- install.modules.in.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/module/debian/install.modules.in.in`
- lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/module/debian/lintian-overrides`
- rules.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/module/debian/rules.in`
- not-installed.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/not-installed.in`
- nv-readme-open.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nv-readme-open.ids`
- nv-readme.ids (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nv-readme.ids`
- nvidia-alternative.dirs.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-alternative.dirs.in`
- nvidia-alternative.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-alternative.lintian-overrides.in`
- nvidia-alternative.maintscript.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-alternative.maintscript.in`
- nvidia-alternative.postinst.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-alternative.postinst.in`
- nvidia-alternative.prerm.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-alternative.prerm.in`
- nvidia-alternative.triggers.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-alternative.triggers.in`
- nvidia-blacklists-nouveau.conf (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-blacklists-nouveau.conf`
- nvidia-cuda-mps.dirs (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-cuda-mps.dirs`
- nvidia-cuda-mps.install (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-cuda-mps.install`
- nvidia-cuda-mps.links (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-cuda-mps.links`
- nvidia-cuda-mps.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-cuda-mps.lintian-overrides`
- nvidia-cuda-mps.manpages (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-cuda-mps.manpages`
- nvidia-detect.install (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-detect.install`
- nvidia-driver-bin.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-driver-bin.install.in`
- nvidia-driver-bin.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-driver-bin.lintian-overrides.in`
- nvidia-driver-libs.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-driver-libs.lintian-overrides`
- nvidia-driver-libs.postinst.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-driver-libs.postinst.in`
- nvidia-driver.docs (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-driver.docs`
- nvidia-egl-common.install (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-egl-common.install`
- nvidia-egl-common.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-egl-common.lintian-overrides`
- nvidia-kernel-dkms.README.Debian (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-dkms.README.Debian`
- nvidia-kernel-dkms.dkms.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-dkms.dkms.in`
- nvidia-kernel-dkms.docs (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-dkms.docs`
- nvidia-kernel-dkms.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-dkms.install.in`
- nvidia-kernel-dkms.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-dkms.lintian-overrides.in`
- nvidia-kernel-source.README.Debian.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-source.README.Debian.in`
- nvidia-kernel-source.docs (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-source.docs`
- nvidia-kernel-source.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-source.install.in`
- nvidia-kernel-support.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-support.install.in`
- nvidia-kernel-support.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-support.links.in`
- nvidia-kernel-support.postinst.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-support.postinst.in`
- nvidia-kernel-support.postrm.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-kernel-support.postrm.in`
- nvidia-legacy-check.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-legacy-check.lintian-overrides`
- nvidia-legacy-check.preinst.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-legacy-check.preinst.in`
- nvidia-legacy-check.templates (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-legacy-check.templates`
- nvidia-libopencl1.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-libopencl1.install.in`
- nvidia-libopencl1.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-libopencl1.links.in`
- nvidia-libopencl1.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-libopencl1.lintian-overrides`
- nvidia-libopencl1.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-libopencl1.symbols`
- nvidia-load.conf.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-load.conf.in`
- nvidia-modprobe.conf.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-modprobe.conf.in`
- nvidia-opencl-common.install (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-opencl-common.install`
- nvidia-opencl-icd.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-opencl-icd.install.in`
- nvidia-opencl-icd.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-opencl-icd.links.in`
- nvidia-opencl-icd.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-opencl-icd.lintian-overrides.in`
- nvidia-opencl-icd.symbols (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-opencl-icd.symbols`
- nvidia-options.conf.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-options.conf.in`
- nvidia-powerd.examples (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-powerd.examples`
- nvidia-powerd.install (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-powerd.install`
- nvidia-powerd.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-powerd.lintian-overrides`
- nvidia-smi.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-smi.install.in`
- nvidia-smi.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-smi.lintian-overrides.in`
- nvidia-suspend-common.install (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-suspend-common.install`
- nvidia-suspend-common.lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-suspend-common.lintian-overrides`
- nvidia-vdpau-driver.docs (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-vdpau-driver.docs`
- nvidia-vdpau-driver.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-vdpau-driver.install.in`
- nvidia-vdpau-driver.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-vdpau-driver.links.in`
- nvidia-vulkan-common.install (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia-vulkan-common.install`
- nvidia.NEWS (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia.NEWS`
- nvidia.README.Debian.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/nvidia.README.Debian.in`
- man-fixes-nvidia-smi.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/man-fixes-nvidia-smi.patch`
- 0001-bump-minimum-supported-kernel-version-to-3.10.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0001-bump-minimum-supported-kernel-version-to-3.10.patch`
- 0002-conftest.sh-remove-empty-lines-from-uts_release-outp.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0002-conftest.sh-remove-empty-lines-from-uts_release-outp.patch`
- 0034-fix-typos.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0034-fix-typos.patch`
- 0042-Log-an-error-message-when-nv_mem_client_init-fails-d.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0042-Log-an-error-message-when-nv_mem_client_init-fails-d.patch`
- 0046-backport-nv_get_kern_phys_address-changes-from-555.4.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0046-backport-nv_get_kern_phys_address-changes-from-555.4.patch`
- 0052-backport-uvm-warning-fixes-from-560.28.03.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0052-backport-uvm-warning-fixes-from-560.28.03.patch`
- 0053-fix-more-warnings.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0053-fix-more-warnings.patch`
- 0054-backport-warning-fixes-from-575.51.02.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0054-backport-warning-fixes-from-575.51.02.patch`
- 0058-backport-warning-fixes-from-565.57.01.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0058-backport-warning-fixes-from-565.57.01.patch`
- 0062-Support-BTF-generation-for-non-release-builds.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0062-Support-BTF-generation-for-non-release-builds.patch`
- 0062-let-pahole-ignore-c-11-in-addition-to-c.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0062-let-pahole-ignore-c-11-in-addition-to-c.patch`
- 0063-backport-drm_client_setup.h-changes-from-570.124.04.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0063-backport-drm_client_setup.h-changes-from-570.124.04.patch`
- 0065-backport-ccflags-y-changes-from-570.153.02.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0065-backport-ccflags-y-changes-from-570.153.02.patch`
- 0066-backport-nv_timer_delete_sync-changes-from-570.153.0.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0066-backport-nv_timer_delete_sync-changes-from-570.153.0.patch`
- 0068-backport-__iowrite64_lo_hi-changes-from-570.153.02.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0068-backport-__iowrite64_lo_hi-changes-from-570.153.02.patch`
- 0069-backport-page_pgmap-changes-from-570.153.02.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0069-backport-page_pgmap-changes-from-570.153.02.patch`
- 0070-backport-make_device_exclusive-changes-from-570.153..patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0070-backport-make_device_exclusive-changes-from-570.153..patch`
- 0071-backport-nv_vma_start_write-changes-from-570.169.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0071-backport-nv_vma_start_write-changes-from-570.169.patch`
- 0072-backport-iommu_dev_enable_feature-changes-from-535.2.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0072-backport-iommu_dev_enable_feature-changes-from-535.2.patch`
- 0073-backport-NV_DRM_FBDEV_AVAILABLE-changes-from-570.169.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0073-backport-NV_DRM_FBDEV_AVAILABLE-changes-from-570.169.patch`
- 0074-backport-drm_fb_create_takes_format_info-changes-fro.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/0074-backport-drm_fb_create_takes_format_info-changes-fro.patch`
- bashisms.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/bashisms.patch`
- cc_version_check-gcc5.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/cc_version_check-gcc5.patch`
- conftest-prefer-arch-headers.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/conftest-prefer-arch-headers.patch`
- conftest-verbose.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/conftest-verbose.patch`
- series (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/series`
- use-kbuild-compiler.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/use-kbuild-compiler.patch`
- use-kbuild-flags.patch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/module/use-kbuild-flags.patch`
- series-postunpack (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/patches/series-postunpack`
- POTFILES.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/POTFILES.in`
- ca.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/ca.po`
- cs.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/cs.po`
- da.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/da.po`
- de.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/de.po`
- es.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/es.po`
- fr.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/fr.po`
- gl.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/gl.po`
- it.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/it.po`
- ja.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/ja.po`
- nl.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/nl.po`
- pl.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/pl.po`
- pt.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/pt.po`
- pt_BR.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/pt_BR.po`
- ro.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/ro.po`
- ru.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/ru.po`
- sk.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/sk.po`
- sv.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/sv.po`
- templates.pot (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/templates.pot`
- tr.po (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/po/tr.po`
- rules (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/rules`
- rules.defs (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/rules.defs`
- format (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/source/format`
- lintian-overrides (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/source/lintian-overrides`
- nvidia.conf (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/systemd-homed.service.d/nvidia.conf`
- nvidia.conf (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/systemd-suspend.service.d/nvidia.conf`
- autopkgtest-pkg-dkms.conf (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/tests/autopkgtest-pkg-dkms.conf`
- autopkgtest-pkg-dkms.conf.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/tests/autopkgtest-pkg-dkms.conf.in`
- control (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/tests/control`
- control.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/tests/control.in`
- metadata (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/upstream/metadata`
- watch (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/watch`
- watch.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/watch.in`
- xserver-xorg-video-nvidia.docs (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/xserver-xorg-video-nvidia.docs`
- xserver-xorg-video-nvidia.install.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/xserver-xorg-video-nvidia.install.in`
- xserver-xorg-video-nvidia.links.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/xserver-xorg-video-nvidia.links.in`
- xserver-xorg-video-nvidia.lintian-overrides.in (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/xserver-xorg-video-nvidia.lintian-overrides.in`
- xserver-xorg-video-nvidia.postrm (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/membres/7443113cc564/debian/xserver-xorg-video-nvidia.postrm`
- __init__.py (référence locale historique non publiée)
- config-6.18.54-1-t2-trixie (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission04K-preparation/hote-[UUID EXPURGÉ]-20261011-215637/config-6.18.54-1-t2-trixie`
- 595-Kbuild.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/595-Kbuild.txt`
- 595-README.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/595-README.txt`
- 595-conftest.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/595-conftest.txt`
- 595-dependances.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/595-dependances.json`
- 595-egpu.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/595-egpu.txt`
- 595-supportedchips.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/595-supportedchips.txt`
- SHA256SUMS (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/SHA256SUMS`
- backports-nonfree-Packages.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/backports-nonfree-Packages.txt`
- backports-nonfree-selection.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/backports-nonfree-selection.json`
- backports-patches.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/backports-patches.txt`
- backports-source-index.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/backports-source-index.txt`
- cuda-bibliotheques.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/cuda-bibliotheques.json`
- dkms-config.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/dkms-config.txt`
- etat-local.stderr (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/etat-local.stderr`
- etat-local.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/etat-local.txt`
- nvidia-debian13-Packages.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-debian13-Packages.txt`
- nvidia-debian13-selection.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-debian13-selection.json`
- control (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-driver-cuda-control/control`
- md5sums (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-driver-cuda-control/md5sums`
- nvidia-driver-cuda-regles.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-driver-cuda-regles.txt`
- nvidia-driver-pinning-595-config.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-driver-pinning-595-config.txt`
- conffiles (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-driver-pinning-595-control/conffiles`
- control (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-driver-pinning-595-control/control`
- md5sums (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-driver-pinning-595-control/md5sums`
- control (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-open-dkms-control/control`
- md5sums (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-open-dkms-control/md5sums`
- postinst (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-open-dkms-control/postinst`
- prerm (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-open-dkms-control/prerm`
- nvidia-kernel-support-config.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-support-config.txt`
- conffiles (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-support-control/conffiles`
- control (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-support-control/control`
- md5sums (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-support-control/md5sums`
- postinst (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-support-control/postinst`
- postrm (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/nvidia-kernel-support-control/postrm`
- ollama-install.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/ollama-install.txt`
- paquets-locaux.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/paquets-locaux.txt`
- sources.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/sources.json`
- trixie-nonfree-Packages.txt (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/trixie-nonfree-Packages.txt`
- trixie-nonfree-selection.json (référence locale historique non publiée) — membre `archives/recuperation-2026-10-14/sources/home/adminjarvis/JARVIS/rapports/mission05A-preuves/trixie-nonfree-selection.json`
- mission05A.md (référence locale historique non publiée)

## Références et dépendances

05-I, 05A-P. Les citations sont des références documentaires ; leur présence ne prouve pas une dépendance d’exécution. Les successeurs sont recensés par recherche inverse dans les README et la chronologie.

## Extraits des rapports

### mission05A.md (référence locale historique non publiée)

Date : 12 octobre 2026, Europe/Paris. Macmini8,1, Debian 13, noyau `6.18.54-1-t2-trixie`. Mission documentaire : lectures locales, consultation des sources officielles et téléchargement de métadonnées/paquets **pour inspection dans le répertoire de preuves seulement**. Aucun paquet installé, aucun script de maintenance exécuté, aucun module chargé, aucun dépôt système modifié, aucune compilation, aucun changement initramfs/GRUB/EFI, aucun redémarrage ou branchement.

## 1. Décision proposée

**Candidat recommandé : NVIDIA 595.91.07-1 du dépôt NVIDIA Debian 13, modules ouverts via `nvidia-kernel-open-dkms`, composants de calcul via `nvidia-driver-cuda`.** Recommandation conditionnelle : compilation DKMS réussie pour le noyau exact, cohérence des bibliothèques/firmware/modules, puis validation CUDA et hotplug. **La compatibilité opérationnelle avec 6.18.54 T2Linux n’est pas encore démontrée.**

La Quadro RTX 5000 Turing `10de:1eb0`, compute capability **7.5**, est explicitement prise en charge. Les sources 595 comprennent des adaptations aux API de Linux 6.18. Le choix du module ouvert suit la recommandation NVIDIA pour les GPU compatibles ; un module propriétaire n’est pas intrinsèquement préférable pour ce Turing. Les deux variantes utilisent les mêmes composants NVIDIA en espace utilisateur et ne peuvent pas être installées ensemble. Sources : [GPU et sources 595.91.07](https://github.com/NVIDIA/open-gpu-kernel-modules/blob/595.91.07/README.md), [comparaison des modules](https://download.nvidia.com/XFree86/Linux-x86_64/595.91.07/README/kernel_open.html).

La branche 595 est une branche production. La publication graphique amont annonce déjà **595.104.02**, alors que le dépôt Debian 13 consulté fournit encore **595.91.07-1**. Ne pas confondre dernière version amont et dernière version APT disponible. Recontrôler les correctifs de sécurité et la disponibilité avant toute installation ; si une révision production plus récente entre dans le dépôt, la réévaluer plutôt q
