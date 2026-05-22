import struct
import json
from typing import Dict, TYPE_CHECKING
from .client import Client
from .base import socket

if TYPE_CHECKING:
    from ..node import Node
    from ...constant import C


class AgentTcpClient(Client):
    def __init__(self):
        super().__init__()
        self.message_handler = None
        self.outputs: Dict[str, dict] = dict()
        self.agent_id = ""
        self.platform = None
        self.hostname = None
        self.ip = None
        self.port = None
        self.last_heartbeat = None

    def send(self, data):
        if isinstance(data, str):
            data = data.encode("utf-8")
        length = struct.pack("!I", len(data))
        self.sock.sendall(length + data)

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        from ..node import Node
        
        try:
            while True:
                data = self._recv_exact(4)
                if not data:
                    self.close()
                    break
                length = struct.unpack("!I", data)[0]
                body = self._recv_exact(length)
                if not body:
                    self.close()
                    break
                msg = Node.from_dict(json.loads(body.decode("utf-8")))
                if self.message_handler:
                    self.message_handler(msg)
                else:
                    self.server.receive_msg(self, msg)
        except Exception:
            self.close()

    def close(self):
        if self.agent_id:
            if hasattr(self, "server") and hasattr(self.server, "manage"):
                self.server.manage.unregister_agent(self.agent_id)
        super().close()

    def _recv_exact(self, n):
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                return None
            data += chunk
        return data

    def write_node(self, node: "Node"):
        self.write(node.to_json_str())

    def store_output(self, msg: "Node", manage):
        from ...constant import C
        
        cmd_id = msg.key
        if cmd_id not in self.outputs:
            self.outputs[cmd_id] = {
                "agent_id": self.agent_id,
                "lines": [],
                "exit_code": None,
                "done": False,
            }
        output = self.outputs[cmd_id]
        msg_type = msg.type
        if msg_type == C.MSG_EXEC_STDOUT:
            output["lines"].append(("stdout", msg.data.get("data")))
        elif msg_type == C.MSG_EXEC_STDERR:
            output["lines"].append(("stderr", msg.data.get("data")))
        elif msg_type == C.MSG_EXEC_DONE:
            output["exit_code"] = msg.data.get("exit_code")
            output["done"] = True
        manage.send(
            f"{C.TOPIC_AGENT_OUTPUT}.{cmd_id}",
            msg,
        )

    def get_output(self, cmd_id):
        return self.outputs.get(cmd_id)