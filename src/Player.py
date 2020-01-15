#!/usr/bin/env python

import time
from board import Board
import random
from Carte import Carte
import sysv_ipc
from termcolor import colored


class Player:
    """Object used to represent the player """

    def __init__(self, game_sm, deck_sm, mq, mqType, lock):
        self.hand = []
        self.temps_max = 10
        self.game = game_sm
        self.deck = deck_sm
        self.mq = mq
        self.mqType = mqType
        self.lock = lock
        self.mqTypeBoard = 1

    def __str__(self):
        return self.hand

    def printHand(self):
        for i in range(len(self.hand) - 1):
            print(self.hand[i], " , ")
        print("\n")

    # Function which prints the game state for the player
    def getGameState(self):
        with self.lock:
            print(" L'état du jeu est maintenant le suivant :", "\n")
            print(" Votre main : ")
            self.printHand()
            print(" La dernière carte en jeu est : ", print(self.game[0]), " La pioche contient ", len(self.deck),
                  "cartes")

    # Function which allows the player to pick a card
    def pickCard(self):
        with self.lock:
            new_card = self.deck.pop(0)
            self.hand.append(new_card)

    # Function checking if the card played is valid or not
    def validCard(self,
                  card):  # Je pense pas que ca soit necessaire de mettre game en args pck on l'a dans notre contexte
        with self.lock:
            return (card.num == self.game[0].num and
                    card.col == self.game[0].col) or \
                   (card.num == self.game[0].num - 1) or \
                   (card.num == self.game[0].num + 1)

    def handEmpty(self):
        return len(self.hand) == 0

    def creationMain(self):
        for i in range(5):
            self.pickCard()
        print(colored(self.hand, "blue"))

    def sendMessageToBoard(self, msg):
        self.mq.send(msg.encode(), type=self.mqTypeBoard)

    # Function to receive msg from Board
    def getMesgFromBoard(self):
        value = self.mq.receive(type=self.mqType)[0].decode()
        print(colored("{}".format(self.mqType), "green"))

        if value == "playing":
            print(" WARING DECK AND GAME LOCKED someone is playing")

        if value == "game_update":
            with self.lock:
                print(" WARING , game was updated ")
                self.get_Game_State(self.deck)

        if value == "someone_won":
            print(" WARING a player won")

        if value == "pick_card":  # touche speciale pour piocher
            with self.lock:
                self.pickCard(self.deck)

        if value == "play_card":  # toche spéciale pour jouer
            with self.lock:
                self.playingCard(self.game)

        if value == "creation_main":
            self.creationMain()

    # Function used by the player to put a card on the Game
    def playingCard(self):
        played = False
        seconds = time.time()  # lance timer
        # signal envoyé au père pour dire commence

        while time.time() - seconds < 10 and played == False:  # timer à 10 seconds
            # Recupère infos sur jeu
            # Lock sur Deck et Game

            with self.lock:

                print(" Vous avez 10 secondes pour jouer. Votre jeu est le suivant : ")
                self.printHand()
                num_picked = int(input(" Quelle position dans la liste de cartes souhaitez vous piocher ?"))
                while num_picked > len(self.hand):
                    num_picked = int(input(" Veuillez choisir un rang valide ! "))
                if self.valid_card(self.hand[num_picked], self.game):
                    card_picked = self.hand[num_picked]
                    self.game.insert(0, card_picked)
                    print(" Carte valide et ajoutée")
                if not self.valid_card(self.hand[num_picked], self.game):
                    print(" Carte invalide. Vous avez du piocher")
                    self.pick_card(self.deck)

                played = True

        if played:
            print(" Votre jeu est maintenant le suivant ")

        if not played:
            print(
                "Time's out ! Vous auriez du être plus rapide. Vous avez du piocher. Votre jeu est maintenant le "
                "suivant : ")
            self.pick_card(self.deck)

        self.printHand()
        # Signal envoyé au père pour dire fini
