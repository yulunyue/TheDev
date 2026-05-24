import json
import time
from threading import Thread

import tornado.websocket
import tornado.ioloop
from tornado.web import Application

from common.util.export import IO_MANAGE, C, AgentTcpClient
from common.third_util.http import (
    TornadaWebSocketConnectHandler,
    MainHandler,
)
from tool.service.agent_runner import AgentRunner


PORT_BASE = 50030


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


def _wait_for_done(agent_id, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        output = _get_agent_output(agent_id)
        if output and output.get("done"):
            return output
        time.sleep(0.05)
    return _get_agent_output(agent_id)


class TestE2E:
    WS_PORT = PORT_BASE
    AGENT_PORT = PORT_BASE + 1

    @classmethod
    def setup_class(cls):
        IO_MANAGE.start_agent_server(host="127.0.0.1", port=cls.AGENT_PORT)
        time.sleep(0.5)

        cls.runner = AgentRunner(
            server="127.0.0.1", port=cls.AGENT_PORT, agent_id="e2e-agent"
        )
        cls.runner_thread = Thread(target=cls.runner.run, daemon=True)
        cls.runner_thread.start()

        for _ in range(20):
            if "e2e-agent" in IO_MANAGE.io_map:
                break
            time.sleep(0.25)
        assert "e2e-agent" in IO_MANAGE.io_map, "agent failed to register"

        TornadaWebSocketConnectHandler.handler_msg = IO_MANAGE.handler_msg

        cls.app = Application([
            (r"/ws", TornadaWebSocketConnectHandler),
            (r"/(.*)", MainHandler),
        ])
        cls.app.listen(cls.WS_PORT)

    @classmethod
    def teardown_class(cls):
        cls.runner.stop()
        IO_MANAGE.io_map.clear()
        IO_MANAGE.topics.clear()

    def test_http_api_exec_and_output(self):
        from app.tool.agent import Agent

        api = Agent()
        result = api.exec(agent_id="e2e-agent", command="echo hello api")
        assert result.ok

        output = _wait_for_done("e2e-agent")
        assert output is not None
        assert output["done"]
        assert output["exit_code"] == 0
        stdout = "".join(l[1] for l in output["lines"] if l[0] == "stdout")
        assert "hello api" in stdout

        api_result = api.output(agent_id="e2e-agent")
        assert api_result.data.get("done")
        assert api_result.data.get("exit_code") == 0

    def test_ws_receive_exec_output(self):
        IO_MANAGE.topics.clear()

        async def flow():
            ws = await tornado.websocket.websocket_connect(
                f"ws://127.0.0.1:{self.WS_PORT}/ws"
            )

            ws.write_message(json.dumps({"type": "login", "value": "e2e-ws"}))
            login_resp = json.loads(await ws.read_message())
            assert login_resp["type"] == "login_ok"

            topic = f"{C.TOPIC_AGENT_OUTPUT}.e2e-agent"
            ws.write_message(json.dumps({"type": "sub", "value": topic}))
            await tornado.gen.sleep(0.1)

            _send_exec("e2e-agent", "echo hello ws")

            received = []
            for _ in range(30):
                msg = json.loads(await ws.read_message())
                received.append(msg)
                if msg.get("value", {}).get("type") == "exec_done":
                    break

            stdout_msgs = [
                m
                for m in received
                if m.get("value", {}).get("type") == "exec_stdout"
            ]
            assert len(stdout_msgs) >= 1, f"no stdout msgs in {received}"
            assert any(
                "hello ws" in str(m) for m in stdout_msgs
            ), f"no hello in {received}"

            ws.close()

        tornado.ioloop.IOLoop.current().run_sync(flow, timeout=10)
