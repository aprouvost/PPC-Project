

class Carte(int num, String col):
    """Object used to represent the cards present in the Deck initially, and in the player's hand """

    def __init__(self, num, col):
            self.num= num
            self.col=col

    def new_Card(num,col):
        card=Carte(num,col)
        return card
