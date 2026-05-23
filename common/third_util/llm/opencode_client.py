from opencode_ai import Opencode
from opencode_ai.types.session import Session
from opencode_ai.types.text_part_input_param import TextPartInputParam
from typing import Optional
import httpx
from .llm_config import LlmConfig
from common.tool.export import ProcessLock, System
from common.util.export import logger
import re
import sys
import time


class OpencodeClient:

    def __init__(self, config_name="opencode"):
        self.config = LlmConfig.get(config_name)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            http_client = httpx.Client(trust_env=False)
            self._client = Opencode(
                base_url=self.config.base_url.get_value(),
                http_client=http_client,
                timeout=1800,
            )
        return self._client

    @property
    def provider_id(self):
        return self.config.provider_id.get_value()

    @property
    def model_id(self):
        return self.config.model_id.get_value()

    def create_session(self, title="py") -> Optional[Session]:
        return self.client.session.create(extra_body=dict(title=title))

    def execute_task(self, session_id: str, prompt: str) -> str:
        text_part = TextPartInputParam(type="text", text=prompt)
        result = self.client.session.chat(
            id=session_id,
            model_id=self.model_id,
            provider_id=self.provider_id,
            parts=[text_part],
        )
        parts = (result.model_extra or {}).get("parts", [])
        for part in reversed(parts):
            if isinstance(part, dict) and part.get("type") == "text":
                return part.get("text", "")
        return ""

    def run(self, prompt):
        s = self.create_session()
        return self.execute_task(s.id, prompt)

    @staticmethod
    def _get_port_from_config(config_name="opencode"):
        config = LlmConfig.get(config_name)
        base_url = config.base_url.get_value()
        m = re.search(r":(\d+)", base_url)
        return int(m.group(1)) if m else 4396

    @classmethod
    def start_server(
        cls,
        config_name="opencode",
        hostname="127.0.0.1",
        port=None,
        wait_timeout=30,
    ):
        port = port or cls._get_port_from_config(config_name)
        lock = ProcessLock(f"opencode_{port}")
        cmd = [
            "opencode",
            "serve",
            "--port",
            str(port),
            "--hostname",
            hostname,
        ]
        pid = lock.start_process(cmd)
        for _ in range(wait_timeout):
            if System.get_pid_by_port(port):
                logger.info(f"opencode server ready on port {port} (PID={pid})")
                return pid
            time.sleep(1)
        raise TimeoutError(
            f"opencode server failed to start on port {port} within {wait_timeout}s"
        )

    @classmethod
    def stop_server(cls, config_name="opencode", port=None):
        port = port or cls._get_port_from_config(config_name)
        lock = ProcessLock(f"opencode_{port}")
        if lock.is_running():
            System.kill(lock.get_pid())
            lock.clear()
            logger.info(f"opencode server on port {port} stopped")
        else:
            logger.info(f"opencode server on port {port} not running")

    @classmethod
    def is_server_running(cls, config_name="opencode", port=None):
        port = port or cls._get_port_from_config(config_name)
        return ProcessLock(f"opencode_{port}").is_running()


if __name__ == "__main__":
    print(OpencodeClient(sys.argv[1]).run("hellow"))
