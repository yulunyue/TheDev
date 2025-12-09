from common.util.export import UdpServer, UdpClient, ToolBase


class Io(ToolBase):
    def udp_server(self, src_ip, src_port, proxy):
        u = UdpServer(src_ip=src_ip, src_port=src_port)
        u.run()
