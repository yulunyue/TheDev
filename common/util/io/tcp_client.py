from .client import Client
from .base import socket


class TcpClient(Client):
    def send(self, data):
        self.sock.sendall(data)

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
