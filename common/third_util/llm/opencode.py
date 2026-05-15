from opencode_ai import Opencode
from opencode_ai.types.session import Session
from opencode_ai.types.text_part_input_param import TextPartInputParam
from typing import Optional


class OpencodeClient:
    client: Opencode

    def __init__(self):
        self.client = Opencode()

    def get_info(self) -> dict:
        """
        获取当前 opencode 信息
        
        返回 session 列表和 providers 信息
        """
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
        """
        创建一个新的 session
        
        返回：Session 对象，包含 id、title 等属性
        """
        try:
            session = self.client.session.create()
            return session
        except Exception as e:
            print(f"create_session error: {e}")
            return None

    def execute_task(self, session_id: str, prompt: str) -> str:
        """
        在指定 session 执行任务
        
        参数：
        - session_id: session ID
        - prompt: 用户输入的指令
        
        返回：执行结果文本
        """
        try:
            text_part = TextPartInputParam(
                type="text",
                text=prompt
            )
            result = self.client.session.chat(
                id=session_id,
                model_id="codeagent/maas-glm-5-aliyun-codeagent",
                provider_id="codeagent_lzh",
                parts=[text_part]
            )
            if hasattr(result, 'content'):
                return result.content
            if hasattr(result, 'model_dump'):
                return str(result.model_dump())
            return str(result)
        except Exception as e:
            return f"execute_task error: {e}"


client = OpencodeClient()