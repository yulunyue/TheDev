import json
import re

from common.util.export import File, logger
from common.third_util.llm.opencode_db import OpencodeDb

from .constants import (
    Fp,
    OPENCODE_JSON_FILE_NAME,
    CODING_AGENT_SYSTEM_PROMPT_FILE,
    TOOLS_SCHEMA,
)


class TrajectoryBuilder:
    def build(self, opencode_data, task_data, final_diff_content, root):
        return {
            "instance_id": task_data["instance_id"],
            "instruction": self._build_instruction(task_data),
            "language": "python",
            "metadata": self._build_metadata(task_data),
            "metrics": {
                "completion_tokens": 0,
                "prompt_tokens": 0,
                "total_tokens": 0,
                "cost": 0.0,
            },
            "task_category": "bug_fix",
            "task_id": task_data["instance_id"],
            "trajectory": self._convert_messages(opencode_data),
            "instance": self._build_instance(task_data, final_diff_content, root),
        }

    def _build_instruction(self, task_data):
        return f"""<task>
我当前目录下是一个Python语言的项目{task_data['repo']}，这是一个issue修复任务。

问题陈述：
{task_data['problem_statement']}

请分析问题，定位相关代码，并提供修复方案。
</task>"""

    def _build_metadata(self, task_data):
        coding_agent_prompt = CODING_AGENT_SYSTEM_PROMPT_FILE.read_file()
        return {
            "agent": "build",
            "model": "codeagent/maas-glm-5-aliyun-codeagent",
            "thinking_mode": True,
            "tools": TOOLS_SCHEMA,
            "coding_agent_system_prompt": coding_agent_prompt,
            "data_source": "opencode",
            "eval_output_dir": "",
            "source": task_data["instance_id"],
        }

    def _convert_messages(self, opencode_data):
        messages = opencode_data["data"]["messages"]
        trajectory = []

        for msg in messages:
            role = msg["info"]["role"]
            ts = int(msg["info"]["time"]["created"])

            text_parts = []
            thinking_parts = []
            tool_parts = []

            for part in msg["parts"]:
                part_type = part["type"]

                if part_type == "text":
                    text_parts.append({"type": "text", "text": part["text"]})
                elif part_type == "tool":
                    tool_parts.append(self._process_tool_part(part, ts))
                elif part_type in ("step-start", "step-finish"):
                    thinking_parts.append(
                        {"type": "thinking", "thinking": part.get("text", "")}
                    )

            if role == "user" and not tool_parts:
                content_parts = text_parts + thinking_parts
                if content_parts:
                    trajectory.append(
                        {"role": role, "content": content_parts, "ts": ts}
                    )

            elif role == "assistant":
                content_parts = thinking_parts + text_parts

                for tool in tool_parts:
                    content_parts.append(
                        {
                            "type": "tool_use",
                            "id": tool["id"],
                            "call_id": tool["id"],
                            "name": tool["name"],
                            "input": tool["input"],
                            "reasoning_details": [],
                        }
                    )

                if content_parts:
                    trajectory.append(
                        {"role": "assistant", "content": content_parts, "ts": ts}
                    )

                for tool in tool_parts:
                    trajectory.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool["id"],
                                    "content": tool["output"],
                                }
                            ],
                            "ts": tool["ts"],
                        }
                    )

        return trajectory

    def _process_tool_part(self, part, ts):
        tool_id = part["call_id"]
        tool_name = part.get("tool", "unknown")
        tool_state = part.get("state", {})
        tool_input = tool_state.get("input", {})
        tool_output = tool_state.get("output", "")
        tool_ts = int(part["state"]["time"]["end"]) if "time" in tool_state else ts

        tool_use_id = tool_id.replace("tool-", "tooluse_")
        return {
            "id": tool_use_id,
            "name": tool_name,
            "input": tool_input,
            "output": (
                tool_output
                if isinstance(tool_output, str)
                else json.dumps(tool_output, ensure_ascii=False)
            ),
            "ts": tool_ts,
        }

    def _build_instance(self, task_data, final_diff_content, root):
        return {
            "repo": task_data["repo"],
            "base_commit": task_data["base_commit"],
            "git_context": {
                "initial_state": self._get_initial_state(root, final_diff_content)
            },
            "patch": task_data["patch"],
            "test_patch": task_data["test_patch"],
            "FAIL_TO_PASS": task_data["FAIL_TO_PASS"],
            "PASS_TO_PASS": task_data["PASS_TO_PASS"],
            "problem_statement": task_data["problem_statement"],
        }

    def _get_initial_state(self, root, final_diff_content):
        files = self._parse_diff_files(final_diff_content)
        initial_state = {}
        for f in files:
            file_path = root.search_one(f)
            if file_path and file_path.exists():
                initial_state[f] = file_path.read_file()
        return initial_state

    def _parse_diff_files(self, diff_content):
        pattern = r"^diff --git a/(.*?) b/"
        matches = re.findall(pattern, diff_content, re.MULTILINE)
        return matches

    def _load_opencode_data(self, root):
        session_id_file = root.child(".opencode_session_id")
        if session_id_file.exists():
            session_id = session_id_file.read_file().strip()
            if session_id:
                db = OpencodeDb()
                messages = db.get_messages(session_id)
                if messages:
                    logger.info(f"从 DB 读取 session_id={session_id}")
                    return {"data": {"messages": messages}}
        opencode_json = root.child(OPENCODE_JSON_FILE_NAME)
        if opencode_json.exists():
            logger.info(f"从 JSON 文件读取: {opencode_json.path}")
            return opencode_json.read_file()
        return None

    def build_from_root(self, root):
        instance_id = root.name
        instance_json = root.child(f"{instance_id}.json")
        trajectory_json = root.child(Fp.trajectory_json)
        final_diff = root.child("final.diff")

        if trajectory_json.exists():
            logger.info(f"trajectory.json already exists: {trajectory_json.path}")
            return None

        opencode_data = self._load_opencode_data(root)
        if not opencode_data:
            logger.warning(f"opencode data not found at {root.path}")
            return None

        if not instance_json.exists():
            logger.warning(f"instance json not found: {instance_json.path}")
            return None

        if not final_diff.exists():
            logger.warning(f"final.diff not found: {final_diff.path}")
            return None

        task_data = instance_json.read_file()

        trajectory = self.build(opencode_data, task_data, final_diff.read_file(), root)

        trajectory_json.write_file(trajectory)
        logger.info(f"Generated trajectory.json: {trajectory_json.path}")
        return trajectory
