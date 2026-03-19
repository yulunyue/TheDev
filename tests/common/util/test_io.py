from common.util.export import logger, TcpServer, TcpClient
import requests
import time


class TestIo:

    def test_base(self):
        PORT = 50001
        IP_LOCAL = "127.0.0.1"
        t = TcpServer().set_addr(src_ip="0.0.0.0", src_port=PORT)
        t.start()
        u = TcpClient().set_addr(dst_ip=IP_LOCAL, dst_port=PORT)
        time.sleep(1)
        u.connect()
        send_data = b"hello world"
        u.write(send_data)
        time.sleep(0.1)
        assert send_data, t.msgs[-1].msg
