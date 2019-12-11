
# Process Père ( board)  


PROCESS BOARD 

  * Communication:
    - Pipe avec fils
    

  * Objet:
  
    - Deck en shared memory
    - Board en shared memory
    - Message queue

  * Fonction:
  
    - Fonction mélanger cartes
    
      **def function shuffleCards**{
              shuffle(cards)
              returns cards
          }
        
    - Creation deck ( dico)
    
      **def function deckCreation** {
         card_colors = ["red", "blue"]
         card_types = list of integers between 0 et 10
         
        for color in card_colors do :
          for card_type in card_types do:
            add to Deck ({'type': card_type, 'color': color})
            
        returns Deck
          
      }
      
    - Creation board ( dico 1 entrée, initial: 1 carte piochée deck)
    
      **def function GameCreation** {

          new type dictionnary {'type', 'color'} -> Game 
          returns Game
      
      }


    - Creation fils

    - Fonction gagner ( plus de carte dans main)

    **def playerWins** {

        Boolean wins <- False
        IF ( received signal from son saying the player's hand is empty) do:
            wins<- True
        END IF
        returns wins
    }


    - Fonction perdu ( plus de cartes dans deck)

    **def playerLost** {

        Boolean lost <- False
        IF ( Deck is empty) do:
            lost<- True
        End IF
        returns lost
    }




    - Fonction afficher état du jeu

    **def getGameSettings** {
        
        Print ( Game state, number of cards in player one's hand, number of cards in player two's hand, if Deck is empty )
    }

    - FilsVeutPoser( appelle Verifie est valide, poserCarteDuFils)

    **def playerPlayingCard** {

        IF ( received signal from player saying he wants to play a new_card AND the new_card is correct) do:
            Game = new_card
            player.hand.remove( new_card)
            send player_two(Game_state)
            getGameSettings()
        END IF

    }
    - VerifieEstValide ( pour poser carte + retourne signal si bon ou non)

    **checkIfValid** {

        Boolean isValid <- False
        IF (received_card == Game.color OR received_card == Game.type) do:
            isValid <- True
        END IF
        returns isValid
    }

    - TimeOutUnDesJoueurs ( informe autre joueur, geler timer de l'autre joueur)

    **timeOutPlayer** {

        IF ( received signal from player_A saying timeOut) do:
            player_A.lock ( Deck )
            player_A.lock ( Game )
            send player_B ( freeze timer)

        END IF
    
    }
    
    
  
