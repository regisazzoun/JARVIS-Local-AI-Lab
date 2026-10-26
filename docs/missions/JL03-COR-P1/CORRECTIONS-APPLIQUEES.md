# Corrections de capture appliquées — qualification propriétaire à faire

25octobre2026. Sur demande du propriétaire, la correction candidate est installée sur l'accèsJL03existant. **D01/D02 ne sont pas déclarées qualifiées.**

## Changements réels

- La limite de parole est comptée depuis la première activité vocale, et non depuis le silence précédant la commande. Une parole démarrée vers la fin de la fenêtre silencieuse n'est plus coupée immédiatement. La rotation des segments silencieux et la limite de parole restent actives.
- Une génération de capture isole les demandes de microphone et les enregistreurs successifs. Une autorisation tardive, un ancien événementstop ou la fermeture de l'ancienAudioContext ne réactive ni n'écrase la nouvelle capture.
- Un segment terminé est traité une fois. Deux émissions volontairement identiques restent distinctes ; aucun filtrage arbitraire du texte n'est ajouté.
- Couper le microphone conserve une émission déjà enregistrée et ne touche pas aux missions ni à la réponse en cours.

Le changement concerne`site/voice.js`. **Codex a développé cette correction ponctuelle**, après constat queJARVIS n'avait produit aucun patch vocal exploitable et restait bloqué sur ses tests. Les travaux/erreursJARVIS sont conservés dans ses branches isolées ; aucune attribution de ce correctif àJARVIS.

## Contrôles techniques effectués

Huit cas de régression déterministes : avant correction, troisPASS/cinqFAIL ; après, huitPASS. Ils couvrent le silence avant commande, la permissionmicrophone tardive, l'ancien événementstop, la fermeture de l'anciencontexte, l'unicité par segment et les répétitions volontaires, les limites de durée et l'arrêt conservant une émission.

Les neuf contrôlesPython existants passent et les huit modulesJavaScript sont contrôlés syntaxiquement. Les nouveaux tests vocaux font partie de`npm test` via`test:voice`.

Un navigateur réel a injecté unWAV autoriséTTS01 dansWebAudio/MediaRecorder après17,3s de silence, puis utilisé le serviceWhisper canonique : une requêteSTT, un segment et une transcription complète, sans erreur, capture arrêtée proprement. Le temps du scénario était28,87s, **silence et durée duWAV compris** ; ce n'est pas une mesure de latence conversationnelle. La sourcemicrophone est synthétique : acoustique physique et expérience propriétaire restent à qualifier.

Le serviceHTTP retourne exactement l'empreinte du fichier installé. Aucun redémarrage deJL01/JL02, changement de modèleWhisper, mémoire ou routage n'est effectué. Aucunmerge automatiquemain.

## Essais simples du propriétaire

RechargerJL03 puis essayer :

1. Activer le micro, attendre15à17s, prononcer une commande complète ; vérifier transcription et prise en compte sans répéter.
2. Couper puis réactiver rapidement le micro, et parler ; vérifier que la capture reste utilisable.
3. Prononcer volontairement deux fois la même commande en deux émissions ; elles doivent rester distinctes.
4. Interrompre une réponse vocale puis reprendre le dialogue ; noter tout symptôme restant.

D02reste notamment à qualifier sur la capture et les conditions réelles : le corpusSTTcontrôlé passait déjà sans modification du modèle. Ce patch traite une cause concrète de fragmentation ; il ne prétend pas résoudre toute transcription incohérente, toute latence ou les défautsD03/D04/D17.

## Retour arrière

Avant de poursuivre le développement, rebaser les worktreesD01/D02sur cette version pour ne pas écraser la capture installée. La versionprécédente est conservée dansGit et dans la sauvegarde privée de déploiement. Pour un retour ciblé, restaurer uniquement`site/voice.js` depuis le commitparent de la correction, puis recharger la page ; ne pas restaurer toute la politique ou les autres services.
