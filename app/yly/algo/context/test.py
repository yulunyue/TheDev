from common.util.export import TestBase, Module, logger, run_catch_error
from common.mock import CgMock


class LCTest(TestBase):
    uri = "https://leetcode.cn"

    def get_ins(self, file_name):
        file_name = self.argvs[1]
        md = Module().load_module(f"app.yly.algo.context.{file_name}")
        Module().compile_one(f"app/yly/algo/context/{file_name}.py")
        logger.enable_cache()
        ins: CgMock = md.Solution()
        return ins

    def test_lc(self, name, fun_name):
        ins: CgMock = self.get_ins(name)
        for c in ins.get_cases():
            s = c.pop("result") if "result" in c else None
            r = getattr(ins, fun_name)(**c)
            self.expect(r, s, f"{c}\n" + logger.get_and_clear_cache())

    def test_cf(self, name):
        ins: CgMock = self.get_ins(name)
        for k, v in ins.get_cases().items():
            ins.set_inputs(k)
            e = f"\n{ins.run()}\n"
            v = f"\n{v}\n"
            self.expect(e, v)


if __name__ == "__main__":
    LCTest().run()
