from common.util.export import File, Module
from .config import CODE_DIR
from .parser import LcContentParser


class LcTestService:
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
            method_name = LcContentParser.get_method_name(cache["code_snippet"])
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
        method_name = LcContentParser.get_method_name(code_snippet)
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
