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

def joueur(mqBP, mqPB, game_shared_memory, deck_shared_memory, lock):
    print(colored("Player Start", "red"))
    player = Player(game_shared_memory, deck_shared_memory, mqBP, mqPB, lock)
    while True:
        player.getMesgFromBoard()


# Board

def board(mqBP, mqPB, deck_shared_memory, game_shared_memory, lock):
    print(colored("Board Start", "red"))
    board = Board(game_shared_memory, deck_shared_memory, mqBP, mqPB, lock)
    while True:  # fait un kill sur process si un gagne
        board.getMessageFromPlayer()


if __name__ == "__main__":

    keyPB = 666
    keyBP = 667

    lock = threading.Lock()
    mqPB = sysv_ipc.MessageQueue(keyPB, sysv_ipc.IPC_CREAT)
    mqBP = sysv_ipc.MessageQueue(keyBP, sysv_ipc.IPC_CREAT)

    BUFFER_SIZE = 100
    deck_shared_memory = Manager().list()
    game_shared_memory = Manager().list()

    lock = Lock()

    process_pere = Process(target=board, args=(mqBP, mqPB, game_shared_memory, deck_shared_memory, lock))
    process_pere.start()
    mqPB.send("creation_jeu".encode())
    print(deck_shared_memory)

    player_nb = int(input("combien de joueurs ?"))

    # Faire un waiting pour attendre que tous les joueurs soient connecté

    print(" CREATION PROCESS ----------------------")
    process = []
    for n in range(int(player_nb)):
        process.append(
            Process(target=joueur, args=(mqBP, mqPB, deck_shared_memory, game_shared_memory, lock)))

    for p in process:
        print(colored(p, "cyan"))
        p.start()


    for p in process:
        print(" CREATION MAIN ----------------------")
        mqBP.send("creation_main".encode())

    for p in process:
        p.join()

    mqBP.remove()
    mqPB.remove()

    process_pere.terminate()

    for p in process:
        p.terminate()

    print("Fin du jeu ")
