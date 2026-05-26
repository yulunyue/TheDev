import re
import json


class LcContentParser:
    LANG = "Python3"

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
