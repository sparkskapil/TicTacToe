import socket
from threading import Thread
import uuid

HOST = 'localhost'
PORT = 5000

clients = []


def ServeClient(conn, addr):
    global clients
    Index = len(clients)
    clients.append((conn, addr))

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            for index, client in enumerate(clients):
                if index == Index:
                    continue
                client[0].sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)
    while True:
        conn, addr = s.accept()
        thread = Thread(target=ServeClient, args=(conn, addr))
        thread.start()
