from common.util.export import IO_MANAGE
from app.tool.agent import Agent


class TestAgentApi:
    @classmethod
    def setup_class(self):
        self.api = Agent()

    def test_list(self):
        IO_MANAGE.register_agent("test-node", dict(platform="linux", hostname="w1"))
        result = self.api.list()
        data = result.get_data()
        assert "agents" in data
        assert any(a["agent_id"] == "test-node" for a in data["agents"])
        IO_MANAGE.unregister_agent("test-node")

    def test_exec_no_agent(self):
        try:
            self.api.exec(agent_id="nonexistent", command="echo hi")
            assert False, "should raise"
        except ValueError:
            pass
