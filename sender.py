import socket
from typing import List


class Sender:

    host = socket.gethostname()
    port = 12345

    def __init__(self) -> None:
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def send(self, msg):
        self.sock.connect((self.host, self.port))
        self.sock.sendall(msg.encode())
