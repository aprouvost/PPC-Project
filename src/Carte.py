#!/usr/bin/env python

from termcolor import colored


class Carte:
    """Object used to represent the cards present in the Deck initially, and in the player's hand """

    def __init__(self, num, col):
        self.num = num
        self.col = col

    def __str__(self):
        return colored("{} {}".format(self.col, self.num), self.col)
