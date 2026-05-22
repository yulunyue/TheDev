from .tcp_server import TcpServer
from .agent_client import AgentTcpClient


class AgentTcpServer(TcpServer):
    CLIENT_CLASS = AgentTcpClient

    def __init__(self, manage):
        super().__init__()
        self.manage = manage

    def receive_msg(self, client, msg):
        if msg.get("type") == "register":
            client.agent_id = msg["agent_id"]
        self.manage.handler_agent_msg(client, msg)
