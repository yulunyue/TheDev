from common.util.export import (
    TestBase,
    Module,
    defaultdict,
    logger,
    File,
    run_catch_error,
)
from common.tool.export import ThreadRecord
from common.mock import MockCf


def get_ins(file_name):
    md = Module().load_module(f"app.yly.algo.context.{file_name}")
    Module().compile_one(f"app/yly/algo/context/{file_name}.py")
    # logger.enable_cache()
    ins: MockCf = md.Solution()
    ins.dev = True
    return ins


class LCTest(TestBase):

    def cases(self, file_name, fun_name="execute", case_idx=None):
        ins: MockCf = get_ins(file_name)
        cases = ins.get_cases()
        if case_idx is None:
            case_idx = list(range(len(cases)))
        else:
            case_idx = [int(case_idx)]
        for cid in case_idx:
            input_param = cases[cid]
            except_result = (
                input_param.pop("result") if "result" in input_param else None
            )

            r = getattr(ins, fun_name)(**input_param)
            if isinstance(ins, ThreadRecord):
                ins.log()
            msg = f"{cases[cid]}\nlogger:\n{logger.get_and_clear_cache()}"
            self.expect(r, except_result, msg)
            File("data/test/a.txt").write_file(r)
            File("data/test/b.txt").write_file(except_result)

    def test_debug(self):
        self.cases("lc_3700")


if __name__ == "__main__":
    LCTest(raise_err=False).run()
