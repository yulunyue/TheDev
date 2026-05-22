import time
import sys
import os as os_mod
from threading import Thread
from common.util.export import AgentTcpClient
from common.tool.export import OsUtil


class AgentRunner:
    def __init__(self, server, port, agent_id, platform=None, hostname=None):
        self.server_host = server
        self.server_port = port
        self.agent_id = agent_id
        self.platform = platform or self._detect_platform()
        self.hostname = hostname or os_mod.uname().nodename
        self._running = False
        self.client = AgentTcpClient()
        self.client.message_handler = self._on_message

    def _detect_platform(self):
        if os_mod.name == "nt":
            return "windows"
        return "linux"

    def _get_shell(self):
        return "cmd" if self.platform == "windows" else "bash"

    def run(self):
        self._running = True
        while self._running:
            try:
                self._connect_and_serve()
            except Exception as e:
                print(f"connection error: {e}", file=sys.stderr)
                time.sleep(5)

    def stop(self):
        self._running = False
        self.client.close()

    def _connect_and_serve(self):
        self.client = AgentTcpClient()
        self.client.message_handler = self._on_message
        self.client.set_addr(dst_ip=self.server_host, dst_port=self.server_port)
        self.client.connect()

        self.client.write(
            dict(
                type="register",
                agent_id=self.agent_id,
                platform=self.platform,
                hostname=self.hostname,
            )
        )

        Thread(target=self._heartbeat_loop, daemon=True).start()
        self.client.run()

    def _heartbeat_loop(self):
        while self._running:
            time.sleep(15)
            try:
                self.client.write(dict(type="heartbeat", agent_id=self.agent_id))
            except Exception:
                break

    def _on_message(self, msg):
        t = msg.get("type")
        if t == "exec":
            Thread(target=self._exec_cmd, args=(msg,), daemon=True).start()
        elif t == "exec_stop":
            self._stop_cmd(msg.get("cmd_id"))

    def _exec_cmd(self, msg):
        cmd_id = msg["cmd_id"]
        command = msg["command"]
        timeout = msg.get("timeout", 30)
        shell = self._get_shell()

        try:
            os = OsUtil(shell)
            if self.platform == "windows":
                proc = os.popen("/c", command)
            else:
                proc = os.popen("-c", command)

            for line in iter(proc.stdout.readline, ""):
                self.client.write(
                    dict(
                        type="exec_stdout",
                        cmd_id=cmd_id,
                        data=line,
                    )
                )
            proc.wait(timeout=timeout)
            self.client.write(
                dict(
                    type="exec_done",
                    cmd_id=cmd_id,
                    exit_code=proc.returncode,
                )
            )
        except Exception as e:
            self.client.write(
                dict(
                    type="exec_done",
                    cmd_id=cmd_id,
                    exit_code=-1,
                    error=str(e),
                )
            )

    def _stop_cmd(self, cmd_id):
        pass


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Remote Agent Runner")
    parser.add_argument("--server", required=True, help="Server host")
    parser.add_argument("--port", type=int, default=20001, help="Server port")
    parser.add_argument("--id", required=True, help="Agent ID")
    parser.add_argument("--platform", help="Platform (linux/windows)")
    parser.add_argument("--hostname", help="Hostname")
    args = parser.parse_args()

    runner = AgentRunner(
        server=args.server,
        port=args.port,
        agent_id=args.id,
        platform=args.platform,
        hostname=args.hostname,
    )
    print(f"agent [{args.id}] starting, connecting to {args.server}:{args.port}")
    runner.run()


if __name__ == "__main__":
    main()
