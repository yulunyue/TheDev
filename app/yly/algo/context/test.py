from common.util.export import (
    TestBase,
    Module,
    defaultdict,
    logger,
    File,
    run_catch_error,
)
from common.mock import MockBase, IoTxtFile


class LCTest(TestBase):
    uri = "https://leetcode.cn"

    def get_ins(self, file_name):
        file_name = self.argvs[1]
        md = Module().load_module(f"app.yly.algo.context.{file_name}")
        Module().compile_one(f"app/yly/algo/context/{file_name}.py")
        logger.enable_cache()
        ins: MockBase = md.Solution()
        return ins

    def test_lc(self, name, fun_name):
        ins: MockBase = self.get_ins(name)
        for c in ins.get_cases():
            s = c.pop("result") if "result" in c else None
            r = getattr(ins, fun_name)(**c)
            self.expect(r, s, f"{c}\n" + logger.get_and_clear_cache())

    def test_cf(self, name):
        ins: MockBase = self.get_ins(name)
        if isinstance(ins.io, IoTxtFile):
            dt = defaultdict(dict)
            for fp in File(f"data/algo/{name}").list_dir():
                tp, idx = fp.name.split("_")
                dt[idx][tp] = fp.read_file()
            cases = [[v["input"], v["output"]] for v in dt.values()]
        else:
            cases = ins.get_cases().items()

        for input_line, v in cases:
            input_lines = input_line.split("\n")
            ins.io.input = lambda: input_lines.pop(0)
            results = []
            ins.io.output = lambda v: results.append(str(v))
            ins.run()
            rs = "\n".join(results)
            e = f"\n{rs}\n"
            v = f"\n{v}\n"
            self.expect(e, v, f"input:\n{input_line}\n" + logger.get_and_clear_cache())


if __name__ == "__main__":
    LCTest().run()
