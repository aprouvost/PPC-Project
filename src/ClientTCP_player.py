import os
import socket
import threading
import pynput

from termcolor import colored

os.system("clear")
print("-------------------------------------------------------------------------------- \n "
      "BIENVENUE ! \n \n "
      "VOICI LES REGLES : Tu peux poser le même numero que celui en jeu, ou bien la même couleur de celui-ci si la "
      "valeur "
      "de la carte est de plus ou moins 1 que celle en jeu ! Pense bien avant de jouer, si tu te trompes tu devras "
      "piocher ... \n "
      "Mais fais attention, si la pioche est vide tout le monde a perdu ! \n \n "
      "BON COURAGE !  \n \n")

nbPlayer = int(input("Quel est votre numero de Player ?"))

TCP_IP = "127.0.0.1"
TCP_PORT = 667 + nbPlayer
TCP_BUFFER = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

os.system("clear")


def KeyBoardListener(s):
    print("I am Strat")
    print(s)
    def on_press(key):
        try:
            s.send(str(key.char).encode())
        except:
            pass

    def on_release(key):
        if key == pynput.keyboard.Key.esc:
            # Stop listener
            return False

    with pynput.keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


KeyListener = threading.Thread(target=KeyBoardListener, args=(s,))
KeyListener.start()


while True:
    # print('boucle')

    # l'idee est de tout le temps regarder si on recoit quelque chose par la connexion TCP pour pouvoir l'afficher
    # directement
    # Si le joueur veut jouer il faut interompre cette ecoute pour le faire jouer (Sigaux ?? / Evenement ??) mais il
    # faut bloquer le joueur s'il y en a un autre qui joue
    #
    # print(colored(listener.is_alive(), "yellow"))
    # if not listener.is_alive():
    #     listener.join()

    print("waiting TCP")
    dataRCV = s.recv(TCP_BUFFER)
    if not dataRCV:
        break
    else:
        os.system("clear")
        print(dataRCV.decode())
        print(colored("Que voulez vous faire ?    "
                      "'*' -> piocher | '+' -> Game status | '/' -> play a card", "cyan", attrs=["bold"]))

    # data = input(colored("Que voulez vous faire ?    "
    #                      "'*' -> piocher | '+' -> Game status | '/' -> play a card", "cyan", attrs=["bold"]))
    #
    # while not data:
    #     data = input(colored("Saisie incorrecte, réessayer", "cyan", attrs=["bold"]))
    #
    # s.send(data.encode())
