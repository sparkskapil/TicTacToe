import socket
from threading import Thread
import os
import pickle
from NetworkMessage import MessageChannel

HOST = '192.168.1.208'  # The server's hostname or IP address
PORT = 55050        # The port used by the server
CLOSED = False


# Mimic C++ cin


def getInput():
    string = ''
    while string == '':
        string = input()
    return string


def handleServer(s):
    global CLOSED
    msg = None
    channel = MessageChannel(s)
    while not msg == 'exit' or CLOSED:
        msg = channel.receiveMessage()
        if len(msg) == 0:
            break
        print()
        print(msg)
    CLOSED = True


def handleClient(s):
    channel = MessageChannel(s)
    global CLOSED
    data = None
    while not data == 'exit' or CLOSED:
        data = getInput()
        channel.sendMessage(data)
    CLOSED = True


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected to the Server.\n')
    thread = Thread(target=handleServer, args=(s,))
    thread.start()
    handleClient(s)
    s.close()
