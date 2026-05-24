from common.util.export import Node, ApiBase, IO_MANAGE, AgentTcpClient
from common.tool.export import FontSearch


class Agent(ApiBase):
    ROUTE_PATH = "/agent"

    def _get_agent(self, agent_id):
        io = IO_MANAGE.io_map.get(agent_id)
        return io if isinstance(io, AgentTcpClient) else None

    def list(self, **kw):
        agents = [
            k for k, v in IO_MANAGE.io_map.items() if isinstance(v, AgentTcpClient)
        ]
        return FontSearch().add_childs(*agents)

    def exec(self, agent_id, command, timeout=30, **kw):
        client = self._get_agent(agent_id)
        if not client or not client.is_connected():
            return Node(ok=False, title=f"agent not found: {agent_id}")
        output = client.current_output
        if output and not output.get("done"):
            return Node(ok=False, title="agent is busy, stop current command first")
        client.exec_command(command, timeout)
        return Node(ok=True)

    def kill(self, agent_id, **kw):
        client = self._get_agent(agent_id)
        if not client or not client.is_connected():
            return Node(ok=False, title="agent not found")
        client.kill_exec()
        return Node(ok=True)

    def output(self, agent_id, **kw):
        client = self._get_agent(agent_id)
        if not client:
            return Node(data=dict(error="no running command"))
        output = client.current_output or (
            client.history[-1] if client.history else None
        )
        if not output:
            return Node(data=dict(error="no running command"))
        return Node(data=output)

    def history(self, agent_id, limit=60, **kw):
        client = self._get_agent(agent_id)
        if not client:
            return Node(children=[])
        return Node(children=[Node(data=r) for r in client.get_history(limit)])
