import time
from threading import Thread
from common.util.export import IO_MANAGE, AgentTcpClient
from common.tool.export import OsUtil


def _get_agent(agent_id):
    io = IO_MANAGE.io_map.get(agent_id)
    return io if isinstance(io, AgentTcpClient) else None

def _send_exec(agent_id, command, timeout=30):
    client = _get_agent(agent_id)
    if not client or not client.is_connected():
        raise ValueError(f"agent not found: {agent_id}")
    client.exec_command(command, timeout)


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
                type="login",
                value="test-node",
                data=dict(
                    platform="linux",
                    hostname="test-worker",
                ),
            )
        )
        time.sleep(0.3)

        assert "test-node" in IO_MANAGE.io_map
        cli = IO_MANAGE.io_map["test-node"]
        assert cli.ip is not None

        last_hb = cli.last_heartbeat
        c.write(dict(type="heartbeat"))
        time.sleep(0.1)
        assert IO_MANAGE.io_map["test-node"].last_heartbeat != last_hb

        c.write(dict(type="login_out"))
        time.sleep(0.1)
        assert "test-node" not in IO_MANAGE.io_map

        c.close()

    def test_os_util_popen(self):
        os = OsUtil("echo")
        proc = os.popen("hello")
        assert proc.stdout is not None
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
                type="login",
                value="exec-node",
                data=dict(
                    platform="linux",
                    hostname="exec-worker",
                ),
            )
        )
        time.sleep(0.3)

        assert "exec-node" in IO_MANAGE.io_map

        _send_exec("exec-node", "echo hello")
        time.sleep(0.3)

        assert len(received) >= 1
        assert received[0].type == "exec"
        assert received[0].data.get("command") == "echo hello"

        c.close()
