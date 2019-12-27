

PROCESS BOARD
 def function shuffleCards() {

     shuffle(cards)
     returns cards
}

 def function deckCreation(numberOfRepeat) {

card_colors = ["red", "blue"]
card_types = list of integers between 0 and 10

for nb in range(1,numberOfRepeat) do:
  for color in card_colors do :
    for card in card_types do:
      add to Deck ({'type': card_type, 'color' :color})
    End for
  End for
End for
returns Deck
 }

 def function GameCreation() {

new type dictionnary {'type', 'color'} -> Game 
returns Game
 }



def playerWins() {

 Boolean wins <- False
IF ( received signal from son saying the player's hand is empty) do:
    wins<- True
END IF
returns wins

 }


def playerLost() {

 Boolean lost <- False
IF ( Deck is empty) do:
    lost<- True
End IF
returns lost
 }


def getGameSettings() {

 Print ( Game state, number of cards in players’ hands	, if Deck is empty )
 }


def playerPlayingCard() {

 IF ( received signal from player saying he wants to play a new_card) do:
    IF checkIfValid(card) do:
      Game = new_card
      player.hand.remove( new_card)
      send player_two(Game_state)
      getGameSettings()
    ELSE do:
     player.pickCard()
END IF
}

checkIfValid() {

 Boolean isValid <- False
IF (received_card == Game.color OR received_card == Game.type) do:
    isValid <- True
END IF
returns isValid
 }


timeOutPlayer() {

 IF ( received signal from player_A saying timeOut) do:
    player_A.lock ( Deck )
    player_A.lock ( Game )
    send player_B ( freeze timer)
END IF
 }

def send_message (value){
try:
    	value =  str(value)
except:
    	print("Input error, try again!")
message = value.encode()
	mq.send(message)

}


main {
	key= 666
lock = threading.Lock()
mq =sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
Global MEMORY_SIZE=100
deck_shared_memory = Array ('i', MEMORY_SIZE)
game_shared_memory = Array ('i', MEMORY_SIZE)


valid_player_nb = FLASE
	player_nb = input(“combien de joueurs ?”)
WHILE not valid_player_nb do:
		try:
			valid_player_nb = (int(player_nb)
		except ValueError:
			player_nb = input(“Il faut saisir un nombre”)
	END WHILE

	deckCreation(player_nb // 2)
process_fils_list = []
for n in range(player_nb) do:
		process_fils_list.add( Process(target=child, args=( (parent_conn, child_conn), deck_shared_memory, game_shared_memory)
END FOR
for p in process_fils_list do:
	p.start()
 	FOR i IN range(4) do:
		p.pickCard() 
	END FOR
END FOR
parent_conn , child_conn = Pipe ()
shuffleCards() 
GameCreation() 

WHILE (playerWins() or playerLost()) do:
playerPlayingCard()
timeOutPlayer()
END WHILE
getGameSettings()
WHILE (players don't click OK button) do: nothing
END WHILE


child_conn.close()
parent_conn.close()
mq.remove()
for p in process_fils_list do:
	p.terminate()
END FOR
for p in process_fils_list do:
	p.join()
END FOR
}


PROCESS PLAYER
def function child(parent_conn, child_conn){
	while True:
    	phrase = child_conn.recv()
}
def function pickCard(){
  Timer = 0
  send signal from GamerManager player_pick_card
}
def function delCard(card){
hand.remove(card)
}
def function Timeout(){
IF (Timer == OutOfTime) do:
Timer = 0
  print ( "jouer une carte ou piocher")
END IF
}
def function freezTimer(){

IF ( received signal from GameManager saying player_A_TimeOut) do: 
Timer.pause
 END IF
 WHILE (not received signal from GameManger saying palyer_A_played) do nothing 
END WHILE 
Timer.replay()
}
def function palyCard(card){
Timer = 0 
send signal from GameManager player_play card
 WHILE (not received signal from GameManager cant_play || can_paly) do nothing END WHILE 
IF (signal received is cant_play) do: 
pickCard() 
ELSE do:
 delCard(card)
 END IF
}

def updateBoard(){
IF (received signal from GameManager update_board) do: 
Board.get
 END IF
}