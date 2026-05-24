from .tcp_server import TcpServer
from .agent_client import AgentTcpClient
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..node import Node
    from ...constant import C
    from .manage import Manage


class AgentTcpServer(TcpServer):
    CLIENT_CLASS = AgentTcpClient

    def __init__(self, manage):
        super().__init__()
        self.manage: Manage = manage

    def receive_msg(self, client: AgentTcpClient, msg: "Node"):
        self.manage.handler_msg(client, msg)
