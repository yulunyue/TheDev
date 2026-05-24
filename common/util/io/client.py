import struct
from .base import Io, socket
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


class LengthPrefixedClient(Client):
    def __init__(self):
        super().__init__()
        self.message_handler = None

    def send(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        length = struct.pack("!I", len(data))
        self.sock.sendall(length + data)

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        from ..node import Node

        try:
            while True:
                data = self._recv_exact(4)
                if not data:
                    self.close()
                    break
                length = struct.unpack("!I", data)[0]
                body = self._recv_exact(length)
                if not body:
                    self.close()
                    break
                msg = Node.from_json_str(body.decode("utf-8"))
                if self.message_handler:
                    self.message_handler(msg)
                else:
                    self.server.receive_msg(self, msg)
        except Exception:
            self.close()

    def close(self):
        self.sock = None
        super().close()

    def _recv_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                return None
            data += chunk
        return data

    def is_connected(self):
        return self.sock is not None