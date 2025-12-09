from common.util.export import get_log
from .base import Io, socket
from .client import Client


class Server(Io):
    def new_connection(self, addr, t: "Client"):
        self.childs[addr] = t
        t.server = self
        t.set_logger(self.logger)
        self.logger.debug(f"new connecttion {t}")

    def receive_msg(self, client: "Io", msg):
        self.logger.debug(f"{self} receive from {client} msg_len={len(msg)}")

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
