from typing import List, TYPE_CHECKING
from .base import Io, socket

if TYPE_CHECKING:
    from .client import Client


class SocketMsg:
    def __init__(self, sender, recv, msg):
        self.sender = sender
        self.recv = recv
        self.msg = msg


class Server(Io):
    def __init__(self):
        super().__init__()
        self.msgs: List[SocketMsg] = []

    def new_connection(self, addr, t: "Client"):
        self.childs[addr] = t
        t.server = self
        t.set_logger(self.logger)
        self.logger.debug(f"new connecttion {t}")

    def receive_msg(self, client: "Io", msg):
        self.msgs.append(SocketMsg(client, self, msg))

    def run(self):
        self.create_socket()
        self.init_socket()
        self.init_data()
        self.loop()

    def init_socket(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.src_ip, int(self.src_port)))
        self.logger.debug(f"create socket {self}")

    def init_data(self):
        self.childs = dict()