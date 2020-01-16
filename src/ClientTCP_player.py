import socket
import sys
from termcolor import colored

nbPlayer = int(input("Quel est votre numero de Player ?"))

TCP_IP = "127.0.0.1"
TCP_PORT = 666 + nbPlayer
TCP_BUFFER = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while True:

    dataRCV = s.recv(TCP_BUFFER)
    print(dataRCV.decode())

    data = input("Que voulez vous faire ?")
    s.send(data.encode())