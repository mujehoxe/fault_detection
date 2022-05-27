import socket


class receiver:

    host = "127.0.0.1"
    port = 65432

    def __init__(self) -> None:
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def listen(self, callback):
        while(True):
            conn, addr = self.sock.accept()
            print('Connected by', addr)
            self.receive(conn, callback)
            conn.close()

    def receive(self, conn, callback):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            callback(data)
