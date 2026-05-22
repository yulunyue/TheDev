from common.util.export import Node, ApiBase, IO_MANAGE


class Agent(ApiBase):
    ROUTE_PATH = "/agent"

    def list(self, **kw):
        return Node(data=dict(agents=IO_MANAGE.list_agents()))

    def exec(self, agent_id, command, timeout=30, **kw):
        cmd_id = IO_MANAGE.send_exec(agent_id, command, timeout)
        return Node(data=dict(cmd_id=cmd_id))
