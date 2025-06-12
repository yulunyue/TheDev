from common.util.export import TestBase, Module, logger, SolotionBase


class LCTest(TestBase):
    uri = "https://leetcode.cn"

    def test_run(self, name, fun_name):
        md = Module().load_module(f"app.yly.algo.lc.{name}")
        Module().compile_one(md)
        ins: SolotionBase = md.Solution()
        for c in ins.get_cases():
            s = c.pop("result")
            r = getattr(ins, fun_name)(**c)
            self.expect(r, s, "\n" + "\n".join(logger.get_tmp_msgs()))


if __name__ == "__main__":
    LCTest().run()
