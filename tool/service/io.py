from common.util.export import TcpServer, TcpClient, logger
from common.tool.export import FileConfig, ToolBase
from common.third_util.dataa.excel_util import PandasUtil


class Io(ToolBase):
    def tcp_server(self, src_ip, src_port, proto=None):
        u = TcpServer().set_addr(src_ip=src_ip, src_port=src_port)
        u.start()
        input("exit")

    def tcp_client(self, dst_ip, dst_port, proto=None):
        u = TcpClient().set_addr(dst_ip=dst_ip, dst_port=dst_port)
        u.connect()
        u.write(dict(a=1))

    def obs_list_buckets(self, env):
        from common.third_util.io.obs_util import ObsUtil

        logger.info(ObsUtil(env).list_buckets())

    def obs_upload(self, env, path):
        from common.third_util.io.obs_util import ObsUtil

        ObsUtil(env).upload(path)

    def tcli(self, path):
        p = PandasUtil().load(path)
        self.cli(p.hander)

    def api(self, uri):
        pass


if __name__ == "__main__":
    Io().run()
