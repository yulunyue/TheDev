from threading import Thread
import socket


class Io:
    def __init__(self, src_ip, src_port, dst_ip=None, dst_port=None):
        self.src_ip: str = src_ip
        self.src_port = src_port
        self.dst_ip = dst_ip
        self.dst_port = dst_port


class Server(Io):
    pass


class Client(Io):
    pass


class TcpServer(Server):
    pass


class UdpServer(Server):
    pass


class UdpClient(Client):
    pass
