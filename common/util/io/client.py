from .base import Io
from common.util.export import get_log


class Client(Io):
    server: "Io"

    def run(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                self.close()
                break
            self.server.receive_msg(self, data)

    def close(self):
        self.logger.debug(f"{self} close")
