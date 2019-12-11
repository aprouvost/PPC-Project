* interface web avec cherrypi 
* liste de toutes les cartes dans l'ordre
* pour la pile, faire un random sur la liste ( importer shuffle et utiliser un pile.shuffle() pour mélanger) -> N'aura plus qu'à venir tirer une carte sur le dessus à chaque fois qu'on pioche. Mettre un lock dessus
* Initialiser timer en début de jeu. Ré initialise à chaque fois que pose ou pioche. Définition d'un temps limite (je suis pas sur que ca soit necessaire, le sujet dit qu'il n'y a pas de tour de jeu)
* La pile ( deck ) est placée en shared memory car partagée par les deux joueurs. Doit faire des bloquages dessus quand un y accède et compte éventuellement le nombre de cartes restantes
* Les cartes stockées dans un dictionnaire : exemple {'colour': 'blue', 'value': 'two'}


* Signaux échangés entre processus : info sur carte posée 

* Board: Processus père. Vision globale sur tout le jeu , " Game manager"
* Main des joueurs : Processus fils. Vision uniquement de leur jeu + accès au deck et au tas pour poser

* Besoin réactivité et temps d'attente aléatoire pour réponse du joueur: utilisation de multiprocess

*Il faut mettre en place un siganl pour indiqué la mise a jour du Board a l'autre joueur
