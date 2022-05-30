import socket
import json
import time

from simulator import Simulator


class Sender:

    addr = (socket.gethostname(), 12345)

    def __init__(self, simulator: Simulator) -> None:
        self.establish_connection()
        simulator.add_observer(self)

    def establish_connection(self):
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        while self.sock.connect_ex(self.addr) != 0:
            time.sleep(5)

    def send(self, data):
        try:
            self.sock.sendall(bytes(json.dumps(data), encoding='utf-8'))
        except socket.error:
            self.sock.close()
            self.establish_connection()
