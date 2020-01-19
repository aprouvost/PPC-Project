import os
import socket

from orca.braille import clear
from termcolor import colored

os.system("clear")
print("-------------------------------------------------------------------------------- \n BIENVENUE ! \n \n VOICI "
      "LES REGLES : Tu peux poser le même numero que celui en jeu, ou bien la même couleur de celui-ci si la valeur "
      "de la carte est de plus ou moins 1 que celle en jeu ! Pense bien avant de jouer, si tu te trompes tu devras "
      "piocher ... \n Mais fais attention, si la pioche est vide tout le monde a perdu ! \n \n "
      "BON COURAGE !  \n \n")

nbPlayer = int(input("Quel est votre numero de Player ?"))

TCP_IP = "127.0.0.1"
TCP_PORT = 667 + nbPlayer
TCP_BUFFER = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:

    dataRCV = s.recv(TCP_BUFFER)
    if dataRCV:
        print(dataRCV.decode())

    data = input(colored("Que voulez vous faire ?    "
                         "'*' -> piocher | '+' -> Game status | '/' -> play a card", "cyan", attrs=["bold"]))

    while not data:
        data = input(colored("Saisie incorrecte, réessayer", "cyan", attrs=["bold"]))

    s.send(data.encode())
    os.system("clear")
