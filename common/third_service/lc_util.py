import re
import json
from common.third_util.io.api import Api
from common.model.export import LcProblem, LcSubmissionDetail
from common.util.export import File, Module

CACHE_DIR = "data/lc"
CODE_DIR = "app/yly/algo/todo"
LANG = "Python3"


class LcError(Exception):
    pass


class _LcCache:
    DIR = CACHE_DIR

    @classmethod
    def get_path(cls, title_slug: str) -> str:
        return f"{cls.DIR}/{title_slug}.json"

    @classmethod
    def load(cls, title_slug: str):
        path = cls.get_path(title_slug)
        f = File(path)
        if f.exists():
            return f.read_file()
        return None

    @classmethod
    def save(cls, title_slug: str, data: dict) -> dict:
        path = cls.get_path(title_slug)
        File(path).make_dir_if_not_exist().write_file(
            json.dumps(data, ensure_ascii=False, indent=2)
        )
        return data


class _LcContentParser:
    LANG = LANG

    @classmethod
    def get_code_snippet(cls, code_snippets: list, lang: str = None):
        lang = lang or cls.LANG
        for snippet in code_snippets:
            if snippet["lang"] == lang:
                return snippet["code"]
        return None

    @classmethod
    def get_method_name(cls, code_snippet: str) -> str:
        match = re.search(r"def\s+(\w+)\s*\(", code_snippet)
        return match.group(1) if match else "solve"

    @classmethod
    def parse_examples(cls, content: str) -> list:
        examples = []
        pattern = r"<strong class=\"example\">Example \d+:</strong>.*?<pre>(.*?)</pre>"
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            input_match = re.search(
                r"<strong>Input:</strong>\s*(.*?)(?:<strong>|$)", match, re.DOTALL
            )
            output_match = re.search(
                r"<strong>Output:</strong>\s*(.*?)(?:<strong>|$)", match, re.DOTALL
            )
            if input_match and output_match:
                input_str = re.sub(r"<[^>]+>", "", input_match.group(1)).strip()
                output_str = re.sub(r"<[^>]+>", "", output_match.group(1)).strip()
                input_str = re.sub(
                    r"\s*Explanation:.*", "", input_str, flags=re.DOTALL
                ).strip()
                examples.append({"input_str": input_str, "output_str": output_str})
        return examples

    @classmethod
    def parse_input_params(cls, input_str: str) -> list:
        params = []
        input_str = input_str.strip()
        in_json = False
        current = ""
        for c in input_str:
            if c in "[{":
                in_json = True
            elif c in "]}":
                in_json = False
            elif c == "," and not in_json:
                params.append(cls._parse_param(current))
                current = ""
                continue
            current += c
        if current.strip():
            params.append(cls._parse_param(current))
        return params

    @classmethod
    def _parse_param(cls, param: str):
        param = param.strip()
        if "=" in param:
            _, value = param.split("=", 1)
            value = value.strip()
            return cls._safe_json_loads(value)
        return cls._safe_json_loads(param)

    @classmethod
    def parse_output(cls, output_str: str):
        return cls._safe_json_loads(output_str.strip())

    @classmethod
    def _safe_json_loads(cls, value: str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    @classmethod
    def build_test_cases(cls, content: str, sample_test_case: str) -> list:
        examples = cls.parse_examples(content)
        test_cases = []
        for ex in examples:
            input_params = cls.parse_input_params(ex["input_str"])
            expected = cls.parse_output(ex["output_str"])
            test_cases.append({"input": input_params, "expected": expected})

        if not test_cases:
            test_cases = cls._parse_sample_test_case(sample_test_case)

        return test_cases

    @classmethod
    def _parse_sample_test_case(cls, sample_test_case: str) -> list:
        lines = sample_test_case.strip().split("\n")
        inputs = [cls._safe_json_loads(line) for line in lines]
        return [{"input": inputs, "expected": None}]


class _LcLocalTester:
    CODE_DIR = CODE_DIR

    @classmethod
    def test(cls, cache: dict) -> dict:
        question_id = cache["question_id"]
        test_cases = cache["test_cases"]
        code_path = f"{cls.CODE_DIR}/lc_{question_id}.py"

        if not File(code_path).exists():
            return {
                "passed": False,
                "error": f"Code file not found: {code_path}",
                "test_cases": [],
            }

        method = cls.load_solution(question_id, cache["code_snippet"])
        if method is None:
            method_name = _LcContentParser.get_method_name(cache["code_snippet"])
            return {
                "passed": False,
                "error": f"Method {method_name} not found",
                "test_cases": [],
            }

        return cls.run_test_cases(method, test_cases)

    @classmethod
    def load_solution(cls, question_id: str, code_snippet: str):
        module = Module().load_module_object(
            f"lc_{question_id}::Solution", cls.CODE_DIR
        )
        solution = module()
        method_name = _LcContentParser.get_method_name(code_snippet)
        return getattr(solution, method_name, None)

    @classmethod
    def run_test_cases(cls, method, test_cases: list) -> dict:
        results = []
        passed_count = 0

        for tc in test_cases:
            result = cls._run_single_test(method, tc)
            results.append(result)
            if result["passed"]:
                passed_count += 1

        total = len(test_cases)
        summary = cls._build_summary(passed_count, total, results)

        return {
            "passed": passed_count == total,
            "test_cases": results,
            "summary": summary,
        }

    @classmethod
    def _run_single_test(cls, method, tc: dict) -> dict:
        try:
            actual = method(*tc["input"])
            expected = tc.get("expected")
            is_passed = expected is None or actual == expected
            return {
                "input": tc["input"],
                "expected": expected,
                "actual": actual,
                "passed": is_passed,
                "error": None,
            }
        except Exception as e:
            return {
                "input": tc["input"],
                "expected": tc.get("expected"),
                "actual": None,
                "passed": False,
                "error": str(e),
            }

    @classmethod
    def _build_summary(cls, passed: int, total: int, results: list) -> str:
        summary = f"{passed}/{total} passed"
        if passed < total:
            failed = [r for r in results if not r["passed"]]
            details = []
            for r in failed:
                if r["error"]:
                    details.append(f"error: {r['error']}")
                else:
                    details.append(
                        f"input: {r['input']}, expected: {r['expected']}, got: {r['actual']}"
                    )
            summary += f", failed: {'; '.join(details)}"
        return summary


class LeetCode(Api):
    CACHE_DIR = CACHE_DIR
    CODE_DIR = CODE_DIR

    def get_endpoint(self) -> str:
        return "https://leetcode.cn"

    def get_daily(self) -> dict:
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

    def query_num(self, num: str) -> LcProblem:
        query = """
query searchQuestionList($limit: Int, $searchKeyword: String, $skip: Int) {
  problemsetQuestionListV2(limit: $limit, searchKeyword: $searchKeyword, skip: $skip) {
    questions {
      id titleSlug title translatedTitle questionFrontendId paidOnly difficulty
      topicTags { name slug nameTranslated }
      status isInMyFavorites frequency acRate contestPoint
    }
    totalLength finishedLength hasMore
  }
}
"""
        data = self.graphql(
            query, dict(searchKeyword=num, limit=1, skip=0), "searchQuestionList"
        )
        questions = data["data"]["problemsetQuestionListV2"]["questions"]
        if len(questions) != 1:
            raise LcError(f"Question not found: {num}", data)
        ret = LcProblem().set_data(**questions[0])
        if ret.questionFrontendId != num:
            raise LcError(f"Question ID mismatch: {num} vs {ret.questionFrontendId}")
        return ret

    def query_detail(self, title_slug: str) -> dict:
        query = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    codeSnippets { lang code }
    sampleTestCase
    content
  }
}
"""
        return self.graphql(query, dict(titleSlug=title_slug), "getQuestionDetail")

    def check(self, submissionId: str) -> LcSubmissionDetail:
        query = """
query submissionDetails($submissionId: ID!) {
  submissionDetail(submissionId: $submissionId) {
    code
    timestamp
    statusDisplay
    isMine
    runtimeDisplay: runtime
    memoryDisplay: memory
    memory: rawMemory
    lang
    langVerboseName
    question {
      questionId
      titleSlug
      hasFrontendPreview
    }
    user {
      realName
      userAvatar
      userSlug
    }
    runtimePercentile
    memoryPercentile
    submissionComment {
      flagType
    }
    passedTestCaseCnt
    totalTestCaseCnt
    fullCodeOutput
    testDescriptions
    testInfo
    testBodies
    stdOutput
    aiJudgeMessage
    isCompiledLang
    aiRecheckSubmitted
    ... on GeneralSubmissionNode {
      outputDetail {
        codeOutput
        expectedOutput
        input
        compileError
        runtimeError
        lastTestcase
      }
    }
    ... on ContestSubmissionNode {
      outputDetail {
        codeOutput
        expectedOutput
        input
        compileError
        runtimeError
        lastTestcase
      }
    }
  }
}
"""
        data = self.graphql(query, dict(submissionId=submissionId), "submissionDetails")
        return LcSubmissionDetail().set_data(**data["data"]["submissionDetail"])

    def submit(self, title_slug: str = None) -> str:
        daily = self.get_daily()
        if title_slug is None:
            title_slug = daily["titleSlug"]

        cache = _LcCache.load(title_slug)
        if not cache:
            cache = self.prepare_submit(title_slug)

        question_id = cache["question_id"]
        code_path = f"{CODE_DIR}/lc_{question_id}.py"

        if not File(code_path).exists():
            raise LcError(f"Code file not found: {code_path}")

        code = File(code_path).read_file()
        data = self.post(
            f"/problems/{title_slug}/submit",
            dict(lang="python3", question_id=question_id, typed_code=code),
        )
        return data["submission_id"]

    def graphql(self, query: str, variables: dict, operationName: str = None) -> dict:
        param = dict(query=query, variables=variables)
        if operationName:
            param["operationName"] = operationName
        return self.post("/graphql", param)

    def prepare_submit(self, title_slug: str = None) -> dict:
        daily = self.get_daily()
        if title_slug is None:
            title_slug = daily["titleSlug"]

        cache = _LcCache.load(title_slug)
        if cache:
            return cache

        if title_slug == daily["titleSlug"]:
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

        test_cases = _LcContentParser.build_test_cases(
            question_data["content"], question_data["sampleTestCase"]
        )

        cache_data = {
            "question_id": question_id,
            "title_slug": title_slug,
            "title": title,
            "difficulty": difficulty,
            "code_snippet": _LcContentParser.get_code_snippet(
                question_data["codeSnippets"]
            ),
            "test_cases": test_cases,
            "content": question_data["content"],
        }
        return _LcCache.save(title_slug, cache_data)

    def test_local(self, title_slug: str = None) -> dict:
        daily = self.get_daily()
        if title_slug is None:
            title_slug = daily["titleSlug"]

        cache = _LcCache.load(title_slug)
        if not cache:
            cache = self.prepare_submit(title_slug)

        return _LcLocalTester.test(cache)
