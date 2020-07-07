import socket
from threading import Thread
import os

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000        # The port used by the server
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
    while not msg == 'exit' or CLOSED:
        msg = s.recv(1024)
        if len(msg) == 0:
            break
        msg = msg.decode('utf-8')
        print()
        print(msg)
    CLOSED = True

def handleClient(s):
    global CLOSED
    data = None
    while not data == 'exit' or CLOSED:
        data = getInput()
        s.sendall(data.encode('utf-8'))
    CLOSED = True


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected to the Server.\n')
    thread = Thread(target=handleServer, args=(s,))
    thread.start()
    handleClient(s)
    s.close()
