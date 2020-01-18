#!/usr/bin/env python

from auto_install_package import autoInstall

autoInstall()

from termcolor import colored
from board import Board
from Player import Player
import threading
from multiprocessing import Process, Manager, Lock
import sysv_ipc
import time
import sys
import socket
from io import TextIOWrapper, BytesIO


# joueurs

def joueur(mq, mqType, game_shared_memory, deck_shared_memory, lock):
    print(colored("Player Start", "red"))
    player = Player(game_shared_memory, deck_shared_memory, mq, mqType, lock)
    player.getMesgFromBoard()

    TCP_IP = "127.0.0.1"
    TCP_PORT = 667 + mqType
    TCP_BUFFER = 20
    old_stdout = sys.stdout
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print(colored("Waiting TCP conn : {}".format(mqType), "green"))
    conn, addr = s.accept()
    print(colored("Connection address: {}".format(addr), "green"))

    def sendToClient():
        sys.stdout.seek(0)
        reponse = sys.stdout.read()
        print(" DEBUG sending response to client : ", reponse)
        conn.send(str(reponse).encode())

    def restore_stdout():
        sys.stdout.close()
        sys.stdout = old_stdout

    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
    player.getGameState()
    sendToClient()
    restore_stdout()

    while True:

        print(colored("Checking for mq", "green"))
        player.getMesgFromBoard()

        if player.handEmpty():
            player.sendMessageToBoard("someone_won")

        print(colored("Waiting for instruction", "green"))
        data = conn.recv(TCP_BUFFER)
        print(colored(data, "yellow"))

        if not data:
            break

        if data.decode() == "*":
            print(colored("{} Pioche".format(mqType), "yellow"))
            sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
            print("sending to client : ", sys.stdout)
            player.pickCard()
            player.getGameState()
            sendToClient()
            restore_stdout()

        if data.decode() == "+":
            print(colored("{} check game status".format(mqType), "yellow"))
            sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
            player.getGameState()
            sendToClient()
            restore_stdout()

        if data.decode() == "/":
            print(colored("{} Joue".format(mqType), "yellow"))
            # player.sendMessageToBoard("playing")  # Il faut regarder pk le msg est recu/envoyer beaucoup trop de fois
            sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
            played = False
            seconds = time.time()  # lance timer
            # signal envoyé au père pour dire commence
            actual_time = time.time()

            print(" Vous avez 10 secondes pour jouer. Votre jeu est le suivant : \n"
                  " Quelle position dans la liste de cartes souhaitez vous piocher ?")
            sendToClient()
            while not played:  # timer à 10 seconds

                with player.lock:

                    actual_time = time.time()
                    print(actual_time)
                    # Recupère infos sur jeu
                    # Lock sur Deck et Game

                    num_picked = int(conn.recv(TCP_BUFFER).decode())
                    while num_picked > len(player.hand):
                        print("Saisie incorecte")
                        num_picked = int(conn.recv(TCP_BUFFER).decode())
                    if player.validCard(player.hand[num_picked]):
                        card_picked = player.hand[num_picked]
                        player.game.insert(0, card_picked)
                        player.hand.remove(card_picked)
                        print(" Carte valide et ajoutée")
                        played = True
                    else:
                        print(" Carte invalide. Vous avez du piocher")
                        player.pickCard()
                        played = True

            if played:
                print(" Votre jeu est maintenant le suivant ")

            if not played:
                print(
                    "Time's out ! Vous auriez du être plus rapide. Vous avez du piocher. Votre jeu est maintenant le "
                    "suivant : ")
                player.pickCard()

            print(player.printHand())
            sendToClient()
            restore_stdout()
            player.sendMessageToBoard("ended_playing")


# Board

def board(mq, mqType, deck_shared_memory, game_shared_memory, lock, listOfPlayer):
    print(colored("Board Start", "red"))
    board = Board(game_shared_memory, deck_shared_memory, mq, mqType, lock)

    board.getMessageFromPlayer(listOfPlayer)
    time.sleep(1)

    while True:  # fait un kill sur process si un gagne
        board.getMessageFromPlayer(listOfPlayer)
        if board.playerLost():
            board.sendMessageToPlayers("everyone_looses", listOfPlayer)


if __name__ == "__main__":

    key = 667

    lock = threading.Lock()
    mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    BUFFER_SIZE = 100
    deck_shared_memory = Manager().list()
    game_shared_memory = Manager().list()

    lock = Lock()

    mqTypeBoard = 1
    player_nb = int(input("combien de joueurs ?"))

    process_pere = Process(target=board, args=(
    mq, mqTypeBoard, game_shared_memory, deck_shared_memory, lock, [i + 2 for i in range(player_nb)]))
    process_pere.start()

    mq.send("creation_jeu".encode(), type=1)
    print(deck_shared_memory)
    time.sleep(1)

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
