import json
import re

from common.util.export import File, logger
from common.third_util.llm.opencode_db import OpencodeDb

from .constants import (
    Fp,
    OPENCODE_JSON_FILE_NAME,
    CODING_AGENT_SYSTEM_PROMPT_FILE,
    REPO_ROOT,
)


class TrajectoryBuilder:
    def build(self, opencode_data, task_data, final_diff_content, root, initial_state_data=None):
        trajectory = self._convert_messages(opencode_data)
        turn_count = sum(
            1 for m in trajectory if m.get("role") == "assistant"
        )
        return {
            "instance_id": task_data["instance_id"],
            "instruction": f"修复 {task_data.get('issue_url', '')} 的问题。",
            "language": "python",
            "metadata": self._build_metadata(task_data),
            "metrics": {
                "completion_tokens": 0,
                "prompt_tokens": 0,
                "total_tokens": 0,
                "cost": 0.0,
                "turn_count": turn_count,
            },
            "task_category": "bug_fix",
            "task_id": task_data["instance_id"],
            "trajectory": trajectory,
            "instance": self._build_instance(task_data, final_diff_content, root, initial_state_data),
        }

    def _build_metadata(self, task_data):
        coding_agent_prompt = CODING_AGENT_SYSTEM_PROMPT_FILE.read_file()
        return {
            "agent": "opencode",
            "model": "unknown",
            "thinking_mode": "enabled",
            "tools": self._build_tools_spec(),
            "coding_agent_system_prompt": coding_agent_prompt,
            "data_source": "opencode",
            "eval_output_dir": ".",
            "source": task_data["instance_id"],
        }

    def _build_tools_spec(self):
        tool_defs = [
            ("bash", "Execute shell commands", {"command": "The command string to execute"}, ["command"]),
            ("read", "Read file contents", {"filePath": "Absolute path to the file"}, ["filePath"]),
            ("edit", "Edit file contents", {"filePath": "File path", "oldString": "Text to replace", "newString": "Replacement text"}, ["filePath", "oldString", "newString"]),
            ("glob", "Find files by pattern", {"pattern": "Glob pattern to match"}, ["pattern"]),
            ("grep", "Search file contents", {"pattern": "Regex pattern to search"}, ["pattern"]),
            ("webfetch", "Fetch web content", {"url": "URL to fetch"}, ["url"]),
            ("task", "Launch sub-agent tasks", {"prompt": "Task description for the agent"}, ["prompt"]),
            ("todowrite", "Manage todo list", {"todos": "List of todo items"}, ["todos"]),
            ("question", "Ask user questions", {"question": "Question to ask", "options": "Available options", "task_progress": "Task progress checklist"}, ["question"]),
            ("skill", "Load specialized skills", {"name": "Skill name to load"}, ["name"]),
        ]
        tools = []
        for name, desc, props, required in tool_defs:
            properties = {}
            for k, v in props.items():
                properties[k] = {"type": "string", "description": v}
            tools.append({
                "name": name,
                "description": desc,
                "input_schema": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            })
        return tools

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

    def _build_instance(self, task_data, final_diff_content, root, initial_state_data=None):
        repo_root = REPO_ROOT.child(task_data["instance_id"].split("-")[0])
        clean_diff = self._clean_final_diff(final_diff_content)
        return {
            "repo": task_data["repo"],
            "base_commit": task_data["base_commit"],
            "git_context": {
                "initial_state": self._get_initial_state(repo_root, clean_diff, initial_state_data),
                "final_diff": clean_diff,
            },
            "patch": task_data["patch"],
            "test_patch": task_data["test_patch"],
            "FAIL_TO_PASS": task_data["FAIL_TO_PASS"],
            "PASS_TO_PASS": task_data["PASS_TO_PASS"],
            "problem_statement": task_data["problem_statement"],
        }

    def _get_initial_state(self, repo_root, final_diff_content, initial_state_data=None):
        if initial_state_data and isinstance(initial_state_data, dict):
            return initial_state_data
        files = self._parse_diff_files(final_diff_content)
        initial_state = {}
        for f in files:
            file_path = repo_root.search_one(f)
            if file_path and file_path.exists():
                initial_state[f] = file_path.read_file()
        return initial_state

    def _parse_diff_files(self, diff_content):
        pattern = r"^diff --git a/(.*?) b/"
        matches = re.findall(pattern, diff_content, re.MULTILINE)
        return matches

    def _clean_final_diff(self, diff_content):
        lines = diff_content.splitlines()
        clean_lines = []
        for line in lines:
            if line.startswith("diff --git "):
                clean_lines.append(line)
            elif clean_lines:
                clean_lines.append(line)
        return ("\n".join(clean_lines) + "\n") if clean_lines else diff_content

    def _load_opencode_data(self, root):
        opencode_json = root.child(OPENCODE_JSON_FILE_NAME)
        if opencode_json.exists():
            opencode_data = opencode_json.read_file()
            session_id = opencode_data.get("session_id") if isinstance(opencode_data, dict) else None
            if session_id:
                db = OpencodeDb()
                messages = db.get_messages(session_id)
                if messages:
                    logger.info(f"从 DB 读取 session_id={session_id}")
                    return {"data": {"messages": messages}}
            logger.info(f"从 JSON 文件读取: {opencode_json.path}")
            return opencode_data
        return None

    def build_from_root(self, root):
        instance_id = root.name
        instance_json = root.child(f"{instance_id}.json")
        trajectory_json = root.child(Fp.trajectory_json)
        final_diff = root.child("final.diff")

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

        initial_state_data = None
        opencode_json = root.child(OPENCODE_JSON_FILE_NAME)
        if opencode_json.exists():
            json_data = opencode_json.read_file()
            if isinstance(json_data, dict):
                initial_state_data = json_data.get("initial_state")

        trajectory = self.build(opencode_data, task_data, final_diff.read_file(), root, initial_state_data)

        trajectory_json.write_file(trajectory)
        logger.info(f"Generated trajectory.json: {trajectory_json.path}")
        return trajectory
