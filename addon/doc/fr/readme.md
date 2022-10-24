# YoutubeChannelManager
[Gerardo Késsler](http://gera.ar)  

Cette extension vous permet de gérer les chaînes favorites de la plate-forme YouTube avec des raccourcis clavier et une interface invisible et simple.  

## Raccourcis de l'extension

* NVDA + i grec; Active et désactive l'interface invisible.
* Non assigné; Active le lecteur Web personnalisé avec le lien d'une vidéo à partir du presse-papiers.

## Raccourcis disponibles dans l'interface invisible

* échap; Ferme l'interface virtuelle et renvoie les raccourcis clavier à sa fonction par défaut.
* Flèche droite; Se déplace à la chaîne suivante.
* Flèche gauche; Se déplace à la chaîne précédente.
* Flèche bas; Se déplace à la suivante vidéo de la chaîne focalisée.
* Flèche haut; Se déplace à la vidéo précédente de la chaîne focalisée.
* début; Se déplace à la première vidéo de la chaîne focalisée.
* fin; Verbalise la position, le nom de la chaîne, et le nombre de vues de la vidéo.
* n; Ouvre le dialogue pour ajouter une nouvelle chaîne.
* o; Ouvre le lien de la vidéo dans le navigateur par défaut.
* r; Ouvre le lien de l'audio dans un lecteur Web personnalisé.
* c; Copie le lien de la vidéo dans le presse-papiers.
t; Copie le titre de la vidéo dans le presse-papiers.
* d; Obtiens les données de la vidéo et les affichent dans une fenêtre de NVDA.
* b; Active le dialogue de recherche dans la base de données.
* Contrôle + b; Active le dialogue de recherche générale.
* f5; Recherche s'il y a de nouvelles vidéos sur la chaîne focalisée.
* s; Active la fenêtre de configuration de la chaîne focalisée.
* g; Active la fenêtre Options globales.
* Effacement; Élimine la chaîne focalisée, et dans la fenêtre de résultats, il supprime la colonne et retourne à la liste des chaînes.
* contrôle + maj + effacement; Élimine la base de données.
* f1; Active l'aide des commandes.

### Ajouter des chaînes

Pour ajouter une nouvelle chaîne à la base de données, il vous suffit d'ouvrir l'interface virtuelle avec le raccourci pour cette action, par défaut; NVDA + i grec. Et appuyer sur la lettre n.
La fenêtre demande 2 champs. Un nom de la chaîne, et l'URL de celle-ci. Dans ce dernier cas, l'extension permet la saisi des formats d'URL suivants:

* Lien d'une vidéo, qui a généralement le format suivant:

    https://www.youtube.com/watch?v=IdDeLaVideo

* Lien d'une chaîne

    https://www.youtube.com/channel/IdDeLaChaine

Donc un moyen de l'obtenir est en ouvrant une quelconque vidéo sur la page de YouTube via le navigateur, appuyez sur alt et la lettre d pour ouvrir la barre d'adresse et copier l'URL avec contrôle + c, qui sera déjà sélectionnée par défaut.  
Les chaînes peuvent également être ajoutées depuis la liste des résultats globaux. Pour cela, il suffit  d'effectuez la recherche, se situer sur la vidéo de la chaîne à ajouter et appuyez sur la touche n.  
Cela activera le dialogue pour saisir les données de la chaîne, qui seront automatiquement complétées avec le lien et le nom pris depuis Youtube.

### Assistant de mise à jour automatique:

L'extension vous permet de cocher des chaînes comme favorites et d'activer la vérification des nouveautés avec un intervalle de temps stipulée.  
Pour cocher ou décocher une chaîne comme favorite:  

* Activer l'interface virtuelle avec le geste assigné, par défaut, NVDA + i grec.
* Sélectionner la chaîne souhaitée avec les flèches gauche ou droite.
* Activer la fenêtre de configuration de la chaîne avec la lettre s.
* Cocher la case correspondante et appuyez sur le bouton pour enregistrer la configuration.

La vérification des nouveautés dans les chaînes favorites est désactivée par défaut. Pour le modifier, vous devez suivre les étapes suivantes:

* Activer l'interface virtuelle avec le geste assigné, par défaut, NVDA + i grec.
* Activer la fenêtre de configuration globale avec la lettre g.
* Tabuler jusqu'à la liste des options, et sélectionner avec les flèches haut  et bas l'intervalle souhaitée.
* Appuyer sur le bouton pour enregistrer les configurations.

En trouvant des nouveautés, l'extension émettra un son lors de la mise à jour et un message à la fin de celle-ci.

### Recherche de vidéos dans la base de données:

L'extension permet de rechercher par mots-clés entre les vidéos des chaînes ajoutées à la base de données.  

* Activer l'interface virtuelle avec le geste assigné, par défaut, NVDA + i grec.
* Activer la fenêtre de recherche avec la lettre b.
* Écrire un mot ou une phrase de référence.
* Appuyer sur Entrée ou sur le bouton Démarrer la recherche.

Si aucun résultat n'est trouvé, ceci est notifié par un message et l'interface virtuelle n'est pas modifiée.  
Dans le cas de la recherche de vidéos correspondant aux données saisies, ceci est notifié par un message et l'interface de résultats est activée.  
Pour naviguer à travers de celle-ci, cela peut être fait avec les flèches haut et bas. Les mêmes commandes sont disponibles comme dans l'interface  des chaînes; r pour le lecteur Web personnalisé, o pour ouvrir dans le navigateur, etc.  
Pour revenir à l'interface des chaînes vous devez appuyer sur la touche effacement dans l'interface des résultats, qui supprimera cette colonne et retournera à la liste des chaînes et des vidéos.

### Recherche globale:

Pour effectuer une recherche globale en dehors de la base de données, vous devez procéder comme suit:

* Activer l'interface virtuelle avec le geste assigné, par défaut, NVDA + i grec.
* Activer la fenêtre de recherche avec le raccourci contrôle + b.
* Écrire un mot ou une phrase de référence et sélectionner la quantité de résultats à afficher.
* Appuyer sur le bouton Démarrer la recherche.

Si aucun résultat n'est trouvé, ceci est notifié par un message.  
Lorsque des résultats sont trouvés, ceux-ci sont ajoutés à la liste principale que nous pouvons parcourir avec les flèches haut et bas.  
Ici, nous avons également les mêmes raccourcis que dans la recherche de la base de données. O pour ouvrir dans le navigateur, r pour le lecteur Web, c pour copier le lien, etc.  
Si l'une des vidéos est sur une chaîne que vous souhaitez ajouter à la base de données, appuyer sur la lettre n sur cette liste laquelle activera le dialogue de nouvelle chaîne avec les champs du nomb et l'URL déjà complets. Ces champs peuvent être édités si l'on préfère ainsi.  
Comme dans les recherches dans la base de données, pour revenir à la liste des chaînes, vous devez simplement appuyer sur la touche effacement pour supprimer les résultats et revenir à l'interface des chaînes.

### Historique de recherches

L'extension enregistre le texte des 20 dernières recherches globales dans la base de données. 
Pour accéder à l'historique, il vous suffit d'appuyer sur la touche Applications sur le champ d'édition de recherche globale. En appuyant sur celui-ci, un menu contextuel est activé avec les dernières recherches, et en appuyant sur Entrée sur l'un d'eux le champ est complété avec le texte correspondant.

## Traducteurs:

	Rémy Ruiz (Français)
	Ângelo Miguel Abrantes (Portugais)
	Umut KORKMAZ (Turc)
	wafiqtaher (Arabe)

