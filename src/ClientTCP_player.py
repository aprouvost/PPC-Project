import socket
from termcolor import colored

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
