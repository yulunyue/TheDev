from common.util.export import IO_MANAGE, Node
from common.util.io.agent_client import AgentTcpClient
from app.tool.agent import Agent


class TestLlmAgent:
    @classmethod
    def setup_class(cls):
        cls.api = Agent()

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

    def test_confirm_no_pending_command(self):
        fake = AgentTcpClient()
        fake.username = "test-confirm"
        fake.sock = True
        fake.send = lambda data: None
        fake.pending_command = None
        IO_MANAGE.io_map["test-confirm"] = fake

        result = self.api.confirm(agent_id="test-confirm")
        assert not result.ok
        assert "no pending command" in result.title

        IO_MANAGE.io_map.pop("test-confirm", None)

    def test_clear_history_no_agent(self):
        result = self.api.clear_history(agent_id="nonexistent")
        assert not result.ok
        assert "agent not found" in result.title

    def test_clear_history_success(self):
        fake = AgentTcpClient()
        fake.username = "test-clear"
        fake.sock = True
        fake.send = lambda data: None
        fake.chat_history = [{"role": "user", "content": "hello"}]
        fake.pending_command = "ls"
        IO_MANAGE.io_map["test-clear"] = fake

        result = self.api.clear_history(agent_id="test-clear")
        assert result.ok
        assert fake.chat_history == []
        assert fake.pending_command is None

        IO_MANAGE.io_map.pop("test-clear", None)

    def test_chat_with_mock_agent(self):
        fake = AgentTcpClient()
        fake.username = "test-chat"
        fake.sock = True
        fake.is_connected = lambda: True
        fake.chat_history = []
        fake.pending_command = None
        IO_MANAGE.io_map["test-chat"] = fake

        result = self.api.chat(agent_id="test-chat", message="check disk")
        assert result.ok
        assert result.data.get("response")
        assert len(fake.chat_history) == 2
        assert fake.chat_history[0]["role"] == "user"
        assert fake.chat_history[0]["content"] == "check disk"

        IO_MANAGE.io_map.pop("test-chat", None)

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

    def test_chat_history_accumulation(self):
        fake = AgentTcpClient()
        fake.username = "test-history"
        fake.sock = True
        fake.is_connected = lambda: True
        fake.chat_history = []
        IO_MANAGE.io_map["test-history"] = fake

        self.api.chat(agent_id="test-history", message="msg1")
        assert len(fake.chat_history) == 2

        self.api.chat(agent_id="test-history", message="msg2")
        assert len(fake.chat_history) == 4

        IO_MANAGE.io_map.pop("test-history", None)

    def test_cancel_clears_pending_command(self):
        fake = AgentTcpClient()
        fake.username = "test-cancel"
        fake.sock = True
        fake.is_connected = lambda: True
        fake.pending_command = "rm -rf /"
        IO_MANAGE.io_map["test-cancel"] = fake

        result = self.api.cancel(agent_id="test-cancel")
        assert result.ok
        assert fake.pending_command is None

        IO_MANAGE.io_map.pop("test-cancel", None)