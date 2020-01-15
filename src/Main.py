import time

from auto_install_package import autoInstall

autoInstall()

from termcolor import colored
from board import Board
from Carte import Carte
from Player import Player
import random
import threading
from multiprocessing import Process, Manager, Lock
from multiprocessing.connection import Pipe
import sysv_ipc


# joueurs

def joueur(mq, mqType, game_shared_memory, deck_shared_memory, lock):
    print(colored("Player Start", "red"))
    player = Player(game_shared_memory, deck_shared_memory, mq, mqType, lock)
    while True:
        player.getMesgFromBoard()


# Board

def board(mq, mqType, deck_shared_memory, game_shared_memory, lock):
    print(colored("Board Start", "red"))
    board = Board(game_shared_memory, deck_shared_memory, mq, mqType, lock)
    while True:  # fait un kill sur process si un gagne
        board.getMessageFromPlayer()


if __name__ == "__main__":

    key = 666

    lock = threading.Lock()
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    # mqBP = sysv_ipc.MessageQueue(keyBP, sysv_ipc.IPC_CREAT)

    BUFFER_SIZE = 100
    deck_shared_memory = Manager().list()
    game_shared_memory = Manager().list()

    lock = Lock()

    mqTypeBoard = 1
    process_pere = Process(target=board, args=(mq, mqTypeBoard, game_shared_memory, deck_shared_memory, lock))
    process_pere.start()
    mq.send("creation_jeu".encode(), type=mqTypeBoard)
    print(deck_shared_memory)

    player_nb = int(input("combien de joueurs ?"))

    # Faire un waiting pour attendre que tous les joueurs soient connecté

    print(" CREATION PROCESS ----------------------")
    process = []
    for n in range(int(player_nb)):
        process.append(
            Process(target=joueur, args=(mq, 1 + n + mqTypeBoard, deck_shared_memory, game_shared_memory, lock)))

    for p in process:
        p.start()

    for p in process:
        sendTo = 1 + process.index(p) + mqTypeBoard
        print(" CREATION MAIN ----------------------", sendTo)
        mq.send("creation_main".encode(), type=sendTo)

    for p in process:
        p.join()

    mq.remove()

    process_pere.terminate()

    for p in process:
        p.terminate()

    print("Fin du jeu ")
