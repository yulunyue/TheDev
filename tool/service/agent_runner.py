import time
import sys
import os as os_mod
import uuid
from threading import Thread, Timer, Lock
from common.util.export import LengthPrefixedClient, Node, C, get_log
from common.tool.export import OsUtil, StrModel, NumberModel, FileConfig, ProcessLock


class AgentRunner:
    def __init__(self, server, port, agent_id, platform=None, hostname=None):
        self.server_host = server
        self.server_port = port
        self.agent_id = agent_id
        self.platform = platform or self._detect_platform()
        self.hostname = hostname or self._get_hostname()
        self._running = False
        self.client = LengthPrefixedClient()
        self.client.message_handler = self._on_message
        self.os = OsUtil(self._get_shell())
        self._exec_lock = Lock()
        self.logger = get_log(f"agent/{agent_id}")

    def _detect_platform(self):
        if os_mod.name == "nt":
            return "windows"
        return "linux"

    def _get_hostname(self):
        if os_mod.name == "nt":
            return os_mod.environ.get("COMPUTERNAME", "unknown")
        return os_mod.uname().nodename

    def _get_shell(self):
        return "cmd" if self.platform == "windows" else "bash"

    def run(self):
        self._running = True
        while self._running:
            try:
                self._connect_and_serve()
            except Exception as e:
                self.logger.error(f"connection error: {e}")
                time.sleep(5)

    def stop(self):
        self._running = False
        self.client.close()
        if self.os.process and self.os.process.poll() is None:
            self.os.process.kill()

    def _connect_and_serve(self):
        self.client = LengthPrefixedClient()
        self.client.message_handler = self._on_message
        self.client.set_addr(dst_ip=self.server_host, dst_port=self.server_port)
        self.client.connect()

        self.client.write_node(
            Node(
                type=C.METHOD_LOGIN,
                value=self.agent_id,
                data={
                    "platform": self.platform,
                    "hostname": self.hostname,
                },
            )
        )

        Thread(target=self._heartbeat_loop, daemon=True).start()
        self.client.run()

    def _heartbeat_loop(self):
        while self._running:
            time.sleep(15)
            try:
                self.client.write_node(Node(type=C.MSG_HEARTBEAT, value=self.agent_id))
            except Exception:
                break

    def _on_message(self, msg: Node):
        if msg.type == C.MSG_EXEC:
            Thread(target=self._exec_cmd, args=(msg,), daemon=True).start()
        elif msg.type == C.MSG_EXEC_KILL:
            self.logger.info("received MSG_EXEC_KILL from server")
            self._kill_exec()

    def _kill_exec(self):
        proc = self.os.process
        if proc and proc.poll() is None:
            self.logger.info(f"killing process pid={proc.pid}")
            proc.kill()
            proc.stdout.close()
            self.logger.info(f"process killed, return_code={proc.poll()}")
        else:
            self.logger.info(f"kill_exec: no running process")

    def _ensure_shell(self):
        proc = self.os.process
        if proc is None or proc.poll() is not None:
            if self.platform == "windows":
                self.os.popen()
            else:
                self.os.popen("-c", "stdbuf -oL bash")
        return self.os.process

    def _send_output(self, msg_type, **data):
        try:
            self.client.write_node(Node(type=msg_type, data=data))
            return True
        except Exception:
            return False

    def _build_cmd_line(self, command, sentinel):
        if self.platform == "windows":
            return f"{command}\nset LAST_EXIT=%errorlevel%\necho {sentinel}\necho %LAST_EXIT%\n"
        return f"{command}\nEXIT_CODE=$?\necho {sentinel}\necho $EXIT_CODE\n"

    def _kill_process(self, proc):
        if proc and proc.poll() is None:
            try:
                proc.kill()
                proc.stdout.close()
                proc.wait()
            except Exception:
                pass

    def _stream_output(self, proc, sentinel):
        for line in proc.stdout:
            line = line.rstrip("\n\r")
            if line == sentinel:
                break
            if not self._send_output(C.MSG_EXEC_STDOUT, data=line + "\n"):
                self._kill_process(proc)
                self.logger.warning("connection lost during exec, killed process")
                raise ConnectionError("connection lost")

        exit_code_line = proc.stdout.readline().strip()
        if not exit_code_line:
            self.logger.warning(
                "stream ended without sentinel, process killed externally"
            )
        if exit_code_line:
            try:
                return int(exit_code_line)
            except (ValueError, TypeError):
                return -1
        return proc.poll() if proc.poll() is not None else -1

    def _exec_cmd(self, msg: Node):
        with self._exec_lock:
            proc = self._ensure_shell()
            timer = None
            try:
                sentinel = f"---CMD_DONE_{uuid.uuid4().hex}---"
                cmd_line = self._build_cmd_line(msg.data["command"], sentinel)
                proc.stdin.write(cmd_line)
                proc.stdin.flush()

                timer = Timer(
                    msg.data.get("timeout", 30), self._kill_process, args=(proc,)
                )
                timer.start()

                exit_code = self._stream_output(proc, sentinel)
                self._send_output(C.MSG_EXEC_DONE, exit_code=exit_code)
            except Exception as e:
                self._kill_process(proc)
                self._send_output(C.MSG_EXEC_DONE, exit_code=-1, error=str(e))
                self.logger.error(f"exec_cmd error: {e}")
            finally:
                if timer:
                    timer.cancel()


class AgentConfig(FileConfig):
    server = StrModel(default_value="127.0.0.1")
    port = NumberModel(default_value=20001)
    agent_id = StrModel(default_value="")
    platform = StrModel(default_value="")
    hostname = StrModel(default_value="")

    @classmethod
    def get_id_by_param(cls, agent_id, **kw):
        return agent_id


AgentConfig.set_resource("config/setting/agent.json")


def main():
    cfg = AgentConfig.get(sys.argv[1])
    cfg.agent_id.set_value(cfg._id)
    cfg.save()

    runner = AgentRunner(
        server=cfg.server.get_value(),
        port=cfg.port.get_value(),
        agent_id=cfg.agent_id.get_value(),
        platform=cfg.platform.get_value() or None,
        hostname=cfg.hostname.get_value() or None,
    )
    runner.logger.info(
        f"agent starting, connecting to {runner.server_host}:{runner.server_port}"
    )
    runner.run()


if __name__ == "__main__":
    main()
