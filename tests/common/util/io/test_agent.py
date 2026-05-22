import time
from common.util.export import IO_MANAGE, AgentTcpClient


class TestAgent:

    def test_register_heartbeat_unregister(self):
        PORT = 50002
        HOST = "127.0.0.1"

        IO_MANAGE.start_agent_server(host=HOST, port=PORT)
        time.sleep(0.5)

        c = AgentTcpClient().set_addr(dst_ip=HOST, dst_port=PORT)
        c.connect()
        c.write(dict(type="register", agent_id="test-node", platform="linux",
                     hostname="test-worker"))
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
        c.write(dict(type="register", agent_id="node-a", platform="windows",
                     hostname="win-pc"))
        time.sleep(0.3)

        agents = IO_MANAGE.list_agents()
        assert any(a["agent_id"] == "node-a" for a in agents)
        c.close()
