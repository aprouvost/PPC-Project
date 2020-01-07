from board import Board
from Carte import Carte

b = Board()

print(b.deckCreation(2))
print(b.deckCreation(3))
print(b.shuffleCards())

l = []

print((not(l)))
print((not(b.deckCreation(2))))


c = Carte(5,"red")
print(c)