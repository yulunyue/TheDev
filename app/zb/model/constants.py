from common.util.export import File, dir_object
from common.third_util.io.http_util import requests_get
from common.tool.export import GC
import json

ROOT = File("app/zb/task")
REPO_ROOT = File("app/zb/repo")
MODEL_ROOT = File("app/zb/model")

CODING_AGENT_SYSTEM_PROMPT_FILE = MODEL_ROOT.child("coding_agent_system_prompt.txt")


def fetch_github_issue(issue_url):
    if not issue_url or "github.com" not in issue_url:
        return None
    
    api_url = issue_url.replace("github.com", "api.github.com/repos")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GC.github_token:
        headers["Authorization"] = f"token {GC.github_token}"
    
    proxy = str(GC.http_proxy) if GC.http_proxy else None
    
    try:
        _, body = requests_get(api_url, headers=headers, timeout=10, proxy=proxy)
        data = json.loads(body.decode("utf-8", errors="ignore"))
        title = data.get("title", "")
        body_text = data.get("body", "")
        return f"# {title}\n\n{body_text}"
    except Exception as e:
        return None


def get_promot(issue_url, issue_content=None, fail_to_pass=None):
    fail_str = ""
    if fail_to_pass:
        fail_str = "\n\n需要修复的测试（FAIL_TO_PASS，修复后应通过）:\n" + "\n".join(f"- {t}" for t in fail_to_pass)
    
    issue_str = ""
    if issue_content:
        issue_str = f"\n\nIssue 内容:\n{issue_content}"
    
    return f"""分析 {issue_url} 的问题。{issue_str}{fail_str}

已为你应用了 test.patch，请阅读测试代码理解测试预期。

要求：
1. 仅分析代码并修复问题，不要安装依赖或运行测试
2. 使用 edit 工具直接修改代码文件
3. 修复完成后告诉我，我会自动生成 diff 补丁
4. 不要执行任何 pip install、pytest 或其他环境操作"""




OPENCODE_JSON_FILE_NAME = "opencode.json"
PROMOT_TXT = "promot.txt"

class Fp:
    run_verification_py = "run_verification.py"
    trajectory_json = "trajectory.json"
    code_patch = "code.patch"
    Dockerfile = "Dockerfile"
    setup_env_sh = "setup_env.sh"
    setup_repo_sh = "setup_repo.sh"
    test_patch = "test.patch"
    final_diff = "final.diff"

    @classmethod
    def docker_build(self):
        return [Fp.Dockerfile, Fp.setup_env_sh, Fp.setup_repo_sh, "entrypoint.sh"]

    @classmethod
    def pre_check(self):
        return [Fp.test_patch, Fp.code_patch, Fp.run_verification_py]

    @classmethod
    def llm_check(self):
        return [
            Fp.final_diff,
            Fp.run_verification_py,
            Fp.test_patch
        ]


