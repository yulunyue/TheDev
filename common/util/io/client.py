from .server import Server
from .base import Io
from common.util.export import get_log

logger = get_log("io_client")


class Client(Io):
    server: "Server"

    def run(self):
        while True:
            data = self.sock.recv(1024)
            if not data:
                self.close()
                break
            self.server

    def close(self):
        logger.debug(f"{self} close")
