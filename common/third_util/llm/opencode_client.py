from opencode_ai import Opencode
from opencode_ai.types.session import Session
from opencode_ai.types.text_part_input_param import TextPartInputParam
from typing import Optional
import httpx
from .llm_config import LlmConfig


class OpencodeClient:
    DEFAULT_CONFIG_PATH = "config/setting/llm.json"
    
    def __init__(self, config_path=None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config = None
        self._client = None
    
    @property
    def config(self):
        if self._config is None:
            self._config = LlmConfig
            self._config.set_resource(self.config_path)
        return self._config
    
    @property
    def client(self):
        if self._client is None:
            base_url = self.config.opencode_base_url.get_value()
            no_proxy = self.config.no_proxy.get_value()
            if no_proxy:
                http_client = httpx.Client(trust_env=False)
                self._client = Opencode(base_url=base_url, http_client=http_client)
            else:
                self._client = Opencode(base_url=base_url)
        return self._client
    
    @property
    def provider_id(self):
        return self.config.provider_id.get_value()
    
    @property
    def model_id(self):
        return self.config.model_id.get_value()
    
    def get_info(self) -> dict:
        try:
            sessions = self.client.session.list()
            providers = self.client.app.providers()
            return {
                "sessions": [
                    {"id": s.id, "title": s.title, "time": s.time.model_dump() if hasattr(s.time, 'model_dump') else s.time}
                    for s in sessions
                ],
                "providers": [
                    p.model_dump() if hasattr(p, 'model_dump') else p.__dict__
                    for p in providers
                ]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_session(self) -> Optional[Session]:
        try:
            return self.client.session.create()
        except Exception as e:
            print(f"create_session error: {e}")
            return None
    
    def execute_task(self, session_id: str, prompt: str) -> str:
        try:
            text_part = TextPartInputParam(type="text", text=prompt)
            result = self.client.session.chat(
                id=session_id,
                model_id=self.model_id,
                provider_id=self.provider_id,
                parts=[text_part]
            )
            if hasattr(result, 'content'):
                return result.content
            if hasattr(result, 'model_dump'):
                return str(result.model_dump())
            return str(result)
        except Exception as e:
            return f"execute_task error: {e}"
    
    def test_connection(self) -> dict:
        try:
            providers = self.client.app.providers()
            sessions = self.client.session.list()
            return {
                "status": "ok",
                "base_url": self.config.opencode_base_url.get_value(),
                "provider_id": self.provider_id,
                "model_id": self.model_id,
                "no_proxy": self.config.no_proxy.get_value(),
                "providers_count": len(providers) if providers else 0,
                "sessions_count": len(sessions) if sessions else 0
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "base_url": self.config.opencode_base_url.get_value(),
                "no_proxy": self.config.no_proxy.get_value()
            }