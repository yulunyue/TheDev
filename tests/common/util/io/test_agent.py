import time
from threading import Thread
from common.util.export import IO_MANAGE, AgentTcpClient
from common.tool.export import OsUtil


class TestAgent:

    def test_register_heartbeat_unregister(self):
        PORT = 50002
        HOST = "127.0.0.1"

        IO_MANAGE.start_agent_server(host=HOST, port=PORT)
        time.sleep(0.5)

        c = AgentTcpClient().set_addr(dst_ip=HOST, dst_port=PORT)
        c.connect()
        c.write(
            dict(
                type="register",
                agent_id="test-node",
                platform="linux",
                hostname="test-worker",
            )
        )
        time.sleep(0.3)

        assert "test-node" in IO_MANAGE.agents
        info = IO_MANAGE.agents["test-node"]
        assert info["platform"] == "linux"
        assert info["hostname"] == "test-worker"
        assert info["ip"] is not None

        last_hb = info.get("last_heartbeat")
        c.write(dict(type="heartbeat", agent_id="test-node"))
        time.sleep(0.1)
        assert IO_MANAGE.agents["test-node"]["last_heartbeat"] != last_hb

        c.write(dict(type="unregister", agent_id="test-node"))
        time.sleep(0.1)
        assert "test-node" not in IO_MANAGE.agents

        c.close()

    def test_list_agents(self):
        PORT = 50003
        HOST = "127.0.0.1"

        IO_MANAGE.start_agent_server(host=HOST, port=PORT)
        time.sleep(0.5)

        agents = IO_MANAGE.list_agents()
        assert isinstance(agents, list)

        c = AgentTcpClient().set_addr(dst_ip=HOST, dst_port=PORT)
        c.connect()
        c.write(
            dict(
                type="register",
                agent_id="node-a",
                platform="windows",
                hostname="win-pc",
            )
        )
        time.sleep(0.3)

        agents = IO_MANAGE.list_agents()
        assert any(a["agent_id"] == "node-a" for a in agents)
        c.close()

    def test_os_util_popen(self):
        os = OsUtil("echo")
        proc = os.popen("hello")
        assert proc.stdout is not None
        assert proc.stderr is not None
        output = proc.stdout.read().strip()
        assert output == "hello"
        proc.wait()
        assert proc.returncode == 0

    def test_send_exec(self):
        PORT = 50004
        HOST = "127.0.0.1"

        IO_MANAGE.start_agent_server(host=HOST, port=PORT)
        time.sleep(0.5)

        received = []

        def agent_message_handler(msg):
            received.append(msg)

        c = AgentTcpClient()
        c.message_handler = agent_message_handler
        c.set_addr(dst_ip=HOST, dst_port=PORT)
        c.connect()
        Thread(target=c.run, daemon=True).start()
        time.sleep(0.2)

        c.write(
            dict(
                type="register",
                agent_id="exec-node",
                platform="linux",
                hostname="exec-worker",
            )
        )
        time.sleep(0.3)

        assert "exec-node" in IO_MANAGE.agent_clients

        cmd_id = IO_MANAGE.send_exec("exec-node", "echo hello")
        assert cmd_id is not None
        time.sleep(0.3)

        assert len(received) > 1
        assert received[1]["type"] == "exec"
        assert received[1]["command"] == "echo hello"

        c.close()
