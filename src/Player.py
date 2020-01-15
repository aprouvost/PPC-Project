#!/usr/bin/env python

import time
from board import Board
import random
from Carte import Carte
import sysv_ipc


class Player:
    """Object used to represent the player """

    def __init__(self, pipe, game_sm, deck_sm):
        self.hand = []
        self.temps_max = 10
        self.pipe = pipe
        self.game = game_sm
        self.deck = deck_sm

    def __str__(self):
        return self.hand

    # def newPlayer(self, hand):
    #     player = Player(hand) #A voir
    #     return player

    def printHand(self):
        for i in range(len(self.hand) - 1):
            print(self.hand[i], " , ")
        print("\n")

    # Function which prints the game state for the player
    def getGameState(self, deck):
        print(" L'état du jeu est maintenant le suivant :", "\n")
        print(" Votre main : ")
        self.printHand()
        print(" La dernière carte en jeu est : ", print(self.game[0]), " La pioche contient ", len(deck), "cartes")

    # Function which allows the player to pick a card
    def pickCard(self, deck):
        new_card = deck.pop(0)
        self.hand.append(new_card)

    # Function checking if the card played is valid or not
    def validCard(self, card, game):       #Je pense pas que ca soit necessaire de mettre game en args pck on l'a dans notre contexte

        if (card.num == game[0].num and card.col == game[0].col) or (card.num == game[0].num - 1) or (
                card.num == game[0].num + 1):
            return True
        else:
            return False

    def handEmpty(self):
        if len(self.hand) == 0:
            return True
        else:
            return False


    def sendMessageToBoard(self, msg, mq):
        mq.send(msg.encode())

    # Function to receive msg from Board
    def getMesgFromBoard(self, message):

        if message.split(":")[1] == "someone playing":
            print(" WARING DECK AND GAME LOCKED, player ", message.split(":")[0], " is playing")
        elif message.split(":")[1] == "game update":
            print(" WARING , game was updated ")
            self.get_Game_State(self.deck)
        elif message.split(":")[1] == "someone won":
            print(" WARING player ", message.split(":")[0], "won")

    # Function used by the player to put a card on the Game
    def playingCard(self):
        played = False
        seconds = time.time()  # lance timer
        # signal envoyé au père pour dire commence

        while time.time() - seconds < 10 and played == False:  # timer à 10 seconds
            # Recupère infos sur jeu
            # Lock sur Deck et Game

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
