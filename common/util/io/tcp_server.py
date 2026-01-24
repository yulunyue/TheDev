from .server import Server, socket
from .tcp_client import TcpClient


class TcpServer(Server):
    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(True)

    def loop(self):
        self.sock.listen(2048)
        while True:
            client_sock, addr = self.sock.accept()
            t = (
                TcpClient()
                .set_addr(
                    src_ip=addr[0],
                    src_port=addr[1],
                    dst_ip=self.src_ip,
                    dst_port=self.src_port,
                )
                .set_sock(client_sock)
            )
            self.new_connection(addr, t)
            t.start()
