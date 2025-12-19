from common.util.export import TcpServer, TcpClient, ToolBase


class Io(ToolBase):
    def tcp_server(self, src_ip, src_port, proto=None):
        u = TcpServer().set_addr(src_ip=src_ip, src_port=src_port)
        u.start()
        input("exit")

    def tcp_client(self, dst_ip, dst_port, proto=None):
        u = TcpClient().set_addr(dst_ip=dst_ip, dst_port=dst_port)
        u.connect()
        u.write(dict(a=1))

    def dev(self):
        pass


if __name__ == "__main__":
    Io().run()
