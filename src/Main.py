#!/usr/bin/env python
import os

from auto_install_package import autoInstall

autoInstall()

from termcolor import colored
from board import Board
from Player import Player
from io import TextIOWrapper, BytesIO
from multiprocessing import Process, Manager, Lock

import sysv_ipc
import time
import sys
import socket
import threading


# joueurs


def joueur(mq, mqType, game_shared_memory, deck_shared_memory, lock):
    print(colored("Player Start", "red"))
    player = Player(game_shared_memory, deck_shared_memory, mq, mqType, lock)
    player.getMesgFromBoard()

    TCP_IP = "192.168.43.100"
    TCP_PORT = 667 + mqType
    TCP_BUFFER = 20
    old_stdout = sys.stdout
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print(colored("Waiting TCP conn : {}".format(mqType), "green"))
    conn, addr = s.accept()
    print(colored("Connection address: {}".format(addr), "green"))

    def sortie():
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
        print("Appuyer sur une touche pour sortir")
        sendToClient()
        restore_stdout()
        data = conn.recv(TCP_BUFFER).decode()
        if data:
            pass
        print(mqType, ' sortie ! ')
        time.sleep(1)
        conn.close()
        sys.exit(0)

    def sendToClient():
        sys.stdout.seek(0)
        reponse = sys.stdout.read()
        # print(" DEBUG sending response to client : ", reponse)
        conn.send(str(reponse).encode())

    def restore_stdout():
        sys.stdout.close()
        sys.stdout = old_stdout

    def timer():
        # print(" Gets inside the timer")
        time.sleep(10)
        sys.exit(0)

    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
    player.getGameState()
    sendToClient()
    restore_stdout()

    while True:

        print(colored("Checking for mq", "green"))
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
        player.getMesgFromBoard()
        sendToClient()
        restore_stdout()

        if player.handEmpty():
            player.sendMessageToBoard("someone_won")
            print(" Un joueur a gagné ! ")
            sortie()

        if len(game_shared_memory) == 0:
            sortie()

        print(colored("Waiting for instruction", "green"))

        data = conn.recv(TCP_BUFFER)

        if not data:
            break

        if data.decode() == "*":
            sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
            player.pickCard()
            player.getGameState()
            sendToClient()
            restore_stdout()

        elif data.decode() == "+":
            sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
            player.getGameState()
            sendToClient()
            restore_stdout()

        elif data.decode() == "/":

            sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
            c = threading.Thread(target=timer)  # Appel de la fonction timer() au dessus
            c.start()
            played = False

            print(" Vous avez 10 secondes pour jouer. \n")
            player.getGameState()
            print(" \n Quelle position dans la liste de cartes souhaitez vous piocher ? ( Commencer à zéro )")
            sendToClient()

            while not played:  # timer à 10 seconds

                with player.lock:

                    try:
                        num_picked = int(conn.recv(TCP_BUFFER).decode())

                        if player.validCard(player.hand[num_picked]) and c.is_alive():
                            card_picked = player.hand[num_picked]
                            player.game.insert(0, card_picked)
                            player.hand.remove(card_picked)
                            print(" Carte valide et ajoutée")
                            played = True
                        elif not player.validCard(player.hand[num_picked]) and c.is_alive():
                            print(" Carte invalide. Vous avez du piocher")
                            player.pickCard()
                            played = True
                        else:
                            break
                        if c.is_alive():
                            break
                    except:
                        if c.is_alive():
                            print(colored("Saisie incorecte", "red"))
                        else:
                            break
                sendToClient()

            if played:
                player.getGameState()

            if not played:
                print("Time's out ! Vous auriez du être plus rapide. Vous avez du piocher.\n")
                player.getGameState()
                player.pickCard()

            print(player.printHand())
            sendToClient()
            restore_stdout()
            player.sendMessageToBoard("ended_playing")

        else:
            sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
            print(colored("Bad command", "red", attrs=["bold"]))
            sendToClient()
            restore_stdout()


# Board

def board(mq, mqType, deck_shared_memory, game_shared_memory, lock, listOfPlayer):
    print(colored("Board Start", "red"))
    board = Board(game_shared_memory, deck_shared_memory, mq, mqType, lock)

    board.getMessageFromPlayer(listOfPlayer)
    time.sleep(1)

    while True:  # fait un kill sur process si un gagne
        board.getMessageFromPlayer(listOfPlayer)
        if board.playerLost() or len(deck_shared_memory) == 0:
            board.sendMessageToPlayers("everyone_looses", listOfPlayer)
            print(" C'est terminé ! ")
            sys.exit(0)


if __name__ == "__main__":

    key = 667

    lock = threading.Lock()
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    BUFFER_SIZE = 100
    deck_shared_memory = Manager().list()
    game_shared_memory = Manager().list()

    lock = Lock()

    mqTypeBoard = 1
    os.system("clear")
    player_nb = int(input("combien de joueurs ?"))

    process_pere = Process(target=board, args=(
        mq, mqTypeBoard, game_shared_memory, deck_shared_memory, lock, [i + 2 for i in range(player_nb)]))
    process_pere.start()

    mq.send("creation_jeu".encode(), type=1)
    time.sleep(1)
    print("SHARED MEMORY: ---------------------- \nCreated")
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
