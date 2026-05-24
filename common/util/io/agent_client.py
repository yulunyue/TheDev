from typing import List, TYPE_CHECKING
from .client import LengthPrefixedClient

if TYPE_CHECKING:
    from ..node import Node
    from ...constant import C


class AgentTcpClient(LengthPrefixedClient):
    def __init__(self):
        super().__init__()
        self.current_output = dict()
        self.history: List[dict] = []

    def exec_command(self, command, timeout=30):
        from ..node import Node
        from ...constant import C

        self.current_output.update(command=command)
        self.write_node(
            Node(
                type=C.MSG_EXEC,
                data={"command": command, "timeout": timeout},
            )
        )

    def kill_exec(self):
        from ..node import Node
        from ...constant import C
        self.write_node(Node(type=C.MSG_EXEC_KILL))

    def _archive_output(self):
        lines = self.current_output.get("lines", [])
        self.current_output["output"] = "".join(line[1] for line in lines)
        self.history.append(self.current_output)
        self.current_output = dict()
        if len(self.history) > 60:
            self.history = self.history[-60:]

    def get_history(self, limit=60):
        return self.history[-limit:]

    def hander_msg(self, msg: "Node"):
        from ...constant import C
        from .manage import IO_MANAGE

        msg_type = msg.type
        if msg_type == C.MSG_EXEC_STDOUT:
            self.current_output.setdefault("lines", []).append(
                ("stdout", msg.data.get("data"))
            )
        elif msg_type == C.MSG_EXEC_STDERR:
            self.current_output.setdefault("lines", []).append(
                ("stderr", msg.data.get("data"))
            )
        elif msg_type == C.MSG_EXEC_DONE:
            self.current_output["exit_code"] = msg.data.get("exit_code")
            self.current_output["done"] = True
            self._archive_output()
        IO_MANAGE.send(f"{C.TOPIC_AGENT_OUTPUT}.{self.username}", msg.to_dict())
