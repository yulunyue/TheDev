import time
import json
import traceback
import re
from common.third_util.io.api import Api
from common.model.export import LcProblem, LcSubmissionDetail
from common.util.export import File, logger, Module
from common.tool.export import PyFile
import sys


class LeetCode(Api):
    CACHE_DIR = "data/lc"
    CODE_DIR = "app/yly/algo/todo"

    def check(self, submissionId):
        query = "\n    query submissionDetails($submissionId: ID!) {\n  submissionDetail(submissionId: $submissionId) {\n    code\n    timestamp\n    statusDisplay\n    isMine\n    runtimeDisplay: runtime\n    memoryDisplay: memory\n    memory: rawMemory\n    lang\n    langVerboseName\n    question {\n      questionId\n      titleSlug\n      hasFrontendPreview\n    }\n    user {\n      realName\n      userAvatar\n      userSlug\n    }\n    runtimePercentile\n    memoryPercentile\n    submissionComment {\n      flagType\n    }\n    passedTestCaseCnt\n    totalTestCaseCnt\n    fullCodeOutput\n    testDescriptions\n    testInfo\n    testBodies\n    stdOutput\n    aiJudgeMessage\n    isCompiledLang\n    aiRecheckSubmitted\n    ... on GeneralSubmissionNode {\n      outputDetail {\n        codeOutput\n        expectedOutput\n        input\n        compileError\n        runtimeError\n        lastTestcase\n      }\n    }\n    ... on ContestSubmissionNode {\n      outputDetail {\n        codeOutput\n        expectedOutput\n        input\n        compileError\n        runtimeError\n        lastTestcase\n      }\n    }\n  }\n}\n    "
        data = self.graphql(query, dict(submissionId=submissionId), "submissionDetails")
        return LcSubmissionDetail().set_data(**data["data"]["submissionDetail"])

    def get_endpoint(self):
        return "https://leetcode.cn"

    def get_daily(self):
        query = """
query questionOfToday {
  todayRecord {
    question {
      questionFrontendId
      title
      titleSlug
      difficulty
    }
    date
  }
}
"""
        data = self.graphql(query, {}, "questionOfToday")
        return data["data"]["todayRecord"][0]["question"]

    def _get_cache_path(self, title_slug):
        return f"{self.CACHE_DIR}/{title_slug}.json"

    def _load_cache(self, title_slug):
        path = self._get_cache_path(title_slug)
        f = File(path)
        if f.exists():
            return f.read_file()
        return None

    def _save_cache(self, title_slug, data):
        path = self._get_cache_path(title_slug)
        File(path).make_dir_if_not_exist().write_file(json.dumps(data, ensure_ascii=False, indent=2))
        return data

    def _get_code_path(self, question_id):
        return f"{self.CODE_DIR}/lc_{question_id}.py"

    def _get_code_snippet(self, code_snippets):
        for snippet in code_snippets:
            if snippet["lang"] == "Python3":
                return snippet["code"]
        return None

    def _parse_examples_from_content(self, content):
        examples = []
        pattern = r"<strong class=\"example\">Example \d+:</strong>.*?<pre>(.*?)</pre>"
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            input_match = re.search(r"<strong>Input:</strong>\s*(.*?)(?:<strong>|$)", match, re.DOTALL)
            output_match = re.search(r"<strong>Output:</strong>\s*(.*?)(?:<strong>|$)", match, re.DOTALL)
            if input_match and output_match:
                input_str = input_match.group(1).strip()
                output_str = output_match.group(1).strip()
                input_str = re.sub(r"<[^>]+>", "", input_str).strip()
                output_str = re.sub(r"<[^>]+>", "", output_str).strip()
                input_str = re.sub(r"\s*Explanation:.*", "", input_str, flags=re.DOTALL).strip()
                examples.append({"input_str": input_str, "output_str": output_str})
        return examples

    def _parse_input_params(self, input_str):
        params = []
        input_str = input_str.strip()
        in_json = False
        json_start = 0
        current = ""
        for i, c in enumerate(input_str):
            if c in "[{":
                if not in_json:
                    in_json = True
                    json_start = i
            elif c in "]}":
                if in_json:
                    in_json = False
            elif c == "," and not in_json:
                param = current.strip()
                if "=" in param:
                    _, value = param.split("=", 1)
                    value = value.strip()
                    try:
                        params.append(json.loads(value))
                    except:
                        params.append(value)
                current = ""
                continue
            current += c
        param = current.strip()
        if "=" in param:
            _, value = param.split("=", 1)
            value = value.strip()
            try:
                params.append(json.loads(value))
            except:
                params.append(value)
        return params

    def _parse_output(self, output_str):
        output_str = output_str.strip()
        try:
            return json.loads(output_str)
        except:
            return output_str

    def prepare_submit(self, title_slug=None):
        if title_slug is None:
            daily = self.get_daily()
            title_slug = daily["titleSlug"]
        cache = self._load_cache(title_slug)
        if cache:
            return cache
        if title_slug == self.get_daily().get("titleSlug"):
            daily = self.get_daily()
            question_id = daily["questionFrontendId"]
            title = daily["title"]
            difficulty = daily["difficulty"]
        else:
            problem = self.query_num(title_slug.split("-")[-1])
            question_id = problem.questionFrontendId
            title = problem.title
            difficulty = problem.difficulty
        detail = self.query_detail(title_slug)
        question_data = detail["data"]["question"]
        code_snippet = self._get_code_snippet(question_data["codeSnippets"])
        sample_test_case = question_data["sampleTestCase"]
        content = question_data["content"]
        examples = self._parse_examples_from_content(content)
        test_cases = []
        for ex in examples:
            input_params = self._parse_input_params(ex["input_str"])
            expected = self._parse_output(ex["output_str"])
            test_cases.append({"input": input_params, "expected": expected})
        if not test_cases:
            lines = sample_test_case.strip().split("\n")
            inputs = []
            for line in lines:
                try:
                    inputs.append(json.loads(line))
                except:
                    inputs.append(line)
            test_cases.append({"input": inputs, "expected": None})
        cache_data = {
            "question_id": question_id,
            "title_slug": title_slug,
            "title": title,
            "difficulty": difficulty,
            "code_snippet": code_snippet,
            "test_cases": test_cases,
            "content": content,
        }
        return self._save_cache(title_slug, cache_data)

    def test_local(self, title_slug=None):
        if title_slug is None:
            daily = self.get_daily()
            title_slug = daily["titleSlug"]
        cache = self._load_cache(title_slug)
        if not cache:
            cache = self.prepare_submit(title_slug)
        question_id = cache["question_id"]
        test_cases = cache["test_cases"]
        code_path = self._get_code_path(question_id)
        code_file = File(code_path)
        if not code_file.exists():
            return {"passed": False, "error": f"Code file not found: {code_path}", "test_cases": []}
        module = Module().load_module_object(f"lc_{question_id}::Solution", self.CODE_DIR)
        solution = module()
        method_name = self._get_method_name(cache["code_snippet"])
        method = getattr(solution, method_name, None)
        if not method:
            return {"passed": False, "error": f"Method {method_name} not found in Solution", "test_cases": []}
        results = []
        passed_count = 0
        for i, tc in enumerate(test_cases):
            try:
                actual = method(*tc["input"])
                expected = tc.get("expected")
                is_passed = expected is None or actual == expected
                if is_passed:
                    passed_count += 1
                results.append({
                    "input": tc["input"],
                    "expected": expected,
                    "actual": actual,
                    "passed": is_passed,
                    "error": None,
                })
            except Exception as e:
                results.append({
                    "input": tc["input"],
                    "expected": tc.get("expected"),
                    "actual": None,
                    "passed": False,
                    "error": str(e),
                })
        total = len(test_cases)
        summary = f"{passed_count}/{total} passed"
        if passed_count < total:
            failed_cases = [r for r in results if not r["passed"]]
            details = []
            for r in failed_cases:
                if r["error"]:
                    details.append(f"error: {r['error']}")
                else:
                    details.append(f"input: {r['input']}, expected: {r['expected']}, got: {r['actual']}")
            summary += f", failed: {'; '.join(details)}"
        return {
            "passed": passed_count == total,
            "test_cases": results,
            "summary": summary,
        }

    def _get_method_name(self, code_snippet):
        match = re.search(r"def\s+(\w+)\s*\(", code_snippet)
        if match:
            return match.group(1)
        return "solve"

    def submit(self, title_slug=None):
        if title_slug is None:
            daily = self.get_daily()
            title_slug = daily["titleSlug"]
        cache = self._load_cache(title_slug)
        if not cache:
            cache = self.prepare_submit(title_slug)
        question_id = cache["question_id"]
        code_path = self._get_code_path(question_id)
        code_file = File(code_path)
        if not code_file.exists():
            raise Exception(f"Code file not found: {code_path}")
        code = code_file.read_file()
        data = self.post(
            f"/problems/{title_slug}/submit",
            dict(lang="python3", question_id=question_id, typed_code=code),
        )
        return data["submission_id"]

    def query_detail(self, title):
        query = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    codeSnippets { lang code }
    sampleTestCase
    content
  }
}
"""
        data = self.graphql(query, dict(titleSlug=title), "getQuestionDetail")
        return data

    def query_num(self, num):
        data = self.graphql(
            "\n    query searchQuestionList($limit: Int, $searchKeyword: String, $skip: Int) {\n  problemsetQuestionListV2(\n    limit: $limit\n    searchKeyword: $searchKeyword\n    skip: $skip\n  ) {\n    questions {\n      id\n      titleSlug\n      title\n      translatedTitle\n      questionFrontendId\n      paidOnly\n      difficulty\n      topicTags {\n        name\n        slug\n        nameTranslated\n      }\n      status\n      isInMyFavorites\n      frequency\n      acRate\n      contestPoint\n    }\n    totalLength\n    finishedLength\n    hasMore\n  }\n}\n    ",
            dict(searchKeyword=num, limit=1, skip=0),
            "searchQuestionList",
        )
        try:
            questions = data["data"]["problemsetQuestionListV2"]["questions"]
            if len(questions) != 1:
                raise Exception(questions, num)
            ret = LcProblem().set_data(**questions[0])
            if ret.questionFrontendId != num:
                raise Exception(num, ret.questionFrontendId)
            return ret
        except Exception as e:
            raise Exception(e, data)

    def graphql(self, query, variables, operationName=None):
        param = dict(query=query, variables=variables)
        if operationName:
            param.update(operationName=operationName)
        return self.post(f"/graphql", param)
