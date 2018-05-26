import socket
import argparse
import sys
from threading import *

parser = argparse.ArgumentParser()
parser.add_argument("serverAdd", nargs = '?', type = str, \
                    help = "Server address")
parser.add_argument("--listen", "-l", type = str, help = "IP to listen on")
parser.add_argument("--port", "-p", type = int, \
                    help = "Listen port.(Default = 6000)", default = '6000')
args = parser.parse_args()

def reciever(connection):
        while True:
            data = connection.recv(1024)
            print(data.decode())

if len(sys.argv) == 1:
    print("Invalid usage : Refer --help for usage information")
    quit()

if args.listen:
    print("Listening on " + args.listen + ":" + str(args.port))
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((args.listen, args.port))
    serverSocket.listen()
    conn, address = serverSocket.accept()

    print("Connected with " + address[0] + " on port " + str(address[1]))
    conn.send(str.encode("WELCOME!!!!\n"))

    Thread(target = reciever, args = (conn,)).start()

    while True:
        send = input()
        conn.send(send.encode())

if args.serverAdd:
    print("Connecting to " + args.serverAdd + ":" + str(args.port))
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((args.serverAdd, args.port))

    Thread(target = reciever, args = (clientSocket,)).start()

    while True:
        send = input()
        clientSocket.sendall(send.encode())
