from .base import Io
from ..log import get_log


class Client(Io):
    server: "Io"

    def run(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                self.close()
                break
            self.server.receive_msg(self, data)

    def init_socket(self):
        pass

    def connect(self):
        self.create_socket()
        self.init_socket()
        self.sock.connect((self.dst_ip, int(self.dst_port)))

    def close(self):
        self.logger.debug(f"{self} close")