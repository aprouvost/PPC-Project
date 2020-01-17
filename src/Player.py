#!/usr/bin/env python

import os
import time
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
        hand = ""
        for i in range(len(self.hand)):
            hand += str(self.hand[i]) + " | "
        return hand

    # Function which prints the game state for the player
    def getGameState(self):
        with self.lock:
            print(" L'état du jeu est maintenant le suivant :\n")
            print(" Votre main : {} \n".format(self.printHand()))
            print(" La dernière carte en jeu est : ", self.game[0], " La pioche contient ", len(self.deck),
                  "cartes")

    # Function which allows the player to pick a card
    def pickCard(self):
        # with self.lock:
        new_card = self.deck.pop(0)
        self.hand.append(new_card)

    # Function checking if the card played is valid or not
    def validCard(self, card):
        # with self.lock:
        return (card.num == self.game[0].num - 1 and card.col == self.game[0].col) or \
               (card.num == self.game[0].num + 1 and card.col == self.game[0].col) or \
               (card.num == self.game[0].num)

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

        if self.mq.current_messages != 0:# donne le nombre de message dans la MQ
            value = self.mq.receive(type=0)
            if value[1] == self.mqType:
                decodeValue = value[0].decode()
        # Quand on recoit le msg, il est mit dans un tuple (msg, type) faire une fonction qui recupere les msg et
        # verifie que le msg soit bien pour nous. Pour recuperer n'importe quel msg il faut mettre le type a 0
        # A faire pour le board aussi


                print(colored("{} {}".format(self.mqType, value[0]), "green"))

                if decodeValue == "playing":
                    print(" WARING DECK AND GAME LOCKED someone is playing")

                if decodeValue == "game_update":
                    print(" WARING , game was updated ")
                    self.get_Game_State()

                if decodeValue == "someone_won":
                    print(" WARING a player won")

                if decodeValue == "play_card":  # toche spéciale pour jouer
                    with self.lock:
                        self.playingCard(self.game)

                if decodeValue == "creation_main":
                    self.creationMain()
                if decodeValue == "everyone_looses":
                    print(colored("ENDING", "red"))
                    print("You loose")
                    os.fork()
            else:
                self.mq.send(value[0], type=value[1])

    # Function used by the player to put a card on the Game
    def playingCard(self, card):
        played = False
        seconds = time.time()  # lance timer
        # signal envoyé au père pour dire commence

        print("Playing...")

        while time.time() - seconds < 10 and played == False:  # timer à 10 seconds
            # Recupère infos sur jeu
            # Lock sur Deck et Game

            with self.lock:

                print(" Vous avez 10 secondes pour jouer. Votre jeu est le suivant : ")
                self.printHand()
                num_picked = int(input(" Quelle position dans la liste de cartes souhaitez vous piocher ?"))
                while num_picked > len(self.hand):
                    num_picked = int(input(" Veuillez choisir un rang valide ! "))
                if self.valid_card(self.hand[num_picked]):
                    card_picked = self.hand[num_picked]
                    self.game.insert(0, card_picked)
                    print(" Carte valide et ajoutée")
                if not self.valid_card(self.hand[num_picked]):
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
