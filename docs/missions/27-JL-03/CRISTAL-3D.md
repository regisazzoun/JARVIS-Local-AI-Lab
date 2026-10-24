# Cristal et audio

Prototype séparé `/prototype.html` : commandes des trois états graphiques simulés, spectre simulé identifié, choixWAV, WAVprivé de test et microphone réel. Le mode principal n'active pas de simulation.

Icosaèdre facetté semi-transparent et déformations irrégulières ; arêtes et sommets lumineux, variations par facette, rotation et mouvement de repos permanents. Trois couleurs imposées : écoute bleu, traitement rouge, parole vert. La machine d'état prend en compte la requête, la mission sélectionnée et la lecture réelle ; le bouton microphone n'est pas le sélecteur de couleur.

FFT2048,16 bandes logarithmiques de60à12000Hz, lissage, zones basses/médiums/aigus distinctes et déformations directionnelles. Le filaire utilise la même transformation que les facettes. Ce n'est pas une simple échelle proportionnelle au volume. Le budget est plafonné à30images/s,4lorsque l'onglet est masqué et DPR1,5. Les pistes externes analysées ne sont pas arrêtées par l'orbe.

Les premiers essais ont découvert un mauvais typeFFT, des exports/constructeurs invalides, une absence d'appelrenderer.render, des compteurs non probants et un arrêt indu de pistes. Les sources originales sont conservées ; les réparations sont attribuées à Codex. Des captures initiales du cristal étaient vides : elles ne constituent pas les images de réception.

Réception : rendu WebGL réellement visible et3drawcalls sur le code final ; vraiWAVet vraiPiper analysés, pic de bande0,748. Les tons120/1200/6000Hz ont alimenté des zones différentes ; les vecteurs de transformation contrôlés sont des fixtures distinctes du signal réel. Chromium utilise SwiftShader : aucun chiffre de performanceMacBook ou GPU navigateur physique n'est déduit. Appréciation visuelle finale au propriétaire.
