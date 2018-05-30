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
        try:
                while True:
                    data = connection.recv(1024)
                    print(data.decode())
        except:
                print("Connection error occured, closing...")
                sys.exit()

def listener(socket):
        return socket.listen()

if len(sys.argv) == 1:
    print("Invalid usage : Refer --help for usage information")
    quit()

if args.listen:
    print("Creating listner on " + args.listen + ":" + str(args.port))
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSocket.bind((args.listen, args.port))
        print("Success!\n\nListening...")
    except:
        print("Error binding to address, exiting...")
        quit()
        
    Thread(target = listener, args = (serverSocket,)).start()
    conn, address = serverSocket.accept()

    print("Connected with " + address[0] + " from port " + str(address[1]) + "\n")
    conn.send(str.encode("WELCOME!!!!\n"))

    Thread(target = reciever, args = (conn,)).start()

    try:
        while True:
                send = input()
                if not send:
                        conn.send("\n".encode())
                conn.send(send.encode())
    except:
        print("Connection error occured, closing...")

if args.serverAdd:
    print("Connecting to " + args.serverAdd + ":" + str(args.port) + "\n")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((args.serverAdd, args.port))
    except:
        print("Error connecting to server, exiting...")
        quit()

    Thread(target = reciever, args = (clientSocket,)).start()

    while True:
        try:
                send = input()
                if not send:
                        conn.send("\n".encode())
                clientSocket.sendall(send.encode())
        except:
                print("Connection error occured, closing...")
                sys.exit()
