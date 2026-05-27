from opencode_ai import Opencode
from opencode_ai.types.session import Session
from opencode_ai.types.text_part_input_param import TextPartInputParam
from typing import Optional
import httpx
from .llm_config import LlmConfig
from common.tool.export import ProcessLock, System
from common.util.export import logger, Node
import re
import sys
import time


class OpencodeClient:
    def __init__(self, cwd: str, base_url: str, timeout=15 * 60):
        self.cwd = cwd
        self.base_url = base_url
        self.timeout = timeout
        self.model_id = ""
        self.provider_id = ""
        self._client: Opencode = None

    @classmethod
    def new(cls, cwd, base_url):
        return cls(cwd, base_url)

    @classmethod
    def load(cls, config_name):
        config = LlmConfig.get(config_name)
        return cls.new(config.cwd.get_value(), config.base_url.get_value())

    @property
    def client(self):
        if self._client is None:
            http_client = httpx.Client(trust_env=False)
            self._client = Opencode(
                base_url=self.base_url,
                http_client=http_client,
                timeout=self.timeout,
            )
        return self._client

    def create_session(self, title="") -> Optional[Session]:
        title = title or self.cwd.split("/").pop()
        return self.client.session.create(extra_body=dict(title=title))

    def execute_task(self, session_id: str, prompt: str) -> Node:
        text_part = TextPartInputParam(type="text", text=prompt)
        self.client.session.chat(
            id=session_id,
            model_id=self.model_id,
            provider_id=self.provider_id,
            parts=[text_part],
        )

        messages = self.client.session.messages(id=session_id)
        text = ""
        tool_parts = []

        for msg in messages:
            if msg.info.role != "assistant":
                continue
            for part in msg.parts:
                part_dict = part.model_dump()
                part_type = part_dict.get("type")
                if part_type == "text":
                    text = part_dict.get("text", "")
                elif part_type == "tool":
                    tool_parts.append(part_dict)

        return Node(
            ok=True,
            value=text,
            data={
                "tool_parts": tool_parts,
                "messages": [m.model_dump() for m in messages],
            },
        )

    def do_prompt(self, prompt) -> Node:
        s = self.create_session()
        ret = self.execute_task(s.id, prompt)
        return ret

    def _get_port_from_config(self):
        m = re.search(r":(\d+)", self.base_url)
        return int(m.group(1))

    def start_server(self):
        port = self._get_port_from_config()

        if System.get_pid_by_port(self._get_port_from_config()):
            return self
        cmd = ["opencode", "serve", "--port", str(port)]
        start_pid = System.popen(*cmd, cwd=self.cwd)
        time.sleep(1)
        logger.info(f"START_PID {cmd} {start_pid}")
        return self
