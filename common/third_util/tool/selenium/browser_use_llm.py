from browser_use.llm.base import BaseChatModel
from browser_use.llm.views import ChatInvokeCompletion
from browser_use.llm.messages import BaseMessage
from common.third_util.llm.llm_client import LlmClient
from typing import TypeVar, Type, Any, List, Dict
from common.util.export import logger
from browser_use.agent.views import AgentOutput

T = TypeVar("T")


class BrowserUseLlm(BaseChatModel):
    """将 LlmClient 包装为 browser-use 可用的 LLM"""

    def __init__(self, config_name: str = "codeagent"):
        self._client = LlmClient(config_name)

    @property
    def model_name(self) -> str:
        return self._client.model

    @property
    def model(self) -> str:
        return self._client.model

    @property
    def name(self) -> str:
        return self._client.model

    @property
    def provider(self) -> str:
        return "local"

    async def ainvoke(
        self,
        messages: List[BaseMessage],
        output_format: Type[T] | None = None,
        **kwargs: Any
    ) -> ChatInvokeCompletion[T] | ChatInvokeCompletion[str]:
        llm_messages = self._convert_messages(messages)
        result = self._client.chat(llm_messages, stream=True)
        content = result["choices"][0]["message"]["content"]
        content = self._clean_content(content)
        logger.map(result=result, content=content, output_format=output_format)
        parsed_completion = output_format.model_validate_json(content)
        return ChatInvokeCompletion(completion=parsed_completion)

    def _clean_content(self, content: str) -> str:
        """去除 markdown 代码块包裹"""
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()

    def _convert_messages(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        converted = []
        for msg in messages:
            role = msg.role
            content = msg.content
            if isinstance(content, str):
                converted.append({"role": role, "content": content})
            elif isinstance(content, list):
                text_parts = []
                for part in content:
                    if hasattr(part, "text") and part.text:
                        text_parts.append(part.text)
                converted.append({"role": role, "content": " ".join(text_parts)})
            else:
                converted.append({"role": role, "content": str(content)})
        return converted
