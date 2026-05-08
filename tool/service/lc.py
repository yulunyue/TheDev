from common.tool.export import ToolBase, PyFile
from common.third_service.lc_util import LeetCode, LcProblem, Module
from common.util.export import json, log, time, logger, LOG


def parse_case(case: str):
    try:
        if case.startswith('"') or case.startswith("'"):
            case = case[1:-1]
        try:
            return [json.loads(case)]
        except Exception as e:
            return [case]
    except Exception as e:
        raise Exception(case, e)


class Lc(ToolBase):
    def submit(self, number):
        t = LcProblem.new(number)
        code = PyFile(t.f.path).compile_to_one_file()
        cases = LcProblem.get_storge().get(number, "cases", default_value=dict())
        fun = Module().load_module_object(
            f"app.yly.algo.todo.lc_{number}::Solution::{t.fun_name}"
        )
        for key, case in cases.items():
            LOG.clear()
            LOG.info(f"-------\ncase:{key}; inputs:{case['input']}")
            result = fun(*parse_case(case["input"]))
            expectedOutput = case["expectedOutput"]
            if str(expectedOutput) != str(result):
                raise Exception(f"result:{result};  expectedOutput:{expectedOutput}")
        t.submit(code)


if __name__ == "__main__":
    Lc().run()
