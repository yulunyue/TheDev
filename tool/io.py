from common.util.export import TcpServer, TcpClient, ToolBase
from common.third_util.py_test_util import PyTestUtil
from common.third_util.obs_util import ObsUtil


class Io(ToolBase):
    def tcp_server(self, src_ip, src_port, proto=None):
        u = TcpServer().set_addr(src_ip=src_ip, src_port=src_port)
        u.start()
        input("exit")

    def tcp_client(self, dst_ip, dst_port, proto=None):
        u = TcpClient().set_addr(dst_ip=dst_ip, dst_port=dst_port)
        u.connect()
        u.write(dict(a=1))

    def test(self):
        PyTestUtil().set_aim("tests/test_io.py").set_root(".").main()

    def obs_list_buckets(self, env):
        ObsUtil(env).list_buckets()

    def obs_upload(self, env, path):
        ObsUtil(env).upload(path)


if __name__ == "__main__":
    Io().run()
