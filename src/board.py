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

    def handling_signal(self):  # si touche de gauche: joueur 1, si touche de droite: joueur 2.
        # Envoi du messa au joueur concerné,
        # prévient les autres
        pass

    def shuffleCards(self):
        with self.lock:
            random.shuffle(self.deck)

    def playerLost(self):
        with self.lock:
            print(" Plus de cartes dans la pioche tout le monde a perdu ")
            return not self.deck

    def playerWin(self, sig):
        return sig.split(":")[1] == "empty hand"

    def getGameSettings(self):
        with self.lock:
            print("Game state : the deck has ", len(self.deck), "cards")

    def gameCreation(self):
        with self.lock:
            self.game.append(self.deck.pop(0))

    def sendMessageToPlayers(self, msg):
        self.mq.send(msg.encode())

    def getMessageFromPlayer(self):
        value = self.mq.receive(type=self.mqType)[0].decode()
        print("VALUE RECEIVED   ", value)

        if value == "playing":
            self.send_message_to_players("playing", self.mq)
        if value == "ended_playing":
            self.send_message_to_players("game_update", self.mq)
        if value == "someone_won":
            self.send_message_to_players("someone_won", self.mq)
        if value == "creation_jeu":
            self.deckCreation(2)
            print(" CREATION DECK ---------------")
            self.shuffleCards()
            self.gameCreation()
            print(colored(self.game[0], "yellow"))
