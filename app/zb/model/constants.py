from common.util.export import File, dir_object

ROOT = File("app/zb/task")
REPO_ROOT = File("app/zb/repo")
MODEL_ROOT = File("app/zb/model")

CODING_AGENT_SYSTEM_PROMPT_FILE = MODEL_ROOT.child("coding_agent_system_prompt.txt")

PROMOT_TEMPLATE = """通过base_commit可以在wsl的docker构建一个有issue_url问题的环境，帮我修复下呢，生成final.diff文件，仅仅是核心代码，不能从code.patch生成，需要你自己思考，然后再docker里帮我用run_verification.py 验证，其中不用code.patch用final.diff"""

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