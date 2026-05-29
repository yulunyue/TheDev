from common.tool.export import ToolBase, PyFile
from common.third_service.lc import (
    get_lc_service,
    LcProblemService,
    LcError,
    LcCache,
)
from common.model.export import LcProblem
from common.util.export import json, log, time, logger, LOG, sys, Module, File
import re
import html
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def parse_case(case: str):

    if case.startswith('"') or case.startswith("'"):
        case = case[1:-1]
    case = case.split("\n")
    cases = []
    for c in case:
        try:
            cases.append(json.loads(c))
        except Exception as e:
            cases.append(c)
    return cases


class Lc(ToolBase):
    name = "lc"

    def read(self, num, *args, **kw):
        fresh = "--fresh" in args or kw.get("fresh")
        client = get_lc_service()

        try:
            problem = client.query_num(num)
        except LcError:
            print(f"未找到题目 {num}，请检查编号是否正确")
            return

        title_slug = problem.titleSlug

        cache_path = LcCache.get_path(title_slug)
        if fresh:
            File(cache_path).remove()

        try:
            data = LcProblemService(client).prepare_submit(title_slug)
        except Exception as e:
            err = str(e)
            if "请先登录" in err or "请先注册/登录" in err or "认证失败" in err:
                print("LeetCode 登录已过期，请更新 config/setting/api.json 中的 cookie")
            else:
                raise
            return

        question_id = data["question_id"]
        title = getattr(problem, "translatedTitle", None) or data["title"]
        difficulty = {"Hard": "困难", "Medium": "中等", "Easy": "简单"}.get(data["difficulty"], data["difficulty"])
        raw_content = data.get("translatedContent") or data.get("content", "")
        code_snippet = data.get("code_snippet", "")
        code_path = f"app/yly/algo/todo/lc_{num}.py"
        file_exists = File(code_path).exists()

        desc, examples, constraints = self._parse_content(raw_content)

        print(f"#{question_id}. {title}（{difficulty}）\n")
        print("--- 题目描述 ---")
        print(desc)
        print()
        if examples:
            print("--- 示例 ---")
            for i, ex in enumerate(examples, 1):
                print(f"示例 {i}:")
                print(f"  输入: {ex['input']}")
                print(f"  输出: {ex['output']}")
                print()
        if constraints:
            print("--- 约束条件 ---")
            for c in constraints:
                print(f"  • {c}")
        print()
        print("Python3 模板:")
        print(code_snippet)
        print()
        print(f"本地文件: {code_path}")
        if not file_exists:
            self._create_file(num, code_path, code_snippet)
            print("(已自动创建)")

    def _create_file(self, num, code_path, code_snippet):
        match = re.search(r"class Solution:\s+def (\w+)\(self, (.+?)\) -> (.+?):", code_snippet)
        if match:
            func_name, params, return_type = match.group(1), match.group(2), match.group(3)
            code = f"""from common.util.export import List, Dict, Optional


class Solution:
    def {func_name}(self, {params}) -> {return_type}:
        pass
"""
        else:
            code = code_snippet
        File(code_path).write_file(code)

    def _parse_content(self, raw_content):
        if not raw_content:
            return "", [], []

        # split description from first example
        parts = re.split(r"<strong\s+class=\"example\">\s*Example\s*\d+\s*:\s*</strong>", raw_content, flags=re.I)
        desc = html.unescape(re.sub(r"<[^>]+>", "", parts[0])).strip()

        # constraints: <strong>Constraints:</strong></p>\n\n<ul><li>...
        constraints = []
        cm = re.search(
            r"<strong>\s*Constraints\s*:\s*</strong>.*?<ul>(.*?)</ul>",
            raw_content, re.DOTALL | re.I
        )
        if cm:
            items = re.findall(r"<li>(.*?)</li>", cm.group(1), re.DOTALL)
            constraints = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in items]

        # examples: <strong class="example">Example N:</strong></p>\n\n<div class="example-block">...</div>
        example_blocks = re.findall(
            r"<strong\s+class=\"example\">\s*Example\s*\d+\s*:\s*</strong>.*?<div[^>]*class=\"example-block\"[^>]*>(.*?)</div>",
            raw_content, re.DOTALL | re.I
        )
        examples = []
        for block in example_blocks:
            inp = ""
            out = ""
            im = re.search(
                r"<strong>\s*Input\s*:\s*</strong>.*?<span[^>]*class=\"example-io\"[^>]*>(.*?)</span>",
                block, re.DOTALL | re.I
            )
            om = re.search(
                r"<strong>\s*Output\s*:\s*</strong>.*?<span[^>]*class=\"example-io\"[^>]*>(.*?)</span>",
                block, re.DOTALL | re.I
            )
            if im:
                inp = html.unescape(re.sub(r"<[^>]+>", "", im.group(1))).strip()
            if om:
                out = html.unescape(re.sub(r"<[^>]+>", "", om.group(1))).strip()
            if inp or out:
                examples.append({"input": inp, "output": out})

        return desc, examples, constraints

    def check(self, number, case_name=None):
        t = LcProblem.new(number)

        cases = LcProblem.get_storge().get(number, "cases", default_value=dict())
        fun = Module().load_module_object(
            f"app.yly.algo.todo.lc_{number}::Solution::{t.fun_name}"
        )
        if case_name is not None:
            cases = {case_name: cases[case_name]}
        for key, case in cases.items():
            LOG.clear()
            LOG.info(f"-------\ncase:{key}; inputs:{case['input']}")
            result = fun(*parse_case(case["input"]))
            expectedOutput = parse_case(case["expectedOutput"])[0]
            LOG.info(f"result:{result};  expectedOutput:{expectedOutput}")
            if str(expectedOutput) != str(result):
                LOG.info(f"result:{result};  expectedOutput:{expectedOutput}")
                return False
        return True

    def submit(self, number):
        t = LcProblem.new(number)
        code = PyFile(t.f.path).compile_to_one_file()
        t.submit(code)


if __name__ == "__main__":
    Lc().run()
