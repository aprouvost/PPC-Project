
# Process Père ( board)  

  Communication:
    
    - Pipe avec fils
    

  Objet:
    - Deck en shared memory
    - Board en shared memory
    - Message queue

  Fonctions:
 
    - Fonction mélanger cartes
    - Creation deck ( dico)
    - Creation board ( dico 1 entrée, initial: 1 carte piochée deck)
    - Creation fils
    - Fonction gagner ( plus de carte dans main)
    - Fonction perdu ( plus de cartes dans deck)
    - Fonction fin 
    - Fonction afficher état du jeu
    - FilsVeutPoser( appelle Verifie est valide, poserCarteDuFils)
    - VerifieEstValide ( pour poser carte + retourne signal si bon ou non)
    - poserCarteDuFils ( retirer chez fils, afficher le jeu, poser dans board, update du jeu chez les fils )
    - TimeOutUnDesJoueurs ( informe autre joueur, geler timer de l'autre joueur)
    
    
  
