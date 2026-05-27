from common.util.export import IO_MANAGE, Node
from common.util.io.agent_client import AgentTcpClient
from app.tool.agent import Agent


class TestAgent:
    @classmethod
    def setup_class(cls):
        cls.api = Agent()

    def test_list(self):
        client = AgentTcpClient()
        client.username = "test-node"
        client.platform = "linux"
        client.hostname = "w1"
        IO_MANAGE.io_map["test-node"] = client
        result = self.api.list()
        childs = result.get_childs()
        assert len(childs) > 0
        assert any(c.get("value") == "test-node" for c in childs)
        IO_MANAGE.io_map.pop("test-node", None)

    def test_exec_no_agent(self):
        result = self.api.exec(agent_id="nonexistent", command="echo hi")
        assert not result.ok

    def test_kill_no_agent(self):
        result = self.api.kill(agent_id="nonexistent")
        assert not result.ok

    def test_chat_no_agent(self):
        result = self.api.chat(agent_id="nonexistent", message="hello")
        assert not result.ok
        assert "agent not found" in result.title

    def test_cancel_no_agent(self):
        result = self.api.cancel(agent_id="nonexistent")
        assert not result.ok
        assert "agent not found" in result.title

    def test_confirm_no_agent(self):
        result = self.api.confirm(agent_id="nonexistent")
        assert not result.ok
        assert "agent not found" in result.title

    def test_clear_history_no_agent(self):
        result = self.api.clear_history(agent_id="nonexistent")
        assert not result.ok
        assert "agent not found" in result.title

    def test_extract_command(self):
        text1 = "建议执行 [CMD] df -h [/CMD]"
        cmd1 = self.api._extract_command(text1)
        assert cmd1 == "df -h"

        text2 = "没有命令建议"
        cmd2 = self.api._extract_command(text2)
        assert cmd2 is None

        text3 = "[CMD] ls -la [/CMD]"
        cmd3 = self.api._extract_command(text3)
        assert cmd3 == "ls -la"