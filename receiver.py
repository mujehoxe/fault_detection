import socket
import json


class Receiver:

    addr = (socket.gethostname(), 12345)

    def __init__(self) -> None:
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.addr)
        self.sock.listen()

    def receive(self, conn: socket.socket, callback):

        def str_to_json(msg):
            try:
                return json.loads(msg)
            except Exception as e:
                print(msg, e)

        while True:
            msg = conn.recv(2048)
            if not msg:
                break
            callback(str_to_json(msg.decode('utf-8')))


class ProxyReceiver:

    def __init__(self) -> None:
        self.receiver: Receiver = Receiver()

    def listen(self, callback):
        print(f"listening for data on: {self.receiver.addr}")

        conn, addr = self.receiver.sock.accept()
        print('Connected by', addr)
        try:
            while(True):
                self.receive(conn, callback)
        except KeyboardInterrupt:
            conn.close()

    def receive(self, conn, callback):
        self.receiver.receive(conn, callback)
