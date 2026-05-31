from opencode_ai import Opencode
from opencode_ai.types.session import Session
from opencode_ai.types.text_part_input_param import TextPartInputParam
from typing import Optional, Callable
import httpx
import time
import threading

from .llm_config import LlmConfig
from .opencode_db import OpencodeDb
from common.tool.export import ProcessLock, System
from common.util.export import logger, Node, Dict
import re


class OpencodeClient:
    def __init__(self, cwd: str, base_url: str = None, timeout: int = 5 * 60):
        self.cwd = cwd
        self.base_url = base_url
        self.timeout = timeout
        self.model_id = ""
        self.provider_id = ""
        self._client: Opencode = None

    instacnce: Dict[str, "OpencodeClient"] = dict()

    @classmethod
    def new(cls, cwd, base_url=None):
        if cwd in cls.instacnce:
            return cls.instacnce[cwd]
        cls.instacnce[cwd] = cls(cwd, base_url)
        return cls.instacnce[cwd]

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

    def execute_task(self, session_id: str, prompt: str, timeout: int = 300) -> str:
        text_part = TextPartInputParam(type="text", text=prompt)

        def _chat_thread():
            try:
                self.client.session.chat(
                    id=session_id,
                    model_id=self.model_id,
                    provider_id=self.provider_id,
                    parts=[text_part],
                    timeout=timeout,
                )
            except Exception as e:
                logger.warning(f"chat 异常, session_id={session_id}: {e}")

        thread = threading.Thread(target=_chat_thread, daemon=True)
        thread.start()

        return session_id

    def wait_result(
        self,
        session_id: str,
        timeout: int = 300,
        stall_timeout: int = 300,
        wait_call: Optional[Callable[[str], bool]] = None,
    ) -> Node:
        db = OpencodeDb.get_instance()
        checker = wait_call or db.is_session_complete

        start = time.time()
        last_part_count = 0
        last_active_time = start

        while time.time() - start < timeout:
            if checker(session_id):
                messages = db.get_messages(session_id)
                text, tool_parts = self._parse_messages(messages)
                return Node(
                    ok=True,
                    value=text,
                    data={"session_id": session_id, "tool_parts": tool_parts},
                )

            current_count = db._conn.execute(
                "SELECT COUNT(*) as cnt FROM part WHERE session_id = ?",
                (session_id,),
            ).fetchone()["cnt"]
            if current_count > last_part_count:
                last_part_count = current_count
                last_active_time = time.time()
            elif time.time() - last_active_time > stall_timeout:
                return Node(
                    ok=False,
                    title=f"LLM 会话卡住，{stall_timeout}秒无新消息",
                    data={"session_id": session_id},
                )

            time.sleep(3.0)

        return Node(
            ok=False,
            title="等待 LLM 结果超时",
            data={"session_id": session_id},
        )

    @staticmethod
    def _parse_messages(messages):
        text = ""
        tool_parts = []
        for msg in messages:
            if msg["info"]["role"] != "assistant":
                continue
            for part in msg["parts"]:
                part_type = part.get("type")
                if part_type == "text":
                    text = part.get("text", "")
                elif part_type == "tool":
                    tool_parts.append(part)
        return text, tool_parts

    def _get_port_from_config(self):
        m = re.search(r":(\d+)", self.base_url)
        return int(m.group(1))

    def get_pid(self):
        return System.get_pid_by_port(self._get_port_from_config())

    def start_server(self, wait_timeout=30):
        if self.base_url is None:
            port = System.find_free_port()
            self.base_url = f"http://127.0.0.1:{port}"
        else:
            port = self._get_port_from_config()
        pid = self.get_pid()
        if pid:
            return self
        cmd = ["opencode", "serve", "--port", str(port)]
        System.popen(*cmd, cwd=self.cwd or None)
        self._client = None
        import socket
        deadline = time.time() + wait_timeout
        while time.time() < deadline:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=1):
                    logger.info(f"START_PID opencode serve --port {port}")
                    return self
            except (ConnectionRefusedError, OSError):
                time.sleep(0.5)
        logger.warning(f"opencode serve 启动超时 port={port}")
        return self

    def stop(self):
        pid = self.get_pid()
        if pid:
            System.kill(pid)
            logger.info(f"kill {self.cwd} {pid} {self._get_port_from_config()}")
        return self
