from common.util.export import File, dir_object

ROOT = File("app/zb/task")
REPO_ROOT = File("app/zb/repo")
MODEL_ROOT = File("app/zb/model")

CODING_AGENT_SYSTEM_PROMPT_FILE = MODEL_ROOT.child("coding_agent_system_prompt.txt")


def get_promot(issue_url, test_patch_content, diff_path, fail_to_pass=None, problem_statement=None):
    fail_str = ""
    if fail_to_pass:
        fail_str = "\n\n需要修复的测试（FAIL_TO_PASS，修复后应通过）:\n" + "\n".join(f"- {t}" for t in fail_to_pass)
    
    problem_str = ""
    if problem_statement:
        problem_str = f"\n\n问题描述:\n{problem_statement}"
    
    return f"分析 {issue_url} 的问题。{problem_str}{fail_str}\n\n根据 test.patch 内容:\n{test_patch_content}\n\n修复这个问题，并将修复的代码补丁输出到 {diff_path}。\n\n注意:\n- 任何错误请停止并说明原因，不要自行处理\n- 确保修复后 FAIL_TO_PASS 测试全部通过"


TOOLS_SCHEMA = [
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
]

OPENCODE_JSON_FILE_NAME = "opencode.json"


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
    opencode_json = "opencode.json"
    promot_txt = "promot.txt"
    @classmethod
    def docker_build(self):
        return [Fp.Dockerfile, Fp.setup_env_sh, Fp.setup_repo_sh, Fp.entrypoint_sh]

    @classmethod
    def pre_check(self):
        return [Fp.test_patch, Fp.code_patch, Fp.run_verification_py]

    @classmethod
    def llm_check(self):
        return []

    @classmethod
    def package(cls):
        pass
