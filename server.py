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
        if len(clients) == 1:
            conn.sendall(b'O')
        else:
            conn.sendall(b'X')
        while True:
            try:
                data = conn.recv(1024)
                if len(data) == 0:
                    print('{} connnection closed.'.format(addr))
                    break
                for index, client in enumerate(clients):
                    if index == Index:
                        continue
                    client[0].sendall(data)

            except Exception as e:
                print(e)
                break
        clients.remove((conn, addr))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server listening at {} Port {}'.format(HOST, PORT))
    while len(clients) < 2:
        conn, addr = s.accept()
        thread = Thread(target=ServeClient, args=(conn, addr))
        thread.start()
    print('Server closed for new connections.')
