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
#
# from Player import Player
# from multiprocessing import Manager, Lock
# import sysv_ipc
#
# key = 6667
# deck_sm = Manager().list()
# game_sm = Manager().list()
# lock = Lock()
# mqType = 1
# mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
#
# msg = "coucou"
#
# mq.send(msg.encode(), type=1)
#
# while True:
#     print(mq.receive(type=1)[0].decode())
#     print(mq.receive(type=2)[0].decode())
#     print(mq.receive(type=3)[0].decode())
#     print(mq.receive()[0].decode())
#
# joueur = Player(game_sm, deck_sm, mq, mqType, lock)
# joueur.playingCard()

# import time
# a= time.time()
# print(a)
# time.sleep(2)
# b = time.time()
# print(int(b-a))

test = [i+2 for i in range(2)]
print(test)