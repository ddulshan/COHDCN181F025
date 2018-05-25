import socket
import argparse
from threading import *

parser = argparse.ArgumentParser()
parser.add_argument("--listen", "-l", type = str, help = "IP to listen on")
parser.add_argument("--port", "-p", type = int, help = "Listen port.(Default = 6000)", \
                    default = '6000')
args = parser.parse_args()

print(args.listen + ":" + str(args.port))
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((args.listen, args.port))
serverSocket.listen()
conn, address = serverSocket.accept()

print("Connected with " + address[0] + " on port " + str(address[1]))
conn.send(str.encode("WELCOME NIGGA!!!!\n"))

def recieve():
    while True:
        data = conn.recv(1024)
        print(data.decode())

Thread(target = recieve).start()

while True:
    send = input()
    conn.send(send.encode())
