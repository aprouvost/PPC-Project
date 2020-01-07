import random
import threading
from Carte import Carte
from multiprocessing import Process, Array
from multiprocessing.connection import Pipe

import sysv_ipc


class Board:

    def __init__(self):
        self.deck = []

    def deckCreation(self, numberOfReapeat):
        card_color = ["red", "blue"]
        card_types = range(0, 9)

        for nb in range(1, numberOfReapeat):
            for color in card_color:
                for types in card_types:
                    card = Carte(color, types)
                    self.deck.append(card)

        return self.deck

    def shuffleCards(self):
        random.shuffle(self.deck)
        return self.deck

    def playerLost(self):
        return not self.deck

    def getGameSettings(self):
        print( "Game state : the deck has ", len(deck), "cards", "\n number of cards in player one's hand : ",    "\n number of cards in player two's hand : ",      )  # A compléter



if __name__ == "__main":

    key = 666
    lock = threading.Lock()
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    global MEMORY_SIZE
    MEMORY_SIZE_DECK = 20
    MEMORY_SIZE=100
    deck_shared_memory = Array('i', MEMORY_SIZE_DECK)
    game_shared_memory = Array('i', MEMORY_SIZE)

    valid_player_nb = False
    player_nb = input("combien de joueurs ?")
    while not valid_player_nb:
        try:
            valid_player_nb = (int(player_nb))
        except ValueError:
            player_nb = input("Il faut saisir un nombre")

        Board.deckCreation(int(player_nb) // 2)
        Board.shuffleCards()

        parent_conn, child_conn = Pipe()
        Board.GameCreation()
        process_fils_list = []

        # for n in range(player_nb):
        #     process_fils_list.add(Process(target=child,
        #                                   args=((parent_conn, child_conn), deck_shared_memory, game_shared_memory)
        #
        #     for p in process_fils_list:
        #         p.start()
        #
        #     for i in range(4)
        #         p.pickCard()

        while Board.playerWins() or Board.playerLost():  #Board.playerWins à définir
            Board.playerPlayingCard()
            Board.timeOutPlayer()

        Board.getGameSettings()
        while ("players don't click OK button"):
            pass

        child_conn.close()
        parent_conn.close()
        mq.remove()

        for p in process_fils_list:
            p.terminate()

        for p in process_fils_list:
            p.join()
