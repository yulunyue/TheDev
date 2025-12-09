from common.util.export import get_log
from .base import Io, socket
from .client import Client

logger = get_log("io_server")


class Server(Io):
    def new_connection(self, addr, t: "Client"):
        self.childs[addr] = t
        t.server = self
        logger.debug(f"new connecttion {t}")

    def run(self):
        self.create_socket()
        self.init_socket()
        self.init_data()
        self.loop()

    def init_socket(self):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.src_ip, self.src_port))
        self.sock.setblocking(False)
        logger.debug(f"create socket {self}")

    def init_data(self):
        self.childs = dict()

    def receive_msg(self, client: Client, msg):
        logger.debug(f"{self} receive from {client}")
