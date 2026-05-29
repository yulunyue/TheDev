import httpx
import json
from typing import Dict, Any, List
from .llm_config import LlmConfig
import sys


class LlmClient:

    def __init__(self, config_name):
        self.config = LlmConfig.get(config_name)
        self._http_client = None

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

    @property
    def headers(self) -> Dict[str, str]:
        headers = {}
        api_key = self.config.api_key.get_value()
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        return headers

    def chat(
        self, messages: List[Dict[str, str]], stream=True, **kwargs
    ) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            **kwargs,
        }
        url = f"{self.base_url}/chat/completions"
        resp = self.http_client.post(url, json=payload, headers=self.headers)

        if resp.status_code != 200:
            error_data = (
                resp.json()
                if resp.headers.get("content-type", "").startswith("application/json")
                else {"error": resp.text}
            )
            raise Exception(
                f"\nurl=>{url} status_code:{resp.status_code}\npayload=>{payload}\nresp=>{error_data}"
            )

        if stream:
            return self._parse_stream(resp)
        return resp.json()

    def _parse_stream(self, resp) -> Dict[str, Any]:
        content = ""
        for line in resp.iter_lines():
            if line.startswith("data: "):
                data = line[6:]
                if data == "[DONE]":
                    break
                chunk = json.loads(data)
                if chunk.get("choices"):
                    delta = chunk["choices"][0].get("delta", {})
                    content += delta.get("content", "")
        return {"choices": [{"message": {"content": content}}]}

    def get_models(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/models"
        resp = self.http_client.get(url, headers=self.headers)
        if resp.status_code != 200:
            raise Exception(f"API Error {resp.status_code}: {resp.text}")
        return resp.json().get("data", [])

    def simple_chat(self, prompt: str, **kwargs) -> str:
        messages = [{"role": "user", "content": prompt}]
        result = self.chat(messages, **kwargs)
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        return ""


if __name__ == "__main__":
    llm = LlmClient(sys.argv[1])
    print(llm.get_models())
    print(llm.chat([{"role": "user", "content": "123"}]))
