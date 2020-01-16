# from auto_install_package import autoInstall
#
# autoInstall()
#
# from termcolor import colored
# from board import Board
# from Carte import Carte
#
#
# b = Board()
#
# print(b.deckCreation(2))
# print(b.deckCreation(3))
# print(b.shuffleCards())
#
# l = []
#
# print((not(l)))
# print((not(b.deckCreation(2))))
#
#
# c = Carte(5,"red")
# c1 = Carte(5,"blue")
# print(c)
# print(c1)
#
# l.append(1)
# l.append(2)
#
# print(l)
#
# print(colored("hello world", "green"))

from Player import Player
from multiprocessing import Manager, Lock
import sysv_ipc

key = 666
deck_sm = Manager().list()
game_sm = Manager().list()
lock = Lock()
mqType = 1
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

joueur = Player(game_sm, deck_sm, mq, mqType, lock)
joueur.playingCard()