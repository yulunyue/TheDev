import re
from common.util.export import Node, ApiBase, IO_MANAGE, AgentTcpClient
from common.tool.export import FontSearch
from common.third_util.llm.llm_client import LlmClient

SYSTEM_PROMPT = """你是远程机器管理助手。你可以帮助用户：
1. 分析用户意图，建议要执行的 shell 命令
2. 解释命令含义和潜在风险
3. 分析命令执行结果

当需要建议命令时，使用格式：
[CMD] 命令内容 [/CMD]

例如：
用户: 检查磁盘空间
助手: 我建议执行以下命令查看磁盘使用情况：
[CMD] df -h [/CMD]
这个命令会显示各分区的磁盘使用情况，请确认是否执行。"""


class Agent(ApiBase):
    ROUTE_PATH = "/agent"
    _llm = None

    def _get_llm(self):
        if Agent._llm is None:
            Agent._llm = LlmClient("codeagent")
        return Agent._llm

    def _get_agent(self, agent_id):
        io = IO_MANAGE.io_map.get(agent_id)
        return io if isinstance(io, AgentTcpClient) else None

    def list(self, **kw):
        agents = [
            k for k, v in IO_MANAGE.io_map.items() if isinstance(v, AgentTcpClient)
        ]
        return FontSearch().add_childs(*agents)

    def exec(self, agent_id, command, timeout=30, **kw):
        client = self._get_agent(agent_id)
        if not client or not client.is_connected():
            return Node(ok=False, title=f"agent not found: {agent_id}")
        output = client.current_output
        if output and not output.get("done"):
            return Node(ok=False, title="agent is busy, stop current command first")
        client.exec_command(command, timeout)
        return Node(ok=True)

    def kill(self, agent_id, **kw):
        client = self._get_agent(agent_id)
        if not client or not client.is_connected():
            return Node(ok=False, title="agent not found")
        client.kill_exec()
        return Node(ok=True)

    def output(self, agent_id, **kw):
        client = self._get_agent(agent_id)
        if not client:
            return Node(data=dict(error="no running command"))
        output = client.current_output or (
            client.history[-1] if client.history else None
        )
        if not output:
            return Node(data=dict(error="no running command"))
        return Node(data=output)

    def history(self, agent_id, limit=60, **kw):
        client = self._get_agent(agent_id)
        if not client:
            return Node(children=[])
        return Node(children=[Node(data=r) for r in client.get_history(limit)])

    def _extract_command(self, text):
        match = re.search(r"\[CMD\](.*?)\[/CMD\]", text, re.DOTALL)
        return match.group(1).strip() if match else None

    def chat(self, agent_id, message, **kw):
        client = self._get_agent(agent_id)
        if not client or not client.is_connected():
            return Node(ok=False, title=f"agent not found: {agent_id}")

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(client.chat_history)
        messages.append({"role": "user", "content": message})

        llm = self._get_llm()
        result = llm.chat(messages)
        assistant_msg = result["choices"][0]["message"]["content"]

        suggested_cmd = self._extract_command(assistant_msg)

        client.chat_history.append({"role": "user", "content": message})
        client.chat_history.append({"role": "assistant", "content": assistant_msg})

        if suggested_cmd:
            client.pending_command = suggested_cmd

        return Node(
            ok=True,
            data={
                "response": assistant_msg,
                "suggested_command": suggested_cmd,
                "need_confirm": bool(suggested_cmd),
            },
        )

    def confirm(self, agent_id, timeout=30, **kw):
        client = self._get_agent(agent_id)
        if not client or not client.is_connected():
            return Node(ok=False, title="agent not found")
        if not client.pending_command:
            return Node(ok=False, title="no pending command to confirm")

        command = client.pending_command
        client.pending_command = None
        return self.exec(agent_id, command, timeout)

    def cancel(self, agent_id, **kw):
        client = self._get_agent(agent_id)
        if not client:
            return Node(ok=False, title="agent not found")
        client.pending_command = None
        return Node(ok=True, title="command cancelled")

    def clear_history(self, agent_id, **kw):
        client = self._get_agent(agent_id)
        if not client:
            return Node(ok=False, title="agent not found")
        client.chat_history = []
        client.pending_command = None
        return Node(ok=True)
