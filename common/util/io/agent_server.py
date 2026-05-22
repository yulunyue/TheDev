from .tcp_server import TcpServer
from .agent_client import AgentTcpClient


class AgentTcpServer(TcpServer):
    CLIENT_CLASS = AgentTcpClient

    def __init__(self, manage):
        super().__init__()
        self.manage = manage

    def receive_msg(self, client, msg):
        t = msg.get("type")
        if t == "register":
            client.agent_id = msg["agent_id"]
            self.manage.register_agent(
                msg["agent_id"],
                dict(
                    platform=msg.get("platform"),
                    hostname=msg.get("hostname"),
                    ip=client.src_ip,
                    port=client.src_port,
                ),
            )
            client.write(dict(type="register_ok"))
        elif t == "heartbeat":
            self.manage.heartbeat_agent(msg["agent_id"])
        elif t == "unregister":
            self.manage.unregister_agent(msg["agent_id"])
