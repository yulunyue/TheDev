from common.util.export import (
    TestBase,
    Module,
    defaultdict,
    logger,
    File,
    run_catch_error,
)
from common.mock import MockBase


class LCTest(TestBase):
    uri = "https://leetcode.cn"

    def get_ins(self, file_name):
        file_name = self.argvs[1]
        md = Module().load_module(f"app.yly.algo.context.{file_name}")
        Module().compile_one(f"app/yly/algo/context/{file_name}.py")
        logger.enable_cache()
        ins: MockBase = md.Solution()
        ins.dev = True
        return ins

    def test_exec(self, name, fun_name="run"):
        ins: MockBase = self.get_ins(name)
        for c in ins.get_cases():
            if isinstance(c, dict):
                except_result = c.pop("result") if "result" in c else None
                input_param = c
            else:
                input_param, except_result = c
            msg = f"{c}\n" + logger.get_and_clear_cache()
            if isinstance(input_param, str):
                ins.set_inputs(input_param)
                r = getattr(ins, fun_name)()
                msg = f"\nii-----:\n{input_param}\nio----:\n{except_result}\nloger:\n{logger.get_and_clear_cache()}"
            else:
                r = getattr(ins, fun_name)(**input_param)
            if isinstance(except_result, str) and isinstance(r, list):
                self.expect_dfs(r, except_result.split("\n")[1:], msg)
            else:
                self.expect(r, except_result, msg)


if __name__ == "__main__":
    LCTest().run()
