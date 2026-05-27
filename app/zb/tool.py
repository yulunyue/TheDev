from common.third_util.llm.opencode_client import OpencodeClient, logger
from common.tool.export import ToolBase
from common.util.export import File, dir_object
import json

ROOT = File("app/zb/task")
TEMPLATE_ROOT = ROOT.child("dynaconf__dynaconf/dynaconf__dynaconf-1008")

opencode_json_file_name = "opencode.json"


class Fp:
    run_verification_py = "run_verification.py"
    trajectory_json = "trajectory.json"
    code_patch = "code.patch"
    Dockerfile = "Dockerfile"
    entrypoint_sh = "entrypoint.sh"
    flag_txt = "flag.txt"
    setup_env_sh = "setup_env.sh"
    setup_repo_sh = "setup_repo.sh"
    test_patch = "test.patch"
    final_diff = "final.diff"


class ZbTool(ToolBase):
    promot_template = "通过base_commit可以在wsl的docker构建一个有issue_url问题的环境，帮我修复下呢，生成final.diff文件，仅仅是核心代码，不能从code.patch生成，需要你自己思考，然后再docker里帮我用run_verification.py 验证，其中不用code.patch用final.diff"

    def build(self, name):
        root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        root.child(Fp.final_diff).remove()
        o = OpencodeClient.new(root.path, "http://127.0.0.1:45799").start_server()
        d = o.do_prompt(f"{self.promot_template}")

        opencode_json = root.child("opencode.json")
        logger.info(opencode_json.write_file(d.to_json()))

    def _build_trajectory(self, root):
        instance_id = root.name
        instance_json = root.child(f"{instance_id}.json")
        opencode_json = root.child(opencode_json_file_name)
        trajectory_json = root.child(Fp.trajectory_json)
        final_diff = root.child("final.diff")

        if trajectory_json.exists():
            logger.info(f"trajectory.json already exists: {trajectory_json.path}")
            return

        if not opencode_json.exists():
            logger.warning(f"opencode.json not found: {opencode_json.path}")
            return

        if not instance_json.exists():
            logger.warning(f"instance json not found: {instance_json.path}")
            return

        if not final_diff.exists():
            logger.warning(f"final.diff not found: {final_diff.path}")
            return

        template_json = TEMPLATE_ROOT.child(Fp.trajectory_json).read_file()
        task_data = instance_json.read_file()
        opencode_data = opencode_json.read_file()

        trajectory = self._convert_opencode_to_trajectory(
            opencode_data, task_data, final_diff.read_file(), template_json, root
        )

        trajectory_json.write_file(trajectory)
        logger.info(f"Generated trajectory.json: {trajectory_json.path}")

    def _convert_opencode_to_trajectory(
        self, opencode_data, task_data, final_diff_content, template, root
    ):
        instruction = f"""<task>
我当前目录下是一个Python语言的项目{task_data['repo']}，这是一个issue修复任务。

问题陈述：
{task_data['problem_statement']}

请分析问题，定位相关代码，并提供修复方案。
</task>"""

        metadata = {
            "agent": "build",
            "model": "codeagent/maas-glm-5-aliyun-codeagent",
            "thinking_mode": True,
            "tools": [
                {"type": "function", "function": {"name": "bash"}},
                {"type": "function", "function": {"name": "edit"}},
                {"type": "function", "function": {"name": "glob"}},
                {"type": "function", "function": {"name": "grep"}},
                {"type": "function", "function": {"name": "read"}},
                {"type": "function", "function": {"name": "write"}},
                {"type": "function", "function": {"name": "webfetch"}},
                {"type": "function", "function": {"name": "task"}},
                {"type": "function", "function": {"name": "question"}},
                {"type": "function", "function": {"name": "todowrite"}},
                {"type": "function", "function": {"name": "skill"}},
            ],
            "coding_agent_system_prompt": template["metadata"][
                "coding_agent_system_prompt"
            ],
            "data_source": "opencode",
            "eval_output_dir": "",
            "source": task_data["instance_id"],
        }

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
                    tool_id = part["call_id"]
                    tool_name = part.get("tool", "unknown")
                    tool_state = part.get("state", {})
                    tool_input = tool_state.get("input", {})
                    tool_output = tool_state.get("output", "")
                    tool_ts = (
                        int(part["state"]["time"]["end"])
                        if "time" in tool_state
                        else ts
                    )

                    tool_use_id = tool_id.replace("tool-", "tooluse_")
                    tool_parts.append(
                        {
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
                    )
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

        return {
            "instance_id": task_data["instance_id"],
            "instruction": instruction,
            "language": "python",
            "metadata": metadata,
            "metrics": {
                "completion_tokens": 0,
                "prompt_tokens": 0,
                "total_tokens": 0,
                "cost": 0.0,
            },
            "task_category": "bug_fix",
            "task_id": task_data["instance_id"],
            "trajectory": trajectory,
            "instance": {
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
            },
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
        import re

        pattern = r"^diff --git a/(.*?) b/"
        matches = re.findall(pattern, diff_content, re.MULTILINE)
        return matches

    def package(self, name):
        root = ROOT.search_one(f"{name}/{Fp.run_verification_py}").parent()
        instance_json = root.child(f"{root.name}.json")
        self._build_trajectory(root)
        z = root.extend(".zip").remove()
        z.zip(targets=[root.child(d) for d in dir_object(Fp, str)] + [instance_json])
        logger.info(z)


if __name__ == "__main__":
    ZbTool().run()
