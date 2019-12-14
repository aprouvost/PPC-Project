* Process fils :

  Communication:
    
    - Pipe avec le pere
    
  Objets:
  
    - Main (dico, initialement 5 cartes piocher)
    - Boark (sharedMemory)
    - Timer
    - OutOfTime (time)
  
  
  Fonctions:
  
   - Piocher carte : signal envoyé au pere
    
      * un siganl est envoyé au pere pour indiquer que le fils pioche
      * la pile est lock pendant que le fils pioche pour eviter que le 2eme fils pioche la meme carte
      * remet le timer a 0
      
      
   **def function pickCard**{
      
        Timer = 0
        send signal from GamerManager player_pick_card
        
   }
      
 -Supprimer une card de la main 
 
  * function appelé quand le pere envoie un signal ( signal envoyé quand mal joué)
  
  **def function delCard(card)**{
  
    main.remove(card)
    
  }
  
  - Timeout -> Pop-up jouer ou piocher lock Pioche et Board + envoyer un signal au pere

      * Le joueur est obligé de jouer ou de piocher apres un temps definie
      * remet le timer a 0
  
  **def function Timeout**{
  
    IF (Timer == OutOfTime) do:
      Timer = 0
      print ( "jouer une carte ou piocher")
    END IF
    
  }
  
- freezTimer : signal du pere quand timeout de l'autre joueur

  * quand le timer arrive a expiration de l'autre joueur celui-ci se freez
  * lorsque l'autre joueur a jouer ou piocher son timer reprend
  
  **def function freezTimer**{
  
  
    IF ( received signal from GameManager saying player_A_TimeOut) do:
      Timer.pause
    END IF
    WHILE (not received signal from GameManger saying palyer_A_play) do nothing
    END WHILE
    Timer.replay
    
  }
  
- Poser carte : signal envoyé au pere + retour du pere pour supprimer la carte si valid sinon garder la carte et piocher

  * un signal est envoyer au pere indiquant que le joueur veut jouer ( cette demande est mis dans la message queue)
  * le pere verifie la jouabilité de la carte : 
  
        + si pas jouable : le pere envoie un signal au fils de piocher
        + si jouable : le pere envoie un signal au fils de supprimer la crte qu'il joue
  * remet le timer a 0
  
  **def function palyCard(card)**{
  
  
    Timer = 0
    send signal from GameManager player_play card
    WHILE (not received signal from GameManager cant_play || can_paly) do nothing
    END WHILE
    IF (signal received is cant_play) do:
      pickCard()
    ELSE do:
      delCard(card)
    END IF
    
  }
  
- UpdateBoard : signal du pere pour update quand l'autre a jouer

  * un signal est envoyé par le pere pour indiquer un changement de la carte au dessus du Board
  * le joueur recupere la carte qui est sur le Board et met a jour celle qui est affiché a l'ecran
  
  **def updateBoard**{
  
  
    IF (received signal from GameManager update_board) do:
    Board.get
    END IF
    
  }
