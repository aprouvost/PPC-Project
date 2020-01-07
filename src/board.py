#!/usr/bin/env python

import random
import threading
from Carte import Carte
from multiprocessing import Process, Array
from multiprocessing.connection import Pipe
import sysv_ipc
import socket

TCP_IP = "127.0.0.1"
TCP_PORT = "666"
BUFFER_SIZE = 1024


class Board:

    def __init__(self):
        self.deck = []
        self.game = []

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

    def playerWin(self, sig):
        return sig.split(":")[1] == "empty hand"

    def getGameSettings(self):
        print("Game state : the deck has ", len(self.deck), "cards", "\n number of cards in player one's hand : ",
              "\n number of cards in player two's hand : ", )  # A compléter

    def gameCreation(self):
        self.game = self.deck.pop(0)
        return self.game

    def playerPlayingCard(self, sig, fils_addr_list):
        if sig.split(":")[1] == "play a card":
            if self.checkIfValid(sig.split(":")[2]):
                card = Carte(sig.split(":")[2].split()[0], sig.split(":")[2].split()[1])
                self.game = card
                player.hand.remove(card)

                for addr, port in fils_addr_list:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((addr, port))
                    s.send(bytes("update game"))
            else:
                player.pickCard()



if __name__ == "__main":

    key = 666
    lock = threading.Lock()
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    global MEMORY_SIZE
    MEMORY_SIZE_DECK = 20
    MEMORY_SIZE = 100
    deck_shared_memory = Array('i', MEMORY_SIZE_DECK)
    game_shared_memory = Array('i', MEMORY_SIZE)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    data = ""
    print("Connection from", addr)

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

        # Faire un waiting pour attendre que tous les joueurs soient connecté

        # for n in range(player_nb):
        #     process_fils_list.add(Process(target=child,
        #                                   args=((parent_conn, child_conn), deck_shared_memory, game_shared_memory)
        #
        #     for p in process_fils_list:
        #         p.start()
        #
        #     for i in range(4)
        #         p.pickCard()

        while Board.playerWin(data) or Board.playerLost():  # Board.playerWins à définir
            data = conn.recv(BUFFER_SIZE)
            if not data:
                continue
            else:
                pass  # fonctions avec la communication des fils
            Board.playerPlayingCard(data, fils_addr_list)

        Board.getGameSettings()
        while data.split(":")[1] == "end ok":
            pass

        child_conn.close()
        parent_conn.close()
        mq.remove()

        for p in process_fils_list:
            p.terminate()

        for p in process_fils_list:
            p.join()
