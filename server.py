import signal
import sys
import socket
from threading import Thread
import uuid
from NetworkMessage import MessageChannel

HOST = socket.gethostbyname(socket.gethostname())
PORT = 55050

clients = []


def processMessage(conn, addr, data):
    for c, _, channel in clients:
        if not c == conn:
            channel.sendMessage(data)


def ServeClient(conn, addr):
    global clients
    channel = MessageChannel(conn, addr)
    info = (conn, addr, channel)
    clients.append(info)

    with conn:
        print('Connected by', addr)
        while True:
            try:
                data = channel.receiveMessage()
                processMessage(conn, addr, data)
                if len(data) == 0:
                    print('{} connnection closed.'.format(addr))
                    break
            except Exception as e:
                print(e)
                break
            except KeyboardInterrupt:
                break

        clients.remove(info)


def signal_handler(signal, frame):
    print(signal)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print('Server listening at {} Port {}'.format(HOST, PORT))
    while True:
        try:
            conn, addr = s.accept()
            thread = Thread(target=ServeClient, args=(conn, addr))
            thread.start()
        except KeyboardInterrupt:
            break
    print('Server closed for new connections.')
