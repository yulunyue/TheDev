from common.util.export import TestBase, logger, TcpServer, TcpClient
import requests
import time

PORT = 50001
IP_LOCAL = "127.0.0.1"


class TestIo(TestBase):
    def setup_class(self):
        self.t = TcpServer().set_addr(src_ip="0.0.0.0", src_port=PORT)
        self.t.start()

    def test_base(self):
        u = TcpClient().set_addr(dst_ip=IP_LOCAL, dst_port=PORT)
        u.connect()
        send_data = b"hello world"
        u.write(send_data)
        time.sleep(0.1)
        self.expect(send_data, self.t.msgs[-1].msg)
