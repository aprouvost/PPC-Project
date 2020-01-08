#!/usr/bin/env python

import random
from Carte import Carte
import sysv_ipc


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

    def sendMessageToPlayers(self, msg):  #Redefinir avec sysv_ipc
        for addr, port in fils_addr_list:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((addr, port))
            s.send(bytes(msg))

    def getSignalFromProcess(self, sig, fils_addr_list):
        if sig.split(":")[1] == "starts playing":
            self.send_message_to_players("{} playing".format(sig.split(":")[0]))
        elif sig.split(":")[1] == "ended playing":
            self.send_message_to_players("update game")

    #Function used when press bar is hit to know which process is playing
    def getNumProcess(self):
        num = int(input( " Quel joueur a tapé la barre espace ? ( entrez le numéro du process ) "))