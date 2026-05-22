from .tcp_server import TcpServer
from .agent_client import AgentTcpClient
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..node import Node
    from ...constant import C


class AgentTcpServer(TcpServer):
    CLIENT_CLASS = AgentTcpClient

    def __init__(self, manage):
        super().__init__()
        self.manage = manage

    def receive_msg(self, client: AgentTcpClient, msg: "Node"):
        from ...constant import C
        
        if msg.type == C.MSG_REGISTER:
            client.agent_id = msg.data.get("agent_id")
        self.manage.handler_agent_msg(client, msg)