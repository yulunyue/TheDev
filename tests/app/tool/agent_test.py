from common.util.export import IO_MANAGE
from common.util.io.agent_client import AgentTcpClient
from app.tool.agent import Agent


class TestAgentApi:
    @classmethod
    def setup_class(self):
        self.api = Agent()

    def test_list(self):
        fake = AgentTcpClient()
        fake.username = "test-node"
        fake.platform = "linux"
        fake.hostname = "w1"
        IO_MANAGE.io_map["test-node"] = fake
        result = self.api.list()
        childs = result.get_childs()
        assert len(childs) > 0
        assert any(c.get("value") == "test-node" for c in childs)
        IO_MANAGE.io_map.pop("test-node", None)

    def test_exec_no_agent(self):
        result = self.api.exec(agent_id="nonexistent", command="echo hi")
        assert not result.ok

    def test_kill(self):
        fake = AgentTcpClient()
        fake.username = "test-kill"
        fake.sock = True
        fake.send = lambda data: None
        IO_MANAGE.io_map["test-kill"] = fake

        result = self.api.kill(agent_id="test-kill")
        assert result.ok

        IO_MANAGE.io_map.pop("test-kill", None)

    def test_kill_no_agent(self):
        result = self.api.kill(agent_id="nonexistent")
        assert not result.ok
