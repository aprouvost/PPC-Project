from auto_install_package import autoInstall
autoInstall()

from board import Board
from Carte import Carte
from Player import Player
import random
import threading
from Carte import Carte
from multiprocessing import Process, Array
from multiprocessing.connection import Pipe
import sysv_ipc
import socket

if __name__ == "__main":

    key = 666
    lock = threading.Lock()
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
    global MEMORY_SIZE
    MEMORY_SIZE_DECK = 20
    MEMORY_SIZE = 100
    deck_shared_memory = Array('i', MEMORY_SIZE_DECK)
    game_shared_memory = Array('i', MEMORY_SIZE)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    data = ""
    print("Connection from", addr)

    valid_player_nb = False
    player_nb = input("combien de joueurs ?")
    while not valid_player_nb:
        try:
            valid_player_nb = (int(player_nb))
        except ValueError:
            player_nb = input("Il faut saisir un nombre")

    Board.deckCreation(int(player_nb) // 2)
    Board.shuffleCards()

    parent_conn, child_conn = Pipe()
    Board.GameCreation()
    process_fils_list = []

    # Faire un waiting pour attendre que tous les joueurs soient connecté

    for n in range(player_nb):
        process_fils_list.add(
            Process(target=Player, args=((parent_conn, child_conn), deck_shared_memory, game_shared_memory)))

    for p in process_fils_list:
        p.start()

    for i in range(4):
        p.pickCard()

        while Board.playerWin(data) or Board.playerLost():  # Board.playerWins à définir
            data = conn.recv(BUFFER_SIZE)
            if not data:
                continue
            else:
                pass  # fonctions avec la communication des fils
            Board.playerPlayingCard(data, fils_addr_list)

        Board.getGameSettings()
        while data.split(":")[1] == "end ok":
            pass

        child_conn.close()
        parent_conn.close()
        mq.remove()

        for p in process_fils_list:
            p.terminate()

        for p in process_fils_list:
            p.join()
