import socket
from threading import Thread
import uuid

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8081

clients = []


def processMessage(conn, addr, data):
    print(str(addr) + ':' + data.decode('utf-8'))


def ServeClient(conn, addr):
    global clients
    len(clients)
    clients.append((conn, addr))

    with conn:
        print('Connected by', addr)
        while True:
            try:
                data = conn.recv(1024)
                processMessage(conn, addr, data)
                if len(data) == 0:
                    print('{} connnection closed.'.format(addr))
                    break
            except Exception as e:
                print(e)
                break
        clients.remove((conn, addr))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server listening at {} Port {}'.format(HOST, PORT))
    while True:
        conn, addr = s.accept()
        thread = Thread(target=ServeClient, args=(conn, addr))
        thread.start()
    print('Server closed for new connections.')
