import httpx
import json
from typing import Dict, Any, List
from .llm_config import LlmConfig


class MaasClient:
    DEFAULT_CONFIG_PATH = "config/setting/llm.json"
    
    def __init__(self, config_path=None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config = None
        self._http_client = None
    
    @property
    def config(self):
        if self._config is None:
            self._config = LlmConfig
            self._config.set_resource(self.config_path)
        return self._config
    
    @property
    def http_client(self):
        if self._http_client is None:
            timeout = self.config.timeout.get_value()
            no_proxy = self.config.no_proxy.get_value()
            if no_proxy:
                self._http_client = httpx.Client(trust_env=False, timeout=timeout)
            else:
                self._http_client = httpx.Client(timeout=timeout)
        return self._http_client
    
    @property
    def base_url(self):
        return self.config.base_url.get_value()
    
    @property
    def model(self):
        return self.config.model.get_value()
    
    def chat(self, messages: List[Dict[str, str]], stream=False, **kwargs) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        url = f"{self.base_url}/chat/completions"
        resp = self.http_client.post(url, json=payload)
        
        if resp.status_code != 200:
            error_data = resp.json() if resp.headers.get('content-type', '').startswith('application/json') else {"error": resp.text}
            raise Exception(f"API Error {resp.status_code}: {error_data}")
        
        return resp.json()
    
    def get_models(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/models"
        resp = self.http_client.get(url)
        if resp.status_code != 200:
            raise Exception(f"API Error {resp.status_code}: {resp.text}")
        return resp.json().get("data", [])
    
    def simple_chat(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        result = self.chat(messages, **kwargs)
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        return ""