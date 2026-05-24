import time
from threading import Thread
from common.util.export import IO_MANAGE, Node, C, AgentTcpClient
from common.util.io.base import Io
from tool.service.agent_runner import AgentRunner


def _get_agent(agent_id):
    io = IO_MANAGE.io_map.get(agent_id)
    return io if isinstance(io, AgentTcpClient) else None

def _send_exec(agent_id, command, timeout=30):
    client = _get_agent(agent_id)
    if not client or not client.is_connected():
        raise ValueError(f"agent not found: {agent_id}")
    client.exec_command(command, timeout)

def _get_agent_output(agent_id):
    client = _get_agent(agent_id)
    if not client:
        return None
    if client.current_output:
        return client.current_output
    if client.history:
        return client.history[-1]
    return None


class MockIo(Io):
    def __init__(self, username):
        self.username = username
        self.received = []

    def send_data(self, data):
        self.received.append(data)

    def send(self, data):
        pass


PORT_BASE = 50010


def _wait_for_done(agent_id, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        output = _get_agent_output(agent_id)
        if output and output.get("done"):
            return output
        time.sleep(0.05)
    return _get_agent_output(agent_id)


class TestAgentRunnerIntegration:
    def _setup(self, port, agent_id="test-agent"):
        IO_MANAGE.start_agent_server(host="127.0.0.1", port=port)
        time.sleep(0.3)

        self.runner = AgentRunner(
            server="127.0.0.1", port=port, agent_id=agent_id
        )
        t = Thread(target=self.runner.run, daemon=True)
        t.start()
        time.sleep(0.5)

        assert agent_id in IO_MANAGE.io_map

        self.mock = MockIo("ws-tester")
        IO_MANAGE.io_map["ws-tester"] = self.mock

    def _teardown(self):
        self.runner.stop()
        IO_MANAGE.io_map.clear()
        IO_MANAGE.topics.clear()

    def test_basic_exec(self):
        port = PORT_BASE + 0
        self._setup(port)

        try:
            _send_exec("test-agent", "echo hello world")

            IO_MANAGE.sub(f"{C.TOPIC_AGENT_OUTPUT}.test-agent", "ws-tester")

            result = _wait_for_done("test-agent")
            assert result is not None, "output not found"
            assert result["done"]
            assert result["exit_code"] == 0
            lines_text = "".join(l[1] for l in result["lines"] if l[0] == "stdout")
            assert "hello world" in lines_text, f"unexpected output: {lines_text}"

            topic = f"{C.TOPIC_AGENT_OUTPUT}.test-agent"
            ws_msgs = [r for r in self.mock.received if r.get("type") == topic]
            assert len(ws_msgs) >= 1, "no WS messages received"

            done_msgs = [m for m in ws_msgs if m["value"]["type"] == C.MSG_EXEC_DONE]
            assert len(done_msgs) == 1
            assert done_msgs[0]["value"]["data"].get("exit_code") == 0
        finally:
            self._teardown()

    def test_sequential_exec(self):
        port = PORT_BASE + 1
        self._setup(port)

        try:
            _send_exec("test-agent", "echo first")
            IO_MANAGE.sub(f"{C.TOPIC_AGENT_OUTPUT}.test-agent", "ws-tester")
            r_a = _wait_for_done("test-agent")
            assert r_a and r_a["done"] and r_a["exit_code"] == 0
            lines_a = "".join(l[1] for l in r_a["lines"] if l[0] == "stdout")
            assert "first" in lines_a

            _send_exec("test-agent", "echo second")
            r_b = _wait_for_done("test-agent")
            assert r_b and r_b["done"] and r_b["exit_code"] == 0
            lines_b = "".join(l[1] for l in r_b["lines"] if l[0] == "stdout")
            assert "second" in lines_b
        finally:
            self._teardown()

    def test_exit_recover(self):
        port = PORT_BASE + 2
        self._setup(port)

        try:
            _send_exec("test-agent", "exit 42")
            IO_MANAGE.sub(f"{C.TOPIC_AGENT_OUTPUT}.test-agent", "ws-tester")
            r_exit = _wait_for_done("test-agent")
            assert r_exit and r_exit["done"], "exit command not done"
            assert r_exit["exit_code"] == 42, f"expected 42, got {r_exit['exit_code']}"

            _send_exec("test-agent", "echo recovered")
            r_rec = _wait_for_done("test-agent")
            assert r_rec and r_rec["done"], "recovery command not done"
            assert r_rec["exit_code"] == 0
            lines_rec = "".join(l[1] for l in r_rec["lines"] if l[0] == "stdout")
            assert "recovered" in lines_rec, f"unexpected: {lines_rec}"
        finally:
            self._teardown()

    def test_streaming_output(self):
        port = PORT_BASE + 3
        self._setup(port)

        try:
            _send_exec("test-agent", "for i in 1 2 3; do echo $i; done")
            IO_MANAGE.sub(f"{C.TOPIC_AGENT_OUTPUT}.test-agent", "ws-tester")

            result = _wait_for_done("test-agent")
            assert result and result["done"]
            assert result["exit_code"] == 0

            stdout_lines = [l[1] for l in result["lines"] if l[0] == "stdout"]
            assert len(stdout_lines) >= 3, f"expected >=3 lines, got {len(stdout_lines)}"
            assert any("1" in l for l in stdout_lines)
            assert any("2" in l for l in stdout_lines)
            assert any("3" in l for l in stdout_lines)

            topic = f"{C.TOPIC_AGENT_OUTPUT}.test-agent"
            ws_msgs = [r for r in self.mock.received if r.get("type") == topic]
            stdout_msgs = [m for m in ws_msgs if m["value"]["type"] == C.MSG_EXEC_STDOUT]
            assert len(stdout_msgs) >= 3, f"expected >=3 WS stdout msgs, got {len(stdout_msgs)}"
        finally:
            self._teardown()
