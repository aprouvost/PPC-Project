#!/usr/bin/env python

import random
from Carte import Carte
import sysv_ipc
from termcolor import colored


class Board:

    def __init__(self, game_sm, deck_sm, mq, mqType, lock):
        self.deck = deck_sm
        self.game = game_sm
        self.mq = mq
        self.mqType = mqType
        self.lock = lock

    def deckCreation(self, numberOfReapeat):
        card_color = ["red", "blue"]
        card_types = range(0, 10)
        for nb in range(1, numberOfReapeat):
            for color in card_color:
                for types in card_types:
                    card = Carte(types, color)
                    with self.lock:
                        self.deck.append(card)
        print(colored(self.deck, "cyan"))

    def handling_signal(self):  # si touche de gauche: joueur 1, si touche de droite: joueur 2.
        # Envoi du messa au joueur concerné,
        # prévient les autres
        pass

    def shuffleCards(self):
        with self.lock:
            random.shuffle(self.deck)

    def playerLost(self):
        if not self.deck:
            print(" Plus de cartes dans la pioche tout le monde a perdu ")
            return True
        else:
            return False

    def playerWin(self, sig):
        return sig.split(":")[1] == "empty hand"

    def getGameSettings(self):
        with self.lock:
            print("Game state : the deck has ", len(self.deck), "cards")

    def gameCreation(self):
        with self.lock:
            self.game.append(self.deck.pop(0))

    def sendMessageToPlayers(self, msg, mqPlayer):
        for i in mqPlayer:
            self.mq.send(msg.encode(), type=i)

    def getMessageFromPlayer(self, mqPlayer):
        print(colored(str(self.mqType), "yellow"))
        value = self.mq.receive(type=1)[0].decode()
        print(colored(value, "yellow"))

        if value == "playing":
            self.sendMessageToPlayers("playing", mqPlayer)
        if value == "ended_playing":
            self.sendMessageToPlayers("game_update", mqPlayer)
        if value == "someone_won":
            self.sendMessageToPlayers("someone_won", mqPlayer)
        if value == "creation_jeu":
            self.deckCreation(2)
            print(" CREATION DECK ---------------")
            self.shuffleCards()
            self.gameCreation()
            print(colored(self.game[0], "yellow"))
