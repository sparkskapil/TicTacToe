
HEADERLENGTH = 20


class MessageChannel:
    def __init__(self, conn):
        self.Connection = conn

    def sendMessage(self, message):
        length = len(message)
        header = str(length).ljust(HEADERLENGTH)

        messageToSend = (header + message).encode('utf-8')
        self.Connection.sendall(messageToSend)

    def receiveMessage(self):
        msgSize = int(self.Connection.recv(HEADERLENGTH).decode('utf-8'))
        message = self.Connection.recv(msgSize).decode('utf-8')
        return message
