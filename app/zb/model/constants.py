from common.util.export import File, dir_object

ROOT = File("app/zb/task")
REPO_ROOT = File("app/zb/repo")
MODEL_ROOT = File("app/zb/model")

CODING_AGENT_SYSTEM_PROMPT_FILE = MODEL_ROOT.child("coding_agent_system_prompt.txt")


def get_promot(base_commit, issue_url, test_batch, diff_path):
    return f"将代码仓库切换到{base_commit} 并分析{issue_url}的问题，根据test.path:\n{test_batch}\n的错误用例，修成这个问题，并将关键代码输出到{diff_path}, 注意，有任何错误你不应该自己处理，退出让我分析处理"


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
