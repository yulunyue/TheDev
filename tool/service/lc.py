from common.tool.export import ToolBase, PyFile
from common.third_service.lc_util import LeetCode, LcProblem, Module
from common.util.export import json, log, time, logger, LOG, sys


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


class Lc:
    def submit(self, number, case_name=None):
        t = LcProblem.new(number)
        code = PyFile(t.f.path).compile_to_one_file()
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
                raise Exception(f"result:{result};  expectedOutput:{expectedOutput}")
        t.submit(code)


if __name__ == "__main__":
    Lc().submit(*sys.argv[1:])
