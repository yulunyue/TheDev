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

    def __init__(self, config_name):
        self.config_name = config_name
        self.config = LlmConfig.get(config_name)
        self._client = None

    @property
    def client(self):
        if self._client is None:
            http_client = httpx.Client(trust_env=False)
            self._client = Opencode(
                base_url=self.config.base_url.get_value(),
                http_client=http_client,
                timeout=self.config.timeout.get_value(),
            )
        return self._client

    @property
    def provider_id(self):
        return self.config.provider_id.get_value()

    @property
    def model_id(self):
        return self.config.model_id.get_value()

    def create_session(self, title="") -> Optional[Session]:
        title = title or self.config_name
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

    def do_prompt(self, prompt):
        s = self.create_session()
        return self.execute_task(s.id, prompt)

    def _get_port_from_config(self):
        base_url = self.config.base_url.get_value()
        m = re.search(r":(\d+)", base_url)
        return int(m.group(1)) if m else 4396

    def start_server(self):
        port = self._get_port_from_config()

        if System.get_pid_by_port(self._get_port_from_config()):
            return self
        cmd = ["opencode", "serve", "--port", str(port)]
        start_pid = System.popen(*cmd, cwd=self.config.cwd.get_value())
        time.sleep(1)
        logger.info(f"START_PID {cmd} {start_pid}")
        return self


if __name__ == "__main__":
    print(OpencodeClient(sys.argv[1]).start_server().do_prompt(sys.argv[2]))
