class Carte:
    """Object used to represent the cards present in the Deck initially, and in the player's hand """

    def __init__(self, num, col):
        self.num = num
        self.col = col

    def __str__(self):
        return "{} {}".format(self.col, self.num)

    def new_Card(self, num, col):
        card = Carte(num, col)
        return card
