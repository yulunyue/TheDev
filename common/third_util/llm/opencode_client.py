from opencode_ai import Opencode
from opencode_ai.types.session import Session
from opencode_ai.types.text_part_input_param import TextPartInputParam
from typing import Optional
import httpx
from .llm_config import LlmConfig
import sys


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
            model_id="",
            provider_id="",
            parts=[text_part],
        )

        if hasattr(result, "parts"):
            for part in result.parts:
                if isinstance(part, dict) and part.get("type") == "text":
                    return part.get("text", "")
            return ""

        if isinstance(result, dict) and "parts" in result:
            for part in result["parts"]:
                if part.get("type") == "text":
                    return part.get("text", "")
            return ""

        if hasattr(result, "content"):
            return result.content
        if hasattr(result, "model_dump"):
            return result.model_dump()
        return str(result)

    def run(self, prompt):
        s = self.create_session()
        return self.execute_task(s.id, prompt)


if __name__ == "__main__":
    print(OpencodeClient(sys.argv[1]).run("hellow"))
