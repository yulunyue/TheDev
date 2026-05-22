import struct
import json
from .client import Client
from .base import socket


class AgentTcpClient(Client):
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
                msg = json.loads(body.decode("utf-8"))
                if self.message_handler:
                    self.message_handler(msg)
                else:
                    self.server.receive_msg(self, msg)
        except Exception:
            self.close()

    def close(self):
        if hasattr(self, "agent_id"):
            if hasattr(self, "server") and hasattr(self.server, "manage"):
                self.server.manage.unregister_agent(self.agent_id)
        super().close()

    def _recv_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                return None
            data += chunk
        return data
